from django.contrib import admin
from django.urls import path, include
from user import views
# path 순서도 중요! 로그인 할때 login으로 갈수도있고 obj_id로 갈수도 있으니까 login이 위에 있어야 함
urlpatterns = [
    path('',views.UserView.as_view()),
    path('login/',views.UserAPIView.as_view()),
    path('logout/', views.UserAPIView.as_view()),
    path('<obj_id>/', views.UserView.as_view()),
]
