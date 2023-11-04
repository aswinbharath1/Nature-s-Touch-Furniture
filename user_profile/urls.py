from django.urls import path
from . import views



urlpatterns = [
    
    path('',views.UserProfile,name="user_profile"),
    path('edit-profile/<int:user_id>/',views.EditUserProfile,name="edit_user_profile"),
    path('address-view',views.AddressView,name='view_address'),
    path('user-address/<int:user_id>/',views.AddAddress,name="add_address"),
    path('user-edit-address/<int:address_id>/',views.EditAddress,name="edit_address"),
    path('user-delete-address<int:address_id>',views.DeleteAddress,name="delete_address"),
    path('default-address',views.DefaultAddress,name="default_address"),

]   