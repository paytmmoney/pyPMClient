import logging

from pmClient.pmClient import PMClient

pm = PMClient(api_key="api_key", api_secret="api_secret")

pm.generate_session("your_request_token")

pm.set_access_token("your_access_token")

try:
    pm.order_book()
except Exception as e:
    logging.info("Error : {}".format(e))