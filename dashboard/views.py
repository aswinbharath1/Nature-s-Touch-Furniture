
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from store.models import *
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.models import CustomUser, UserWallet
from django.contrib import messages
from categories.models import Category,Sub_Category
from cart.models import Order,OrderItem
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from django.template.loader import get_template
from xhtml2pdf import pisa
from dashboard.models import Banner
from store.models import Coupon

# Create your views here.
def AdminLogin(request):
    if 'adminmail' in request.session :
        return redirect ('admin_home')
    
    if request.method =="POST":
        email = request.POST.get('email')
        password= request.POST.get('password')

        user= authenticate(request, email= email , password= password )
        if user is not None and user.is_superuser:
            login(request,user)
            request.session['adminmail']= email
            return redirect('admin_home')
        else:
            messages.error(request,"Invalid credentials try again !!")


    return render(request,"dashboard/adminlogin.html")

def AdminHome(request):
    Delevered  = Order.objects.filter(status = 'Delevered').count()
    Users_active= CustomUser.objects.filter(is_active=True).count()
    Users_block= CustomUser.objects.filter(is_active=False).count()
    orders=Orders.objects.filter(status='Order confirmed')
    revenue = 0
    
    print(Delevered)
    context ={
        'Delevered':Delevered,
        'Users_active': Users_active,
        'Users_block':Users_block,
        
    }

    return render(request, 'dashboard/adminhome.html', context)

def AdminLogout(request):
    if 'adminemail' in request.session:

        logout(request)
        return redirect('admin_login')
    else:
        return redirect('admin_login')
    
#view function for going to user page 
def Users(request):
    user = CustomUser.objects.filter(is_superuser= False).order_by('id')

    context= {
        'users': user
    }
    return render (request, 'dashboard/users.html',context)

#view function for blocking and unblocking the users
def BlockUser(request, user_id):
    user=CustomUser.objects.get(pk=user_id)
    
    if user.is_active:
        user.is_active=False
        user.save()
        
        if request.user.is_authenticated and request.user.id == user.id:
            logout(request)


        users=CustomUser.objects.filter(is_superuser= False).order_by('id')

        context={
         
            'users':users
        
        }

        return render(request,'dashboard/users.html',context)
    
    else:
        user.is_active=True
        user.save()
        users= CustomUser.objects.filter(is_superuser=False).order_by('id')
        context = {
            'users' : users
        }
        return render(request,'dashboard/users.html',context)

def Categories(request):

    category = Category.objects.all().order_by('id')
    context={
        'categories' : category 
    }

    return render(request,'dashboard/category.html',context)


def AddCategories(request):

    if request.method == 'POST':
        category_name = request.POST.get('categoryName')
        category_desc = request.POST.get('categoryDescription')
        category_image = request.FILES.get('category_img')

        if Category.objects.filter(category_name = category_name).exists():
            messages.error(request, "Cannot Add An Existing Category !!")
            return redirect('categories')
        else:
            category = Category(category_name= category_name, description = category_desc , category_image= category_image)
            category.save()
            return redirect('categories')
def EditCategories(request,category_id):
    category = Category.objects.get(id=category_id)
    category_image=category.category_image
    if request.method=="POST":
        category_name= request.POST.get('categoryName')
        
        category.description    = request.POST.get('categoryDescription')
        category_img = request.FILES.get('category_img')

        if category_img is None:
            category.category_image = category_image
    
        else:
            category.category_image = category_img

        if Category.objects.filter(category_name=category_name).exclude(id=category_id).exists():
            messages.error(request,"Entered Category is already taken!!")
            return redirect('categories')
            
        else:
             category.category_name  = category_name
             category.save()
             return redirect('categories')
        
def DeleteCategories(request,category_id):
    category=Category.objects.get(pk=category_id)

    if category.is_activate:
        category.is_activate=False
        category.save()
        try:
            sub=Sub_Category.objects.filter(category=category)
            for item in sub:
                item.is_activate=False
                item.save()
                try:
                    products=Product.objects.filter(sub_category=item)
                    for product in products:
                        product.is_activate=False
                        print('hihterehhtereerereerererere')
                        try:
                            variant=Variation.objects.filter(product=product)
                            for variant in variant:
                                variant.is_available=False
                        except:
                            pass
                except:
                    pass
        except:
            pass
       
    
        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }
        return render(request,'dashboard/categories.html',context)
    else:
        category.is_activate=True
        category.save()
        # categories=Category.objects.all
        try:
            sub=Sub_Category.objects.filter(category=category)
            for item in sub:
                item.is_activate=True
                item.save()
                try:
                    products=Product.objects.filter(sub_category=item)
                    for product in products:
                        product.is_activate=True
                        try:
                            variant=Variation.objects.filter(product=product)
                            for variant in variant:
                                variant.is_available=True
                        except:
                            pass
                except:
                    pass
        except:
            pass

        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }
        return render(request,'dashboard/categories.html',context)
    

