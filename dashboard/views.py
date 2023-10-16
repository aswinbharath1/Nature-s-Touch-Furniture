from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from accounts.models import CustomUser
from django.contrib import messages
from categories.models import Category,Sub_Category

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

def AdminHome (request):

    return render(request, 'dashboard/adminhome.html')

def AdminLogout(request):
    if 'adminmail' in request.session :
        logout(request)
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

       
    
        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }
        return render(request,'dashboard/category.html',context)
    else:
        category.is_activate=True
        category.save()
        # categories=Category.objects.all

        category=Category.objects.all().order_by('id')
        context={
            'categories':category
        }
        return render(request,'dashboard/categories.html',context)
    

def SubCategories(request):
    category=Category.objects.filter(is_activate=True)
    subcategory=Sub_Category.objects.all().order_by('id')
    context={
        'subcategories':subcategory,
        'categories':category
    }

    return render(request,'dashboard/subcategories.html',context)
 
def AddSubCategories(request):
    if request.method=="POST":
        # setting value as category_name as category id and fetching it 
        category_id=request.POST.get('category_name')
        # using category id update the category field of sub_category by passing the particular category instance
        category_instance = Category.objects.get(pk=category_id)
        sub_category_name=request.POST.get('categoryName')
        description = request.POST.get('categoryDescription')
        cat_image = request.FILES.get('cat_img')
        cat = Sub_Category(category=category_instance, sub_category_name=sub_category_name, sub_category_description=description,
                           sub_Category_image=cat_image)
        cat.save()   
        return redirect('sub_categories')

def EditSubcategories(request,subcategory_id):

    subcategory=Sub_Category.objects.get(pk=subcategory_id)
    # fetching the image from data base for when user is not edited the image field we will have to give the previous image  
    sub_category_image=subcategory.sub_Category_image

    if request.method=="POST":
        # setting value as category_name as category id and fetching it 
        category_id = request.POST.get('category_name')
        # using category id update the category field of sub_category
        subcategory.category = Category.objects.get(pk=category_id)
        sub_category_name = request.POST.get('categoryName')
        subcategory.sub_category_name =  sub_category_name
        subcategory.sub_category_description = request.POST.get('categoryDescription')

        sub_Category_img = request.FILES.get('cat_img')
        # checking if the subcategory image is none 
        if sub_Category_img is None:
            subcategory.sub_Category_image = sub_category_image
        else:
            subcategory.sub_Category_image = sub_Category_img      


        if Sub_Category.objects.filter(sub_category_name=sub_category_name).exclude(id=subcategory_id).exists():

            messages.error(request,"Entered Sub Category is already taken!!")
            return redirect('sub_categories')
        
        else:

            subcategory.save()   
            return redirect('sub_categories')
            
def DeleteSubcategories(request,subcategory_id):

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