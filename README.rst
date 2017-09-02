nike-py-sdk
===========

This is an *unofficial* Python3 API wrapper for Nike services. WIP.

Basic Usage
-----------

.. code:: py

    import nikepysdk

    nike = nikepysdk.NikeSdk()

    username = 'test@example.com'
    password = 'Password123!'
    access_token = nike.get_access_token(username, password)
    print(access_token) # Some long access token

    account_verified = nike.is_account_verified(access_token)
    print(account_verified) # True or False

    account_data = {
        'email': 'newaccount@example.com',
        'password': 'Password12345!',
        'first_name': 'John',
        'last_name': 'Smith',
        'date_of_birth': '2000-01-01', # YYYY-MM-DD
        'gender': 'male' # or female
    }
    account_created = nike.create_account(account_data)
    print(account_created)

    event = nike.get_event_by_id(88145)
    print(event.event_id, event.title, event.location)

SDK Documentation
-----------------

``nike.get_access_token``
~~~~~~~~~~~~~~~~~~~~~~~~~

``nike.get_access_token(username, password)``

Returns an access token for an account given a username and password
that can be used to interact with authenticated API endpoints.

Parameters
^^^^^^^^^^

1. ``string`` - Username for the account
2. ``string`` - Password for the account

Returns
^^^^^^^

``string`` Access token in a string format

Example
^^^^^^^

.. code:: py

    username = 'example@test.com'
    password = 'Password123!'
    access_token = nike.get_access_token(username, password)
    print(access_token) # Some long string

``nike.create_account``
~~~~~~~~~~~~~~~~~~~~~~~

``nike.create_account(account_data)``

Creates a new Nike+ account given the account data. ``account_data`` is
a dictionary with the following schema:

::

    {
        'email': string,
        'password': string,
        'first_name': string,
        'last_name': string,
        'date_of_birth': string, # YYYY-MM-DD
        'gender': string # 'male' or 'female'
    }

Parameters
^^^^^^^^^^

1. ``dict`` - Account data as a dict

Returns
^^^^^^^

``bool`` Success of the account creation

Example
^^^^^^^

.. code:: py

    account_data = {
        'email': 'newaccount@example.com',
        'password': 'Password12345!',
        'first_name': 'John',
        'last_name': 'Smith',
        'date_of_birth': '2000-01-01', # YYYY-MM-DD
        'gender': 'male' # or female
    }
    account_created = nike.create_account(account_data)
    print(account_created) # True, hopefully

``nike.is_account_verified``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``nike.is_account_verified(access_token)``

Checks if an account is verified given an account's valid access token

Parameters
^^^^^^^^^^

1. ``string`` - Account access token

Returns
^^^^^^^

``bool`` If the account is verified or not

Example
^^^^^^^

.. code:: py

    is_verified = nike.create_account(access_token)
    print(is_verified) # True, hopefully

``nike.send_sms_code``
~~~~~~~~~~~~~~~~~~~~~~

``nike.send_sms_code(access_token, phone_number)``

Sends an SMS verification code to an account given its access token and
phone number.

Parameters
^^^^^^^^^^

1. ``string`` - Account access token
2. ``string`` - Phone number to send code to

Returns
^^^^^^^

``bool`` Success of the operation

Example
^^^^^^^

.. code:: py

    phone_number = '1112223333'
    sms_sent = nike.send_sms_code(access_token, phone_number)
    print(sms_sent) # True, hopefully

``nike.verify_sms_code``
~~~~~~~~~~~~~~~~~~~~~~~~

``nike.verify_sms_code(access_token, sms_code)``

Verifies the SMS code for an account.

Parameters
^^^^^^^^^^

1. ``string`` - Account access token
2. ``string`` - SMS code that was received

Returns
^^^^^^^

``bool`` Success of the operation

Example
^^^^^^^

.. code:: py

    sms_code = '123456'
    sms_verified = nike.verify_sms_code(access_token, sms_code)
    print(sms_verified) # True, hopefully

``nike.add_shipping_address``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``nike.add_shipping_address(access_token, shipping_info)``

Adds a new shipping address to an account. ``shipping_info`` is a
dictionary with the following schema:

::

    {
        'first_name': string,
        'last_name': string,
        'address_1': string,
        'address_2': string,
        'city': string,
        'state': string, # Initials
        'zip': string,
        'phone': string, # 1112223333
    }

Parameters
^^^^^^^^^^

1. ``string`` - Access token for the account\_
2. ``dict`` - Shipping address data as a dict

Returns
^^^^^^^

``string`` Address ID for use in adding billing info

Example
^^^^^^^

.. code:: py

    shipping_info = {
        'first_name': 'John',
        'last_name': 'Smith',
        'address_1': '123 Main Street',
        'address_2': 'APT 1A',
        'city': 'Sometown',
        'state': 'OH',
        'zip': '12345',
        'phone': '1234567890'
    }
    address_id = nike.add_shipping_address(access_token, shipping_info)
    print(address_id) # Some uuid4 string

``nike.add_card``
~~~~~~~~~~~~~~~~~

``nike.add_card(access_token, card_info)``

Adds a new card to an account. ``card_info`` is a dictionary with the
following schema:

::

    {
        'number': string,
        'type': string, # VISA or similar
        'exp_month': string, # XX
        'exp_year': string, # XXXX
        'cvv': string
    }

Parameters
^^^^^^^^^^

1. ``string`` - Access token for the account\_
2. ``dict`` - Card data as a dict

Returns
^^^^^^^

``string`` Card ID for use in adding billing info

Example
^^^^^^^

.. code:: py

    card_info = {
        'number': '1111222233334444,
        'type': 'VISA', # VISA or similar
        'exp_month': '12', # XX
        'exp_year': '2021', # XXXX
        'cvv': '123'
    }
    card_id = nike.add_card(access_token, card_info)
    print(card_id) # Some uuid4 string

``nike.add_billing_info``
~~~~~~~~~~~~~~~~~~~~~~~~~

``nike.add_billing_info(access_token, access_token, billing_info, address_id, card_id)``

Adds a new billing profile to an account. ``billing_info`` is a
dictionary with the following schema:

::

    {
        'first_name': string,
        'last_name': string,
        'address_1': string,
        'address_2': string,
        'city': string,
        'state': string, # Initials
        'zip': string,
        'phone': string, # 1112223333
    }

``address_id`` and ``card_id`` are IDs returned by
``add_shipping_address`` and ``add_card``.

Parameters
^^^^^^^^^^

1. ``string`` - Access token for the account
2. ``dict`` - Billing data as a dict
3. ``string`` - Address ID to add to the profile
4. ``string`` - Card ID to add to the profile

Returns
^^^^^^^

``bool`` Success of the operation

Example
^^^^^^^

.. code:: py

    billing_info = {
        'first_name': 'John',
        'last_name': 'Smith',
        'address_1': '123 Main Street',
        'address_2': 'APT 1A',
        'city': 'Sometown',
        'state': 'OH',
        'zip': '12345',
        'phone': '1234567890'
    }
    billing_added = nike.add_billing_info(access_token, billing_info, address_id, card_id)
    print(billing_added) # True, hopefully

``nike.get_event_by_id``
~~~~~~~~~~~~~~~~~~~~~~~~

``nike.get_event_by_id(event_id)``

Returns a ``NikeEvent`` object that contains information about an event

Parameters
^^^^^^^^^^

1. ``string`` - ID of the event

Returns
^^^^^^^

``NikeEvent`` Event data as a ``NikeEvent`` object

Example
^^^^^^^

.. code:: py

    event_id = '12345'
    event = nike.get_event_by_id(event_id)
    print(event.title) # Some string
