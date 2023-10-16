from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.db.models import Q
from categories.models import Category
from categories.models import Sub_Category
from accounts.models import CustomUser
from store.models import Product

# Create your views here.

def Home(request):
    
    if 'adminemail' in request.session:
        return redirect('admin_home')
    
    return render(request,'index.html')

def ViewShop(request):
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    context={
        'category':categories,
        'product':products,
    }


    return render(request,'shop.html',context)

def ViewSubCategory(request,category_id):
   
    subcategory=Sub_Category.objects.filter(Q(is_activate=True) & Q(category=category_id))
    context={
        'subcategory':subcategory
    }

    return render(request,'subcategory.html',context)



def DisplayProducts(request,sub_category_id):
    
    product=Product.objects.filter(Q(is_activate=True) & Q(sub_category = sub_category_id))
    context={
        'product':product
            
            }                            

    return render(request,'products_display.html',context)       

def ProductDetails(request,product_id):

    product=Product.objects.filter(Q(is_activate=True) & Q(id=product_id))

    context={
        'product':product
    }

    return render(request,'product_details.html',context)