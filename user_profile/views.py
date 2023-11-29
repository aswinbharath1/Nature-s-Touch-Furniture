from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import Http404, HttpResponse, JsonResponse
from accounts.models import CustomUser
from .models import Address
from django.core.paginator import Paginator, EmptyPage
from accounts.models import CustomUser, UserWallet
from cart.models import Order, OrderItem
from xhtml2pdf import pisa
import os
from io import BytesIO
from django.template.loader import get_template
# Create your views here.

def UserProfile(request):
    if 'useremail' in request.session:
        email = request.session['useremail']
        user = CustomUser.objects.get(email = email)
        user_id = user.id
        address = Address.objects.filter(user_id = user_id)
        context = {
            'users': user,
            'address': address
        }
    else:
        return redirect('user_login')
    return render(request,'userprofile/user_profile.html',context)
def EditUserProfile(request, user_id):
    if request.method ==  'POST':
        user = CustomUser.objects.get(id = user_id)

        if user :
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.phone = request.POST.get('phone')
            user.save()

            return redirect('user_profile')
def AddAddress(request, user_id):
    if request.method == 'POST':
            user = CustomUser.objects.get(pk = user_id)
            user_id = user
            house_no = request.POST.get('house_no')
            recipient_name = request.POST.get('RecipientName')
            street_name =  request.POST.get('street_name')
            village_name = request.POST.get('Village')
            postal_code = request.POST.get('postal_code')
            district = request.POST.get('district')
            state = request.POST.get('state')
            country = request.POST.get('country')
            exists = Address.objects.filter(user_id = user_id).exists()
            if not exists:
                address = Address(
                    user_id= user_id,
                    house_no = house_no,
                    recipient_name = recipient_name,
                    street_name = street_name,
                    village_name = village_name,
                    postal_code = postal_code,
                    district = district,
                    state = state,
                    country = country,
                    is_default = True                 

                 )
            else :
                address = Address(
                    user_id= user_id,
                    house_no = house_no,
                    recipient_name = recipient_name,
                    street_name = street_name,
                    village_name = village_name,
                    postal_code = postal_code,
                    district = district,
                    state = state,
                    country = country,      
                 )
            address.save()
            return redirect('user_profile')
    
def AddressView( request):
    if 'useremail' in request.session:
        email = request.session['useremail']
        user = CustomUser.objects.get(email = email)
        user_id = user.id
        address = Address.objects.filter(user_id = user_id) 
        context = {
            'user' : user,
            'address' : address
        }
    else :
        return redirect( 'user_login')
    return render(request, 'userprofile/address.html' , context)

def EditAddress( request, address_id):
    if request.method=='POST':   
        address=Address.objects.get(id=address_id)
        
        address.house_no = request.POST.get('house_no')
        address.recipient_name = request.POST.get('RecipientName')
        address.street_name = request.POST.get('street_name')
        address.village_name =  request.POST.get('Village')
        address.postal_code =  request.POST.get('postal_code')
        address.district =  request.POST.get('district')
        address.state =  request.POST.get('state')
        address.country =  request.POST.get('country')

        address.save()

        return redirect('user_profile')
    
def DeleteAddress(request,address_id):
    address=Address.objects.get(id=address_id)
    address.delete()
    return redirect('user_profile')


def DefaultAddress(request):
    if request.method =='POST':
        try:
            default_address_check = Address.objects.get(is_default=True)
            
            # If a default address exists, remove the old default address
            default_address_check.is_default = False
            default_address_check.save()
            
        except Address.DoesNotExist:
            # Handle the case where no default address exists
            pass

        address_id = request.POST.get("default_address")  # getting the address selected by the user
        
        try:
            # Attempt to retrieve the selected address
            address = Address.objects.get(id=address_id)
            address.is_default = True
            address.save()
        except Address.DoesNotExist:
            # Handle the case where the selected address doesn't exist
            raise Http404("The selected address does not exist")  # Raise Http404 to indicate a not found error

    return redirect('user_profile')

def MyOrders(request):
    if request.user:
        order_items = None
        user_email = request.session['useremail']
        print(user_email)
        user = CustomUser.objects.get(email=user_email)
        try:
            orders = Order.objects.filter(user=user)
            # Paginate the orders
            paginator = Paginator(orders, 10)  # Set the number of orders per page
            page = request.GET.get('page', 1)

            try:
                orders = paginator.page(page)
            except EmptyPage:
                orders = paginator.page(paginator.num_pages)

            order_items = OrderItem.objects.filter(order__in=orders).order_by('order').distinct('order')
        except:
            orders = None
            order_items = None

        context = {
            "orders": orders,
            "order_items": order_items
        }

        return render(request, "userprofile/my_orders.html", context)
def OrderDetails(request,order_id):
    
    order=Order.objects.get(id=order_id)
    order_items=OrderItem.objects.filter(order=order)
    status=order.status
    context={
        "order_items":order_items,
        "order":order,
        "status":status
    }
    return render(request,"userprofile/order_details.html",context)

def OrderCancellation(request, order_id):
    order = Order.objects.get(id=order_id)
    user = request.user
    user_wallet = UserWallet(user=user, amount=0)  # Set default amount here
    user_wallet.save()

    order.status = 'Cancelled'
    order.save()

    if order.payment_mode == "Paid by Razorpay":
        user.wallet += order.total_price
        user_wallet.amount += order.total_price

    user_wallet.transaction = 'credited'
    user.save()
    user_wallet.save()

    order_items = OrderItem.objects.filter(order=order)
    status = order.status
    context = {
        "order_items": order_items,
        "order": order,
        "status": status
    }
    return render(request, "userprofile/order_details.html", context)


def RenderToPdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def PdfDownload(request,id):
    order=Order.objects.get(id=id)
    neworderitems=OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'cart_items': neworderitems
    }
    pdf = RenderToPdf('userprofile/order_invoice.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % (context['order'])
        content = "inline; filename='%s'" % (filename)
        content = "attachment; filename=%s" % (filename)
        response['Content-Disposition'] = content
        return response
    
def OrderReturn(request,order_id):

    order=Order.objects.get(id=order_id)
    order.status='Return requested'
    order.save()

    order_items=OrderItem.objects.filter(order=order)
    status=order.status
    context={
        "order_items":order_items,
        "order":order,
        "status":status
    }
    return render(request,"userprofile/order_details.html",context)

def UserWallets(request):

    wallets=UserWallet.objects.filter(user=request.user)
    if request.user:
        user =  request.user
        balance = user.wallet
    context={
        'wallets':wallets,
        'balance': balance,
    }

    return render(request,'userprofile/wallet.html',context)