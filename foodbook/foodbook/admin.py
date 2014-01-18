from django.contrib import admin
from models import Ingredient, IngredientType, ServingSize

class ServingSizeAdmin(admin.ModelAdmin):
	list_display = ('name', 'abbr', 'gram_conversion')

admin.site.register(Ingredient)
admin.site.register(ServingSize, ServingSizeAdmin)
admin.site.register(IngredientType)