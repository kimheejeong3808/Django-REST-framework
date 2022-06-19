from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta       # time 연산 가능하게 함
from django.utils import timezone   # datetimefield 사용시 timezone 써야 함

# datetimefield 와 비교시( 현재 user의 models.py의  join_date 는 datetimefield로 되어 있음)
# user.join_date < (timezone.now()-timedelta(days=3))

# datefield 와 비교시
# print(f"user join date : {user.join_date}")
# print(f"now date : {datetime.now().date()}")
# user.join_date < (datetime.now().date()-timedelta(days=3))

class RegistedMoreThanAWeekUser(BasePermission):
    """
    가입일 기준 3일 이상 지난 사용자만 접근 가능
    """
    message = '가입 후 3일 이상 지난 사용자만 게시글을 쓸 수 있습니다.'
    
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        
        # Date field :  2002-10-2
        # DateTime field : 2002-10-2 10:50:21
        # 가입일이 3일 전보다 더 적어야 3일 이상 된 것이임 -> True
        
        # print(f"user join date : {user.join_date}")
        # print(f"now date : {timezone.now()}")
        # print(f"a week ago date : {timezone.now()-timedelta(days=3)}")
        # return bool(user.join_date < (timezone.now()-timedelta(days=3)))
        
        return bool(request.user and request.user.join_date < (timezone.now() - timedelta(days=3)))
    