import datetime


def epoch_converter(input_epoch_value):
    utc = datetime.timezone.utc
    ninety_eighty = datetime.datetime(1980, 1, 1, tzinfo=utc)
    time_new = int(ninety_eighty.timestamp())
    output_epoch_value = input_epoch_value + time_new
    return output_epoch_value
