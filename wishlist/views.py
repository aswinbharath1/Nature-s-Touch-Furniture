from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from cart.views import AddCart
from store.models import Variation
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from . models import Wishlist
# Create your views here.


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@login_required(login_url='user_login')
def Wishlists(request):
    wishlist = Wishlist.objects.filter(user = request.user)
    context = {
        'wishlist': wishlist,
    }
    return render(request,'userprofile/wishlist.html', context)

@login_required(login_url='user_login')
def AddToWishlist(request,product_id):
    variant = Variation.objects.get(id=product_id)
    user=request.user
    try:
        is_exist = Wishlist.objects.filter(user = user, product_name = variant).exists()
        if is_exist:
            messages.error(request,"This Product is already in your wishlist")
            return redirect('product_details',variant_id=variant.id)
        else :
            wishlist = Wishlist(user = user, product_name = variant)
            wishlist.save()
            messages.success(request, "Product Succesfully Added To Wishlist ")
            return redirect('wishlist_view')
    except Exception as e:
        messages.error(request, 'Failed to add to wishlist ')
        return redirect('wishlist_view')
def RemoveWishlist(request,product_id):
    wishlist = None
    try :
        product = Variation.objects.get(id = product_id)
        wishlist=Wishlist.objects.get(product_name = product , user = request.user)
        wishlist.delete()
    except Wishlist.DoesNotExist:
        pass
    wishlists = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist' : wishlists
    }
    return render(request, 'userprofile/wishlist.html',context)