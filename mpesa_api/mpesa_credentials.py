import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64


class MpesaC2bCredential:
    #secret keys for printshop and django

# class MpesaAccessToken:
#     r = requests.get(
#                     MpesaC2bCredential.api_URL,
#                     auth=HTTPBasicAuth(
#                                         MpesaC2bCredential.consumer_key, 
#                                         MpesaC2bCredential.consumer_secret
#                                         )
#                     )
#     json_resp = r.json()
    # mpesa_access_token = json.loads(r.text)
    # validated_mpesa_access_token = json_resp['access_token']
    # validated_mpesa_access_token = mpesa_access_token['access_token']

class LipanaMpesaPassword:
    lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
    Business_short_code = "174379"  # we define the business paybill no., in this case is a test one from https://developer.safaricom.co.ke/test_credentials
    Test_c2b_shortcode = "600995"
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'    # pass key also given from link above
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode('utf-8')