# View for displaying subcategories
def SubCategories(request):
    # Fetch active categories from the database
    category = Category.objects.filter(is_activate=True)
    # Fetch all subcategories and order them by their ID
    subcategory = Sub_Category.objects.all().order_by('id')
    context = {
        'subcategories': subcategory,
        'categories': category
    }
    return render(request, 'dashboard/subcategories.html', context)

# View for adding subcategories
def AddSubCategories(request):
    if request.method == "POST":
        # Get the selected category's ID from the form
        category_id = request.POST.get('category_name')
        # Retrieve the selected category instance
        category_instance = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get('categoryName')
        description = request.POST.get('categoryDescription')
        cat_image = request.FILES.get('cat_img')
        cat = Sub_Category(
            category=category_instance,
            sub_category_name=sub_category_name,
            sub_category_description=description,
            sub_Category_image=cat_image
        )
        cat.save()
        return redirect('sub_categories')

# View for editing subcategories
def EditSubCategories(request, subcategory_id):
    subcategory = Sub_Category.objects.get(pk=subcategory_id)
    # Fetch the image from the database for when the user hasn't edited the image field
    sub_category_image = subcategory.sub_Category_image

    if request.method == "POST":
        # Get the selected category's ID from the form
        category_id = request.POST.get('category_name')
        # Update the category field of the subcategory using the selected category ID
        subcategory.category = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get('categoryName')
        subcategory.sub_category_name = sub_category_name
        subcategory.sub_category_description = request.POST.get('categoryDescription')

        sub_Category_img = request.FILES.get('cat_img')
        # Check if the subcategory image is None
        if sub_Category_img is None:
            subcategory.sub_Category_image = sub_category_image
        else:
            subcategory.sub_Category_image = sub_Category_img

        # Check if the new subcategory name is already taken
        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exclude(id=subcategory_id).exists():
            messages.error(request, "Entered Sub Category is already taken!!")
            return redirect('sub_categories')
        else:
            subcategory.save()
            return redirect('sub_categories')

# View for activating or deactivating subcategories
def DeleteSubCategories(request, subcategory_id):
    category=Sub_Category.objects.get(pk=subcategory_id)

    if category.is_activate:
        category.is_activate=False
        category.save()

       
        
        category=Category.objects.filter(is_activate=True).order_by('id')
        subcategory=Sub_Category.objects.all().order_by('id')
        context={
            'subcategories':subcategory,
            'categories':category
        }

        return render(request,'dashboard/subcategories.html',context)
    else:
        category.is_activate=True
        category.save()
        

        category=Category.objects.filter(is_activate=True).order_by('id')
        subcategory=Sub_Category.objects.all().order_by('id')
        context={
            'subcategories':subcategory,
            'categories':category
         }
    return render(request,'dashboard/subcategories.html',context)

def coupon(request):
    
    coupon=Coupon.objects.all().order_by('id')

    context={
        'coupon':coupon,
    }
    return render(request,'dashboard/coupon.html',context)

def add_coupon(request):
    
    if request.method=='POST':
        coupon_name=request.POST.get('couponName')
        coupon_code=request.POST.get('couponCode')
        discountAmount=request.POST.get('discountAmount')
        validFrom=request.POST.get('validFrom')
        validTo=request.POST.get('validTo')
        minimumAmount=request.POST.get('minimumAmount')

        if Coupon.objects.filter(coupon_name=coupon_name).exists():
            messages.error(request,"Entered Coupon is already exists!!")
            return redirect('coupon')
        elif Coupon.objects.filter(code=coupon_code).exists():
            messages.error(request,"Entered Coupon code is already exists!!")
            return redirect('coupon')
            
        else:
            coupon=Coupon(coupon_name=coupon_name,code=coupon_code,discount=discountAmount, valid_from = validFrom, valid_to = validTo, minimum_amount = minimumAmount)
            coupon.save()

            return redirect('coupon')
        
def edit_coupon(request,coupon_id):

    if request.method=='POST':
        coupon=Coupon.objects.get(id=coupon_id)

        coupon_name = request.POST.get('couponName')
        coupon.coupon_name = coupon_name

        coupon_code = request.POST.get('couponCode')
        coupon.coupon_code = request.POST.get('couponCode')

        coupon.discount = request.POST.get('discountAmount')
        coupon.valid_from = request.POST.get('validFrom')
        coupon.valid_to = request.POST.get('validTo')
        coupon.minimum_amount = request.POST.get('minimumAmount')

        

        if Coupon.objects.filter(coupon_name=coupon_name).exclude(id=coupon_id).exists():

            messages.error(request,"Coupon name you have chosen is already taken ")
            return redirect('coupon')
        
        elif Coupon.objects.filter(code=coupon_code).exclude(id=coupon_id).exists():
             messages.error(request,"Coupon code you have chosen is already taken ")
             return redirect('coupon')
        
        else:
            coupon.save()
            return redirect('coupon')
        
