from .enums import OrderType, Requests, ProductType
from .apiService import ApiService
from .constants import Constants


class PMClient(ApiService, Constants):

    def __init__(self, api_secret, api_key, access_token=None):
        if api_key is not None:
            self._api_key = api_key
        else:
            raise TypeError("Api Key cannot be null or empty")
        if api_secret is not None:
            self.api_secret = api_secret
        else:
            raise TypeError("Api Secret cannot be null or empty")
        self.access_token = access_token
        ApiService.__init__(self)
        Constants.__init__(self)

    # Login flow to generate access token
    def set_access_token(self, access_token):
        self.access_token = access_token
        return self.access_token

    def login(self, state_key):
        config = self._service_config
        if state_key is not None:
            return "%s%s%s%s" % (config['routes']['login'], self._api_key, config['login_param'], state_key)
        else:
            raise TypeError("State Key cannot be null or empty")

    def generate_session(self, request_token=None):
        if request_token is not None:
            params = {'apiKey': self._api_key, 'requestToken': request_token}
            request_body = {'merchantSecret': self.api_secret}
        else:
            raise TypeError("Request Token cannot be null or empty")

        response = self.api_call_helper("access_token", Requests.POST, params, request_body)

        if "data" in response:
            self.set_access_token(response["data"])

        return response

    # Fetch User Details
    def get_user_details(self):
        return self.api_call_helper('user_details', Requests.GET, None, None)

    # Logout the session
    def logout(self):
        self.validate_access_token()
        response = self.api_call_helper('logout', Requests.DELETE, None, None)
        self.set_access_token(None)
        return response

    def validate_access_token(self):
        """Check if access token is valid or not"""
        if self.access_token is None:
            raise TypeError("Access Token is not valid")

    # Orders
    def place_order(self, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price,
                    source, off_mkt_flag=False, trigger_price=None, profit_value=None, stoploss_value=None,
                    edis_txn_id=None, edis_auth_mode=None):
        self.validate_access_token()
        order = {
            'txn_type': txn_type,
            'exchange': exchange,
            'segment': segment,
            'product': product,
            'security_id': security_id,
            'quantity': quantity,
            'validity': validity,
            'order_type': order_type,
            'price': price,
            'source': source,
            'off_mkt_flag': off_mkt_flag
        }

        helper = 'place_regular'

        # For placing stop loss order or stop loss market order
        if order_type is OrderType.StopLossLimit.value or OrderType.StopLossMarket.value:
            order['trigger_price'] = trigger_price

        # If placing sell CNC order
        if edis_txn_id is not None:
            order['edis_txn_id'] = edis_txn_id
            order['edis_auth_mode'] = edis_auth_mode

        # For Cover Order
        if product is ProductType.CoverOrder.value:
            helper = 'place_cover'
            del order['off_mkt_flag']
            if trigger_price is not None:
                order['trigger_price'] = trigger_price
            else:
                raise TypeError("Required parameter trigger_price is None")

        # For Bracket Order
        if product is ProductType.BracketOrder.value:
            helper = 'place_bracket'
            del order['off_mkt_flag']
            if stoploss_value is not None:
                order['stoploss_value'] = stoploss_value
            else:
                raise TypeError("Required parameter stoploss_value is None")
            if profit_value is not None:
                order['profit_value'] = profit_value
            else:
                raise TypeError("Required parameter profit_value is None")

        return self.api_call_helper(helper, Requests.POST, None, order)

    def modify_order(self, source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type,
                     price, mkt_type, order_no, serial_no, group_id, trigger_price=None, off_mkt_flag=False,
                     leg_no=None, algo_order_no=None, edis_txn_id=None, edis_auth_mode=None):
        self.validate_access_token()
        order = {
            'txn_type': txn_type,
            'exchange': exchange,
            'segment': segment,
            'product': product,
            'security_id': security_id,
            'quantity': quantity,
            'validity': validity,
            'order_type': order_type,
            'price': price,
            'mkt_type': mkt_type,
            'order_no': order_no,
            'serial_no': serial_no,
            'group_id': group_id,
            'source': source,
            'off_mkt_flag': off_mkt_flag
        }

        helper = 'modify_regular'

        if order_type is OrderType.StopLossLimit.value or OrderType.StopLossMarket.value:
            order['trigger_price'] = trigger_price

        # If modifying sell CNC order
        if edis_txn_id is not None:
            order['edis_txn_id'] = edis_txn_id
            order['edis_auth_mode'] = edis_auth_mode

        # For Cover Order
        if product is ProductType.CoverOrder.value:
            helper = 'modify_cover'
            if leg_no is not None:
                order['leg_no'] = leg_no
            else:
                raise TypeError("Required parameter leg_no is None")

        # For Bracket Order
        if product is ProductType.BracketOrder.value:
            helper = 'modify_bracket'
            if leg_no is not None:
                order['leg_no'] = leg_no
            else:
                raise TypeError("Required parameter leg_no is None")
            if algo_order_no is not None:
                order['algo_order_no'] = algo_order_no

            else:
                raise TypeError("Required parameter algo_order_no is None")

        return self.api_call_helper(helper, Requests.POST, None, order)

    def cancel_order(self, source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type,
                     price, mkt_type, order_no, serial_no, group_id, trigger_price=None, off_mkt_flag=False,
                     leg_no=None, algo_order_no=None):
        self.validate_access_token()
        order = {
            'txn_type': txn_type,
            'exchange': exchange,
            'segment': segment,
            'product': product,
            'security_id': security_id,
            'quantity': quantity,
            'validity': validity,
            'order_type': order_type,
            'price': price,
            'mkt_type': mkt_type,
            'order_no': order_no,
            'serial_no': serial_no,
            'source': source,
            'group_id': group_id,
            'off_mkt_flag': off_mkt_flag
        }
        helper = 'cancel_regular'

        if order_type is OrderType.StopLossLimit.value or OrderType.StopLossMarket.value:
            order['trigger_price'] = trigger_price

        # For Cover Order
        if product is ProductType.CoverOrder.value:
            helper = 'exit_cover'
            if leg_no is not None:
                order['leg_no'] = leg_no
            else:
                raise TypeError("Required parameter leg_no is None")

        # For Bracket Order
        if product is ProductType.BracketOrder.value:
            helper = 'exit_bracket'
            if leg_no is not None:
                order['leg_no'] = leg_no
            else:
                raise TypeError("Required parameter leg_no is None")
            if algo_order_no is not None:
                order['algo_order_no'] = algo_order_no
            else:
                raise TypeError("Required parameter algo_order_no is None")

        return self.api_call_helper(helper, Requests.POST, None, order)

    def convert_regular(self, source, txn_type, exchange, mkt_type, segment, product_from, product_to, quantity,
                        security_id, edis_auth_mode=None, edis_txn_id=None):
        self.validate_access_token()
        order = {
            'txn_type': txn_type,
            'exchange': exchange,
            'segment': segment,
            'security_id': security_id,
            'quantity': quantity,
            'mkt_type': mkt_type,
            'source': source,
            'product_from': product_from,
            'product_to': product_to,
        }

        # If converting sell CNC order
        if edis_txn_id is not None:
            order['edis_txn_id'] = edis_txn_id
            order['edis_auth_mode'] = edis_auth_mode

        return self.api_call_helper('convert_regular', Requests.POST, None, order)

    # Order & Trade Book
    def order_book(self):
        self.validate_access_token()
        return self.api_call_helper('order_book', Requests.GET, None, None)

    def trade_details(self, order_no, leg_no, segment):
        """
        order_no: order id of the order
        leg_no: leg no of the order
        segment: segment of the order
        All the can be retrieved from order book
        """
        self.validate_access_token()
        params = {'order_no': order_no, 'leg_no': leg_no, 'segment': segment}
        return self.api_call_helper('trade_details', Requests.GET, params, None)

    def position(self):
        self.validate_access_token()
        return self.api_call_helper('position', Requests.GET, None, None)

    def position_details(self, security_id, product, exchange):
        """
        Retrieve the details of a position
        security_id: security_id of the position
        product: product type of the position
        exchange: exchange of the position
        All the data can be retrieved from position
        """
        self.validate_access_token()
        params = {'security_id': security_id, 'product': product, 'exchange': exchange}
        return self.api_call_helper('position_details', Requests.GET, params, None)

    def funds_summary(self, config=False):
        """
        Fetch funds history
        config: set config to True for credit and debit details
        """
        self.validate_access_token()
        params = {'config': config}
        return self.api_call_helper('funds_summary', Requests.GET, params, None)

    def holdings_value(self):
        """Get value of the holdings"""
        self.validate_access_token()
        return self.api_call_helper('holdings_value', Requests.GET, None, None)

    def user_holdings_data(self):
        """Get holdings data of User"""
        self.validate_access_token()
        return self.api_call_helper('user_holdings_data', Requests.GET, None, None)

    # Margins
    def scrips_margin(self, source, margin_list=None, *args, **kwargs):
        """
        source: source from where the order is being placed check enums.py for detail
        margin_list: List of objects(dictionary) to calculate margin
        """
        self.validate_access_token()
        if margin_list is None:
            margin_list = []
        order = {
            'source': source,
            'margin_list': margin_list
        }
        return self.api_call_helper('scrips_margin', Requests.POST, None, order)

    def order_margin(self, source, exchange, segment, security_id, txn_type, quantity, price, product, trigger_price):
        params = {'source': source, 'exchange': exchange, 'segment': segment, 'security_id': security_id,
                  'txn_type': txn_type, 'quantity': quantity, 'price': price, 'product': product,
                  'trigger_price': trigger_price}
        self.validate_access_token()
        return self.api_call_helper('order_margin', Requests.GET, params, None)

    def security_master(self):
        """Details in a CSV file of all securities"""
        return self.api_call_helper('security_master', Requests.GET, None, None)

    def generate_tpin(self):
        """To generate TPIN to place sell CNC order"""
        self.validate_access_token()
        return self.api_call_helper('generate_tpin', Requests.GET, None, None)

    def validate_tpin(self, trade_type, isin_list=None, *args, **kwargs):
        """To validate the TPIN"""
        self.validate_access_token()
        if isin_list is None:
            isin_list = []
        request_body = {
            'trade_type': trade_type,
            'isin_list': isin_list
        }
        return self.api_call_helper('validate_tpin', Requests.POST, None, request_body)

    def status(self, edis_request_id):
        """Check the status of transaction"""
        self.validate_access_token()
        params = {'edis_request_id': edis_request_id}
        return self.api_call_helper('status', Requests.GET, params, None)
