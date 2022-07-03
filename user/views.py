from functools import partial
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

from user.serializers import UserSerializer,UserSignupSerializer


# Create your views here.
class UserView(APIView): # CBV 방식
    # permission_classes = [permissions.AllowAny] # 누구나 view 조회 가능 
    # permission_classes = [permissions.IsAdminUser] # admin만 view 조회 가능
    permission_classes = [permissions.IsAuthenticated] # 로그인 된 사용자만 view 조회 가능
    # permission_classes = [RegistedMoreThanAweekUser] # permissions.py 에서 정의한 것

    # 사용자 정보 조회
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

        # 20일 강의)) request.user를 넘겨주는데 context를 추가해 내가 원하는 정보를 같이 넘겨줌
        # user_serializer = UserSerializer(request.user, context={"request":request}).data
        # return Response(user_serializer, status=status.HTTP_200_OK)

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
        # 비밀번호 해싱해서 가입하는 방법1
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '가입 완료!!!!'})
        else:
            print(serializer.errors)
            return Response({'message': '가입 실패!!!!'})
        
        # 21일 강의)) serializer 각 필드의 옵션을 POST에도 적용해보기
        # user_serializer = UserSerializer(data=request.data)
        # if user_serializer.is_valid():
        #     user_serializer.save()
        #     return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        # # False
        # return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    # 회원 정보 수정 (urls.py에도 <obj_id>추가 포스트맨 테스트용으로 id 2번 어드민)
    def put(self, request, obj_id):
        user = UserModel.objects.get(id=obj_id)
        # 실제로 회원정보 수정기능 만들때 본인 것만 수정하도록 해야함
        # user=request.user
        
        # 시리얼라이저에 넣기 전에 pop을 사용하여 변경되지 않을 필드 지정해줌(유저네임에 어떤걸 넣어도 안바뀜)
        request.data.pop("username", "")
        # user를 써서 어떤걸 수정할지 지정해줌 나머지는 post와 같음 / 필드에 있는 데이터가 일부만 들어가도 되는 partial
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 회원 탈퇴
    def delete(self, request):
        return Response({'message': 'delete method!!'})
    
    
# JWT 방식으로 로그인하기 때문에 UserAPIView 필요 없음    
# class UserAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
#     # 로그인
#     def post(self, request):
#         username = request.data.get('username', '')
#         password = request.data.get('password', '')

#         user = authenticate(request, username=username, password=password)
#         if not user:
#             return Response({"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

#         login(request, user)
#         return Response({"message": "로그인 성공!!"}, status=status.HTTP_200_OK)
    
#     # 로그아웃
#     def delete(self, request):
#         logout(request)
#         return Response({"message": "로그아웃 성공!!"})
