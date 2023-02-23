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
    tpin = pm.generate_tpin()
    logging.info("TPIN : {}".format(tpin))
    # TPIN sent on mobile number. Wait for 6 minutes.

    validate = pm.validate_tpin(
        trade_type="PRE-TRADE",
        isin_list=[
            {
                "isin": "isin",
                "qty": 2
            },
            {
                "isin": "isin",
                "qty": 3
            }
        ]
    )
    logging.info("Validation : {}".format(validate))
    # In response, we get the edis_request_id

    auth = pm.status("edis_request_id")
    logging.info("Message : {}".format(auth))

except Exception as e:
    logging.info("Error : {}".format(e))
