from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from UserAccount.forms import UserEditForm, UserOrderForm

from mpesa_api.forms import MpesaPaymentForm
from cart.cart import Cart
from order.models import Order


def order_placed(request):
    cart = Cart(request)
    cart.clear()
    
    return render(request, 'payment/orderplaced.html')

class Error(TemplateView):
    template_name = 'payment/error.html'

@login_required(login_url='UserAccount:login')
def checkout_view(request):
    if request.method == 'POST':
        order_form = UserOrderForm(instance=request.user, data=request.POST)
        if order_form.is_valid():
            order_form.save()
    else:
        order_form = UserOrderForm(instance=request.user)
    
    if request.method == 'POST':
        # pay_form = MpesaPaymentForm(instance=request.user, data=request.POST)
        # if order_form.is_valid():
        pay_form = MpesaPaymentForm()
            # pay_form = MpesaPaymentForm()
            # order_form.save()
    else:
        pay_form = MpesaPaymentForm()
    
    context = {
        'pay_form': pay_form,
        'order_form': order_form
        }
    
    return render(request, 'printshop/checkout.html', context)
