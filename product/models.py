from django.db import models
from django.utils import timezone


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    thumbnail = models.FileField(upload_to = 'product/', verbose_name="썸네일")
    content = models.TextField("제품설명")
    registration_date = models.DateTimeField("제품등록일자", auto_now_add=True)
    exposure_start = models.DateTimeField("노출시작일자", default=timezone.now)
    exposure_finish = models.DateTimeField("노출종료일자", default=timezone.now)
