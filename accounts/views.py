from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.views.decorators.cache import cache_control
from django.contrib import messages
from .models import CustomUser, CustomUserManager
import pyotp
from .utils import send_otp

from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime
from django.contrib.auth.hashers import make_password


@cache_control(no_cache=True , no_store=True)
def UserLogin(request):
    # Check if the user is already logged in and redirect to the home page.
    if 'useremail' in request.session:
        return redirect('home')

    # Check if the login form has been submitted.
    if request.method == 'POST':
        # Get the user's email and password from the form.
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        
        # Get the user by email or return None using get() with filter.
        user = CustomUser.objects.filter(email=user_email).first()

        if user:
            # Check if the user is active.
            if not user.is_active:
                messages.error(request, 'Your account has been blocked')
                return redirect('user_login')

            # Attempt to authenticate the user.
            user = authenticate(request, email=user_email, password=user_password)

            if user is not None and not user.is_superuser:
                # Login the user and set the session variable.
                login(request, user)
                request.session['useremail'] = user_email
                return redirect('home')
            else:
                messages.error(request, 'Email or Password is Incorrect')
        else:
            messages.error(request, 'User Does not Exist')

    # Render the login page.
    return render(request, 'accounts/login.html')


def UserSignup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        user_email=request.POST.get('email')
        phone = request.POST.get('phone_no')
        password=request.POST.get('password')   
        confirm_password=request.POST.get('confirmpassword')

        email_checking = CustomUser.objects.filter(email=user_email)

        if email_checking.exists():
            messages.error(request,"Email already taken")
            return redirect('user_signup')
        elif password == confirm_password:
            otp=send_otp(request)
            subject= 'Verify your email to continue to create an account '
            message=otp
            from_email= settings.EMAIL_HOST_USER
            recipient_list = [user_email]

            send_mail(subject,message,from_email,recipient_list)

            request.session['useremail'] = user_email
            request.session['username' ]  = username
            request.session[ 'phoneno' ]   = phone
            request.session['password' ]  = password
    
            return redirect('user_otp')
        else:
             messages.error(request,'Password do not match')

    return render(request,'accounts/signup.html') 



@cache_control(no_cache=True ,must_revalidate=True , no_store=True)
def UserLogout(request):
    if 'useremail' in request.session:
        # Log out the user and flush the session.
        logout(request)
        # Debugging output
        print("User has been logged out")

        # Flush the session to ensure the user is logged out and clear any stored session data.
        request.session.flush()

    return redirect('home')


def OtpVerification(request):
    if request.method=='POST':
        otp=request.POST.get('otp')

        user_email = request.session['useremail']
        username=request.session['username']
        phone = request.session['phoneno']
        password = request.session['password']

        otp_secret_key=request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)
             
            if valid_until > datetime.now():
                totp=pyotp.TOTP(otp_secret_key, interval=60)

                if totp.verify(otp):
                    my_User = CustomUser.objects.create_user(email=user_email,password=password, username=username,phone=phone)
                    my_User.save()

                    del request.session['useremail']
                    del request.session['username' ]
                    del request.session['phoneno']
                    del request.session['password']
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']


                    return redirect('user_login')
                else:
                     messages.error(request,"! Entered an incorrect otp !")

            else:
                 del request.session['useremail']
                 del request.session['username']
                 del request.session['phoneno']
                 del request.session['password']
                 del request.session['otp_secret_key']
                 del request.session['otp_valid_date']
                 messages.error(request," Time for otp validation expired  !! ")

    return render(request,'accounts/verify.html')

#view function for resending the otp
def OtpResend(request):
     #deleting the session of existing one time password
    del request.session['otp_secret_key']

    otp=send_otp(request)

    user_email = request.session['usermail']
    username=request.session['username']
    phone = request.session['phoneno']
    password= request.session['password']

    subject =  " Verify your email to Create an account at Nature's Touch furniture " 
    message = otp
    from_email= settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message , from_email , recipient_list)

    otp_secret_key = request.session['otp_secret_key']
    otp_valid_date = request.session['otp_valid_date']

    if otp_secret_key and otp_valid_date is not None:
        valid_until = datetime.fromisoformat(otp_valid_date)

        if valid_until > datetime.now():
            totp= pyotp.TOTP(otp_secret_key, interval = 60)

            if totp.vetify(otp):
                   
                my_User = CustomUser.objects.create_user(email=user_email , password = password , username = username , phone = phone )
                my_User.save()


                del request.session[' usermail ']
                del request.session[ ' username ' ]
                del request.session[ ' phoneno ' ]
                del request.session[ ' password ' ]
                del request.session[ ' otp_secret_key ' ]
                del request.session[ ' otp_valid_date ' ]


                return redirect( ' user_login ' )
    
    
    return render(request , 'accouts/verify.html')


def ForgotPass(request):
    if request.method == 'POST' :
        email = request.POST.get('email')
        request.session['check_mail'] = email
        if CustomUser.objects.filter(email = email).exists():
               
            user= CustomUser.objects.get(email=email)
            user_email =user.email

            otp = send_otp(request)
            subject= 'Verify your email to continue to reset your password '
            message = otp
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user_email]

            send_mail(subject, message , from_email, recipient_list)

            return redirect('forgot_pass_otp')
        else:
            messages.error(request,"There is no account linkeed with this email please check the Email once more !")
            return redirect('forgot_pass')
    return render(request, 'accounts/forgotpass.html')

# function for validating the otp 

def ForgotPassOtp(request):

    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None :
            valid_until = datetime.fromisocalendar(otp_valid_date)

            if valid_until > datetime.now() :
                totp = pyotp.TOTP(otp_secret_key, interval = 60)

                if totp.verify(otp):

                    del request.session['otp_valid_date']
                    del request.session['otp_secret_key']

                    return redirect('reset_pass')
                else:
                    messages.error(request,"OTP You have entered is incorrect ")
                    return redirect('forgot_pass_otp')
            else:
                messages.error(request,"Time limit Exceeded ")
                return redirect ('forgot_pass_otp')
        return render(request, 'accounts/forgotpass_verify.html')



# function for reseting the password

def ResetPass(request):
    if request.method=='POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 == password2:
            email = request.session.get('check_mail')
            try:
                user = CustomUser.objects.get(email = email )
                user.set_password(password1)
                user.save()
                del request.session['check_mail']
                return redirect('user_login')
            except CustomUser.DoesNotExist:
                messages.error(request, " There is no account linked with this mail  !!")
                return redirect('reset_pass')
        else:
            messages.error(request, "Password does not match ")

    return render(request, 'accounts/resetpass.html')