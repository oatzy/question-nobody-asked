import pygame
import random as r
import numpy as np

pygame.init()

### Globals ###

fps = 50

G = 1.
c = 12.
a = 1.5 # boost acceleration

# Switches
collision_handling = True
relativistic = True
record = False

pt = 0 #proper time
ct = 0 #coordinate time

# Create game screen
screen = pygame.display.set_mode((640, 480))
screen.fill((255, 255, 255))
pygame.display.set_caption("Gravity Particle")


### Particle Class ###

class Particle(pygame.sprite.Sprite):
    
    def __init__(self, pos, vel, mass, static=False):
        pygame.sprite.Sprite.__init__(self)
        
        self.vel = vel
        self.static = static
        self.radius = 12.5
        self.x, self.y = pos
        self.mass = mass
        self.L = None

        # load sprite
        if static:
            self.image = pygame.image.load("star.png").convert_alpha()
        else:
           self.image = pygame.image.load("planet.png").convert_alpha()

        # set position
        self.rect = self.image.get_rect()
        self.rect.center = (pos[0], pos[1])


    ## Move Functions ##
    
    def update(self, obstacles=None, boost=None):
        global pt, ct
        if not self.static:

            # move particle
            self.x, self.y = self.get_move(obstacles, boost)
            self.rect.center = (round(self.x), round(self.y))

            # update times
            pt += 1
            ct += self.dilation(obstacles)

    def get_move(self, obstacles, boost):
        x, y = self.x, self.y
        
        if boost != None:
            self.vel = np.add(self.vel, boost)
            #recalculate angular momentum
            self.update_angmom(obstacles, boost)
            
        acc = self.get_acceleration(obstacles)
        self.vel = np.add(self.vel, acc)
        x, y = x+self.vel[0], y+self.vel[1]
        
        if collision_handling:
            x, y = self.collision(x, y, obstacles)
            
        # boundry recoil
        if x < 0:
            x = -x
            self.vel[0] = -self.vel[0]
        if x > 640:
            x = (1280 - x)
            self.vel[0] = -self.vel[0]
        if y < 0:
            y = -y
            self.vel[1] = -self.vel[1]
        if y > 480:
            y = (960 - y)
            self.vel[1] = -self.vel[1]
        return x, y

    def get_acceleration(self, obstacles):
        ax, ay = [0,0]
        if obstacles != None:
            for obj in obstacles:
                
                x, y = obj.x, obj.y
                dx = x - self.x
                dy = y - self.y
                r = mag([dx,dy])

                if r < 10*self.schild(obj):
                    # if in a radius of influence
                    if obj.L == None:
                        obj.L = self.ang_momentum(obj)
                    obj.L += self.torque(obj, obstacles)
                else:
                    obj.L = None

                
                # Newtonian
                newt = G*obj.mass/(r*r*r)
                
                # Relativity
                rel = 0
                if relativistic and (obj.L != None):
                    rel = (3*obj.L*obj.L)/(c*r)**2
                
                ax += newt*(1+rel)*dx
                ay += newt*(1+rel)*dy

        return [ax, ay]


    ## Collision Handling ##
    
    def intersect(self, x0, y0, obj):
        #does the particle path cross the obstacle?
        
        if x0-self.x == 0:
            xmin = self.x
            ymin = obj.y
        elif y0 - self.y == 0:
            ymin = self.y
            xmin = obj.x
        
        else:
            m = float(y0-self.y)/(x0-self.x)
            c = y0 - m*x0
            xmin = (x0+m*y0-m*c)/(1+m*m)
            ymin = m*xmin + c
            
        dx = obj.x - xmin
        dy = obj.y - ymin
        
        return (dx*dx + dy*dy < self.radius+obj.radius) and ((self.x<=xmin<=x0) or (x0<=xmin<=self.x))

    def contact(self, x0, y0, obj):
        #find the point of first contact
        
        if self.vel[0] == 0 or self.vel[1] == 0:
            return self.lin_contact(x0, y0, obj)
        
        m = float(self.vel[1])/self.vel[0]
        c = y0 - m*x0
        
        a = 1 + m*m
        b = obj.x + m*obj.y - m*c
        c1 = obj.x**2 + obj.y**2 + c*c - 2*obj.y*c - (self.radius+obj.radius)**2
        det = np.sqrt(b*b - a*c1)
        
        if self.vel[0] > 0:
            x = (b - det)/a
        else:
            x = (b + det)/a

        return x, m*x+c

    def lin_contact(self, x0, y0, obj):
        # find point of first contact - special case
        
        x, y = obj.x, obj.y
        sep = self.radius+obj.radius
        
        if abs(dx)<sep:
            if self.vel[0] > 0:
                x0 = (x-sep)
            else:
                x0 = (x+sep)
        if abs(dy)<sep:
            if self.vel[1] > 0:
                y0 = (y-sep)
            else:
                y0 = (y+sep)
        return x0, y

    def collision(self, x0, y0, obstacles):
        if obstacles != None:
            for obj in obstacles:
                
                x, y = obj.x, obj.y
                dx = x - x0
                dy = y - y0
                sep = self.radius+obj.radius
                
                # is there a collision?
                if (dx*dx + dy*dy) < sep*sep or self.intersect(x0, y0, obj):
                    
                    # move to point of first contact
                    x1, y1 = self.contact(x0, y0, obj)
                    
                    # recoil angle
                    beta = 2*np.arctan2(dy,dx)-np.arctan2(self.vel[1],self.vel[0])

                    # recoil velocity
                    v = mag(self.vel)
                    self.vel = [-v*np.cos(beta), -v*np.sin(beta)]

                    # recoil position
                    R = mag([x0-x1,y0-y1])
                    x2 = x1 - R*np.cos(beta)
                    y2 = y1 - R*np.sin(beta)

                    return x2, y2
        return x0, y0


    ## Other Functions ##

    def ang_momentum(self, obj):
        dx = self.x-obj.x
        dy = self.y-obj.y
        return (dx*self.vel[1]-dy*self.vel[0])

    def update_angmom(self, obstacles, boost):
        # after a speed boost
        for obj in obstacles:
            if obj.L != None:
                dx = self.x - obj.x
                dy = self.y - obj.y
                obj.L += dx*boost[1] - dy*boost[0]

    def torque(self, obj, obstacles):
        torq = 0
        for ob in obstacles:
            if ob != obj:
                dx1 = self.x - obj.x
                dx2 = self.x - ob.x
                dy1 = self.y - obj.y
                dy2 = self.y - ob.y
                s = dx2*dy1 - dx1*dy2
                r = mag([dx2,dy2])
                torq += G*ob.mass*s/(r*r*r)
        return torq

    def schild(self, obj):
        return 2*G*obj.mass/(c*c)

    def potential(self, obstacles):
        U = 0
        for obj in obstacles:
            U += G*obj.mass/mag([self.x-obj.x,self.y-obj.y])
        return U

    def Lsquare(self, obstacles):
        for obj in obstacles:
            if obj.L != None:
                r = mag([self.x-obj.x,self.y-obj.y])
                return G*obj.mass*(obj.L/c)**2/(r**3)
        return 0

    def dilation(self, obstacles):
        t = 1
        if obstacles != None:
            U = self.potential(obstacles)
            t += mag(self.vel)/(c*c)
            t -= (2*U/(c*c))
            t -= 2*self.Lsquare(obstacles)/c**2
            t = np.sqrt(t)
            t /= (1-2*U/(c*c))
        return t


