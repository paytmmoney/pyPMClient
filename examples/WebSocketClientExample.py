from pmClient.WebSocketClient import WebSocketClient

webSocketClient = WebSocketClient("your_public_access_token")

customerPreferences = []

preference = {
    "actionType": 'ADD',  # 'ADD', 'REMOVE'
    "modeType": 'LTP',  # 'LTP', 'FULL', 'QUOTE'
    "scripType": 'INDEX',  # 'ETF', 'FUTURE', 'INDEX', 'OPTION', 'EQUITY'
    "exchangeType": 'NSE',  # 'BSE', 'NSE'
    "scripId": '13'
}

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
