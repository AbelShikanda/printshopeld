from django.http.response import JsonResponse
from django.shortcuts import render

from cart.cart import Cart

from .models import Order, OrderItem


def add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('rand_num') 
        name = request.POST.get('first_name') 
        name2 = request.POST.get('last_name') 
        tao = request.POST.get('town') 
        esto = request.POST.get('estate') 
        land_mark = request.POST.get('landmark') 
        hao = request.POST.get('house_no') 
        simu = request.POST.get('phone') 
        user_id = request.user.id
        carttotal = cart.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(
                                            user_id=user_id, 
                                            first_name=name, 
                                            last_name=name2, 
                                            town=tao, 
                                            estate = esto,
                                            landmark=land_mark,
                                            house_no=hao,
                                            phone = simu,
                                            total_paid=carttotal, 
                                            order_key=order_key
                                        )
            order_id = order.pk # get primary key from the order

            for item in cart:
                OrderItem.objects.create(
                                            order_id=order_id, 
                                            product=item['product'], 
                                            price=item['price'], 
                                            quantity=item['qty']
                                        )

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(complete=True)


def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(complete=True)
    return orders
