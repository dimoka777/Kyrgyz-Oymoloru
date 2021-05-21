from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, OfficeRegion, Present


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'address', 'check_number', 'check_image',
                       'passport_number', 'office_location', 'phone_number',
                       'by_whom', 'status', 'followers', 'level', 'is_staff',)
        }),
    )
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'is_staff', 'status', 'by_whom']


admin.site.register(Present)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OfficeRegion)
