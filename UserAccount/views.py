from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from UserAccount.models import UserBase
from order.models import Order
from order.views import user_orders
from .forms import RegistrationForm, UserEditForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import  urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import account_activation_token
from django.http import HttpResponse
from django.contrib.auth import login, logout

# Create your views here.

# @login_required
# def accounts_view(request):

@login_required(login_url='UserAccount:login')
def accounts_view(request):
    orders = user_orders(request)
    # orders = Order.objects.all()
    
    context = {
                # 'section': 'profile',
                'orders': orders
                }
    return render(request, 'user/accounts.html', context)

def login_view (request):   
    return render(request, 'registration/login.html', {});

@login_required(login_url='UserAccount:login')
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    
    context = {'user_form': user_form}
    return render(request, 'user/edit_details.html', context)

@login_required(login_url='UserAccount:login')
def delete_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('UserAccount:delete_confirmation')

def register_view(request):
    
    if request.user.is_authenticated:
        return redirect('UserAccount:accounts')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.user_name = registerForm.cleaned_data['user_name']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your PrintShop Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('you are registered succesfully and an activation has been sent to your email')
    else:
        registerForm = RegistrationForm()
    context = {'form': registerForm}
    
    return render(request, 'registration/register.html', context);

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('UserAccount:accounts_view')
    else:
        return render(request, 'registration/activation_invalid.html')
