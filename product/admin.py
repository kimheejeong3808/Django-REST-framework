from django.contrib import admin
from product.models import Product as ProductModel
from product.models import Review as ReviewModel


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','user','title')
    list_display_links = ('title',)
    list_filter = ('user',)
    serch_fields = ('user',)
    
    fieldsets = (
        ("info", {'fields': ('user', 'title',"is_active", "price",)}),
        ("img", {'fields' : ('thumbnail', )}),
        ('date', {'fields': ('created', 'exposure_end_date', )}),)
    
    filter_horizontal = []
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('user', 'created', )
        else:
            return ('created', )
    
admin.site.register(ProductModel, ProductAdmin)
admin.site.register(ReviewModel)