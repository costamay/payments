from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword, Mpesab2bSecurityCredential
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment

def getAccessToken(request):
    consumer_key = 'ASTQ3Az2twBDxSgc5GQcOWZjaVMOENXF'
    consumer_secret = 'uxKyQuPLW4RsnW3I'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPassword.Business_short_code,
        "Password": LipanaMpesaPassword.decode_password,
        "Timestamp": LipanaMpesaPassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254705413505,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPassword.Business_short_code,
        "PhoneNumber": 254705413505,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Titus",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    # print(request.text)
    return HttpResponse('success')

def b2bpayment(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2b/v1/paymentrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "Initiator": Mpesab2bSecurityCredential.initiator_name,
        "SecurityCredential": Mpesab2bSecurityCredential.securitycredential,
        "CommandID": "BusinessToBusinessTransfer",
        "SenderIdentifierType": Mpesab2bSecurityCredential.partyAshortcode,
        "RecieverIdentifierType": Mpesab2bSecurityCredential.partyBshortcode,
        "Amount": 200,
        "PartyA": Mpesab2bSecurityCredential.partyAshortcode,
        "PartyB": Mpesab2bSecurityCredential.partyBshortcode,
        "AccountReference": " Arronax ",
        "Remarks": "this a busines2business transaction",
        "QueueTimeOutURL": "http://your_timeout_url",
        "ResultURL": "http://your_result_url"
    }
  
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)
    return HttpResponse('success')

def b2cpayment(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"
    headers = { "Authorization": "Bearer %s" % access_token }
    request = {
        "InitiatorName": Mpesab2bSecurityCredential.initiator_name,
        "SecurityCredential": Mpesab2bSecurityCredential.securitycredential,
        "CommandID": "BusinessPayment",
        "Amount": 1000,
        "PartyA": LipanaMpesaPassword.Business_short_code,
        "PartyB": 254705413505,
        "Remarks": "busines to customer transaction",
        "QueueTimeOutURL": "http://your_timeout_url",
        "ResultURL": "http://your_result_url",
        "Occasion": " "
    }
  
    response = requests.post(api_url, json = request, headers=headers)
    print (response.text)
    return HttpResponse('success')
    

@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {
        "ShortCode": LipanaMpesaPassword.Test_c2b_shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://5a49179f.ngrok.io/v1/c2b/confirmation",
        "ValidationURL": "https://5a49179f.ngrok.io/api/v1/c2b/validation"
    }
    
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    
    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType']
    )
    payment.save()
    
    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    
    return JsonResponse(dict(context))

