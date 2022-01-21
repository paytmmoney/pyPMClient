import enum


# API Methods
class Requests(enum.Enum):
    POST = 1
    GET = 2
    PUT = 3
    DELETE = 4


# Transaction Type
class TransactionType(enum.Enum):
    Buy = 'BUY'
    Sell = 'SELL'


# Order Type
class OrderType(enum.Enum):
    Market = 'MKT'
    Limit = 'LMT'
    StopLossLimit = 'SL'
    StopLossMarket = 'SLM'


# Product Type
class ProductType(enum.Enum):
    Intraday = 'T'
    Delivery = 'C'
    CoverOrder = 'V'
    BracketOrder = 'B'
    Margin = 'M'


# Source
class Source(enum.Enum):
    Website = 'W'
    MobileWeb = 'M'
    Android = 'N'
    IOS = 'I'
    OperatorWorkStation = 'O'
