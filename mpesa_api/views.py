from asyncio.windows_events import NULL
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .models import MpesaPayment, LipaNaMpesaOnline
from .mpesa_credentials import LipanaMpesaPassword, MpesaC2bCredential
from mpesa_api.forms import MpesaPaymentForm
from cart.cart import Cart
from django.views.decorators.http import require_http_methods

def getAccessToken():
    consumer_key = MpesaC2bCredential.consumer_key
    consumer_secret = MpesaC2bCredential.consumer_secret
    api_URL = MpesaC2bCredential.api_URL

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    
    return validated_mpesa_access_token


def lipa_na_mpesa_online(request):
    
    # cart = Cart(request)
    # total = str(cart.get_total_price())
    # total = total.replace('.', '')
    # total = int(total)
    # total = str(request.POST.get('price'))

    if request.method == 'POST':
        total = str(request.POST.get('price'))
        total = total.replace('.00', '')
        total = str(total)
        phone = str(request.POST.get('phone'))
        ref_no = str(request.POST.get('rand'))
        # form = MpesaPaymentForm(request.POST)
        # if form.is_valid():
        #     phone = form.cleaned_data['phone']
        access_token = getAccessToken()
        api_url =   "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = { "Authorization": "Bearer %s" % access_token}
        req = {
            "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
            "Password": LipanaMpesaPassword.decode_password,
            "Timestamp": LipanaMpesaPassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": total,
            "PartyA": phone,  # replace with your phone number to get stk push
            "PartyB": LipanaMpesaPassword.Business_short_code,
            "PhoneNumber": phone,  # replace with your phone number to get stk push
            # "CallBackURL": "https://127.0.0.1:8000/api/v1/c2b/callback/",
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": ref_no,
            "TransactionDesc": "Print Shop Eld"
        }
        response = requests.post(api_url, json=req, headers=headers)
        print(response.text.encode('utf8'))
        return HttpResponse(response)
        # return HttpResponse(total + phone + ref_no)
        # return HttpResponse(this)

@csrf_exempt
def call_back(request):
    merchant_id = request.data['Body']['stkCallback']['MerchantRequestID']
    checkout_id = request.data['Body']['stkCallback']['CheckoutRequestID']
    result_description = request.data['Body']['stkCallback']['ResultDesc']
    amount = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    receipt_no = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    date = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value']
    phone_number = request.data['Body']['stkCallback']['CallbackMetadata']['Item'][4]['Value']
    
    transaction = LipaNaMpesaOnline.objects.create(
                                                    checkout_request_ID=checkout_id,
                                                    merchant_request_ID=merchant_id,
                                                    result_desc=result_description,
                                                    amount=amount,
                                                    receipt_number=receipt_no,
                                                    transaction_date=date,
                                                    phone_number=phone_number,
                                                )
    transaction.save()
    return redirect(reverse('checkout'))

@csrf_exempt
def confirmation(request):  # we use this function to save successfully transaction in our database.
    mpesa_body = request.body.decode('utf-8')  # we get the mpesa transaction from the body by decoding using utf-8
    mpesa_payment = json.loads(mpesa_body)  # we use json.loads method which will assist us to access variables in our request.
    payment = MpesaPayment.objects.create(
                                            first_name=mpesa_payment['FirstName'],
                                            last_name=mpesa_payment['LastName'],
                                            middle_name=mpesa_payment['MiddleName'],
                                            description=mpesa_payment['TransID'],
                                            phone_number=mpesa_payment['MSISDN'],
                                            amount=mpesa_payment['TransAmount'],
                                            reference=mpesa_payment['BillRefNumber'],
                                            organization_balance=mpesa_payment['OrgAccountBalance'],
                                            type=mpesa_payment['TransactionType'],
                                        )
    payment.save()
    # Also add a complete order to the order table
    # 
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))
