from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import SiteInformation, FlashMessage, Testimonial

class SiteInformationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_number', 'address')
    search_fields = ('site_name', 'contact_email', 'contact_number')
    fieldsets = (
        (None, {
            'fields': ('site_name', 'logo', 'favicon')
        }),
        ('Social Links', {
            'fields': ('facebook_link', 'twitter_link', 'instagram_link', 'tiktok_link')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_number', 'address')
        }),
    )

class FlashMessageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('message', 'published', 'created_at')
    search_fields = ('message',)
    list_filter = ('published', 'created_at')

class TestimonialAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('name', 'content')
    search_fields = ('name',)

admin.site.register(FlashMessage, FlashMessageAdmin)
    
admin.site.register(SiteInformation, SiteInformationAdmin)

admin.site.register(Testimonial, TestimonialAdmin)