def block_coupon(request,coupon_id):

    coupon=Coupon.objects.get(id=coupon_id)
    print("hjksjhfkjhdkjfhksjdfhksdhfksdjhfksjdhk")
    if coupon.is_available == True:
        
        coupon.is_available=False
    else:
        coupon.is_available=True
    coupon.save()
    return redirect('coupon')


def banner(request):
    banner=Banner.objects.all()

    context={
        'banner':banner,
    }

    return render(request,'dashboard/banner.html',context)

def add_banner(request):
    if request.method=='POST':
        banner_name = request.POST.get('bannername')
        banner_image = request.FILES.get('banner_img')

        try:
            banner_records_count = Banner.objects.count()
        
        except:
            banner_records_count=0
        
       
      
        if banner_records_count<1:

            if Banner.objects.filter(banner_name=banner_name).exists():
                messages.error(request,"Entered banner name is already taken!!")
                return redirect('banner')
                
            else:
                banner=Banner(banner_name= banner_name,banner_image=banner_image)
                banner.save()
                return redirect('banner')
        else:
            messages.error(request,"banner limit is reached!!")
            return redirect('banner')
        
def edit_banner(request,banner_id):

    banner = Banner.objects.get(id=banner_id)
    banner_image = banner.banner_image
    if request.method=="POST":
        banner_name= request.POST.get('bannername')
        
        banner_images = request.FILES.get('banner_img')

        if banner_images is None:
            banner.banner_image = banner_image
    
        else:
            banner.banner_image = banner_images

        if Banner.objects.filter(banner_name=banner_name).exclude(id=banner_id).exists():
            messages.error(request,"Entered Banner name is already taken!!")
            return redirect('banner')
            
        else:
             banner.banner_name  = banner_name
             banner.save()
             return redirect('banner')

def remove_banner(request,banner_id):

    banner=Banner.objects.get(id=banner_id)
    
    banner.delete()


    return redirect('banner')

def Orders(request):

    orders = Order.objects.all()
    order_items = OrderItem.objects.order_by('order').distinct('order')
    for i in order_items:
        print(i.quantity)
    context={
        "orders":orders,
        "orderitems":order_items
    }
    return render(request,"dashboard/orders.html",context)

def OrdersDetails(request,order_id):
    
    order=Order.objects.get(id=order_id)
    order_item = OrderItem.objects.filter(order=order)

    context={
        "order":order,
        "orderitems":order_item
    }

    return render(request,"dashboard/orders_details.html",context)


def OrderStatus(request):
  
    if request.method == 'POST':
        url = request.META.get('HTTP_REFERER')
        try:
            order_id = request.POST.get('order_id')
            order_status = request.POST.get('order_status')
            print(order_status)
            if order_status == 'Order Status':
                order = Order.objects.get(id=order_id)
                order_item = OrderItem.objects.filter(order=order)
                context = {
                    'order': order,
                    'order_item': order_item
                }
                return redirect(url)
            order = Order.objects.get(id=order_id)
            order_item = OrderItem.objects.filter(order=order)
            
            order.status = order_status
            order.save()
            if order_status == 'Returned':
                email = order.user.email
                user = CustomUser.objects.get(email=email)
                user.wallet = user.wallet + order.total_price
                userwallet = UserWallet()
                userwallet.user = user
                userwallet.amount = order.total_price
                userwallet.transaction = 'Credited'
                userwallet.save()
                user.save()
            order_item = OrderItem.objects.filter(order=order)
            context = {
                'order': order,
                'order_item': order_item
            }
            print(order.total_price)
            print("order_status")
            return redirect(url)
         
        except:
            pass
    print("order_status")
    order_item = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_item': order_item
    }
    return render(request, 'dashboard/orders_details.html', context)




def GetSalesRevenue(request):
    pass




def RenderToPdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Sales_report.pdf"'

    # Create a PDF with xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def SalesReportPdfDownload(request):
    if 'start_date' and 'end_date' in request.session:
         start_date = request.session['start_date']
         end_date = request.session['end_date']
         try:
             order = Order.objects.filter(created_at__range=(start_date, end_date))
             del request.session['start_date']
             del request.session['end_date']
         except:
             order=None
    else:

        order = Order.objects.all()
    context = {
        'orders': order,
    }
    pdf = RenderToPdf('dashboard/sales_report_pdf.html', context)
    return pdf
