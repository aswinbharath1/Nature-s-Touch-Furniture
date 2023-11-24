from django.urls import path
from . import views


urlpatterns = [


       path('',views.AdminLogin,name='admin_login'),
       
       path('admin_home/',views.AdminHome,name='admin_home'),
       path('admin_logout',views.AdminLogout,name='admin_logout'),
       
       path('users/',views.Users,name='users'),
       path('block/<int:user_id>/',views.BlockUser,name='block_user'),
       
       path('categories/',views.Categories,name='categories'),
       path('add_categories/',views.AddCategories,name='add_categories'),
       path('edit_categories/<int:category_id>/',views.EditCategories,name='edit_categories'),
       path('delete_categories/<int:category_id>/',views.DeleteCategories,name='delete_categories'),
       path('sub_categories/',views.SubCategories,name='sub_categories'),

       path('add_subcategories/',views.AddSubCategories,name='add_subcategories'),
       path('edit_subcategories/<int:subcategory_id>/',views.EditSubCategories,name='edit_subcategories'),
       path('delete_subcategories/<int:subcategory_id>/',views.DeleteSubCategories,name='delete_subcategories'),

       path('orders',views.Orders,name="orders"),
       path("orders-details/<int:order_id>/",views.OrdersDetails,name="orders_details"),
       path('order-status',views.OrderStatus,name="order_status"),

       
       path('coupon',views.coupon,name='coupon'),
       path('add-coupon',views.add_coupon,name="add_coupon"),
       path('edit-coupon/<int:coupon_id>/',views.edit_coupon,name="edit_coupon"),
       path('block-coupon/<int:coupon_id>/',views.block_coupon,name="block_coupon"),

       path('banner',views.banner,name="banner"),
       path('add-banner',views.add_banner,name="add_banner"),
       path('edit-banner/<int:banner_id>/',views.edit_banner,name="edit_banner"),
       path('remove-banner/<int:banner_id>/',views.remove_banner,name="remove_banner")

]
