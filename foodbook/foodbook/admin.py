from django.contrib import admin
from models import Ingredient, IngredientType, ServingSize, Recipe, UserPicture

class ServingSizeAdmin(admin.ModelAdmin):
	list_display = ('name', 'gram_conversion')

admin.site.register(Ingredient)
admin.site.register(ServingSize, ServingSizeAdmin)
admin.site.register(IngredientType)
admin.site.register(Recipe)
admin.site.register(UserPicture)