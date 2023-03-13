"""
    WebSocketClient.py

    Client-side websocket implementation for getting live-streaming market data
"""
import json
import struct
import rel
import websocket
from .constants import Constants
from .epochConverterUtil import epoch_converter


class WebSocketClient(Constants):
    """This class handles websocket connection required for live-data streaming"""

    def __init__(self, public_access_token):
        """
        Initialize web_socket_url, callback methods, websocket object and create url using public_access_token

        :param public_access_token: is provided by user for authentication purpose
        """
        Constants.__init__(self)
        self.ws_url = None
        self.on_open_listener = None
        self.on_close_listener = None
        self.on_error_listener = None
        self.on_message_listener = None
        self.ws = None
        self.create_url(public_access_token)

    def create_url(self, public_access_token):
        """
        set websocket_url using given public_access_token

        :param public_access_token: is provided by user for authentication purpose
        """
        config = self._service_config
        url = f"{config['routes']['broadcast_websocket'][0]}"
        params = {
            'public_access_token': public_access_token
        }
        url = url.format(**params)
        self.ws_url = url

    def set_on_message_listener(self, listener):
        """
        set on_message callback method

        :param listener: is callback method for on_message event
        """
        self.on_message_listener = listener

    def set_on_open_listener(self, listener):
        """
        set on_open callback method

        :param listener: is callback method for on_open event
        """
        self.on_open_listener = listener

    def set_on_close_listener(self, listener):
        """
        set on_close callback method

        :param listener: is callback method for on_close event
        """
        self.on_close_listener = listener

    def set_on_error_listener(self, listener):
        """
        set on_error callback method

        :param listener: is callback method for on_error event
        """
        self.on_error_listener = listener

    def on_open(self, ws):
        """
        Called when WebSocket connection gets established

        :param ws: websocket object
        """
        if self.on_open_listener:
            self.on_open_listener()

    def on_message(self, ws, payload):
        """
        Called when text or binary message is received from server

        :param ws: websocket object
        :param payload: message received from server
        """
        if isinstance(payload, str):
            if self.on_error_listener:
                self.on_error_listener(payload)  # to handle error message sent by server in string format
        else:
            if self.on_message_listener:
                self.on_message_listener(self.parse_binary(payload))  # to handle ByteBuffer packets sent by server

    def on_close(self, ws, code, reason):
        """
        Called when connection is closed

        :param ws: websocket object
        :param code: close_status_code
        :param reason: close_message
        """
        if self.on_close_listener:
            self.on_close_listener(code, reason)

    def on_error(self, ws, err):
        """
        Called when error occurs in websocket connection

        :param ws: websocket object
        :param err: error message
        """
        if self.on_error_listener:
            self.on_error_listener(err)

    def connect(self):
        """Create a websocket connection with Broadcast server"""
        try:
            self.ws = websocket.WebSocketApp(self.ws_url,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close
                                             )
            # self.ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second
            # reconnect delay if connection closed unexpectedly
            self.ws.run_forever(dispatcher=rel)
            rel.signal(2, rel.abort)  # Keyboard Interrupt
            rel.dispatch()
        except Exception as err:
            if self.on_error_listener:
                self.on_error_listener(err)

    def subscribe(self, preferences):
        """
        Subscribes for list of preferences

        :param preferences: is list of preferences to be subscribed for
        """
        if self.ws:
            if self.ws.keep_running:
                self.ws.send(json.dumps(preferences))
            else:
                if self.on_error_listener:
                    self.on_error_listener("ticker is not connected")
        else:
            if self.on_error_listener:
                self.on_error_listener("ticker is null")

    def unpack(self, binary, start, end, byte_format="I"):
        """Unpack binary data as given data type format."""
        return struct.unpack("<" + byte_format, binary[start:end])[0]

    def parse_binary(self, buffer_packet):
        """
        This method parses binary data received from Broadcast server to get ticks for each preference subscribed

        :param buffer_packet: ByteBuffer packets received from Broadcast Server
        :return: List of parsed responses
        """
        buffer_length = len(buffer_packet)
        packet = bytearray(buffer_packet)
        response = []
        byte_buffer = packet.copy()
        position = 0

        while position != buffer_length:
            packet_type = byte_buffer[position]
            position += 1
            if packet_type == 64:
                self.process_index_ltp_packet(byte_buffer, response, position)
                position += 22
            elif packet_type == 65:
                self.process_index_quote_packet(byte_buffer, response, position)
                position += 42
            elif packet_type == 66:
                self.process_index_full_packet(byte_buffer, response, position)
                position += 38
            elif packet_type == 61:
                self.process_ltp_packet(byte_buffer, response, position)
                position += 22
            elif packet_type == 62:
                self.process_quote_packet(byte_buffer, response, position)
                position += 66
            elif packet_type == 63:
                self.process_full_packet(byte_buffer, response, position)
                position += 174

        return response

    def process_index_ltp_packet(self, byte_buffer, response, position):
        """
        parses index_ltp packets into readable format

        :param byte_buffer: ByteBuffer packet received from server
        :param response: Response Array in readable format
        :param position: current position of packet to be processed
        """
        response.append({
            "last_price": round(self.unpack(byte_buffer, position, position + 4, "f"), 2),
            "last_update_time": epoch_converter(self.unpack(byte_buffer, position + 4, position + 8)),
            "security_id": self.unpack(byte_buffer, position + 8, position + 12),
            "tradable": byte_buffer[position + 12],
            "mode": byte_buffer[position + 13],
            "change_absolute": round(self.unpack(byte_buffer, position + 14, position + 18, "f"), 2),
            "change_percent": round(self.unpack(byte_buffer, position + 18, position + 22, "f"), 2)
        })

    def process_ltp_packet(self, byte_buffer, response, position):
        """
        parses ltp packets into readable format

        :param byte_buffer: ByteBuffer packet received from server
        :param response: Response Array in readable format
        :param position: current position of packet to be processed
        """
        response.append({
            "last_price": round(self.unpack(byte_buffer, position, position + 4, "f"), 2),
            "last_trade_time": epoch_converter(self.unpack(byte_buffer, position + 4, position + 8)),
            "security_id": self.unpack(byte_buffer, position + 8, position + 12),
            "tradable": byte_buffer[position + 12],
            "mode": byte_buffer[position + 13],
            "change_absolute": round(self.unpack(byte_buffer, position + 14, position + 18, "f"), 2),
            "change_percent": round(self.unpack(byte_buffer, position + 18, position + 22, "f"), 2)
        })

    def process_quote_packet(self, byte_buffer, response, position):
        """
        parses quote packets into readable format

        :param byte_buffer: ByteBuffer packet received from server
        :param response: Response Array in readable format
        :param position: current position of packet to be processed
        """
        response.append({
            "last_price": round(self.unpack(byte_buffer, position, position + 4, "f"), 2),
            "last_trade_time": epoch_converter(self.unpack(byte_buffer, position + 4, position + 8)),
            "security_id": self.unpack(byte_buffer, position + 8, position + 12),
            "tradable": byte_buffer[position + 12],
            "mode": byte_buffer[position + 13],
            "last_traded_quantity": self.unpack(byte_buffer, position + 14, position + 18),
            "average_traded_price": round(self.unpack(byte_buffer, position + 18, position + 22, "f"), 2),
            "volume_traded": self.unpack(byte_buffer, position + 22, position + 26),
            "total_buy_quantity": self.unpack(byte_buffer, position + 26, position + 30),
            "total_sell_quantity": self.unpack(byte_buffer, position + 30, position + 34),
            "open": round(self.unpack(byte_buffer, position + 34, position + 38, "f"), 2),
            "close": round(self.unpack(byte_buffer, position + 38, position + 42, "f"), 2),
            "high": round(self.unpack(byte_buffer, position + 42, position + 46, "f"), 2),
            "low": round(self.unpack(byte_buffer, position + 46, position + 50, "f"), 2),
            "change_percent": round(self.unpack(byte_buffer, position + 50, position + 54, "f"), 2),
            "change_absolute": round(self.unpack(byte_buffer, position + 54, position + 58, "f"), 2),
            "fifty_two_week_high": round(self.unpack(byte_buffer, position + 58, position + 62, "f"), 2),
            "fifty_two_week_low": round(self.unpack(byte_buffer, position + 62, position + 66, "f"), 2)
        })

    def process_index_quote_packet(self, byte_buffer, response, position):
        """
        parses index_quote packets into readable format

        :param byte_buffer: ByteBuffer packet received from server
        :param response: Response Array in readable format
        :param position: current position of packet to be processed
        """
        response.append({
            "last_price": round(self.unpack(byte_buffer, position, position + 4, "f"), 2),
            "security_id": self.unpack(byte_buffer, position + 4, position + 8),
            "tradable": byte_buffer[position + 8],
            "mode": byte_buffer[position + 9],
            "open": round(self.unpack(byte_buffer, position + 10, position + 14, "f"), 2),
            "close": round(self.unpack(byte_buffer, position + 14, position + 18, "f"), 2),
            "high": round(self.unpack(byte_buffer, position + 18, position + 22, "f"), 2),
            "low": round(self.unpack(byte_buffer, position + 22, position + 26, "f"), 2),
            "change_percent": round(self.unpack(byte_buffer, position + 26, position + 30, "f"), 2),
            "change_absolute": round(self.unpack(byte_buffer, position + 30, position + 34, "f"), 2),
            "fifty_two_week_high": round(self.unpack(byte_buffer, position + 34, position + 38, "f"), 2),
            "fifty_two_week_low": round(self.unpack(byte_buffer, position + 38, position + 42, "f"), 2)
        })

    def process_full_packet(self, byte_buffer, response, position):
        """
        parses full packets into readable format

        :param byte_buffer: ByteBuffer packet received from server
        :param response: Response Array in readable format
        :param position: current position of packet to be processed
        """
        depth_size = 20
        depth_packet = {}
        for i in range(5):
            depth = "depth_packet_#" + str(i + 1)
            depth_obj = {
                "buy_quantity": self.unpack(byte_buffer, 1 + (i * depth_size), 5 + (i * depth_size)),
                "sell_quantity": self.unpack(byte_buffer, 5 + (i * depth_size), 9 + (i * depth_size)),
                "buy_order": self.unpack(byte_buffer, 9 + (i * depth_size), 11 + (i * depth_size), "h"),
                "sell_order": self.unpack(byte_buffer, 11 + (i * depth_size), 13 + (i * depth_size), "h"),
                "buy_price": round(self.unpack(byte_buffer, 13 + (i * depth_size), 17 + (i * depth_size), "f"), 2),
                "sell_price": round(self.unpack(byte_buffer, 17 + (i * depth_size), 21 + (i * depth_size), "f"), 2)
            }
            depth_packet[depth] = depth_obj

        tick = {"depth_packet": depth_packet}

        position += 100

        tick["last_price"] = round(self.unpack(byte_buffer, position, position + 4, "f"), 2)
        tick["last_trade_time"] = epoch_converter(self.unpack(byte_buffer, position + 4, position + 8))
        tick["security_id"] = self.unpack(byte_buffer, position + 8, position + 12)
        tick["tradable"] = byte_buffer[position + 12]
        tick["mode"] = byte_buffer[position + 13]
        tick["last_traded_quantity"] = self.unpack(byte_buffer, position + 14, position + 18)
        tick["average_traded_price"] = round(self.unpack(byte_buffer, position + 18, position + 22, "f"), 2)
        tick["volume_traded"] = self.unpack(byte_buffer, position + 22, position + 26)
        tick["total_buy_quantity"] = self.unpack(byte_buffer, position + 26, position + 30)
        tick["total_sell_quantity"] = self.unpack(byte_buffer, position + 30, position + 34)
        tick["open"] = round(self.unpack(byte_buffer, position + 34, position + 38, "f"), 2)
        tick["close"] = round(self.unpack(byte_buffer, position + 38, position + 42, "f"), 2)
        tick["high"] = round(self.unpack(byte_buffer, position + 42, position + 46, "f"), 2)
        tick["low"] = round(self.unpack(byte_buffer, position + 46, position + 50, "f"), 2)
        tick["change_percent"] = round(self.unpack(byte_buffer, position + 50, position + 54, "f"), 2)
        tick["change_absolute"] = round(self.unpack(byte_buffer, position + 54, position + 58, "f"), 2)
        tick["fifty_two_week_high"] = round(self.unpack(byte_buffer, position + 58, position + 62, "f"), 2)
        tick["fifty_two_week_low"] = round(self.unpack(byte_buffer, position + 62, position + 66, "f"), 2)
        tick["OI"] = self.unpack(byte_buffer, position + 66, position + 70)
        tick["OI_change"] = self.unpack(byte_buffer, position + 70, position + 74)

        response.append(tick)

    def process_index_full_packet(self, byte_buffer, response, position):
        """
        parses index_full packets into readable format

        :param byte_buffer: ByteBuffer packet received from server
        :param response: Response Array in readable format
        :param position: current position of packet to be processed
        """
        response.append({
            "last_price": round(self.unpack(byte_buffer, position, position + 4, "f"), 2),
            "security_id": self.unpack(byte_buffer, position + 4, position + 8),
            "tradable": byte_buffer[position + 8],
            "mode": byte_buffer[position + 9],
            "open": round(self.unpack(byte_buffer, position + 10, position + 14, "f"), 2),
            "close": round(self.unpack(byte_buffer, position + 14, position + 18, "f"), 2),
            "high": round(self.unpack(byte_buffer, position + 18, position + 22, "f"), 2),
            "low": round(self.unpack(byte_buffer, position + 22, position + 26, "f"), 2),
            "change_percent": round(self.unpack(byte_buffer, position + 26, position + 30, "f"), 2),
            "change_absolute": round(self.unpack(byte_buffer, position + 30, position + 34, "f"), 2),
            "last_update_time": epoch_converter(self.unpack(byte_buffer, position + 34, position + 38))
        })
