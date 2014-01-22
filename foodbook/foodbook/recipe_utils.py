from models import Ingredient, ServingSize, IngredientWrapper
import decimal

## Returns an array of nutritional values (in order as defined by the model)
## using a JSON array of ingredients.
def calculate_nutritional_value(ingredients):
	nutrients = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	ingredient_list = []
	for i in xrange(len(ingredients['id'])):
		ingredient_list.append(IngredientWrapper(ingredients['id'][i], ingredients['qty'][i], ingredients['unit'][i]))
	for ingredient in ingredient_list:
		ingredient_info = Ingredient.objects.get(id=ingredient.ingredient_id)
		conversion = ingredient.conversion
		qty = decimal.Decimal(ingredient.qty)
		nutrients[0] += decimal.Decimal(ingredient_info.calories) * conversion * qty
		nutrients[1] += decimal.Decimal(ingredient_info.total_fat) * conversion * qty
		nutrients[2] += decimal.Decimal(ingredient_info.saturated_fat) * conversion * qty
		nutrients[3] += decimal.Decimal(ingredient_info.polyunsaturated_fat) * conversion * qty
		nutrients[4] += decimal.Decimal(ingredient_info.monounsaturated_fat) * conversion * qty
		nutrients[5] += decimal.Decimal(ingredient_info.trans_fat) * conversion * qty
		nutrients[6] += decimal.Decimal(ingredient_info.cholesterol) * conversion * qty
		nutrients[7] += decimal.Decimal(ingredient_info.sodium) * conversion * qty
		nutrients[8] += decimal.Decimal(ingredient_info.potassium) * conversion * qty
		nutrients[9] += decimal.Decimal(ingredient_info.total_carbohydrates) * conversion * qty
		nutrients[10] += decimal.Decimal(ingredient_info.dietary_fiber) * conversion * qty
		nutrients[11] += decimal.Decimal(ingredient_info.sugar) * conversion * qty
		nutrients[12] += decimal.Decimal(ingredient_info.vitamin_a) * conversion * qty
		nutrients[13] += decimal.Decimal(ingredient_info.vitamin_c) * conversion * qty
		nutrients[14] += decimal.Decimal(ingredient_info.calcium)  * conversion * qty
		nutrients[15] += decimal.Decimal(ingredient_info.iron) * conversion * qty
		nutrients[16] += decimal.Decimal(ingredient_info.vitamin_d) * conversion * qty
		nutrients[17] += decimal.Decimal(ingredient_info.vitamin_b_6) * conversion * qty
		nutrients[18] += decimal.Decimal(ingredient_info.vitamin_b_12) * conversion * qty
		nutrients[19] += decimal.Decimal(ingredient_info.magnesium) * conversion * qty
	return nutrients

################## JSON Utils
def decimal_json(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError