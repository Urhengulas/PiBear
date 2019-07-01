from time import sleep
import logging

from pibot import (
    leds, buttons, constants as c
)
from pibot.nano import Nano

leds.init_leds()
buttons.init_buttons()

nano = Nano()
nano.reset_encoders()


def blinken():
    leds.set_led(c.LED_LEFT, c.RED)
    sleep(0.5)
    leds.set_led(c.LED_LEFT, c.OFF)
    leds.set_led(c.LED_MID, c.YELLOW)
    sleep(0.5)
    leds.set_led(c.LED_MID, c.OFF)
    leds.set_led(c.LED_RIGHT, c.GREEN)
    sleep(0.5)
    leds.set_led(c.LED_RIGHT, c.OFF)


def stop_motors():
    nano.set_motors(0, 0)


def main():
    speed = 20

    while True:
        nano.set_motors(speed, -speed)

        blinken()

        sleep(0.1)
        stop_motors()


if __name__ == "__main__":
    main()
