import logging

from pibot import leds, constants as c, buttons
from pibot.nano import Nano


def setup():
    logging.info("Initialize LEDs and Buttons")
    leds.init_leds()
    buttons.init_buttons()

    logging.info("Initialize Connection to Arduino Nano ...")
    nano = Nano()
    nano.reset_encoders()

    return nano


def clean_up(motor):
    motor.stop()
    motor.nano.reset_nano()
    stop_leds()


def stop_leds():
    led_list = [c.LED_RIGHT, c.LED_MID, c.LED_LEFT, c.LED_FRONT_LEFT, c.LED_FRONT_RIGHT]

    for led in led_list:
        leds.set_led(led, c.OFF)