### Non-Class Functions ###

def mag(a):
    return np.sqrt(a[0]*a[0] + a[1]*a[1])

        
### Main ###

def main():    
    background = pygame.Surface(screen.get_size())
    background.fill((255, 255, 255))

    # create objects/sprites
    Planet = Particle([320, 240], [1.75,1.75], 50)
    Star = Particle([200, 200], [0,0], 500, True)
    Star1 = Particle([440, 200], [0,0], 500, True)
    obstacles = [Star, Star1]
    allSprites = pygame.sprite.Group(Planet, obstacles)
    
    clock = pygame.time.Clock()
    framenum = 0

    # main loop
    keepGoing = True
    while keepGoing:
        clock.tick(fps)
        
        boost = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False

            # boosts
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    boost = [-a, 0]
                elif event.key == pygame.K_RIGHT:
                    boost = [a, 0]
                elif event.key == pygame.K_UP:
                    boost = [0, -a]
                elif event.key == pygame.K_DOWN:
                    boost = [0, a]

        # update screen
        Planet.update(obstacles, boost)
        allSprites.clear(screen, background)
        allSprites.draw(screen)        
        pygame.display.flip()

        # record screen
        if record:
            pygame.image.save(screen, 'output/frame%05d.png' % framenum)
            framenum += 1

    # game over
    print pt, ct
    pygame.quit()


### Run ###

if __name__ == "__main__":
    main()
    
