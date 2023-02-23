import logging
import sys
sys.path.append('../')
from pmClient import PMClient

pm = PMClient(api_key="api_key", api_secret="api_secret")

pm.generate_session("your_request_token")

pm.set_access_token("your_access_token")
pm.set_public_access_token("your_public_access_token")
pm.set_read_access_token("your_read_access_token")
try:
    res = pm.place_order(
        txn_type="S",
        exchange="NSE",
        segment="E",
        product="I",
        security_id="772",
        quantity=10,
        validity="DAY",
        order_type="SLM",
        price=0,
        source="N",
        off_mkt_flag=False,
        trigger_price=610
    )
    logging.info("Response : {}".format(res))
except Exception as e:
    logging.info("Error : {}".format(e))
