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


def stop_motors():
    nano.set_motors(0, 0)


def main():
    speed = 20

    while True:
        nano.set_motors(speed, -speed)


if __name__ == "__main__":
    main()
