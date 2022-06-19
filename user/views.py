from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import login, logout, authenticate
from django.db.models import F, Q
from user.models import UserProfile as UserProfileModel
from user.models import User as UserModel
from user.models import Hobby as HobbyModel

from user.serializers import UserSerializer

from django_rest_framework.permissions import RegistedMoreThanAWeekUser

# Create your views here.
class UserView(APIView): # CBV 방식
    # permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능 
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    # permission_classes = [RegistedMoreThanAWeekUser] # permissions.py 에서 정의한 것

    # 사용자 정보 조회
    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
        # 모든 사용자 정보를 가져오고 싶을 때
        # all_users = UserModel.objects.all()
        # return Response(UserSerializer(all_users, many=True).data)

        # user = request.user
        
        # 역참조를 사용했을 때 (one-to-one필드라서 _set 안붙음)
        # hobbys = user.userprofile.hobby.all()     # 쿼리셋
        
        # for hobby in hobbys:
            # exclude : 매칭 된 쿼리만 제외, fillter와 반대
            # annotate : 필드 이름을 변경해주기 위해 사용, 이외에도 원하는 필드를 추가하는 등 다양하게 활용 가능
            # values / values_list : 지정한 필드만 리턴 할 수 있음. values는 dict로 return, values_list는 tuple로 return / flat=True는 튜플을 값으로 변환해줌
            # F() : 객체에 해당되는 쿼리를 생성함
            # hobby_members = hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username', flat=True)
            # hobby_members = list(hobby_members)
            # print(f"hobby : {hobby.name} / hobby members : {hobby_members}")
        
        # print(hobbys.all())
        # print(type(hobbys))
        # print(dir(hobbys))
        
        
        # 역참조를 사용하지 않았을 때
        # user_profile = UserProfile.objects.get(user=user)
        # hobbys = user_profile.hobby.all()
        # return Response({'message': hobbys})
    
    # 회원가입
    def post(self, request):
        return Response({'message': 'post method!!'})

    # 회원 정보 수정
    def put(self, request):
        return Response({'message': 'put method!!'})

    # 회원 탈퇴
    def delete(self, request):
        return Response({'message': 'delete method!!'})
    
    
    
class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)
    
    # 로그아웃
    def delete(self, request):
        logout(request)
        return Response({"message": "로그아웃 성공!!"})
