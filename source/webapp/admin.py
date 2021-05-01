from django.contrib import admin
from django.apps import apps
from .models import Product, Category, Review
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description','category']
    list_filter = ['name']
    search_fields = ['name', 'category']
    fields = ['id', 'name', 'description','category','picture']
    readonly_fields = ['id']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']
    list_filter = ['category']
    search_fields = ['category']
    fields = ['category']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'product','review', 'rating', 'created_at', 'updated_at']
    list_filter = ['author']
    search_fields = ['author', 'rating']
    fields = ['id','author', 'product','review', 'rating', 'created_at', 'updated_at']
    readonly_fields = ['id']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)



