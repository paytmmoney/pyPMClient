class Constants:
    def __init__(self):
        self._service_config = {
            'host': 'https://developer.paytmmoney.com',
            'login_param': '&state=',
            'routes': {
                # login endpoints
                'login': 'https://login.paytmmoney.com/merchant-login?apiKey=',
                'logout': '/accounts/v1/logout',
                'user_details': '/accounts/v1/user/details',
                'access_token': '/accounts/v1/gettoken?apiKey={apiKey}&requestToken={requestToken}',

                # regular order endpoints
                'place_regular': '/orders/v1/place/regular',
                'modify_regular': '/orders/v1/modify/regular',
                'cancel_regular': '/orders/v1/cancel/regular',
                'convert_regular': '/orders/v1/convert/regular',

                # cover order endpoints
                'place_cover': '/orders/v1/place/cover',
                'modify_cover': '/orders/v1/modify/cover',
                'exit_cover': '/orders/v1/exit/cover',

                # bracket order endpoints
                'place_bracket': '/orders/v1/place/bracket',
                'modify_bracket': '/orders/v1/modify/bracket',
                'exit_bracket': '/orders/v1/exit/bracket',

                # orderBook, tradeBook & other details endpoints
                'order_book': '/orders/v1/order-book',
                'trade_details': '/orders/v1/trade-details?order_no={order_no}&leg_no={leg_no}&segment={segment}',
                'position': '/orders/v1/position',
                'position_details': '/orders/v1/position-details?security_id={security_id}&product={product}&exchange'
                                    '={exchange}',
                'funds_summary': '/accounts/v1/funds/summary?config={config}',
                'holdings_value': '/holdings/v1/get-holdings-value',
                'user_holdings_data': '/holdings/v1/get-user-holdings-data',
                'security_master': '/data/v1/security-master',

                # margin endpoints
                'scrips_margin': '/margin/v1/scrips/calculator',
                'order_margin': '/margin/v1/order/calculator?source={source}&exchange={exchange}&segment={'
                                'segment}&security_id={security_id}&txn_type={txn_type}&quantity={quantity}&price={'
                                'price}&product={product}&trigger_price={trigger_price}',

                # edis endpoints
                'generate_tpin': '/edis/v1/generate/tpin',
                'validate_tpin': '/edis/v1/validate/tpin',
                'status': '/edis/v1/status?edis_request_id={edis_request_id}'
            }
        }
