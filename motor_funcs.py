import logging


def drive(nano, speed):
    nano.set_motors(speed[0], speed[1])
