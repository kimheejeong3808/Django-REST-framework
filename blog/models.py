from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField("이름", max_length=70, default='')
    description = models.TextField("설명")
    
    def __str__(self):
        return f'{self.name}'
    
class Article(models.Model):
    user = models.ForeignKey('user.User', verbose_name="작성자", on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    category = models.ManyToManyField("Category", verbose_name="카테고리")
    content = models.TextField("본문")
    exposure_start = models.DateTimeField("노출시작일자", default=timezone.now())
    exposure_finish = models.DateTimeField("노출종료일자", default=timezone.now())
    
    def __str__(self):
        return f'{self.title}을 작성하셨습니다.'
    
    
class Comment(models.Model):
    article = models.ForeignKey('Article', verbose_name="게시글", on_delete=models.CASCADE)
    comment_user = models.ForeignKey('user.User', verbose_name="댓글작성자", on_delete=models.CASCADE)
    comment_content = models.TextField("댓글내용", max_length=100)
    
    def __str__(self):
        return f'{self.comment_content}을 작성하셨습니다.'