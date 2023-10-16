from django.db import models
from django.urls import reverse

from categories.models import Category, Sub_Category

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    description  = models.TextField(max_length=500, blank=True)
    price        = models.IntegerField()
    images       = models.ImageField(upload_to='photos/products/')
    image1       = models.ImageField(upload_to='photos/products/')
    image2       = models.ImageField(upload_to='photos/products/')
    image3       = models.ImageField(upload_to='photos/products/')
    stock        = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    modified_data= models.DateField(auto_now=True)
    is_activate  = models.BooleanField(default=True)


   

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    
    def __str__(self):
        return self.product_name