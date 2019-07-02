from time import sleep
import logging

from pibot import leds, buttons
from pibot.nano import Nano

from utilities import clean_up
from motor_funcs import drive, kurve, roboterl, ausscheren, einscheren
import led_funcs as lf

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    speed = 30
    sleep_time = 0.5

    while True:
        try:
            dist = nano.get_distances()
            enc = nano.get_encoders()

            logging.info("enc: {} – dist: {}".format(enc, dist))

            way = dist[1]

            if way <= 10:
                ausscheren(nano, speed)
                roboterl(nano, speed, perc=1)
                einscheren(nano, speed)
            else:
                drive(nano, speed)

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
