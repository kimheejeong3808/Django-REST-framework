from django.contrib import admin
from product.models import Product as ProductModel
from product.models import Review as ReviewModel

# Register your models here.

admin.site.register(ProductModel)
admin.site.register(ReviewModel)