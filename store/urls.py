from django.urls import path
from . import views

urlpatterns = [
    path('',views.ProductView,name="product_view"),
    path('add-products',views.AddProduct,name="add_product"),
    path('edit-products/<int:product_id>/',views.EditProduct,name="edit_product"),
    path('delete-products/<int:product_id>/',views.DeleteProduct,name="delete_product"),
    path('view-varirants/<int:product_id>/',views.VariantView,name="variant_view"),
    path('add-varirants/<int:product_id>/',views.AddVariant,name="add_variant"),
    path('edit-varirants/<int:variant_id>/',views.EditVariants,name="edit_variants"),

]

