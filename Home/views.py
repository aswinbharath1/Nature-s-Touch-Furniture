from django.shortcuts import render,redirect
from django.views.decorators.cache import never_cache
from django.db.models import Q
from categories.models import Category
from categories.models import Sub_Category
from accounts.models import CustomUser
from store.models import Product, Variation
from dashboard.models import Banner
from django.http import HttpResponse, JsonResponse

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
    variants = Variation.objects.filter(is_available=True).order_by('product').distinct('product')


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
    variants = Variation.objects.filter(product__sub_category__in=subcategory,is_available=True)


    context={
        'subcategory':subcategory,
        'base_variant':variants
    }

    return render(request,'subcategory.html',context)

def DisplayProducts(request,sub_category_id):
    
    subcategory = Sub_Category.objects.get(id=sub_category_id)
    variants = Variation.objects.filter(product__sub_category=subcategory,is_available=True)
    context={
        'variants':variants
    }                            

    return render(request,'product_display.html',context)

def ProductDetails(request,variant_id):

    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    available_variants =Variation.objects.filter(product=product_id,is_available=True)

    for i in available_variants:

        print(i.color)
    context={
        # 'product':product,
        'variant': variants,
        'available_variants':available_variants
    }

    return render(request,'product_details.html',context)

def VariantSelect(request,variant_id):
    variants = Variation.objects.get(pk=variant_id)
    product_id = variants.product

    available_variants =Variation.objects.filter(product=product_id,is_available=True)

    for i in available_variants:

        print(i.color)
    context={
        # 'product':product,
        'variant': variants,
        'available_variants':available_variants
    }

    return render(request,'product_details.html',context)

    # variants = Variation.objects.get(pk=variant_id)
    # product_id = variants.product
    

    # return render(request,'product_details.html',variant_id)
    # return render(request, 'product_details.html', {'variant_id': variant_id})



def ProductSearch(request):

    query = request.GET.get('search')
    color_filter = request.GET.get('color')
    print(color_filter)
    sort = request.GET.get('sort')
    print(sort)

    categories = Category.objects.filter(is_activate=True)
    products = Product.objects.filter(is_activate=True)
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()
    variants = Variation.objects.filter(is_available=True)

    if query:
        variants = variants.filter(product__product_name__icontains=query)

    if color_filter:
        variants = variants.filter(color=color_filter)

    if sort == '1':
        variants = variants.order_by('-selling_price')
    else:
        variants = variants.order_by('selling_price')

    context = {
        'category': categories,
        'product': products,
        'variants': variants,
        'color': available_colors,
    }

    return render(request, 'shop.html', context)


def ProductSort(request):
    sort=request.GET.get('sort')
    categories=Category.objects.filter(is_activate=True)
    products=Product.objects.filter(is_activate=True)
    available_colors = Variation.objects.filter(is_available=True).values('color').distinct()

    if sort== '1':
        variants=Variation.objects.filter(is_available=True).order_by('-selling_price')

    else:
         variants=Variation.objects.filter(is_available=True).order_by('selling_price')

    context={
        'category':categories,
        'product':products,
        'variants':variants,
        "color":available_colors,
    }

    return render(request,'shop.html',context)