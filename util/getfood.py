import urllib2

class FoodStuff(object):
    def __init__(self):
        pass

def get_csv(i):
    url = 'http://ndb.nal.usda.gov/ndb/foods/show/%s?format=Abridged&reportfmt=csv' % i
    response = urllib2.urlopen(url)
    return response.read()

def parse_csv(csv):
    csv = csv.split('\n')

    name = csv[3].split(':')[1].strip()
    ind = name.index(',')
    foodid, name = int(name[:ind]), name[ind+1:-1]

    csv = csv[5:]
    for line in csv:
        pass
    return (foodid, name)