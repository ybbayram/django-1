from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

# CustomUser modelini admin panele ekle
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'name', 'is_active', 'is_staff')  # Görünen sütunlar
    search_fields = ('email', 'name')  # Arama yapılacak alanlar
    list_filter = ('is_active', 'is_staff')  # Filtre alanı
    ordering = ('-id',)  # Varsayılan sıralama
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
