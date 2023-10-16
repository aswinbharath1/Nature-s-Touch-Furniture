from django.urls import path
from . import views


urlpatterns = [


       path('',views.AdminLogin,name='admin_login'),
       path('admin_home/',views.AdminHome,name='admin_home'),
       path('admin_logout',views.AdminLogout,name='admin_logout'),
       path('users/',views.Users,name='users'),
       

]
