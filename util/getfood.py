import urllib2
import StringIO
import csv

TOT = 8463

class FoodStuff(object):
    def __init__(self, foodid, name, data):
        self.id = foodid
        self.name = name
        self.data = data

def get_csv(i):
    url = 'http://ndb.nal.usda.gov/ndb/foods/show/%s?format=Abridged&reportfmt=csv' % i
    response = urllib2.urlopen(url)
    return response.read()

def parse_csv(dat):
    dat = list(csv.reader(StringIO.StringIO(dat)))

    name = dat[3][0].split(':')[1].strip()
    ind = name.index(',')
    foodid, name = int(name[:ind]), name[ind+1:]
    data = {}

    dat = dat[5:]
    for line in dat:
        if len(line) >= 3:
            data[line[0]] = (float(line[2]) / 100, line[1].replace('\xc2\xb5', '\xe6')) 
    return FoodStuff(foodid, name, data)

def get_foods(start=1, end=TOT):
    dat = []
    for i in xrange(start, end):
        print "Getting food #%s" % i
        dat.append(parse_csv(get_csv(i)))
    return dat