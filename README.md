# The Paytm Money Equity 1.0 API Python client

The official Python client for communicating with [PaytmMoney Equity API](https://www.paytmmoney.com/stocks/).


# Description

PMClient is a set of REST-like APIs that expose many capabilities required to build a complete investment and
trading platform. Execute orders in real time, manage user portfolio, and more, with the simple HTTP API collection.


[PaytmMoney Technology Pvt Ltd](https://www.paytmmoney.com/) (c) 2022. Licensed under the MIT License.


## Documentation

## Usage

### Install Package
```python
pip install pyPMClient
```


### API Usage

```python
from pyPMClient import PMClient
```


##### User needs to create an object of sdk and pass apiKey & apiSecretKey
```python
# Initialize PMClient using apiKey and apiSecret.
pm = PMClient(api_secret="your_api_secret", api_key="your_api_key")
# Initialize PMClient using apiKey, apiSecret & access_token if user has already generated.
pm = PMClient(api_secret="your_api_secret", api_key="your_api_key", access_token="your_access_token")
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

### Place Order
* Here you can place regular, cover and bracket order.
* For cover order in argument user has to add trigger_price.
* For bracket order in argument user has to add stoploss_value & profit_value.
* To place sell CNC order user has to add edis_txn_id and edis_auth_mode.
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

```python
# Sell CNC Order
order = pm.place_order(txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, source, edis_txn_id, edis_auth_mode)
```

### Modify Order
* Here you can modify orders.
* For cover order in argument user has to add leg_no.
* For bracket order in argument user has to add leg_no & algo_order_no.
* To modify sell CNC order user has to add edis_txn_id and edis_auth_mode.
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

```python
# Sell CNC Order
order = pm.modify_order(source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price, mkt_type, order_no, serial_no, group_id, edis_txn_id, edis_auth_mode)
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
* For converting through eDIS user needs to provide edis_txn_id & edis_auth_mode.
* The above details can be generated by TPIN APIs.
```python
# Regular Order
order = pm.convert_regular(source, txn_type, exchange, mkt_type, segment, product_from, product_to, quantity, security_id)
```

```python
# Sell CNC Order
order = pm.convert_regular(source, txn_type, exchange, mkt_type, segment, product_from, product_to, quantity, security_id, edis_auth_mode, edis_txn_id)
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
pm.scrip_margin(source, margin_list=[
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
* Data will be provided in CSV format.
```python
pm.security_master()
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
