from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from blog.serializers import ArticleSerializer, CommentSerializer


class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()    # 없는 필드를 만들어서 가져오고 싶을때, 변수를 선언하고 get_변수명 을 쓴 함수를 정의함
    def get_same_hobby_users(self, obj):
        # obj : hobby model의 object가 나오고, name이 나오게 model을 만들어서 이름이 찍힘
        # print(type(obj))
        # print(obj)
        
        # dir(obj) 프린트해보면 userprofile_set이 있음! 역참조를 해서 전부 가져오게 함  
        # hobby를 역참조하고 있는 userprofile 의 user의 username을 가져옴
        
        user_list =[]
        for user_profile in obj.userprofile_set.all():
            user_list.append(user_profile.user.username)
        return user_list
        
        # list 축약식 쓰면 이렇게 한줄로 가져올 수 있음 / all 대신 본인 이름 빼려면 exclude쓰면 됨
        # return [user_profile.user.username for user_profile in obj.userprofile_set.all()]
    
    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]                    # fields에는 있는 필드만 들어가야 함
        
        # 위의 내용처럼 실행할 필요 없이(SerializerMethodField()사용할 필요 없이) 바로 역참조로 가져 올 수도 있음
        # fields = ["name", "userprofile_set"]
        
       
        
class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True)                # hobby는 name:null 나오는 이유? many-to-many 관계라서 Queryset 형태 --> many=True 옵션 적어주면 됨!
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby"]



class UserSerializer(serializers.ModelSerializer):
    # userprofile = UserProfileSerializer()          # userprofile은 one-to-one 관계라서 object 형태
    # class Meta:
        # serializer에 사용될 model, fields지정
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용   fields = "__all__"
        # 역참조한 userprofile을 그냥 가져오면 id값이 나옴 / 위에서 UserProfileSerializer()를 변수에 담아 선언해줘야 함
        # model = UserModel
        # fields = ["username", "password", "fullname", "email", "userprofile"] 
        
    user_detail = UserProfileSerializer(source="userprofile")   # userprofile 대신, user_detail 이라고 이름을 이렇게 바꾸고, souce에 userprofile을 넣으면 됨
    articles = ArticleSerializer(many=True, source="article_set")    # article_set = ArticleSerializer(many=True) 이렇게 해도 됨
    # comments = CommentSerializer(many=True, source="comment_set")
    
    class Meta:
        model = UserModel
        fields = ["username", "password", "fullname", "email", "user_detail", "articles"]
        
        

# 비밀번호 해싱해서 가입하는 방법1
# class UserSignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = "__all__"
        
#     # 패스워드 해싱
#     def create(self, *args, **kwargs):
#         user = super().create(*args, **kwargs)   #super() 상위의...
#         p = user.password     # 패스워드를 꺼내와서
#         user.set_password(p)  # set_password로 패스워드를 해싱해서 넣어줌
#         user.save()
#         return user
    
#     def update(self, *args, **kwargs):
#         user = super().create(*args, **kwargs)   
#         p = user.password
#         user.set_password(p)
#         user.save()
#         return user
    
    
