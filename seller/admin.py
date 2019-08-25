from django.contrib import admin
from .models import Seller, Category, SubCategory, Product, Pcount

# Register your models here.
admin.site.register(Seller)

admin.site.register(Category)

admin.site.register(SubCategory)

admin.site.register(Product)

admin.site.register(Pcount)
