from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# custom user model 사용 시 UserManager 클래스와 그 안에 create_user, create_superuser  두 함수가 정의되어 있어야 함
class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# custom user model 커스텀 유저모델 먼저 써보자!
class User(AbstractBaseUser):
    username = models.CharField("사용자 계정", max_length=50, unique=True)    # 중복되면 안되니까 유니크 True
    password = models.CharField("비밀번호", max_length=128)
    email = models.EmailField("이메일 주소", max_length=100)
    fullname = models.CharField("이름", max_length=20)
    join_date = models.DateTimeField("가입일", auto_now_add=True)

	# is_active가 False일 경우 사용자 계정이 비활성화됨
    is_active = models.BooleanField(default=True) 

    # is_staff에서 해당 값 사용
    is_admin = models.BooleanField(default=False)
    
    # id로 사용 할 필드 지정. 유저네임 필드로 사용할 걸 필수적으로 지정해야 함! 이메일필드를 써도 됨!
    # 로그인 시 USERNAME_FIELD에 설정 된 필드와 password가 사용된다.
    USERNAME_FIELD = 'username'

    # user를 생성할 때 입력받은 필드 지정 / 예를들어 createsuperuser 같은걸 입력받을 때 사용자계정, 비번 이외에 입력받을거 지정 /
    # 사용하지 않더라도 이렇게 선언은 되어 있어야 함!!! 
    REQUIRED_FIELDS = []
    
    objects = UserManager() # custom user 생성 시 필요
    
    def __str__(self):
        return f"{self.username} / {self.email} / {self.fullname}"


    # 로그인 사용자의 특정 테이블의 crud 권한을 설정, perm table의 crud 권한이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False / 이거 그대로 씀!
    def has_perm(self, perm, obj=None):
        return True

    
    # 로그인 사용자의 특정 app에 접근 가능 여부를 설정, app_label에는 app 이름이 들어간다.
    # admin일 경우 항상 True, 비활성 사용자(is_active=False)의 경우 항상 False / 이거 그대로 씀!
    def has_module_perms(self, app_label): 
        return True
    
    
    # admin 권한 설정
    @property
    def is_staff(self): 
        return self.is_admin



# 취미 : 운동
class Hobby(models.Model):
    name = models.CharField("취미 이름", max_length=20)
    def __str__(self):
        return self.name
    
# 역참조하는 필드에 related name을 설정하지 않았을 경우 : 기본적으로 테이블 뒤에 _set이 붙음 
# (user가 userprofile을 바라보듯 one-to-one 필드는 예외로 _set이 붙지 않음)



# user profile model
class UserProfile(models.Model):
    user = models.OneToOneField(to=User, verbose_name="사용자", on_delete=models.CASCADE, primary_key=True)
    introduction = models.TextField("자기소개", null=True, blank=True)
    birthday = models.DateField("생일")
    age = models.IntegerField("나이")
    hobby = models.ManyToManyField(Hobby, verbose_name="취미")
    
    def __str__(self):
        return f"{self.user.username}님의 프로필입니다"


