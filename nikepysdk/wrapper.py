import requests
import uuid
import re
import json
from nikepysdk.event import NikeEvent

class NikeSdk(object):
    def __init__(self, proxies={}):
        self.proxies = proxies

    def get_access_token(self, username, password):
        session = requests.session()
        session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
        session.get('https://www.nike.com/snkrs')
        payload = {
            'username': username,
            'password': password,
            'ux_id': 'com.nike.commerce.snkrs.web',
            'client_id': 'HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH',
            'grant_type': 'password',
            'keepMeLoggedIn': 'true'
        }
        endpoint = 'https://unite.nike.com/loginWithSetCookie'
        response = session.post(endpoint, json=payload)
        access_token = response.json()['access_token']
        return access_token

    def create_account(self, account_data):
        payload = {
            'locale': 'en_US',
            'account': {
                'email': account_data['email'],
                'passwordSettings': {
                    'password': account_data['password'],
                    'passwordConfirm': account_data['password']
                }
            },
            'registrationSiteId': 'snkrsweb',
            'username': account_data['email'],
            'firstName': account_data['first_name'],
            'lastName': account_data['last_name'],
            'dateOfBirth': account_data['date_of_birth'],
            'country': 'US',
            'gender': account_data['gender'],
            'receiveEmail': 'false'
        }
        endpoint = 'https://unite.nike.com/join'
        response = requests.post(endpoint, json=payload)
        success = not isinstance(response.json(), list)
        return success

    def is_account_verified(self, access_token):
        payload = {
            'viewId': 'commerce',
            'token': access_token
        }
        endpoint = 'https://unite.nike.com/getUserService'
        response = requests.get(endpoint, params=payload)
        verified = 'verifiedphone' in response.json()
        return verified

    def send_sms_code(self, access_token, phone_number):
        params = {
            'phone': phone_number,
            'country': 'US',
            'token': access_token
        }
        text_endpoint = 'https://unite.nike.com/sendCode'
        response = requests.post(text_endpoint, data={}, params=params)
        success = response.status_code == 202
        return success

    def verify_sms_code(self, access_token, sms_code):
        params = {
            'code': sms_code,
            'token': access_token
        }
        endpoint = 'https://unite.nike.com/verifyCode'
        response = requests.post(endpoint, data={}, params=params)
        success = response.status_code == 200
        return success

    def add_shipping_address(self, access_token, shipping_info):
        address_id = str(uuid.uuid4())
        payload = {
            'address': {
                'shipping': {
                    'preferred': True,
                    'type': 'shipping',
                    'name': {
                        'primary': {
                            'given': shipping_info['first_name'],
                            'family': shipping_info['last_name']
                        }
                    },
                    'line1': shipping_info['address_1'],
                    'line2': shipping_info['address_2'],
                    'locality': shipping_info['city'],
                    'province': shipping_info['state'],
                    'code': shipping_info['zip'],
                    'country': 'US',
                    'phone': {
                        'primary': shipping_info['phone']
                    },
                    'label': 'shipping_1',
                    'guid': address_id
                }
            }
        }
        endpoint = 'https://api.nike.com/user/commerce'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = requests.put(endpoint, json=payload, headers=headers)
        success = response.status_code == 202
        return address_id if success else None

    def add_card(self, access_token, card_info):
        card_id = str(uuid.uuid4())
        payload = {
            'accountNumber': card_info['number'],
            'cardType': card_info['type'],
            'expirationMonth': card_info['exp_month'],
            'expirationYear': card_info['exp_year'],
            'creditCardInfoId': card_id,
            'cvNumber': card_info['ccv']
        }
        endpoint = 'https://paymentcc.nike.com/creditcardsubmit/{}/store'.format(card_id)
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        success = response.status_code == 201
        return card_id if success else None

    def add_billing_info(self, access_token, billing_info, address_id, card_id):
        payload = {
            'currency': 'USD',
            'isDefault': True,
            'billingAddress': {
                'address1': billing_info['address_1'],
                'address2': billing_info['address_2'],
                'city': billing_info['city'],
                'country': 'US',
                'firstName': billing_info['first_name'],
                'guid': address_id,
                'lastName': billing_info['last_name'],
                'phoneNumber': billing_info['phone'],
                'postalCode': billing_info['zip'],
                'state': billing_info['state']
            },
            'creditCardInfoId': card_id,
            'type': 'CreditCard'
        }
        endpoint = 'https://api.nike.com/commerce/storedpayments/consumer/savepayment'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        success = response.status_code == 201
        return success

    def get_event_by_id(self, event_id):
        endpoint = 'https://www.nike.com/events-registration/event?id={0}'.format(event_id)
        response = requests.get(endpoint)
        try:
            event_data = json.loads(re.search('nike\.events\.content = (.*?) \|\| {}', response.text).group(1))
        except AttributeError:
            return None
        event = NikeEvent(event_data)
        return event