import datetime


def epoch_converter(input_epoch_value):
    # Value of ninetyEightyConstant is derived by -
    # utc = datetime.timezone.utc
    # ninety_eighty = datetime.datetime(1980, 1, 1, tzinfo=utc)
    # ninetyEightyConstant = int(ninety_eighty.timestamp())
    ninety_eighty_constant = 315532800
    output_epoch_value = input_epoch_value + ninety_eighty_constant
    return output_epoch_value
