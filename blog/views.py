from importlib.resources import contents
from turtle import title
from unicodedata import category
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from blog.models import Article as CategoryModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel

from django_rest_framework.permissions import RegistedMoreThanAWeekUser
from user.serializers import ArticleSerializer


# Create your views here.
class ArticleView(APIView):
    # 로그인 한 사용자의 게시글 목록을 return 해라
    # permission_classes = [permissions.IsAuthenticated]
    
    # def get(self, request):
    #     user = request.user
        
    #     articles = ArticleModel.objects.filter(user=user)
    #     title = [article.title for article in articles]  # list 축약 문법
        
    #     titles = []
        
    #     for article in articles:
    #         titles.append(article.title)
            
    #     return Response({"article_list": titles})
    
    permission_classes = [RegistedMoreThanAWeekUser]
    
    def get(self, request):
        article = ArticleSerializer(ArticleModel.objects.filter(user=request.user), many=True).data
        return Response(article)
    
    def post(self, request):
        title = request.data.get('title')
        category = request.data.get('category')
        content = request.data.get('content')
        
        if len(title) <= 5:
            return Response({'message': '제목이 5자 이하이기 때문에 게시글을 작성할 수 없습니다.'})
        elif len(content) <= 20:
            return Response({'message': '내용이 20자 이하이기 때문에 게시글을 작성할 수 없습니다.'})
        elif category == '' or None:
            return Response({'message': '카테고리가 지정되지 않았기 때문에 게시글을 작성할 수 없습니다.'})
        
        # category = CategoryModel.objects.get(name=request.data.get('category'))
        
        # article = ArticleModel(title=title, category=category, content=content)
        # article.save()
        # article.category.add(category)
            
        return Response({'message': '게시글이 작성되었습니다.'})