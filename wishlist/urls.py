from django.urls import path
from . import views

urlpatterns = [
    path('',views.Wishlists,name='wishlist_view'),
    path('add_wishlist/<int:product_id>',views.AddToWishlist,name='add_wishlist'),
    path('remove_wishlist/<int:product_id>',views.RemoveWishlist,name='remove_wishlist'),
    
]