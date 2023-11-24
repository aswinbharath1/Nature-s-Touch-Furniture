from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.db.models import Q
from categories.models import Category
from categories.models import Sub_Category
from accounts.models import CustomUser
from store.models import Product, Variation
from dashboard.models import Banner

# Create your views here.

def Home(request):
    
    if 'adminemail' in request.session:
        return redirect('admin_home')
    banners=Banner.objects.all()
    context={
        'banners':banners,
    }
    
    return render(request,'index.html',context)

def ViewShop(request):
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    variants = Variation.objects.order_by('product').distinct('product')
    
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()
    context={
        'category':categories,
        'product':products,
        'variants':variants,
        "color":available_colors,
    }



    return render(request,'shop.html',context)

def ViewSubcategory(request,category_id):
    variants={}
    subcategory=Sub_Category.objects.filter(Q(is_activate=True) & Q(category=category_id))
    # Assuming you already have 'subcategory' containing the filtered subcategories
    variants = Variation.objects.filter(product__sub_category__in=subcategory)


    context={
        'subcategory':subcategory,
        'base_variant':variants
    }

    return render(request,'subcategory.html',context)

def DisplayProducts(request,sub_category_id):
    
    product = Product.objects.filter(Q(is_activate=True) & Q(sub_category = sub_category_id))
    # subcategory=Sub_Category.objects.filter(Q(is_activate=True) & Q(category=category_id))
    variants = Variation.objects.filter(product__sub_category__in=subcategory)    
    

    context={
        'variants':variants
            
            }                            

    return render(request,'products_display.html',context)

def ProductDetails(request,variant_id):

    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    available_variants =Variation.objects.filter(product=product_id)

    
    context={
        # 'product':product,
        'variant': variants,
        'available_variants':available_variants
    }

    return render(request,'product_details.html',context)

def VariantSelect(request,variant_id):

    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    available_variants =Variation.objects.filter(product=product_id)
    
    variant_price = variants.selling_price
    variant_stock = variants.stock
    variant_image1 = variants.image1.url
    variant_image2 = variants.image2.url
    variant_image3 = variants.image3.url
    variant_image4 = variants.image4.url

        # 'available_vatiants':available_variants
    

    return JsonResponse({'variant':variant_price,
                         'variant_stock':variant_stock,
                         'variant_image1':variant_image1,
                         'variant_image2':variant_image2,
                         'variant_image3':variant_image3,
                         'variant_image4':variant_image4
                         })


def ProductSearch(request):

    query=request.GET.get('q')
    modified_string = query.replace(" ", "")
    variants=None
    
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()
    if modified_string == "":
        
        return redirect('shop_page')
    
    else:

        product=Product.objects.filter(product_name__icontains=query)
        for product in product:
            

            variants=Variation.objects.filter(product=product)
        print(variants)
        context={
        'category':categories,
        'product':products,
        'variants':variants,
        "color":available_colors,
    }
        return render(request,'shop.html',context)
