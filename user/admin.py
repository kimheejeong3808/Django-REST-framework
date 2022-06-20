from django.contrib import admin
from .models import Hobby, User, UserProfile

# 장고의 유저어드민 상속받아 사용(패스워드 해싱ok)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# TabularInline(가로정렬) 도 있음
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
    # many-to-many 관계의 필드를 좀더 예쁘게 관리
    filter_horizontal = ['hobby']


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'username', 'fullname', 'email')
    list_display_links = ('username', )
    list_filter = ('username', )
    search_fields = ('username', 'email', )
    
    fieldsets = (('info', {'fields': ('username', 'password', 'email', 'fullname', 'join_date', )}),
                 ('permissions', {'fields': ('is_admin', 'is_active', )}),)
    
    filter_horizontal = []
    
    # 읽기, 쓰기 권한 지정 가능
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('username', 'join_date', )
        else:
            return('join_date', )
    
    # 유저 프로필을 인라인으로 지정했기 때문에 이렇게 선언해야 들어감
    # (유저가 유저프로필을 역참조하고 있음 / 역참조 관계에서만 가능) 
    inlines = (
            UserProfileInline,
        )


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Hobby)