from typing import Protocol
from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login ,authenticate, get_user_model
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from django.contrib import messages

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q

from .tokens import account_activation_token
from .forms import UserRegistrationForm,UserLoginForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from .models import UserProfile
# Create your views here.
# def signup(request):
#     form = SignUpForm()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request,user)
#             return redirect('home')
#     return render(request,'signup.html',{'form': form})



def activate(request, uidb64, token):
    # User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('/login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('/')


def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')








def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = UserRegistrationForm()
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name = "accounts/register.html",
        context={"form": form}
        )






def loginUser(request):
    template = 'accounts/login.html'
    if request.user.is_authenticated:
        return redirect('/')
    # form = UserLoginForm()
    # elif not UserProfile.objects.filter(email=request.POST.get('email')).exists() and not request.POST.get('email') == None:
    #     # for error in list(form.errors.values()):
    #     #         messages.error(request, error)
        
    #     return render(request, template, {
    #         'form': form,
    #         'error_message': 'Email does not exists Please register First.'
    #     })
    
    # elif not request.POST.get('email') == None and not UserProfile.objects.get(
    #         email=request.POST.get('email')).is_active:
    #     return render(request, template, {
    #         'form': form,
    #         'error_message': 'Your Email Does Not Activated Yet Please Activate Your Email First.'
    #     })
    # else:
    if request.method == "POST":
            form = UserLoginForm(request=request, data=request.POST)
            if form.is_valid():
                # email = form.cleaned_data.get('email')
                # password = form.cleaned_data.get('password')
                # user = UserProfile.objects.filter(email=email, password=password)
                user = authenticate(
                    username=form.cleaned_data["username"],
                    password=form.cleaned_data["password"],
                )
                if user :
                    login(request, user)
                    messages.success(request, f"Hello <b>{user.username}</b>! You have been logged in")
                    return redirect("/")

            else:
                for error in list(form.errors.values()):
                    messages.error(request, error) 

    form = UserLoginForm()
    return render(
            request=request,
            template_name = "accounts/login.html",
            context={"form": form}
            )


def password_change(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = UserProfile.objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        <h2>Password reset sent</h2><hr>
                        <p>
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.<br>If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        </p>
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('/')

        for key, error in list(form.errors.values()):
            # if key == 'captcha' and error[0] == 'This field is required.':
            messages.error(request,error)
                # continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
        )




def passwordResetConfirm(request, uidb64, token):
    User = UserProfile
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Home page')
    return redirect("/")