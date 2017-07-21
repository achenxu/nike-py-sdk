import requests
import uuid

# Registers a new Nike account (does NOT verify)
def register(account):
    payload = {
        'locale': 'en_US',
        'account': {
            'email': account['email'],
            'passwordSettings': {
                'password': account['password'],
                'passwordConfirm': account['password']
            }
        },
        'registrationSiteId': 'snkrsweb',
        'username': account['email'],
        'firstName': account['first_name'],
        'lastName': account['last_name'],
        'dateOfBirth': account['date_of_birth'],
        'country': 'US',
        'gender': account['gender'],
        'receiveEmail': 'false'
    }
    endpoint = 'https://unite.nike.com/join'
    response = requests.post(endpoint, json=payload)
    success = not isinstance(response.json(), list)
    return success

# Logs into Nike account, returns an access token
def login(session, account):
    session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'
    session.get('https://www.nike.com/snkrs')
    payload = {
        'username': account['email'],
        'password': account['password'],
        'ux_id': 'com.nike.commerce.snkrs.web',
        'client_id': 'HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH',
        'grant_type': 'password',
        'keepMeLoggedIn': 'true'
    }
    endpoint = 'https://unite.nike.com/loginWithSetCookie'
    response = session.post(endpoint, json=payload)
    access_token = response.json()['access_token']
    return access_token

# Checks if a Nike account is verified
def is_verified(session, access_token):
    payload = {
        'viewId': 'commerce',
        'token': access_token
    }
    endpoint = 'https://unite.nike.com/getUserService'
    response = session.get(endpoint, params=payload)
    verified = 'verifiedphone' in response.json()
    return verified

# Sends a verification code for an account to the given phone number
def send_code(session, phone_number, access_token):
    params = {
        'phone': phone_number,
        'country': 'US',
        'token': access_token
    }
    text_endpoint = 'https://unite.nike.com/sendCode'
    response = session.post(text_endpoint, data={}, params=params)
    success = response.status_code == 202
    return success

# Verifies a code for a given account
def verify_code(session, code, access_token):
    params = {
        'code': code,
        'token': access_token
    }
    endpoint = 'https://unite.nike.com/verifyCode'
    response = session.post(endpoint, data={}, params=params)
    success = response.status_code == 200
    return success

# Adds shipping info and returns the shipping_code (for saving default billing info)
def save_shipping_info(session, access_token, shipping_info):
    shipping_code = str(uuid.uuid4())
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
                'line1': shipping_info['address1'],
                'line2': shipping_info['address2'],
                'locality': shipping_info['city'],
                'province': shipping_info['state'],
                'code': shipping_info['zip'],
                'country': 'US',
                'phone': {
                    'primary': shipping_info['phone']
                },
                'label': 'shipping_1',
                'guid': shipping_code
            }
        }
    }
    endpoint = 'https://api.nike.com/user/commerce'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = session.put(endpoint, json=payload, headers=headers)
    success = response.status_code == 202
    return shipping_code if success else None

# Adds card info and returns the card_info (for saving default billing info)
def save_card_info(session, access_token, card_info):
    card_code = str(uuid.uuid4())
    payload = {
        'accountNumber': card_info['cc'],
        'cardType': card_info['ccType'],
        'expirationMonth': card_info['ccMonth'],
        'expirationYear': card_info['ccYear'],
        'creditCardInfoId': card_code,
        'cvNumber': card_info['ccv']
    }
    endpoint = 'https://paymentcc.nike.com/creditcardsubmit/{}/store'.format(card_code)
    response = session.post(endpoint, json=payload)
    success = response.status_code == 201
    return card_code if success else None

# Saves the default billing info, shipping info, and card info
def save_billing_info(session, access_token, billing_info, shipping_code, card_code):
    payload = {
        'currency': 'USD',
        'isDefault': True,
        'billingAddress': {
            'address1': billing_info['address1'],
            'address2': billing_info['address2'],
            'city': billing_info['city'],
            'country': 'US',
            'firstName': billing_info['first_name'],
            'guid': shipping_code,
            'lastName': billing_info['last_name'],
            'phoneNumber': billing_info['phone'],
            'postalCode': billing_info['zip'],
            'state': billing_info['state']
        },
        'creditCardInfoId': card_code,
        'type': 'CreditCard'
    }
    endpoint = 'https://api.nike.com/commerce/storedpayments/consumer/savepayment'
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    response = session.post(endpoint, json=payload, headers=headers)
    success = response.status_code == 201
    return success
