import urllib2
import StringIO
import csv
import decimal
from foodbook.models import Ingredient, IngredientType, ServingSize

TOT = 8463

class FoodStuff(object):
    def __init__(self, foodid, name, modifier, units, data):
        self.id = foodid
        self.name = name
        self.modifier = modifier
        self.data = data
        self.units = units

def get_csv(i):
    url = 'http://ndb.nal.usda.gov/ndb/foods/show/%s?format=Abridged&reportfmt=csv' % i
    response = urllib2.urlopen(url)
    return response.read()

def parse_csv(dat, cut_first_letter=False):
    dat = list(csv.reader(StringIO.StringIO(dat)))

    name = dat[3][0].split(':')[1].strip()
    ind = name.index(',')
    foodid = int(name[:ind])
    name = name[ind+1:]
    if(cut_first_letter):
        name = name[name.index(',')+1:].strip().capitalize()
        print name
    ind = name.find(',')
    if ind == -1:
        modifier = ''
    else:
        name, modifier = name[:ind].strip(), name[ind+1:].strip()
    units = []
    data = {}

    line = dat[4]
    print line
    print len(line)-1
    units.append(('g', 1.0))
    for i in xrange(3, len(line)-1):
        unit = line[i].split('"')
        print unit[-1][:-1]
        units.append(('"'.join(unit[1:-1]).strip(), decimal.Decimal(unit[-1][:-1])))

    dat = dat[5:]
    for line in dat:
        if len(line) >= 3:
            data[line[0]] = (float(line[2]) / 100, line[1].replace('\xc2\xb5', '\xe6')) 

    return FoodStuff(foodid, name, modifier, units, data)

def save_foods(foodstuffs, type):
    for food in foodstuffs:
        cal = 0
        if 'Energy' in food.data:
            cal = food.data['Energy'][0]
        total_fat = 0
        if 'Total lipid (fat)' in food.data:
            total_fat = food.data['Total lipid (fat)'][0]
        sat_fat = 0
        if 'Fatty acids, total saturated' in food.data:
            sat_fat = food.data['Fatty acids, total saturated'][0]
        mono_fat = 0
        if 'Fatty acids, total monounsaturated' in food.data:
            mono_fat = food.data['Fatty acids, total monounsaturated'][0]
        poly_fat = 0
        if 'Fatty acids, total polyunsaturated' in food.data:
            poly_fat = food.data['Fatty acids, total polyunsaturated'][0]
        trans_fat = 0
        if 'Fatty acids, total trans' in food.data:
            trans_fat = food.data['Fatty acids, total trans'][0]
        cholesterol = 0
        if 'Cholesterol' in food.data:
            cholesterol = food.data['Cholesterol'][0]
        sodium = 0
        if 'Sodium, Na' in food.data:
            sodium = food.data['Sodium, Na'][0]
        potassium = 0
        if 'Potassium, K' in food.data:
            potassium = food.data['Potassium, K'][0]
        carbs = 0
        if 'Carbohydrate, by difference' in food.data:
            carbs = food.data['Carbohydrate, by difference'][0]
        fiber = 0
        if 'Fiber, total dietary' in food.data:
            fiber = food.data['Fiber, total dietary'][0]
        sugar = 0
        if 'Sugars, total' in food.data:
            sugar = food.data['Sugars, total'][0]
        protein = 0
        if 'Protein' in food.data:
            protein = food.data['Protein'][0]
        vit_a = 0
        if 'Vitamin A, RAE' in food.data:
            vit_a = food.data['Vitamin A, RAE'][0]
        vit_c = 0
        if 'Vitamin C, total ascorbic acid' in food.data:
            vit_c = food.data['Vitamin C, total ascorbic acid'][0]
        calcium = 0
        if 'Calcium, Ca' in food.data:
            calcium = food.data['Calcium, Ca'][0]
        iron = 0
        if 'Iron, Fe' in food.data:
            iron = food.data['Iron, Fe'][0]
        vit_d = 0
        if 'Vitamin D (D2 + D3)' in food.data:
            vit_d = food.data['Vitamin D (D2 + D3)'][0]
        vit_b_6 = 0
        if 'Vitamin B-6' in food.data:
            vit_b = food.data['Vitamin B-6'][0]
        vit_b_12 = 0
        if 'Vitamin B-12' in food.data:
            vit_b_12 = food.data['Vitamin B-12'][0]
        magnesium = 0
        if 'Magnesium, Mg' in food.data:
            magnesium = food.data['Magnesium, Mg'][0]
        new_food = Ingredient(name=food.name, modifier=food.modifier, ingredient_type=IngredientType.objects.get(name=type),
            calories=cal, total_fat=total_fat, saturated_fat=sat_fat, polyunsaturated_fat=poly_fat,
            monounsaturated_fat=mono_fat, trans_fat=trans_fat, cholesterol=cholesterol, sodium = sodium,
            potassium = potassium, total_carbohydrates=carbs, sugar=sugar, protein=protein,
            vitamin_a=vit_a, vitamin_c=vit_c, calcium=calcium, iron=iron, vitamin_d=vit_d, vitamin_b_6=vit_b_6,
            vitamin_b_12=vit_b_12 ,magnesium=magnesium)
        new_food.save()
        for unit in food.units:
            new_unit = ServingSize(name=unit[0], gram_conversion=unit[1], ingredients=new_food)
            new_unit.save()


def get_foods(start=1, end=TOT, cut_first_letter=False):
    dat = []
    for i in xrange(start, end):
        print "Getting food #%s" % i
        dat.append(parse_csv(get_csv(i),cut_first_letter))
    return dat