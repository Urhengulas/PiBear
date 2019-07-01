from time import sleep
import logging

from pibot import leds, buttons
from pibot.nano import Nano

from utilities import clean_up
import motor_funcs as mf
import led_funcs as lf

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    speed = (20, -20)
    sleep_time = 0.1

    while True:
        try:
            mf.drive(nano, speed)
            lf.blink()
            sleep(sleep_time)

        except KeyboardInterrupt:
            clean_up(nano)
            logging.error("Keyboard Interupt. Stop motors. Reset Nano. Reset LED's")
            break


if __name__ == "__main__":
    logging.info("Initialize LEDs and Buttons")
    leds.init_leds()
    buttons.init_buttons()

    logging.info("Initialize Connection to Arduino Nano ...")
    nano = Nano()
    nano.reset_encoders()

    main()
