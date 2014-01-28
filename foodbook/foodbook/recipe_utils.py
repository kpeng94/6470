from models import Ingredient, ServingSize, IngredientWrapper, UserDiet
import decimal

## Returns an array of nutritional values (in order as defined by the model)
## using a JSON array of ingredients.
def calculate_nutritional_value(ingredients, user, ss):
	ss = decimal.Decimal(ss)
	nutrients = dict()
	nutrients['calories'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['total-fat'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['saturated'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['polyunsaturated'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['monounsaturated'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['trans'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['cholesterol'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['sodium'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['potassium'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['carbohydrates'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['fiber'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['vita'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['vitc'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['calcium'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['iron'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['vitd'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['vitb6'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['vitb12'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['magnesium'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
	nutrients['protein'] = [decimal.Decimal(0.0),decimal.Decimal(0.0)]
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
	calories = decimal.Decimal(2000)
	fat = decimal.Decimal(65)
	sugar = decimal.Decimal(300)
	protein = decimal.Decimal(50)
	if len(user) > 0:
		user = user[0]
		if user.calories:
			calories = decimal.Decimal(user.calories)
		if user.fat:
			fat = decimal.Decimal(user.fat)
		if user.sugar:
			sugar = decimal.Decimal(user.sugar)
		if user.protein:
			protein = decimal.Decimal(user.protein)
	nutrients['calories'][1] = nutrients['calories'][0]/calories
	nutrients['total-fat'][1] = nutrients['total-fat'][0]/fat
	nutrients['saturated'][1] = nutrients['saturated'][0]/decimal.Decimal(20)
	nutrients['monounsaturated'][1] = nutrients['monounsaturated'][0]/decimal.Decimal(22.5)
	nutrients['polyunsaturated'][1] = nutrients['polyunsaturated'][0]/decimal.Decimal(22.5)
	nutrients['trans'][1] = decimal.Decimal(100) if nutrients['trans'][0] > 0 else decimal.Decimal(0.0)
	nutrients['cholesterol'][1] = nutrients['cholesterol'][0]/decimal.Decimal(300)
	nutrients['sodium'][1] = nutrients['sodium'][0]/decimal.Decimal(2400)
	nutrients['potassium'][1] = nutrients['potassium'][0]/decimal.Decimal(4700)
	nutrients['carbohydrates'][1] = nutrients['carbohydrates'][0]/sugar
	nutrients['fiber'][1] = nutrients['fiber'][0]/decimal.Decimal(25)
	nutrients['vita'][1] = nutrients['vita'][0]/decimal.Decimal(900)
	nutrients['vitc'][1] = nutrients['vita'][0]/decimal.Decimal(90)
	nutrients['calcium'][1] = nutrients['calcium'][0]/decimal.Decimal(1300)
	nutrients['iron'][1] = nutrients['iron'][0]/decimal.Decimal(18)
	nutrients['vitd'][1] = nutrients['vitd'][0]/decimal.Decimal(15)
	nutrients['vitb6'][1] = nutrients['vitb6'][0]/decimal.Decimal(2)
	nutrients['vitb12'][1] = nutrients['vitb12'][0]/decimal.Decimal(2.4)
	nutrients['magnesium'][1] = nutrients['magnesium'][0]/decimal.Decimal(420)
	nutrients['protein'][1] = nutrients['protein'][0]/decimal.Decimal(protein)
	for key in nutrients:
		nutrients[key] = [nutrients[key][0]/ss, nutrients[key][1]/ss*decimal.Decimal(100)]
	return nutrients

def search_recipes(request, recipes, search='', sugar=None, fat=None, protein=None, calories=None, hide=False):
	recipes = recipes.filter(name__icontains=search)
	allow = []
	new_recipes = recipes
	if hide:
		for recipe in recipes:
			if not is_allowed(request, recipe, sugar=sugar, fat=fat, protein=protein, calories=calories):
				new_recipes = new_recipes.exclude(id=recipe.id)
		return list([new_recipes])
	else:
		for recipe in recipes:
			if is_allowed(request, recipe, sugar=sugar, fat=fat, protein=protein, calories=calories):
				allow.append(True)
			else:
				allow.append(False)
		return [new_recipes,allow]

def is_allowed(request, recipe, sugar=None, fat=None, protein=None, calories=None):
	if request.user.is_authenticated():
		diet = UserDiet.objects.filter(user=request.user)
		if len(diet) > 0:
			diet = diet[0]
			if (recipe.halal and diet.halal) or (recipe.lacto and diet.lacto) or (recipe.lactoovo and diet.lactoovo) or (recipe.vegan and diet.vegan) or (recipe.diabetes and diet.diabetes) or (recipe.hypertension and diet.hypertension) or (recipe.nuts and diet.nuts) or (recipe.eggs and diet.eggs) or (recipe.soy and diet.soy) or (recipe.shellfish and diet.shellfish) or (recipe.fish and diet.fish):
				return False
			if not sugar:
				sugar = diet.sugar
			if not fat:
				fat = diet.fat
			if not protein:
				protein = diet.protein
			if not calories:
				calories = diet.calories
	if sugar and (sugar <= recipe.total_carbohydrates):
		return sugar
	if fat and fat <= recipe.total_fat:
		return False
	if protein and protein <= recipe.protein:
		return False
	if calories and calories <= recipe.calories:
		return False
	return True

################## JSON Utils
def decimal_json(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError