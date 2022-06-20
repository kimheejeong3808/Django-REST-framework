from django.contrib import admin
from blog.models import Category as CategoryModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel


# Register your models here.
admin.site.register(CategoryModel)
admin.site.register(ArticleModel)
admin.site.register(CommentModel)