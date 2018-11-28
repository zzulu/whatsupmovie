from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('profile/', views.ProfileDetail.as_view(), name='profile_detail'),
    path('profile/edit/', views.ProfileUpdate.as_view(), name='profile_update'),
]
