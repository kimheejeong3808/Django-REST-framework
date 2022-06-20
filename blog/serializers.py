from rest_framework import serializers
from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel


class CommentSerializer(serializers.ModelSerializer):
    comment_user = serializers.SerializerMethodField()
    
    def get_comment_user(self, obj):
        return obj.comment_user.username
    class Meta:
        model = CommentModel
        fields = ["comment_user", "comment_content"]



class ArticleSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, source="comment_set")
    
    def get_category(self, obj):
        return [category.name for category in obj.category.all()]
    class Meta:
        model = ArticleModel
        fields = ["title", "content", "comments", "category"]