import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    consumer_key = 'ASTQ3Az2twBDxSgc5GQcOWZjaVMOENXF'
    consumer_secret = 'uxKyQuPLW4RsnW3I'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

class MpesaAccessToken:
    r = requests.get(MpesaC2bCredential.api_URL,auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

class LipanaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = '174379'
    Test_c2b_shortcode = '603011'
    
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    data_to_encode = Business_short_code + passkey + lipa_time

    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')   
    
class Mpesab2bSecurityCredential:
    initiator_name = 'apiop42'
    partyAshortcode = '603011'
    partyBshortcode = '600000'
    securitycredential = 'HcpztHXGmx559zdG6a+e3rkwwdX1mun/R2TL1a6Madnwm6xNgBXlLJ2QNlLuQSWs0ZrEaJjwFLZ+a5giqVs/BKGYObuc/pRG7pivd4SMP0E3B3JzeW4XadI7y2ibT8/cXdU5wI/Y3xg/bcT9Nogg7fXvPcmpDnJTvwxItmy5Dmk4HF6osa5tkUbhYmEj0wyzOPZeEGUWWrXWKSgVtoCvYgkyWG1zxn4vMiETKPqEaqQX1siXpqR4eEhVR7H4HXNRy1uvSd9DFhvt2icCdkyL9sjAbxgrQrKK8hIiXwXHEPeWY0xeSvxn90fhDpLoO5MxFd5MiYoGGD+4Gec80S7jEw=='
    
