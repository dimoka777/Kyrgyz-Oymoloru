from django.urls import path
from .views import (SignUpView, UserList, UserDetail,
                    UserUpdateView, UserDeleteView, PresentList,
                    gift_user, UserWaitList, change_status, OfficeListView,
                    OfficeUpdateView, OfficeCreateView, OfficeDeleteView,
                    login_success, change_password)
from users.forms import UserLoginForm
from django.contrib.auth import views

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('users_list/', UserList.as_view(), name='users_list'),
    path('waiting_users/', UserWaitList.as_view(), name='waiting_users'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('user/<int:pk>/update', UserUpdateView.as_view(), name='user_update'),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name='user_delete'),
    path('users/present_list/', PresentList.as_view(), name='present_list'),
    path('present_create/<int:pk>/', gift_user, name='present_create'),
    path('changestatus/<int:pk>', change_status, name='change_status'),
    path('office_list/', OfficeListView.as_view(), name='office_list'),
    path('office_create/', OfficeCreateView.as_view(), name='office_create'),
    path('office/<int:pk>/', OfficeUpdateView.as_view(), name='office_update'),
    path('office/<int:pk>/delete/', OfficeDeleteView.as_view(), name='office_delete'),
    path('login_success/', login_success, name='login_success'),
    path('login/', views.LoginView.as_view(template_name="registration/login.html",
                                           authentication_form=UserLoginForm), name='login'),
    path('changepswd/<int:pk>/', change_password, name='change_pswd'),
]
