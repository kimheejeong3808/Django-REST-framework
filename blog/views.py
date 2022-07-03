from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status


from blog.models import Article as CategoryModel
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel

from django_rest_framework.permissions import IsAdminOrIsAuthenticatedReadOnly, RegisteredMoreThanThreeDaysUser
from user.serializers import ArticleSerializer


# Create your views here.
class ArticleView(APIView):
    # 로그인 한 사용자의 게시글 목록을 return 해라
    # permission_classes = [RegisteredMoreThanThreeDaysUser]
    
    # def get(self, request):
    #     user = request.user
        
    #     articles = ArticleModel.objects.filter(user=user)
    #     titles = [article.title for article in articles]  # list 축약 문법
        
    #     titles = []
        
    #     for article in articles:
    #         titles.append(article.title)
            
    #     return Response({"article_list": titles})
    
    permission_classes = [IsAdminOrIsAuthenticatedReadOnly]
    
    def get(self, request):
        # article = ArticleSerializer(ArticleModel.objects.filter(user=request.user), many=True).data
        
        # OrderDict로 order_by 정렬 못함
        # article = ArticleSerializer(ArticleModel.objects.filter(exposure_start__lte=timezone.now(), exposure_finish__gte=timezone.now()), many=True).data
        # print(article)
        # return Response(article)
    
        articles = ArticleModel.objects.filter(exposure_start__lte=timezone.now(), exposure_finish__gte=timezone.now()).order_by("-id")
        serializer = ArticleSerializer(articles, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        # post에서도 시리얼라이저를 쓸 수 있음 article_serializer 안에 data가 담김
        # user = request.user
        # ArticleSerializer에 user 필드에 들어갈 user의 id 추가해줌
        # request.data['user'] = user.id
        # article_serializer = ArticleSerializer(data=request.data)
        
        # is_valid는 ArticleSerializer의 fields를 기준으로 각 필드들의 유효성을 검증해줌
        # SerializerMethodField로 만든 필드(카테고리)는 기본적으로 read_only라서 검증하지 않음 
        # POST에서 comments는 read_only=True로 지정하고 이 필드는 검증하지 않음
        
        # if article_serializer.is_valid():   # True or False
            # article_serializer.save()
            # return Response(article_serializer.data, status=status.HTTP_200_OK)
        
        # False
        # return Response(article_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
        
        
        
        
        # 시리얼라이저 안쓴 것
        user = request.user
        title = request.data.get('title', "")
        content = request.data.get('content', "")
        category = request.data.pop('category', [])     # **request.data 로 쓸 때 category는 들어가지 않게 pop을 써서 튕겨줌
        # category = request.data.get('category', [])   # 카테고리는 카테고리 id를 리스트로 받음
        # exposure_start = request.data.get('exposure_start')
        # exposure_finish = request.data.get('exposure_finish')
        
        
        if len(title) <= 5:
            return Response({'message': '제목이 5자 이하이기 때문에 게시글을 작성할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if len(content) <= 20:
            return Response({'message': '내용이 20자 이하이기 때문에 게시글을 작성할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if not category:
            return Response({'message': '카테고리가 지정되지 않았기 때문에 게시글을 작성할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        # article = ArticleModel(user=user, title=title, content=content, exposure_start=exposure_start, exposure_finish=exposure_finish)
        article = ArticleModel(user=user, **request.data)
        article.save()
        
        article.category.add(*category)    # 카테고리는 리스트를 풀어서 , , 넣어주면 자동으로 저장됨!
        
        return Response({'message': '게시글이 작성되었습니다.'}, status=status.HTTP_200_OK)