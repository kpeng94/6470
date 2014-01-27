from models import Ingredient, ServingSize, IngredientWrapper, UserDiet
import decimal

## Returns an array of nutritional values (in order as defined by the model)
## using a JSON array of ingredients.
def calculate_nutritional_value(ingredients, user, ss):
	nutrients = dict()
	nutrients['calories'] = [0.0,0.0]
	nutrients['total-fat'] = [0.0,0.0]
	nutrients['saturated'] = [0.0,0.0]
	nutrients['polyunsaturated'] = [0.0,0.0]
	nutrients['monounsaturated'] = [0.0,0.0]
	nutrients['trans'] = [0.0,0.0]
	nutrients['cholesterol'] = [0.0,0.0]
	nutrients['sodium'] = [0.0,0.0]
	nutrients['potassium'] = [0.0,0.0]
	nutrients['carbohydrates'] = [0.0,0.0]
	nutrients['fiber'] = [0.0,0.0]
	nutrients['vita'] = [0.0,0.0]
	nutrients['vitc'] = [0.0,0.0]
	nutrients['calcium'] = [0.0,0.0]
	nutrients['iron'] = [0.0,0.0]
	nutrients['vitd'] = [0.0,0.0]
	nutrients['vitb6'] = [0.0,0.0]
	nutrients['vitb12'] = [0.0,0.0]
	nutrients['magnesium'] = [0.0,0.0]
	nutrients['protein'] = [0.0,0.0]
	ingredient_list = []
	for i in xrange(len(ingredients['id'])):
		ingredient_list.append(IngredientWrapper(ingredients['id'][i], ingredients['qty'][i], ingredients['unit'][i]))
	for ingredient in ingredient_list:
		ingredient_info = Ingredient.objects.get(id=ingredient.ingredient_id)
		conversion = ingredient.conversion
		qty = decimal.Decimal(ingredient.qty)
		nutrients['calories'][0] += decimal.Decimal(ingredient_info.calories) * conversion * qty
		nutrients['total-fat'][0] += decimal.Decimal(ingredient_info.total_fat) * conversion * qty
		nutrients['saturated'][0] += decimal.Decimal(ingredient_info.saturated_fat) * conversion * qty
		nutrients['polyunsaturated'][0] += decimal.Decimal(ingredient_info.polyunsaturated_fat) * conversion * qty
		nutrients['monounsaturated'][0] += decimal.Decimal(ingredient_info.monounsaturated_fat) * conversion * qty
		nutrients['trans'][0] += decimal.Decimal(ingredient_info.trans_fat) * conversion * qty
		nutrients['cholesterol'][0] += decimal.Decimal(ingredient_info.cholesterol) * conversion * qty
		nutrients['sodium'][0] += decimal.Decimal(ingredient_info.sodium) * conversion * qty
		nutrients['potassium'][0] += decimal.Decimal(ingredient_info.potassium) * conversion * qty
		nutrients['carbohydrates'][0] += decimal.Decimal(ingredient_info.total_carbohydrates) * conversion * qty
		nutrients['fiber'][0] += decimal.Decimal(ingredient_info.dietary_fiber) * conversion * qty
		nutrients['vita'][0] += decimal.Decimal(ingredient_info.vitamin_a) * conversion * qty
		nutrients['vitc'][0] += decimal.Decimal(ingredient_info.vitamin_c) * conversion * qty
		nutrients['calcium'][0] += decimal.Decimal(ingredient_info.calcium)  * conversion * qty
		nutrients['iron'][0] += decimal.Decimal(ingredient_info.iron) * conversion * qty
		nutrients['vitd'][0] += decimal.Decimal(ingredient_info.vitamin_d) * conversion * qty
		nutrients['vitb6'][0] += decimal.Decimal(ingredient_info.vitamin_b_6) * conversion * qty
		nutrients['vitb12'][0] += decimal.Decimal(ingredient_info.vitamin_b_12) * conversion * qty
		nutrients['magnesium'][0] += decimal.Decimal(ingredient_info.magnesium) * conversion * qty
		nutrients['protein'][0] += decimal.Decimal(ingredient_info.protein) * conversion * qty
	user = UserDiet.objects.filter(user=user)
	calories = 2000
	fat = 65
	sugar = 300
	protein = 50
	if len(user) > 0:
		user = user[0]
		if user.calories:
			calories = user.calories
		if user.fat:
			fat = user.fat
		if user.sugar:
			sugar = user.sugar
		if user.protein:
			protein = user.protein
	nutrients['calories'][1] = nutrients['calories'][0]/calories
	nutrients['total-fat'][1] = nutrients['total-fat'][0]/fat
	nutrients['saturated'][1] = nutrients['saturated'][0]/20
	nutrients['trans'][1] = 100.0 if nutrients['trans'][0] > 0 else 0.0
	nutrients['cholesterol'][1] = nutrients['cholesterol'][0]/300
	nutrients['sodium'][1] = nutrients['sodium'][0]/2400
	nutrients['potassium'][1] = nutrients['potassium'][0]/4700
	nutrients['carbohydrates'][1] = nutrients['carbohydrates'][0]/sugar
	nutrients['fiber'][1] = nutrients['fiber'][0]/25
	nutrients['vita'][1] = nutrients['vita'][0]/900
	nutrients['vitc'][1] = nutrients['vita'][0]/90
	nutrients['calcium'][1] = nutrients['calcium'][0]/1300
	nutrients['iron'][1] = nutrients['iron'][0]/18
	nutrients['vitd'][1] = nutrients['vitd'][0]/15
	nutrients['vitb6'][1] = nutrients['vitb6'][0]/2
	nutrients['vitb12'][1] = nutrients['vitb12'][0]/2.4
	nutrients['magnesium'][1] = nutrients['magnesium'][0]/420
	nutrients['protein'][1] = nutrients['protein'][0]/protein
	return nutrients

################## JSON Utils
def decimal_json(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError