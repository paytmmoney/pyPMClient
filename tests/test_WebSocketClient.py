import struct
import pytest


def on_open():
    print("on_open_triggered")


def on_close(code, reason):
    print("on_close_triggered")


def on_error(err):
    print("on_error_triggered")


def on_message(arr):
    print("on_message_triggered")


@pytest.fixture()
def setup(web_socket_client):
    web_socket_client.set_on_open_listener(on_open)
    web_socket_client.set_on_close_listener(on_close)
    web_socket_client.set_on_message_listener(on_message)
    web_socket_client.set_on_error_listener(on_error)


def test_create_url(web_socket_client):
    web_socket_client.create_url("access_token")


def test_set_on_message_listener(web_socket_client):
    web_socket_client.set_on_message_listener(None)


def test_set_on_open_listener(web_socket_client):
    web_socket_client.set_on_open_listener(None)


def test_set_on_close_listener(web_socket_client):
    web_socket_client.set_on_close_listener(None)


def test_set_on_error_listener(web_socket_client):
    web_socket_client.set_on_error_listener(None)


def test_on_open(web_socket_client, setup):
    web_socket_client.on_open(None)


def test_on_open_null_callback(web_socket_client):
    web_socket_client.on_open(None)


def test_on_close(web_socket_client, setup):
    web_socket_client.on_close(None, None, None)


def test_on_close_null_callback(web_socket_client):
    web_socket_client.on_close(None, None, None)


def test_on_message_string(web_socket_client, setup):
    web_socket_client.on_message(None, "string")


def test_on_message_string_null_callback(web_socket_client):
    web_socket_client.on_message(None, "string")


def test_on_message_binary(web_socket_client, setup):
    buffer = bytearray(1)
    buffer[0] = 1
    web_socket_client.on_message(None, buffer)


def test_on_message_binary_null_callback(web_socket_client):
    buffer = bytearray(1)
    buffer[0] = 1
    web_socket_client.on_message(None, buffer)


def test_on_error(web_socket_client, setup):
    web_socket_client.on_error(None, None)


def test_on_error_null_callback(web_socket_client):
    web_socket_client.on_error(None, None)


def test_subscribe(web_socket_client, setup):
    web_socket_client.subscribe(["pref"])


def test_subscribe_null_callback(web_socket_client):
    web_socket_client.subscribe(["pref"])


def test_process_index_ltp_packet(web_socket_client):
    byte_buffer = bytearray(23)
    byte_buffer[0] = 64
    struct.pack_into('<f', byte_buffer, 1, 100)
    struct.pack_into('<i', byte_buffer, 5, 100)
    struct.pack_into('<i', byte_buffer, 9, 100)
    byte_buffer[13] = 1
    byte_buffer[14] = 1
    struct.pack_into('<f', byte_buffer, 15, 100)
    struct.pack_into('<f', byte_buffer, 19, 100)

    web_socket_client.parse_binary(byte_buffer)


def test_process_ltp_packet(web_socket_client):
    byte_buffer = bytearray(23)
    byte_buffer[0] = 61
    struct.pack_into('<f', byte_buffer, 1, 100)
    struct.pack_into('<i', byte_buffer, 5, 100)
    struct.pack_into('<i', byte_buffer, 9, 100)
    byte_buffer[13] = 1
    byte_buffer[14] = 1
    struct.pack_into('<f', byte_buffer, 15, 100)
    struct.pack_into('<f', byte_buffer, 19, 100)

    web_socket_client.parse_binary(byte_buffer)


def test_process_index_quote_packet(web_socket_client):
    byte_buffer = bytearray(43)
    byte_buffer[0] = 65
    struct.pack_into('<f', byte_buffer, 1, 100)
    struct.pack_into('<i', byte_buffer, 5, 100)
    byte_buffer[9] = 1
    byte_buffer[10] = 1
    struct.pack_into('<f', byte_buffer, 11, 100)
    struct.pack_into('<f', byte_buffer, 15, 100)
    struct.pack_into('<f', byte_buffer, 19, 100)
    struct.pack_into('<f', byte_buffer, 23, 100)
    struct.pack_into('<f', byte_buffer, 27, 100)
    struct.pack_into('<f', byte_buffer, 31, 100)
    struct.pack_into('<f', byte_buffer, 35, 100)
    struct.pack_into('<f', byte_buffer, 39, 100)

    web_socket_client.parse_binary(byte_buffer)


def test_process_quote_packet(web_socket_client):
    byte_buffer = bytearray(67)
    byte_buffer[0] = 62
    struct.pack_into('<f', byte_buffer, 1, 100)
    struct.pack_into('<i', byte_buffer, 5, 100)
    struct.pack_into('<i', byte_buffer, 9, 100)
    byte_buffer[13] = 1
    byte_buffer[14] = 1
    struct.pack_into('<i', byte_buffer, 15, 100)
    struct.pack_into('<f', byte_buffer, 19, 100)
    struct.pack_into('<i', byte_buffer, 23, 100)
    struct.pack_into('<i', byte_buffer, 27, 100)
    struct.pack_into('<i', byte_buffer, 31, 100)
    struct.pack_into('<f', byte_buffer, 35, 100)
    struct.pack_into('<f', byte_buffer, 39, 100)
    struct.pack_into('<f', byte_buffer, 43, 100)
    struct.pack_into('<f', byte_buffer, 47, 100)
    struct.pack_into('<f', byte_buffer, 51, 100)
    struct.pack_into('<f', byte_buffer, 55, 100)
    struct.pack_into('<f', byte_buffer, 59, 100)
    struct.pack_into('<f', byte_buffer, 63, 100)

    web_socket_client.parse_binary(byte_buffer)


def test_process_index_full_packet(web_socket_client):
    byte_buffer = bytearray(39)
    byte_buffer[0] = 66
    struct.pack_into('<f', byte_buffer, 1, 100)
    struct.pack_into('<i', byte_buffer, 5, 100)
    byte_buffer[9] = 1
    byte_buffer[10] = 1
    struct.pack_into('<f', byte_buffer, 11, 100)
    struct.pack_into('<f', byte_buffer, 15, 100)
    struct.pack_into('<f', byte_buffer, 19, 100)
    struct.pack_into('<f', byte_buffer, 23, 100)
    struct.pack_into('<f', byte_buffer, 27, 100)
    struct.pack_into('<f', byte_buffer, 31, 100)
    struct.pack_into('<i', byte_buffer, 35, 100)

    web_socket_client.parse_binary(byte_buffer)


def test_process_full_packet(web_socket_client):
    byte_buffer = bytearray(175)
    depth_size = 20
    for i in range(5):
        struct.pack_into('<i', byte_buffer, 1 + (i * depth_size), 100)
        struct.pack_into('<i', byte_buffer, 5 + (i * depth_size), 100)
        struct.pack_into('<h', byte_buffer, 9 + (i * depth_size), 100)
        struct.pack_into('<h', byte_buffer, 11 + (i * depth_size), 100)
        struct.pack_into('<f', byte_buffer, 13 + (i * depth_size), 100)
        struct.pack_into('<f', byte_buffer, 17 + (i * depth_size), 100)

    byte_buffer[0] = 63
    struct.pack_into('<f', byte_buffer, 101, 100)
    struct.pack_into('<i', byte_buffer, 105, 100)
    struct.pack_into('<i', byte_buffer, 109, 100)
    byte_buffer[113] = 1
    byte_buffer[114] = 1
    struct.pack_into('<i', byte_buffer, 115, 100)
    struct.pack_into('<f', byte_buffer, 119, 100)
    struct.pack_into('<i', byte_buffer, 123, 100)
    struct.pack_into('<i', byte_buffer, 127, 100)
    struct.pack_into('<i', byte_buffer, 131, 100)
    struct.pack_into('<f', byte_buffer, 135, 100)
    struct.pack_into('<f', byte_buffer, 139, 100)
    struct.pack_into('<f', byte_buffer, 143, 100)
    struct.pack_into('<f', byte_buffer, 147, 100)
    struct.pack_into('<f', byte_buffer, 151, 100)
    struct.pack_into('<f', byte_buffer, 155, 100)
    struct.pack_into('<f', byte_buffer, 159, 100)
    struct.pack_into('<f', byte_buffer, 163, 100)
    struct.pack_into('<i', byte_buffer, 167, 100)
    struct.pack_into('<i', byte_buffer, 171, 100)

    web_socket_client.parse_binary(byte_buffer)
