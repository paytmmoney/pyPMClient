import pytest


def test_set_access_token(pm_api):
    # pm_api.set_access_token("access_token")
    assert pm_api.set_access_token("access_token") == "access_token"


def test_login(pm_api):
    assert pm_api.login() == "https://login-stg.paytmmoney.com/merchant-login?returnUrl=https://www.google.com/&apiKey=<API-KEY>"


def test_generate_session(pm_api):
    with pytest.raises(TypeError):
        pm_api.generate_session(None)


def test_generate_session_connection(pm_api):
    with pytest.raises(ConnectionError):
        pm_api.generate_session("request_token")


def test_logout(pm_api):
    with pytest.raises(ConnectionError):
        pm_api.logout("request_token")


def test_place_order_attribute(pm_api):
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.place_order(
            source="W",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="",
            security_id="772",
            quantity=1,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False
        )


def test_place_order_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.place_order(
            source="W",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="I",
            security_id="772",
            quantity=1,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False
        )


def test_place_order_connection_edis(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.place_order(
            source="W",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="I",
            security_id="772",
            quantity=1,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            edis_txn_id=1012,
            edis_auth_mode="TPIN"
        )


def test_place_order_connection_cover(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.place_order(
            source="W",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="V",
            security_id="772",
            quantity=1,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            trigger_price=90.0
        )


def test_place_order_connection_cover_type(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.place_order(
            source="W",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="V",
            security_id="772",
            quantity=1,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            trigger_price=None
        )


def test_place_order_connection_bracket(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.place_order(
            source="W",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=1,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            stoploss_value=4,
            profit_value=2
        )


def test_place_order_connection_bracket_type1(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.place_order(
            source="W",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=1,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            stoploss_value=None,
            profit_value=2
        )


def test_place_order_connection_bracket_type2(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.place_order(
            source="W",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=1,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            stoploss_value=2,
            profit_value=None
        )


def test_modify_order_attribute(pm_api):
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.modify_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=1,
            group_id=8
        )


def test_modify_order_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.modify_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="I",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=1,
            group_id=8
        )


def test_modify_order_connection_edis(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.modify_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="I",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=1,
            group_id=8,
            edis_txn_id=1012,
            edis_auth_mode="TPIN"
        )


def test_modify_order_connection_cover(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.modify_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="V",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=1,
            group_id=8,
            leg_no="2"
        )


def test_modify_order_connection_cover_type(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.modify_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="V",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=1,
            group_id=8,
            leg_no=None
        )


def test_modify_order_connection_bracket(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.modify_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=1,
            group_id=8,
            leg_no="2",
            algo_order_no="1"
        )


def test_modify_order_connection_bracket_type1(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.modify_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=1,
            group_id=8,
            leg_no=None,
            algo_order_no="1"
        )


def test_modify_order_connection_bracket_type2(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.modify_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=1,
            group_id=8,
            leg_no="2",
            algo_order_no=None
        )


def test_cancel_order_attribute(pm_api):
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.cancel_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="",
            security_id="",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=2,
            group_id=8
        )


def test_cancel_order_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.cancel_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="I",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=2,
            group_id=8
        )


def test_cancel_order_connection_cover(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.cancel_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="V",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=2,
            group_id=8,
            leg_no="2"
        )


def test_cancel_order_connection_cover_type(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.cancel_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="I",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=2,
            group_id=8,
            leg_no=None
        )


def test_cancel_order_connection_bracket(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.cancel_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=2,
            group_id=8,
            leg_no="2",
            algo_order_no="5"
        )


def test_cancel_order_connection_bracket1(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.cancel_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=2,
            group_id=8,
            leg_no="2",
            algo_order_no=None
        )


def test_cancel_order_connection_bracket2(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(TypeError):
        pm_api.cancel_order(
            source="N",
            txn_type="B",
            exchange="NSE",
            segment="E",
            product="B",
            security_id="772",
            quantity=2,
            validity="DAY",
            order_type="LMT",
            price=620.0,
            off_mkt_flag=False,
            mkt_type="NL",
            order_no="order_no",
            serial_no=2,
            group_id=8,
            leg_no=None,
            algo_order_no="5"
        )


def test_convert_order_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.convert_regular(
            source="M",
            txn_type="S",
            exchange="NSE",
            segment="E",
            product_from="C",
            product_to="I",
            security_id="2885",
            quantity=100,
            mkt_type="NL"
        )


def test_order_book_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.order_book()


def test_trade_details_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.trade_details(order_no="order_no", leg_no="1", segment="E")


def test_position_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.position()


def test_position_details_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.position_details(security_id="772", product="I", exchange="NSE")


def test_funds_summary_attribute(pm_api):
    # If no funds could be fetched, this exception will be raised.
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.funds_summary(config=True)


def test_funds_summary_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.funds_summary(config=True)


def test_holdings_value_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.holdings_value()


def test_user_holdings_data_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.user_holdings_data()


def test_scrips_margin_connection(pm_api):
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.scrips_margin(
            source="W",
            margin_list=[
                {
                    "exchange": "NSE",
                    "segment": "",
                    "security_id": "46840",
                    "txn_type": "B",
                    "quantity": "250",
                    "strike_price": "0",
                    "trigger_price": "0",
                    "instrument": "FUTSTK"
                },
                {
                    "exchange": "NSE",
                    "segment": "D",
                    "security_id": "46834",
                    "txn_type": "B",
                    "quantity": "250",
                    "strike_price": "0",
                    "trigger_price": "0",
                    "instrument": "FUTSTK"
                },
                {
                    "exchange": "NSE",
                    "segment": "E",
                    "security_id": "27466",
                    "txn_type": "B",
                    "quantity": "25",
                    "strike_price": "0",
                    "trigger_price": "0",
                    "instrument": "EQUITY"
                }
            ])


def test_scrips_margin_attribute(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.scrips_margin(
            source="W",
            margin_list=[
                {
                    "exchange": "NSE",
                    "segment": "D",
                    "security_id": "46840",
                    "txn_type": "B",
                    "quantity": "250",
                    "strike_price": "0",
                    "trigger_price": "0",
                    "instrument": "FUTSTK"
                },
                {
                    "exchange": "NSE",
                    "segment": "D",
                    "security_id": "46834",
                    "txn_type": "B",
                    "quantity": "250",
                    "strike_price": "0",
                    "trigger_price": "0",
                    "instrument": "FUTSTK"
                },
                {
                    "exchange": "NSE",
                    "segment": "E",
                    "security_id": "27466",
                    "txn_type": "B",
                    "quantity": "25",
                    "strike_price": "0",
                    "trigger_price": "0",
                    "instrument": "EQUITY"
                }
            ])


def test_order_margin_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.order_margin(
            source="W",
            exchange="NSE",
            segment="E",
            security_id="772",
            txn_type="B",
            quantity=100,
            price=0.0,
            product="1",
            trigger_price=0.0
        )


def test_security_master_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.security_master(scrip_type="etf", exchange="NSE")


def test_generate_tpin_attribute(pm_api):
    # If user details could not be fetched, this exception will be thrown.
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.generate_tpin()


def test_generate_tpin_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.generate_tpin()


def test_validate_tpin_attribute(pm_api):
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.validate_tpin(
            trade_type="trade_type",
            isin_list=[]
        )


def test_validate_tpin_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.validate_tpin(
            trade_type="trade_type",
            isin_list=[]
        )


def test_status_attribute(pm_api):
    # Invalid edis_request_id or null may cause this exception.
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.status(edis_request_id="req_id")


def test_status_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.status(edis_request_id="req_id")


def test_get_user_details_attribute(pm_api):
    # If KYC is not done user details cannot be fetched and following exception will be thrown.
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.get_user_details()


def test_get_user_details_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.get_user_details()


def test_price_chart_sym_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.price_chart_sym(
            cont="false",
            exchange="NSE",
            expiry="2022-04-26",
            fromDate="2022-02-10",
            instType="FUTIDX",
            interval="MINUTE",
            symbol="MIDCPNIFTY",
            toDate="2022-02-05"
        )


def test_price_chart_sym_attribute(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(AttributeError):
        pm_api.price_chart_sym(
            cont="false",
            exchange="NSE",
            expiry="2022-04-26",
            fromDate="2022-02-10",
            instType="FUTIDX",
            interval="MINUTE",
            symbol="",
            toDate="2022-02-05"
        )


def test_create_gtt_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.create_gtt(
            segment="E",
            exchange="NSE",
            pml_id="1000001488",
            security_id="14366",
            product_type="C",
            set_price=12.80,
            transaction_type="S",
            quantity=1,
            trigger_price=12.7,
            limit_price=0,
            order_type="MKT",
            trigger_type="SINGLE"
        )


def test_create_gtt_attribute(pm_api):
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.create_gtt(
            segment="E",
            exchange=9.0,
            pml_id="1000001488",
            security_id="14366",
            product_type="C",
            set_price=12.80,
            transaction_type="S",
            quantity=1,
            trigger_price=12.7,
            limit_price=0,
            order_type="MKT",
            trigger_type="SINGLE"
        )


def test_get_gtt_by_status_or_id_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.get_gtt_by_pml_id_and_status(
            status="ACTIVE",
            pml_id="1000001488"
        )


def test_update_gtt_connection(pm_api):
    pm_api.access_token = "valid_token"
    with pytest.raises(ConnectionError):
        pm_api.update_gtt(
            set_price=12.80,
            transaction_type="S",
            quantity=3,
            trigger_price=12.7,
            limit_price=0,
            order_type="MKT",
            trigger_type="SINGLE"
        )


def test_update_gtt_attribute(pm_api):
    pm_api.access_token = "valid_token"
    with pytest.raises(AttributeError):
        pm_api.update_gtt(
            set_price=12.80,
            transaction_type=5,
            quantity=3,
            trigger_price=12.7,
            limit_price=0,
            order_type="MKT",
            trigger_type="SINGLE"
        )


def test_get_gtt_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.get_gtt(
            id=4563,
        )


def test_delete_gtt_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.delete_gtt(
            id=4563,
        )


def test_get_gtt__aggregate_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.get_gtt_aggregate()


def test_get_gtt_expiry_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.get_gtt_expiry_date(
            pml_id="1000001488",
        )


def test_get_gtt_by_instruction_id_connection(pm_api):
    pm_api.access_token = "invalid_token"
    with pytest.raises(ConnectionError):
        pm_api.get_gtt_by_instruction_id(
            id="4563",
        )

