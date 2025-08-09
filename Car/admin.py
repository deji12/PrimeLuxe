from django.contrib import admin
from .models import Car, CarAmenity, CarImage, Review
from import_export.admin import ImportExportModelAdmin

class CarAmenityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'icon', 'is_search_filter_enabled')
    search_fields = ('name',)

class CarAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'brand', 'price_per_day', 'fuel_type', 'transmission')
    search_fields = ('name', 'brand', 'transmission')
    list_filter = ('brand', 'transmission', 'fuel_type', 'is_available', 'body_type', 'rating')
    filter_horizontal = ('amenities',)

class CarImageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('car', 'image')
    search_fields = ('car__name',)

class ReviewAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'car', 'rating', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('rating',)

admin.site.register(CarAmenity, CarAmenityAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(CarImage, CarImageAdmin)
admin.site.register(Review, ReviewAdmin)
