from urllib2 import urlopen
from time import gmtime

places = ["metrocentre/4b1fc511f964a520db2824e3","the-trafford-centre/4be453ef2468c928b09cfe42","westfield-stratford-city/4c4d624bdb2c20a12730b972",
          "bluewater-shopping-centre/4ae1cbb8f964a5207b8721e3","merry-hill-shopping-centre/4b058830f964a520b9b722e3","westfield-london-shopping-centre/4ad08b28f964a52064d820e3",
          "manchester-arndale/4ade0e37f964a5206a6f21e3","meadowhall-shopping-centre/4b116a9ff964a520257c23e3","lakeside-shopping-centre/4be6942dd4f7c9b6e5e22620",
          "eldon-square-shopping-centre/4b576f8ef964a520943728e3","liverpool-one/4bb935aa98c7ef3b9fec3102","st-davids-dewi-sant/4b60506ff964a52025df29e3",
          "bullring-shopping-centre/4b0838f9f964a520a10623e3","whitgift-centre/4b239f53f964a520535724e3","thecentremk/4b400bf7f964a520d1b425e3","westfield-derby-shopping-centre/4b531c4df964a5203d8f27e3",
          "highcross-shopping-centre/4b5afb30f964a52041dd28e3","the-frenchgate-shopping-centre/4b9b79d5f964a520b10936e3","parkgate-shopping-centre/4b980b96f964a520882835e3",
          "victoria-square-shopping-centre/4b03d73ff964a520535022e3","the-oracle/4b1cd272f964a520fb0924e3","eden-shopping-centre/4b5adc10f964a520bbd728e3"]

date = gmtime()
output = "{}/{}/{}".format(date.tm_mday,date.tm_mon,date.tm_year)

def fetch():
    
    global output
    f = open('checkins.txt', 'a')
    z = 'https://foursquare.com/v/'
    
    for venue in places:
        for line in urlopen(z+venue):
            if '<strong>Total<br />check-ins' in line:
                a = str(line)
                a = a[111:].replace('</span></span>\n', '')
                print "{} - {}\n".format(venue[:venue.index("/")].replace("-"," "),a)
                output += "\t{}".format(a)
                
    f.write(output+"\n")
    f.close()
    print "Complete!"

# Run once to set titles/names of centres along top of file
def title():
    f = open('checkins.txt', 'a')
    f.write("Date")
    for venue in places:
        f.write("\t{}".format(venue[:venue.index("/")].replace("-"," ")))
    f.write("\n")
    f.close()


#title()
fetch()
