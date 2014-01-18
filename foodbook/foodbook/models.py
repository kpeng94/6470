from django.db import models

class IngredientType(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Ingredient(models.Model):
	name = models.CharField(max_length=100)
	modifier = models.CharField(max_length=100, null=True, blank=True)
	ingredient_type = models.ManyToManyField(IngredientType)
	calories = models.DecimalField(max_digits=10, decimal_places=5, help_text="Calories per gram")
	total_fat = models.DecimalField(max_digits=10, decimal_places=5, help_text="Total fat (g) per gram")
	saturated_fat = models.DecimalField(max_digits=10, decimal_places=5, help_text="Saturated fat (g) per gram")
	polyunsaturated_fat = models.DecimalField(max_digits=10, decimal_places=5, help_text="Polysaturated fat (g) per gram")
	monounsaturated_fat = models.DecimalField(max_digits=10, decimal_places=5, help_text="Monounsaturated fat (g) per gram")
	trans_fat = models.DecimalField(max_digits=10, decimal_places=5, help_text="Trans fat (g) per gram")
	cholesterol = models.DecimalField(max_digits=10, decimal_places=5, help_text="Cholesterol (mg) per gram")
	sodium = models.DecimalField(max_digits=10, decimal_places=5, help_text="Sodium (mg) per gram")
	potassium = models.DecimalField(max_digits=10, decimal_places=5, help_text="Potassium (mg) per gram")
	total_carbohydrates = models.DecimalField(max_digits=10, decimal_places=5, help_text="Total carbohydrate (g) per gram")
	dietary_fiber = models.DecimalField(max_digits=10, decimal_places=5, help_text="Dietary fiber (g) per gram")
	sugar = models.DecimalField(max_digits=10, decimal_places=5, help_text="Sugar (g) per gram")
	protein = models.DecimalField(max_digits=10, decimal_places=5, help_text="Protein (g) per gram")
	vitamin_a = models.DecimalField(max_digits=10, decimal_places=5, help_text="Per gram")
	vitamin_c = models.DecimalField(max_digits=10, decimal_places=5, help_text="Per gram")
	calcium = models.DecimalField(max_digits=10, decimal_places=5, help_text="Per gram")
	iron = models.DecimalField(max_digits=10, decimal_places=5, help_text="Per gram")
	vitamin_d = models.DecimalField(max_digits=10, decimal_places=5, help_text="Per gram")
	vitamin_b_6 = models.DecimalField(max_digits=10, decimal_places=5, help_text="Per gram")
	vitamin_b_12 = models.DecimalField(max_digits=10, decimal_places=5, help_text="Per gram")
	magnesium = models.DecimalField(max_digits=10, decimal_places=5, help_text="Per gram")

	def __unicode__(self):
		return u'%s (%s)' % (self.name, self.modifier)

class ServingSize(models.Model):
	name = models.CharField(max_length=20)
	abbr = models.CharField(max_length=10)
	gram_conversion = models.DecimalField(max_digits=10, decimal_places=5)
	ingredients = models.ManyToManyField(Ingredient)

	def __unicode__(self):
		return self.name