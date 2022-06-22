from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta       # time 연산 가능하게 함
from django.utils import timezone   # datetimefield 사용시 timezone 써야 함
from rest_framework.exceptions import APIException
from rest_framework import status

class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)

class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        
        # 로그인 하지 않은 사람에게 띄워줄 메시지를 만들기 위해 따로 만듦
        if not user.is_authenticated:
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)
        # admin 사용자 
        if user.is_authenticated and user.is_admin:
            return True
        # 로그인 사용자가 get요청 시 True
        if user.is_authenticated and request.method in self.SAFE_METHODS:
            return True
        # 가입일이 7일 이상 된 사용자의 경우 True
        if user.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=7)):
            return True
        
        return False

# datetimefield 와 비교시( 현재 user의 models.py의  join_date 는 datetimefield로 되어 있음)
# user.join_date < (timezone.now()-timedelta(days=7))

# datefield 와 비교시
# print(f"user join date : {user.join_date}")
# print(f"now date : {datetime.now().date()}")
# user.join_date < (datetime.now().date()-timedelta(days=7))

# class RegistedMoreThanAweekUser(BasePermission):
#     """
#     가입일 기준 7일 이상 지난 사용자만 접근 가능
#     """
#     message = '가입 후 7일 이상 지난 사용자만 게시글을 쓸 수 있습니다.'
    
#     def has_permission(self, request, view):
#         user = request.user
        
#         # if not user or not user.is_authenticated:
#         #     return False
        
#         # Date field :  2002-10-2
#         # DateTime field : 2002-10-2 10:50:21
#         # 가입일이 7일 전보다 더 적어야 7일 이상 된 것이임 -> True
        
#         # print(f"user join date : {user.join_date}")
#         # print(f"now date : {timezone.now()}")
#         # print(f"a week ago date : {timezone.now()-timedelta(days=7)}")
#         # return bool(user.join_date < (timezone.now()-timedelta(days=7)))
        
#         # 두가지 전부 충족되면 True가 나오고, 하나라도 충족되지 않으면 False
#         return bool(request.is_authenticated and request.user.join_date < (timezone.now() - timedelta(days=7)))
    