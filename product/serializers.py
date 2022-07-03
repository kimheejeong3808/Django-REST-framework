from datetime import datetime
from rest_framework import serializers
from product.models import Product as ProductModel
from product.models import Review as ReviewModel
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    # 이걸 안쓰면 user의 id값만 나오니까 메소드필드 추가함
    user = serializers.SerializerMethodField()
    # 이걸 정의하면 바로 user=fullname값이 나옴
    def get_user(self, obj):
        return obj.user.fullname
    
    class Meta:
        model = ReviewModel
        fields = ["user", "product", "content", "created", "rating"]


class ProductSerializer(serializers.ModelSerializer):
    # 상품정보를 리턴할때 리뷰를 같이 보여주는데 그때 리뷰의 형식을 여기서 지정
    review = serializers.SerializerMethodField()
    def get_review(self, obj):
        # product에서 역참조로 review 내용을 다 가져온 것
        reviews = obj.review_set
        return {
            "last_review":ReviewSerializer(reviews.last()).data,
            "average_rating":reviews.aggregate(Avg("rating"))
        }
    # 기존 is_valid() function 에 추가하여 커스텀할 수 있는 validate
    def validate(self, data):
        exposure_end_date = data.get("exposure_end_date", "")
        if exposure_end_date and exposure_end_date < datetime.now().date():
            raise serializers.ValidationError(
                detail = {"error": "유효하지 않은 노출 종료 날짜입니다."},
            )
        return data
    
    def create(self, validated_data):
        product = ProductModel(**validated_data)
        product.save()
        # 2번 저장하는 이유는 위에서 저장을 해야 밑에서 created라는 기능을 쓸 수 있기 때문
        product.content += f"\n\n{product.created.replace(microsecond=0, tzinfo=None)}에 등록된 상품입니다."
        product.save()
        return product
        
    def update(self, instance, validated_data):
        # 위의 과정처럼 해줘도 됨
        # for key, value in validated_data.items():
            # if key == "content":
            #     value += f"\n\n{instance.created.replace(microsecond=0, tzinfo=None)}에 등록된 상품입니다."
            # setattr(instance, key, value)
            # instance.save()
            # instance.content = f"{instance.modified.replace(microsecond=0, tzinfo=None)}에 수정되었습니다.\n\n"\
            #                     + instance.content
            # instance.save()
        for key, value in validated_data.items():
            if key == "content":
                created = getattr(instance, key).split("\n")[-1]
                # validated_data의 value에 가져온 한 줄을 추가
                value += f"\n\n{created}"
            setattr(instance, key, value)
        instance.content = f"{instance.modified.replace(microsecond=0, tzinfo=None)}에 수정되었습니다.\n\n"\
                                + instance.content
        instance.save()
        return instance
                                
    # SlugRelatedField 사용 -> user id값이 아닌 username을 가져올 수 있음
    # user = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='username'
    #     )            
            

    class Meta:
        model = ProductModel
        fields = ["user", "title", "thumbnail", "content", "created", 
                  "modified", "exposure_end_date", "is_active", "price", "review"]
    
    
    
    
    
    
    # # 21일 강의)) custom validator
    # # validate 함수 선언 시 serializer에서 자동으로 해당 함수의 validation을 해줌
    # def validate(self, data):
    #     # custom validation pattern
    #     if not data.get("email", "").endswith("@naver.com"):
    #         # validation에 통과하지 못할 경우 ValidationError class 호출
    #         raise serializers.ValidationError(
    #                 detail={"error": "네이버 이메일만 가입할 수 있습니다."},
    #             )

    #     # validation에 문제가 없을 경우 data return
    #     return data
    
    # # POST에서 save하면 create 가 호출 (유저프로필까지 입력할 경우)
    # def create(self, validated_data):
    #     # object를 생성할때 다른 데이터가 입력되는 것을 방지하기 위해 미리 pop 해준다.
    #     user_profile = validated_data.pop('userprofile')
    #     get_hobbys = user_profile.pop("get_hobbys", [])
    #     password = validated_data.pop("password")

    #     # User object 생성
    #     user = UserModel(**validated_data)
    #     user.set_password(password)
    #     user.save()

    #     # UserProfile object 생성
    #     user_profile = UserProfileModel.objects.create(user=user, **user_profile)
        
    #     # hobby 등록
    #     user_profile.hobby.add(*get_hobbys)
    #     user_profile.save()
        
    #     return user
    
    # # PUT에서 save하면 update가 호출
    # def update(self, instance, validated_data):
    #     # instance에는 입력된 object가 담긴다.
    #     user_profile = validated_data.pop('userprofile')
    #     get_hobbys = user_profile.pop("get_hobbys", [])
        
    #     for key, value in validated_data.items():
    #         # instance.fullname = "user's name"
    #         # instance.username = "user"
    #         if key == "password":
    #             instance.set_password(value)
    #             continue
    #         # setattr 안하면 instance.key 로 들어가서 에러남
    #         setattr(instance, key, value)
    #     instance.save()
        
    #     user_profile_object = instance.userprofile
    #     for key, value in user_profile.items():
    #         setattr(user_profile_object, key, value)
    #     user_profile_object.save()
        
    #     user_profile_object.hobby.set(get_hobbys)   
            
    #     return instance
    
    
    
    # class Meta:
    #     model = UserModel
    #     fields = ["username", "password", "fullname", "email", "userprofile", "articles","join_date"]
        
    #     # 21일 수업)) 각 필드에 해당하는 다양한 옵션 지정
    #     extra_kwargs = {
    #         # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
    #         # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
    #         # 포스트맨에서 보내면 패스워드가 안보여!!
    #         'password': {'write_only': True}, # default : False
    #         'email': {
    #             # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
    #             'error_messages': {
    #                 # required : 값이 입력되지 않았을 때 보여지는 메세지
    #                 'required': '이메일을 입력해주세요.',
    #                 # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
    #                 'invalid': '알맞은 형식의 이메일을 입력해주세요.'
    #                 },
    #                 # required : validator에서 해당 값의 필요 여부를 판단한다!! 아예 required 필요없게함
    #                 'required': False # default : True
    #                 },
    #         }

    
    
