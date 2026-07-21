from django.contrib import admin
from .models import Category, Product

# Register your models here.
admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')

    search_fields = ('name', 'description')

    list_filter = ('category', 'created_at')