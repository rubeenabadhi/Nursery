from django.urls import path
from .import views


urlpatterns =[
    path('register',views.register,name="register"),
    path('user_login', views.user_login, name='user_login'),
    path('logout', views.logout, name='logout'),
    path('nursery_signup', views.nursery_signup, name="nursery_signup"),
    path('nursery_login',views.nursery_login,name='nursery_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('useredit_profile',views.useredit_profile,name='edit_profile'),
    path('nersery_profile/<int:admin_id>/', views.nersery_profile, name='nersery_profile'),
    path('nursery_editprofile/<int:admin_id>/', views.nursery_editprofile, name='nursery_editprofile'),
    path('forgotPassword',views.forgotPassword, name='forgotPassword'),
    path('delete_account', views.delete_account, name='delete_account'),

]