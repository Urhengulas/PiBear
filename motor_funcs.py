import logging


def drive(nano, speed):
    nano.set_motors(speed[0], speed[1])
    logging.info(str(nano.get_encoders()))
