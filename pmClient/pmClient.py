import json
from pdb import pm
from typing import List
from .apiService import ApiService
from .constants import Constants
from .enums import OrderType, Requests, ProductType
from .epochConverterUtil import epoch_converter


class PMClient(ApiService, Constants):

    def __init__(self, api_secret, api_key, access_token=None, public_access_token=None, read_access_token=None):
        if api_key is not None:
            self._api_key = api_key
        else:
            raise TypeError("Api Key cannot be null or empty")
        if api_secret is not None:
            self.api_secret = api_secret
        else:
            raise TypeError("Api Secret cannot be null or empty")
        self.access_token = access_token
        self.public_access_token = public_access_token
        self.read_access_token = read_access_token
        ApiService.__init__(self)
        Constants.__init__(self)

    def set_access_token(self, access_token):
        """Set and initialize access token"""
        self.access_token = access_token
        ApiService.__init__(self)
        Constants.__init__(self)
        return self.access_token

    def set_public_access_token(self, public_access_token):
        """Set and initialize public access token"""
        self.public_access_token = public_access_token
        ApiService.__init__(self)
        Constants.__init__(self)
        return self.public_access_token

    def set_read_access_token(self, read_access_token):
        """Set and initialize read access token"""
        self.read_access_token = read_access_token
        ApiService.__init__(self)
        Constants.__init__(self)
        return self.read_access_token

    def login(self, state_key):
        """Login URL to get the request token"""
        config = self._service_config
        if state_key is not None:
            return "%s%s%s%s" % (config['routes']['login'], self._api_key, config['login_param'], state_key)
        else:
            raise TypeError("State Key cannot be null or empty")

    def generate_session(self, request_token=None):
        """Generate session and get the tokens"""
        if request_token is not None:
            request_body = {'api_key': self._api_key, 'api_secret_key': self.api_secret, 'request_token': request_token}
        else:
            raise TypeError("Request Token cannot be null or empty")
        response = ApiService.api_call_helper(self, "access_token", Requests.POST, None, request_body)
        if "access_token" in response:
            self.set_access_token(response["access_token"])
        if "public_access_token" in response:
            self.set_public_access_token(response["public_access_token"])
        if "read_access_token" in response:
            self.set_read_access_token(response["read_access_token"])
        return response

    # Fetch User Details
    def get_user_details(self):
        return ApiService.api_call_helper(self, 'user_details', Requests.GET, None, None)

    # Logout the session
    def logout(self):
        response = ApiService.api_call_helper(self, 'logout', Requests.DELETE, None, None)
        self.set_access_token(None)
        self.set_public_access_token(None)
        self.set_read_access_token(None)
        return response

    # Orders
    def place_order(self, txn_type, exchange, segment, product, security_id, quantity, validity, order_type, price,
                    source, off_mkt_flag=False, trigger_price=None, profit_value=None, stoploss_value=None):
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
        if order_type is OrderType.StopLossLimit.value or order_type is OrderType.StopLossMarket.value:
            order['trigger_price'] = trigger_price

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

        return ApiService.api_call_helper(self, helper, Requests.POST, None, order)

    def modify_order(self, source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type,
                     price, mkt_type, order_no, serial_no, group_id, trigger_price=None, off_mkt_flag=False,
                     leg_no=None, algo_order_no=None):
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

        if order_type is OrderType.StopLossLimit.value or order_type is OrderType.StopLossMarket.value:
            order['trigger_price'] = trigger_price

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

        return ApiService.api_call_helper(self, helper, Requests.POST, None, order)

    def cancel_order(self, source, txn_type, exchange, segment, product, security_id, quantity, validity, order_type,
                     price, mkt_type, order_no, serial_no, group_id, trigger_price=None, off_mkt_flag=False,
                     leg_no=None, algo_order_no=None):
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

        if order_type is OrderType.StopLossLimit.value or order_type is OrderType.StopLossMarket.value:
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

        return ApiService.api_call_helper(self, helper, Requests.POST, None, order)

    def convert_regular(self, source, txn_type, exchange, mkt_type, segment, product_from, product_to, quantity,
                        security_id):
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

        return ApiService.api_call_helper(self, 'convert_regular', Requests.POST, None, order)

    # Order & Trade Book
    def order_book(self):
        return ApiService.api_call_helper(self, 'order_book', Requests.GET, None, None)
    
    def orders(self):
        return ApiService.api_call_helper(self, 'orders', Requests.GET, None, None)

    def trade_details(self, order_no, leg_no, segment):
        """
        order_no: order id of the order
        leg_no: leg no of the order
        segment: segment of the order
        All the can be retrieved from order book
        """
        params = {'order_no': order_no, 'leg_no': leg_no, 'segment': segment}
        return ApiService.api_call_helper(self, 'trade_details', Requests.GET, params, None)

    def position(self):
        return ApiService.api_call_helper(self, 'position', Requests.GET, None, None)

    def position_details(self, security_id, product, exchange):
        """
        Retrieve the details of a position
        security_id: security_id of the position
        product: product type of the position
        exchange: exchange of the position
        All the data can be retrieved from position
        """
        params = {'security_id': security_id, 'product': product, 'exchange': exchange}
        return ApiService.api_call_helper(self, 'position_details', Requests.GET, params, None)

    def funds_summary(self, config=False):
        """
        Fetch funds history
        config: set config to True for credit and debit details
        """
        params = {'config': config}
        return ApiService.api_call_helper(self, 'funds_summary', Requests.GET, params, None)

    def holdings_value(self):
        """Get value of the holdings"""
        return ApiService.api_call_helper(self, 'holdings_value', Requests.GET, None, None)

    def user_holdings_data(self):
        """Get holdings data of User"""
        return ApiService.api_call_helper(self, 'user_holdings_data', Requests.GET, None, None)

    # Margins
    def scrips_margin(self, source, margin_list=None, *args, **kwargs):
        """
        source: source from where the order is being placed check enums.py for detail
        margin_list: List of objects(dictionary) to calculate margin
        """
        if margin_list is None:
            margin_list = []
        order = {
            'source': source,
            'margin_list': margin_list
        }
        return ApiService.api_call_helper(self, 'scrips_margin', Requests.POST, None, order)

    def order_margin(self, source, exchange, segment, security_id, txn_type, quantity, price, product, trigger_price):
        params = {'source': source, 'exchange': exchange, 'segment': segment, 'security_id': security_id,
                  'txn_type': txn_type, 'quantity': quantity, 'price': price, 'product': product,
                  'trigger_price': trigger_price}
        return ApiService.api_call_helper(self, 'order_margin', Requests.GET, params, None)

    def security_master(self, file_name):
        """
        Details in a file of all securities
        file_name: File name of the csv file   
        """
        if not file_name:
            raise AttributeError("File name should not be null or empty")
        params = {
            'file_name': file_name,
        }
        return ApiService.api_call_helper(self, 'security_master', Requests.GET, params, None)

    def generate_tpin(self):
        """To generate TPIN to place sell CNC order"""
        return ApiService.api_call_helper(self, 'generate_tpin', Requests.GET, None, None)

    def validate_tpin(self, trade_type, isin_list=None, *args, **kwargs):
        """To validate the TPIN"""
        if isin_list is None:
            isin_list = []
        request_body = {
            'trade_type': trade_type,
            'isin_list': isin_list
        }
        return ApiService.api_call_helper(self, 'validate_tpin', Requests.POST, None, request_body)

    def status(self, edis_request_id):
        """Check the status of transaction"""
        params = {'edis_request_id': edis_request_id}
        return ApiService.api_call_helper(self, 'status', Requests.GET, params, None)

    # def price_chart_sym(self, cont, exchange, expiry, from_date, inst_type, interval, symbol, to_date, month_id=None,
    #                     series=None, strike=None):
    #     """Get the historical data of the chart"""
    #     request_body = {
    #         'cont': cont,
    #         'exchange': exchange,
    #         'expiry': expiry,
    #         'fromDate': from_date,
    #         'instType': inst_type,
    #         'interval': interval,
    #         'monthId': month_id,
    #         'series': series,
    #         'strike': strike,
    #         'symbol': symbol,
    #         'toDate': to_date
    #     }
    #     return ApiService.api_call_helper(self, 'price_chart_sym', Requests.POST, None, request_body)

    def get_gtt_by_pml_id_and_status(self, status=None, pml_id=None):
        """Get all gtt for the account or filter by status and pml_id"""
        if status is not None and status != "" and pml_id is not None and pml_id != "":
            params = {
                'status': status,
                'pml_id': pml_id
            }
            return ApiService.api_call_helper(self, 'get_gtt_by_pml_id_and_status', Requests.GET, params, None)
        elif (status is not None and status != "") and (pml_id is None or pml_id == ""):
            params = {
                'status': status,
            }
            return ApiService.api_call_helper(self, 'get_gtt_by_status', Requests.GET, params, None)
        elif (status is None or status == "") and (pml_id is not None and pml_id != ""):
            params = {
                'pml_id': pml_id,
            }
            return ApiService.api_call_helper(self, 'get_gtt_by_pml_id', Requests.GET, params, None)
        else:
            return ApiService.api_call_helper(self, 'gtt', Requests.GET, None, None)

    def create_gtt(self, segment, exchange, pml_id, security_id, product_type, set_price, transaction_type,
                   order_type, trigger_type, quantity, trigger_price, limit_price):
        """Create a GTT Order"""
        transaction_details = []

        transaction_details_obj = {
            'quantity': quantity,
            'trigger_price': trigger_price,
            'limit_price': limit_price
        }
        transaction_details.append(transaction_details_obj)

        request_body = {
            'segment': segment,
            'exchange': exchange,
            'pml-id': pml_id,
            'security_id': security_id,
            'product_type': product_type,
            'set_price': set_price,
            'transaction_type': transaction_type,
            'order_type': order_type,
            'trigger_type': trigger_type,
            'transaction_details': transaction_details
        }

        return ApiService.api_call_helper(self, 'gtt', Requests.POST, None, request_body)

    def get_gtt(self, id):
        """Get GTT order by id"""
        params = {
            'id': id
        }
        return ApiService.api_call_helper(self, 'gtt_by_id', Requests.GET, params, None)

    def update_gtt(self, id, quantity=None, trigger_price=None, limit_price=None, set_price=None, transaction_type=None, order_type=None,
                   trigger_type=None):
        """Update GTT order"""
        params = {
            'id': id
        }

        transaction_details = []

        transaction_details_obj = {
            'quantity': quantity,
            'trigger_price': trigger_price,
            'limit_price': limit_price
        }
        transaction_details.append(transaction_details_obj)

        request_body = {
            'set_price': set_price,
            'transaction_type': transaction_type,
            'order_type': order_type,
            'trigger_type': trigger_type,
            'transaction_details': transaction_details
        }
        return ApiService.api_call_helper(self, 'gtt_by_id', Requests.PUT, params, request_body)

    def delete_gtt(self, id):
        """Delete GTT order"""
        params = {
            'id': id
        }
        return ApiService.api_call_helper(self, 'gtt_by_id', Requests.DELETE, params, None)

    def get_gtt_aggregate(self):
        """Get GTT orders aggregate"""
        return ApiService.api_call_helper(self, 'gtt_aggregate', Requests.GET, None, None)

    def get_gtt_expiry_date(self, pml_id):
        """Get GTT order expiry date by pml_id"""
        params = {
            'pml_id': pml_id
        }
        return ApiService.api_call_helper(self, 'expiry_gtt', Requests.GET, params, None)

    def get_gtt_by_instruction_id(self, id):
        """Get GTT order by Instruction Id"""
        params = {
            'id': id
        }
        return ApiService.api_call_helper(self, 'gtt_by_instruction_id', Requests.GET, params, None)
    
    def get_gtt_by_pml_id_and_status_v2(self, status=None, pml_id=None):
        """Get all gtt for the account or filter by status and pml_id"""
        if status is not None and status != "" and pml_id is not None and pml_id != "":
            params = {
                'status': status,
                'pml_id': pml_id
            }
            return ApiService.api_call_helper(self, 'get_gtt_by_pml_id_and_status_v2', Requests.GET, params, None)
        elif (status is not None and status != "") and (pml_id is None or pml_id == ""):
            params = {
                'status': status,
            }
            return ApiService.api_call_helper(self, 'get_gtt_by_status_v2', Requests.GET, params, None)
        elif (status is None or status == "") and (pml_id is not None and pml_id != ""):
            params = {
                'pml_id': pml_id,
            }
            return ApiService.api_call_helper(self, 'get_gtt_by_pml_id_v2', Requests.GET, params, None)
        else:
            return ApiService.api_call_helper(self, 'gtt_v2', Requests.GET, None, None)
    
    def create_gtt_v2(self, segment, exchange, security_id, product_type, set_price, transaction_type,
                   trigger_type, transaction_details):
        """Create a GTT Order"""
        
        request_body = {
            'segment': segment,
            'exchange': exchange,
            'security_id': security_id,
            'product_type': product_type,
            'set_price': set_price,
            'transaction_type': transaction_type,
            'trigger_type': trigger_type,
            'transaction_details': transaction_details
        }

        return ApiService.api_call_helper(self, 'gtt_v2', Requests.POST, None, request_body)
    
    def get_gtt_v2(self, id):
        """Get GTT order by id"""
        params = {
            'id': id
        }
        return ApiService.api_call_helper(self, 'gtt_by_id_v2', Requests.GET, params, None)
    
    def update_gtt_v2(self, id, set_price=None, transaction_type=None, trigger_type=None, transaction_details=None):
        """Update GTT order"""
        params = {
            'id': id
        }

        request_body = {
            'set_price': set_price,
            'transaction_type': transaction_type,
            'trigger_type': trigger_type,
            'transaction_details': transaction_details
        }
        return ApiService.api_call_helper(self, 'gtt_by_id_v2', Requests.PUT, params, request_body)

    def get_gtt_by_instruction_id_v2(self, id):
        """Get GTT order by Instruction Id"""
        params = {
            'id': id
        }
        return ApiService.api_call_helper(self, 'gtt_by_instruction_id_v2', Requests.GET, params, None)

    def get_live_market_data(self, mode_type, preferences: List[str]):
        """
        Live Market data 
        mode_type: mode of preference
        prefrences: list of pref, example format -> preferences=["exchange:scrip_id:scrip_type","exchange:scrip_id:scrip_type"]
        """
        params = {
            'mode_type': mode_type,
            'preferences': ','.join(preferences)
        }
        response = ApiService.api_call_helper(self, 'live_market_data', Requests.GET, params, None)

        if response.get("data") is not None:
            for tick in response["data"]:
                if tick.get("last_trade_time") is not None:
                    tick["last_trade_time"] = epoch_converter(tick["last_trade_time"])
                if tick.get("last_update_time") is not None:
                    tick["last_update_time"] = epoch_converter(tick["last_update_time"])

        return response

    def get_option_chain(self, type, symbol, expiry):
        """
        Option Chain
        type: type of option chain
        symbol: symbol of option chain
        expiry: expiry in DD-MM-YYYY format
        """
        params = {
            'type': type,
            'symbol': symbol,
            'expiry': expiry
        }
        return ApiService.api_call_helper(self, 'option_chain', Requests.GET, params, None)

    def get_option_chain_config(self, symbol):
        """
        Option Chain config 
        symbol: symbol of option chain
        """
        params = {
            'symbol': symbol
        }
        return ApiService.api_call_helper(self, 'option_chain_config', Requests.GET, params, None)

    def charges_info(self, brokerage_profile_code,transaction_type,product_type,instrument_type,exchange,qty,price):
        """
        Brokrage Charges Info 
        brokerage_profile_code: Customer subscription plan ("D00-I10-F10" / "D15-I15-F15")
        transaction_type: Transaction Type 	"B" | "S" (Buy/Sell)
        product_type: "FUTIDX" | "FUTSTK" | "OPTSTK" | "OPTIDX" | "ES" | "ETF" | "REIT" | "InvITU" | "CB" | "DEB" | "DBT"  | "GB"
        instrument_type:  "I" | "B" | "V" | "C" | "M" 
        exchange: "NSE" | "BSE"
        qty: Quantity of stocks to be traded
        price: Price at which order is to be placed
        """

        request_body = {
            "brokerage_profile_code": brokerage_profile_code,
            "transaction_type": transaction_type, 
            "product_type": product_type,
            "instrument_type": instrument_type,
            "exchange": exchange,
            "qty": qty,
            "price": price
        }

        return ApiService.api_call_helper(self, 'charges_info', Requests.POST, None, request_body)
