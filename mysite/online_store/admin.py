from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import *



class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1

class Consultation_KeysInline(admin.TabularInline):
    model = Consultation_Keys
    extra = 0

@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    inlines = [ProductPhotoInline,Consultation_KeysInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
admin.site.register(Category)
admin.site.register(Pattern)
# admin.site.register(Review)
# admin.site.register(Rating)
# admin.site.register(UserProfile)
# admin.site.register(Cart)
# admin.site.register(CarItem)
