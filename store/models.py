from django.db import models
from django.urls import reverse

from categories.models import Category, Sub_Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_data = models.DateField(auto_now=True)
    is_activate  = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'product'
        verbose_name_plural= 'products'

    # def get_url(self):
    #     return reverse('product_detail', args=[self.category.slug, self.slug])

    
    def __str__(self):
        return self.product_name
    
class Variation(models.Model):
   
 
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    # sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    color = models.CharField(max_length=20)
    stock = models.PositiveIntegerField(default=None)  # Use PositiveIntegerField for stock
    # images = models.ImageField(upload_to='photos/products/',default=None)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2,default=None)  # Use DecimalField for precise pricing
    actual_price = models.DecimalField(max_digits=10, decimal_places=2,blank=True,default=None)
    is_available = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to='photos/products/',default=None)
    image2 = models.ImageField(upload_to='photos/products/',default=None)
    image3 = models.ImageField(upload_to='photos/products/',default=None)
    image4 = models.ImageField(upload_to='photos/products/',default=None)
    class Meta:
        verbose_name = 'variation'
        verbose_name_plural = 'variations'

    def __str__(self):
        return f"{self.product.product_name} - {self.color}"


class VariantImage(models.Model):
    variant = models.ForeignKey(Variation,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products/',default=None)