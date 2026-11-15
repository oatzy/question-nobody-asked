from random import shuffle

class Player():
    def __init__(self,name):
        self.name = name
        self.grid = []
        self.points = 0
        self.bank = 0
        self.mirror = False
        self.shield = False

    def buildGrid(self):
        self.grid = []
        i = 0
        while i<25:
            self.grid += ["200"]
            if i<10:
                self.grid += ["1000"]
            i += 1
        self.grid += ["3000", "3000", "5000"]
        self.grid += ["rob", "kill", "gift", "swap", "peak"]
        self.grid += ["choose", "bomb", "shield", "mirror"]
        self.grid += ["double", "bank"]
        shuffle(self.grid)

    def getScore(self):
        return self.points + self.bank

    def getPoints(self):
        return self.points

    def setPoints(self,num):
        self.points = num

    def addPoints(self,num):
        self.points += num

    def collect(self,kind):
        if kind == "200":
            self.points += 200
        elif kind == "1000":
            self.points += 1000
        elif kind == "3000":
            self.points += 3000
        elif kind == "5000":
            self.points += 5000
        elif kind == "double":
            self.points *= 2
        elif kind == "bomb":
            self.points = 0
        elif kind == "bank":
            self.bank, self.points = self.points, 0
        elif kind == "mirror":
            self.mirror = True
        elif kind == "shield":
            self.shield = True

    def attack(self,player, kind):
        if player.defend(self, kind):
            return
        if kind == "rob":
            self.points += player.getPoints()
            player.setPoints(0)
        elif kind == "kill":
            player.setPoints(0)
        elif kind == "gift":
            player.addPoints(1000)
        elif kind == "swap":
            temp = self.points
            self.points = player.getPoints()
            player.setPoints(temp)

    def defend(self, player, kind):
        if (not(self.mirror or self.shield)) or kind=="gift":
            return False
        if self.shield:
            self.shield = False
        elif self.mirror:
            self.mirror = False
            self.attack(player, kind)
        return True

    def doItemAction(self, player, kind):
        if kind in ["rob", "kill", "gift", "swap"]:
            self.attack(player, kind)
        else:
            self.collect(kind)

    def doIndexAction(self, player, index):
        self.doItemAction(player, self.grid[index])
    
if __name__ == "__main__":
    wins = [0,0]
    player1 = Player("Player1")
    player2 = Player("player2")
    queue = [i for i in xrange(49)]
    for n in xrange(10000):
        player1.buildGrid()
        player2.buildGrid()
        shuffle(queue)
        for i in queue:
            player1.doIndexAction(player2, i)
            player2.doIndexAction(player1, i)
        if player1.getScore() > player2.getScore():
            print "player 1 wins"
            wins[0] += 1
        else:
            print "player 2 wins"
            wins[1] += 1
    print wins
    
