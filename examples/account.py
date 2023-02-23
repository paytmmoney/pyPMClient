import logging
import sys
sys.path.append('../')
from pmClient import PMClient

pm = PMClient(api_key="api_key", api_secret="api_secret")
pm.generate_session("request_token")

pm.set_access_token("your_access_token")
pm.set_public_access_token("your_public_access_token")
pm.set_read_access_token("your_read_access_token")

try:
    pm.get_user_details()
except Exception as e:
    logging.error("Error : {}".format(e))