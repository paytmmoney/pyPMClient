# The Paytm Money Equity 1.1.4 API Python client

The official Python client for communicating with [PaytmMoney Equity API](https://www.paytmmoney.com/stocks/).


# Description

PMClient is a set of REST-like APIs that expose many capabilities required to build a complete investment and
trading platform. Execute orders in real time, manage user portfolio, stream live market data (WebSockets), and more, with the simple HTTP API collection.


[PaytmMoney Technology Pvt Ltd](https://www.paytmmoney.com/) (c) 2022. Licensed under the MIT License.


## Api Documentation

- [PaytmMoney API documentation](https://developer.paytmmoney.com/docs/api/logout/)

## Usage

### Install Package
##### - User need to clone this repo and add it locally to their project. 
##### Requirements
##### - Python version 3.10.1 and
##### - install the packages 
```python
pip3 install -r requirements.txt
```


### API Usage

```python
from pyPMClient import PMClient
```


##### User needs to create an object of sdk and pass apiKey & apiSecretKey
```python
# Initialize PMClient using apiKey and apiSecret.
pm = PMClient(api_secret="your_api_secret", api_key="your_api_key")
# Initialize PMClient using apiKey, apiSecret & jwt tokens if user has already generated.
pm = PMClient(api_secret="your_api_secret", api_key="your_api_key", access_token="access_token", public_access_token="public_access_token", read_access_token="read_access_token")
```

##### User can call the login method and get the login URL.
```python
# state_key : Variable key which merchant/fintech company expects Paytm Money to return with Request Token. This can be string.
pm.login(state_key)
```

##### User manually executes a login url in the browser and fetches requestToken after validating username, password, OTP and passcode. 
##### After a successful login user will be provided the request_token in the URL

##### Once the request_token is obtained you can generate access_token by calling generate_session
1) User manually executes a login url in the browser and fetches requestToken after validating username, password, OTP and passcode. 
2) After a successful login user will be provided the request_token in the URL.
3) Once the request_token is obtained you can generate access_token by calling generate_session.
```python
pm.generate_session(request_token="your_request_token")
```

##### After generating the access_token it will get set and any API can be called with same access_token.

##### To manually set the jwt tokens, 
```python
pm.set_access_token("your_access_token")
pm.set_public_access_token("your_public_access_token")
pm.set_read_access_token("your_read_access_token")
```

### Place Order
* Here you can place regular, cover and bracket order.
* For cover order in argument user has to add trigger_price.
* For bracket order in argument user has to add stoploss_value & profit_value.
```python
# Regular Order
order = pm.place_order(txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, source, off_mkt_flag)
```

```python
# Cover Order
order = pm.place_order(txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, source, trigger_price)
```

```python
# Bracket Order
order = pm.place_order(txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, source, stoploss_value, profit_value)
```

### Modify Order
* Here you can modify orders.
* For cover order in argument user has to add leg_no.
* For bracket order in argument user has to add leg_no & algo_order_no.
```python
# Regular Order
order = pm.modify_order(source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, mkt_type, order_no, serial_no, group_id)
```

```python
# Cover Order
order = pm.modify_order(source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, mkt_type, order_no, serial_no, group_id, leg_no)
```

```python
# Bracket Order
order = pm.modify_order(source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, mkt_type, order_no, serial_no, group_id, leg_no, algo_order_no)
```

### Cancel Order
* Here you can Cancel Orders.
* For cover order in argument user has to add leg_no.
* For bracket order in argument user has to add leg_no & algo_order_no.
```python
# Regular Order
order = pm.cancel_order(source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, mkt_type, order_no, serial_no, group_id)
```

```python
# Cover Order
order = pm.cancel_order(source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, mkt_type, order_no, serial_no, group_id, leg_no)
```

```python
# Bracket Order
order = pm.cancel_order(source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, mkt_type, order_no, serial_no, group_id, leg_no, algo_order_no)
```

### Convert Order
* For converting orders.
```python
# Regular Order
order = pm.convert_regular(source, txn_type, exchange, mkt_type, segment, product_from, product_to, quantity, security_id)
```


