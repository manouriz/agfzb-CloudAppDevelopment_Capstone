from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    #list_display = ('name', 'dealerId')
    #list_filter = ['dealerId']
    #search_fields = ['name', 'description']

# Register models here
admin.site.register(CarMake)
admin.site.register(CarModel)