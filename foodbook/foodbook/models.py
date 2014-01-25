from django.db import models
from django.contrib.auth.models import User;

class IngredientType(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Ingredient(models.Model):
	name = models.CharField(max_length=100)
	modifier = models.CharField(max_length=100, null=True, blank=True)
	ingredient_type = models.ForeignKey(IngredientType)
	calories = models.DecimalField(max_digits=10, decimal_places=5, help_text="Kilocalories per gram")
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
	vitamin_a = models.DecimalField(max_digits=10, decimal_places=5, help_text="ug per gram")
	vitamin_c = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	calcium = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	iron = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	vitamin_d = models.DecimalField(max_digits=10, decimal_places=5, help_text="ug per gram")
	vitamin_b_6 = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	vitamin_b_12 = models.DecimalField(max_digits=10, decimal_places=5, help_text="ug per gram")
	magnesium = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")

	def __unicode__(self):
		return u'%s (%s)' % (self.name, self.modifier)

class ServingSize(models.Model):
	name = models.CharField(max_length=50)
	gram_conversion = models.DecimalField(max_digits=10, decimal_places=5)
	ingredients = models.ForeignKey(Ingredient)

	def __unicode__(self):
		return self.name

class Recipe(models.Model):
	user_id = models.ManyToManyField(User)
	name = models.CharField(max_length=50, blank=True)
	description = models.TextField(blank=True)
	servings = models.IntegerField(null = True, blank = True)
	ingredients = models.TextField(blank=True)
	instructions = models.TextField(blank=True)
	suggested = models.TextField(blank=True)
	upvotes = models.IntegerField()
	variant = models.ForeignKey('self', null = True, blank=True)
	public = models.BooleanField()

	def __unicode__(self):
		return self.name

class UserDiet(models.Model):
	user = models.ForeignKey(User)
	diet_description = models.CharField(max_length=50, blank=True)
	calories = models.IntegerField(null=True, blank=True)
	fat = models.IntegerField(null=True, blank=True)
	sugar = models.IntegerField(null=True, blank=True)
	protein = models.IntegerField(null=True, blank=True)

class UserPicture(models.Model):
	user_id = models.ForeignKey(User)
	pic_link = models.TextField()

class Comment(models.Model):
	original_poster = models.ForeignKey(User)
	receiving_user = models.ForeignKey(User, blank=True, null=True)
	receiving_recipe = models.ForeignKey(Recipe, blank=True, null=True)
	comment = models.TextField()
	date = models.DateTimeField(auto_now=True, auto_now_add=True)

class CustomIngredient(models.Model):
	name = models.CharField(max_length=100)
	modifier = models.CharField(max_length=100, null=True, blank=True)
	ingredient_type = models.ForeignKey(IngredientType)
	calories = models.DecimalField(max_digits=10, decimal_places=5, help_text="Kilocalories per gram")
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
	vitamin_a = models.DecimalField(max_digits=10, decimal_places=5, help_text="ug per gram")
	vitamin_c = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	calcium = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	iron = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	vitamin_d = models.DecimalField(max_digits=10, decimal_places=5, help_text="ug per gram")
	vitamin_b_6 = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	vitamin_b_12 = models.DecimalField(max_digits=10, decimal_places=5, help_text="ug per gram")
	magnesium = models.DecimalField(max_digits=10, decimal_places=5, help_text="mg per gram")
	restrictions = models.TextField()

class IngredientWrapper():
	def __init__(self, iid, quantity, measurement):
		self.ingredient_id = iid
		self.qty = quantity
		self.unit = measurement
		self.conversion = ServingSize.objects.get(name__iexact=measurement, ingredients__id=iid).gram_conversion
		self.name = Ingredient.objects.get(id=iid).name
		ingredient_modifier = Ingredient.objects.get(id=iid).modifier
		if ingredient_modifier:
			self.name = self.name + ' (' + ingredient_modifier + ')'
		self.servingsize = Ingredient.objects.get(id=iid).servingsize_set.all()