from django.db import models
from accounts.models import CustomUser
from user_profile.models import Address
from store.models import *

from store.models import Product, Variation

# Create your models here.
# class Cart(models.Model):
#     user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,null=True,blank=True) 
#     cart_id=models.CharField(max_length=250,blank=True)
#     date_added=models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
         
#         return self.cart_id
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    def calculate_total_price(self):
        # Calculate the total price of items in the cart
        total_price = sum(item.sub_total() for item in self.cartitem_set.filter(is_active=True))
        return total_price

    
class CartItem(models.Model):
    product = models.ForeignKey(Variation, on_delete = models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    is_active =models.BooleanField(default = True)
    
    def sub_total(self):

        return self.product.selling_price * self.quantity

    def __str__(self):

        return self.product.product_name

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=250, null=True)
    message = models.TextField(null=True)
    coupon_applied = models.ForeignKey(Coupon, blank= True, null=True , default= True , on_delete=models.CASCADE)
    tracking_no = models.CharField(max_length=150, null=True)
    # Define orderstatuses as a tuple of tuples for status tracking
    orderstatuses = (
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Return requested', 'Return requested'),
        ('Return processing', 'Return processing'),
        ('Returned', 'Returned'),
    )
    status = models.CharField(max_length=150, choices=orderstatuses, default='Order confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.tracking_no)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant=models.ForeignKey(Variation, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)
    STATUS = (
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Return requested', 'Return requested'),
        ('Return processing', 'Return processing'),
        ('Returned', 'Returned'),
    )
    status = models.CharField(max_length=150, choices=STATUS, default='Order Confirmed')

    def str(self):
        return f"{self.order.id, self.order.tracking_no}"