### Order Details
* Fetch details of all the order.
```python
pm.order_book()
```

### Trade Details
* Fetch Trade Details.
```python
pm.trade_details(order_no, leg_no, segment)
```

### Position
* Get all the positions.
```python
pm.position()
```

### Position Details
* Get position detail of specific stock.
```python

pm.position_details(security_id, product, exchange)
```

### Get Funds History
* Get the funds history.
```python
pm.funds_summary(config)
```

### Scrip Margin
* Calculate Scrip Margin.
```python
pm.scrips_margin(source, margin_list=[
                                 "exchange":"exchange",
                                 "segment":"segment",
                                 "security_id":"security_id",
                                 "txn_type":"txn_type",
                                 "quantity":"quantity",
                                 "strike_price":"strike_price",
                                 "trigger_price":"trigger_price",
                                 "instrument":"instrument"
                                 ])
```

### Order Margin
* Calculate Order Margin.
```python
pm.order_margin(source, exchange, segment, security_id, txn_type, quantity, price, product, trigger_price)
```

### Holdings value
* Get value of the holdings.
```python
pm.holdings_value()
```

### User Holdings Data
* Get holdings data of User.
```python
pm.user_holdings_data()
```

### Security Master
* User can filter by file_name.
* To get the supported fileName [API Doc for fileNames](https://developer.paytmmoney.com/docs/api/security-master/)
```python
pm.security_master(file_name)
```

### User Details
* Fetch user details.
```python
pm.get_user_details()
```

### Generate Tpin
```python
pm.generate_tpin()
```

### Validate Tpin
```python
pm.validate_tpin(trade_type, isin_list=[])
```

### Status 
* user can get the edis_request_id from the response of validate TPIN API.
```python
pm.status(edis_request_id)
```

### Logout
```python
pm.logout()
```

### Create GTT
* To create a GTT order.
```python
pm.create_gtt(segment, exchange, pml_id, security_id, product_type, set_price, transaction_type, order_type, trigger_type, quantity, trigger_price, limit_price)
```

### Get All GTT
* To get all GTT or get by pml_id or status.
```python
pm.get_gtt_by_pml_id_and_status(status, pml_id)
```

### Get GTT
* To get GTT by Id.
```python
pm.get_gtt(id)
```

### Update GTT
* To update GTT by Id.
```python
pm.update_gtt(id, quantity, trigger_price, limit_price, set_price, transaction_type, order_type, trigger_type)
```

### Delete GTT
* To Delete GTT by Id.
```python
pm.delete_gtt(id)
```

### Get Expiry
* To get expiry of the GTT.
```python
pm.get_gtt_expiry_date(pml_id)
```

### Get Aggregate
* To get the aggregate of the GTTs.
```python
pm.get_gtt_aggregate()
```

### Get GTT InstructionId
* To GTT by InstructionId.
```python
pm.get_gtt_by_instruction_id(id)
```

### Create GTT V2
* To create a GTT order.
* Note : transaction_details is a list of dictionary(key-value pair).
* Refer below sample requestBody 
```python
pm.create_gtt_v2(segment, exchange, security_id, product_type, set_price, transaction_type, trigger_type, transaction_details)
```
```python
# Sample requestBody for OCO trigger_type
pm.create_gtt_v2(
        segment = "E",
        exchange = "BSE",
        security_id = 500570,
        product_type = "C",
        set_price = "702.65",
        transaction_type = "S",
        trigger_type = "OCO",
        transaction_details = [
            {
                "sub_type": "STOPLOSS",
                "trigger_price": "695.60",
                "order_type": "MKT",
                "limit_price": 0,
                "quantity": 1
            },
            {
                "sub_type": "TARGET",
                "trigger_price": "709.70",
                "order_type": "MKT",
                "limit_price": 0,
                "quantity": 1
            }
        ]   
    )
```
```python
# Sample requestBody for SINGLE trigger_type
pm.create_gtt_v2(
    segment = "E",
    exchange = "BSE",
    security_id = 500570,
    product_type = "C",
    set_price = "709.35",
    transaction_type = "B",
    trigger_type = "SINGLE",
    transaction_details = [
        {
            "trigger_price": "702.25",
            "order_type": "MKT",
            "limit_price": 0,
            "quantity": 1
        }
    ]
)
```

### Get All GTT V2
* To get all GTT or get by pml_id or status.
```python
pm.get_gtt_by_pml_id_and_status_v2(status, pml_id)
```

### Get GTT V2
* To get GTT by Id.
```python
pm.get_gtt_v2(id)
```

### Update GTT V2
* To update GTT by Id.
* Note : transaction_details is a list of dictionary(key-value pair).
* Refer below sample requestBody 
```python
pm.update_gtt_v2(id, set_price, transaction_type, trigger_type, transaction_details)
```
```python
pm.update_gtt_v2(
    id=217,
    set_price = "8.40",
    transaction_type = "S",
    trigger_type = "OCO",
    transaction_details = [
        {
            "id": 218,               #For OCO only
            "sub_type": "STOPLOSS",  #For OCO only
            "quantity": "2",
            "trigger_price": "9.0",
            "limit_price": "15.0",
            "order_type": "LMT"    
        },
        {
            "id": 219,                #For OCO only
            "sub_type": "TARGET",   #For OCO only
            "quantity": "2",
            "trigger_price": "15.0",
            "limit_price": "20",
            "order_type": "LMT"   
        }
    ]
)
```

### Get GTT InstructionId V2
* To GTT by InstructionId.
```python
pm.get_gtt_by_instruction_id_v2(id)
```

### Get Live Price via API
* To Get Live Price Data via API
```python
pm.get_live_market_data("mode", preferences)
```

### Get Option Chain
* To Get Option Chain using type, symbol and expiry (in DD-MM-YYYY format)
```python
pm.get_option_chain("type", "symbol", "expiry")
```

### Get Option Chain Config
* To Get Option Chain Config using symbol
```python
pm.get_option_chain_config("symbol")
```

### Get All Orders
* Get all orders without apiKey filter
```python
pm.orders()
```

### Brokerage, Statutory & Regulatory Levies
* Get Charges Info
```python
pm.charges_info("brokerage_profile_code", "transaction_type", "product_type", "instrument_type", "exchange", qty, price)
```

### WebSocket Usage
* To use websocket client in your project, add below code in a python file -
```python
from pmClient.WebSocketClient import WebSocketClient

webSocketClient = WebSocketClient("your_public_access_token") # pass your public access token here

customerPreferences = []

preference = {
    "actionType": 'ADD',  # 'ADD', 'REMOVE'
    "modeType": 'LTP',  # 'LTP', 'FULL', 'QUOTE'
    "scripType": 'INDEX',  # 'ETF', 'FUTURE', 'INDEX', 'OPTION', 'EQUITY'
    "exchangeType": 'NSE',  # 'BSE', 'NSE'
    "scripId": '13'
}

# create as many preferences as you like as shown above and append them in customerPreferences array

customerPreferences.append(preference)


def on_open():
    # send preferences via websocket once connection is open
    webSocketClient.subscribe(customerPreferences)


def on_close(code, reason):
    # this event gets triggered when connection is closed
    print(code, reason)


def on_error(error_message):
    # this event gets triggered when error occurs
    print(error_message)


def on_message(arr):
    # this event gets triggered when response is received
    print(arr)


webSocketClient.set_on_open_listener(on_open)
webSocketClient.set_on_close_listener(on_close)
webSocketClient.set_on_error_listener(on_error)
webSocketClient.set_on_message_listener(on_message)

"""
set below reconnect config if reconnect feature is desired
Set first param as true and second param, the no. of times retry to connect to server shall be made  
"""
webSocketClient.set_reconnect_config(True, 5)

# this method is called to create a websocket connection with broadcast server
webSocketClient.connect()

# To explicitly close websocket connection with server, call this method
webSocketClient.disconnect()
```
