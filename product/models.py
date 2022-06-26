from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    thumbnail = models.FileField(upload_to = 'product/', verbose_name="썸네일")
    content = models.TextField("제품설명")
    created = models.DateTimeField("등록시간", auto_now_add=True)
    modified = models.DateTimeField("수정시간", auto_now=True)
    exposure_end_date = models.DateField("노출 종료 일자")
    is_active = models.BooleanField("활성화 여부")
    price = models.IntegerField("가격")
    
class Review(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey('product.Product', verbose_name="상품", on_delete=models.SET_NULL, null=True)
    content = models.TextField("내용")
    created = models.DateTimeField("등록시간", auto_now_add=True)
    rating = models.IntegerField("평점")

    
