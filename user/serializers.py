from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from blog.serializers import ArticleSerializer, CommentSerializer


class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()    # 없는 필드를 만들어서 가져오고 싶을때, 변수를 선언하고 get_변수명 을 쓴 함수를 정의함
    def get_same_hobby_users(self, obj):
        # 20일 강의)) 여기에서도 context가 찍히는지 확인해봄 --> 찍힘!
        # print(self.context)
        # user = self.context["request"].user
        # print(user)
        
        
        # obj : hobby model의 object가 나오고, name이 나오게 model을 만들어서 이름이 찍힘
        # print(type(obj))
        # print(obj)
        
        # dir(obj) 프린트해보면 userprofile_set이 있음! 역참조를 해서 전부 가져오게 함  
        # hobby를 역참조하고 있는 userprofile 의 user의 username을 가져옴
        
        user_list =[]
        for user_profile in obj.userprofile_set.all():
            user_list.append(user_profile.user.username)
        return user_list
        
        
        # list 축약식 쓰면 이렇게 한줄로 가져올 수 있음 / 
        # 20일 강의)) all 대신 본인 이름 빼려면 exclude쓰면 본인 이름만 빠짐!
        # return[userprofile.user.username for userprofile in obj.userprofile_set.exclude(user=user)]
    
    class Meta:
        model = HobbyModel
        fields = ["name", "same_hobby_users"]                    # fields에는 있는 필드만 들어가야 함
        
        # 위의 내용처럼 실행할 필요 없이(SerializerMethodField()사용할 필요 없이) 바로 역참조로 가져 올 수도 있음
        # fields = ["name", "userprofile_set"]
        
       
        
class UserProfileSerializer(serializers.ModelSerializer):
    hobby = HobbySerializer(many=True, read_only=True)                # hobby는 name:null 나오는 이유? many-to-many 관계라서 Queryset 형태 --> many=True 옵션 적어주면 됨!
    get_hobbys = serializers.ListField(required=False)
    class Meta:
        model = UserProfileModel
        fields = ["introduction", "birthday", "age", "hobby","get_hobbys"]



class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()          # userprofile은 one-to-one 관계라서 object 형태
    # class Meta:
        # serializer에 사용될 model, fields지정
        # 모든 필드를 사용하고 싶을 경우 fields = "__all__"로 사용   fields = "__all__"
        # 역참조한 userprofile을 그냥 가져오면 id값이 나옴 / 위에서 UserProfileSerializer()를 변수에 담아 선언해줘야 함
        # model = UserModel
        # fields = ["username", "password", "fullname", "email", "userprofile"] 
        
    # user_detail = UserProfileSerializer(source="userprofile")   # userprofile 대신, user_detail 이라고 이름을 이렇게 바꾸고, souce에 userprofile을 넣으면 됨
    articles = ArticleSerializer(many=True, source="article_set", read_only=True)    # article_set = ArticleSerializer(many=True) 이렇게 해도 됨
    # comments = CommentSerializer(many=True, source="comment_set")
    
    # 20일 강의)) 내가 이 필드를 생성해서 request로 받은거에서 유저의 fullname을 보여줘
    # login_user_fullname = serializers.SerializerMethodField()
    # def get_login_user_fullname(self, obj):
    #     return self.context["request"].user.fullname
    
    # 21일 강의)) custom validator
    # validate 함수 선언 시 serializer에서 자동으로 해당 함수의 validation을 해줌
    def validate(self, data):
        # custom validation pattern
        if not data.get("email", "").endswith("@naver.com"):
            # validation에 통과하지 못할 경우 ValidationError class 호출
            raise serializers.ValidationError(
                    detail={"error": "네이버 이메일만 가입할 수 있습니다."},
                )

        # validation에 문제가 없을 경우 data return
        return data
    
    # POST에서 save하면 create 가 호출 (유저프로필까지 입력할 경우)
    def create(self, validated_data):
        # object를 생성할때 다른 데이터가 입력되는 것을 방지하기 위해 미리 pop 해준다.
        user_profile = validated_data.pop('userprofile')
        get_hobbys = user_profile.pop("get_hobbys", [])
        password = validated_data.pop("password")

        # User object 생성
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        # UserProfile object 생성
        user_profile = UserProfileModel.objects.create(user=user, **user_profile)
        
        # hobby 등록
        user_profile.hobby.add(*get_hobbys)
        user_profile.save()
        
        return user
    
    # PUT에서 save하면 update가 호출
    def update(self, instance, validated_data):
        # instance에는 입력된 object가 담긴다.
        user_profile = validated_data.pop('userprofile')
        get_hobbys = user_profile.pop("get_hobbys", [])
        
        for key, value in validated_data.items():
            # instance.fullname = "user's name"
            # instance.username = "user"
            if key == "password":
                instance.set_password(value)
                continue
            # setattr 안하면 instance.key 로 들어가서 에러남
            setattr(instance, key, value)
        instance.save()
        
        user_profile_object = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_object, key, value)
        user_profile_object.save()
        
        user_profile_object.hobby.set(get_hobbys)   
            
        return instance
    
    
    
    class Meta:
        model = UserModel
        fields = ["username", "password", "fullname", "email", "userprofile", "articles","join_date"]
        
        # 21일 수업)) 각 필드에 해당하는 다양한 옵션 지정
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            # 포스트맨에서 보내면 패스워드가 안보여!!
            'password': {'write_only': True}, # default : False
            'email': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다!! 아예 required 필요없게함
                    'required': False # default : True
                    },
            }
        
        

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




    
    
