from time import sleep
import logging

from pibot import leds, buttons
from pibot.nano import Nano

from utilities import clean_up
from motor_funcs import drive
import led_funcs as lf

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    speed = 40
    sleep_time = 0.5

    while True:
        try:
            dist = nano.get_distances()
            enc = nano.get_encoders()

            logging.info("enc: {}".format(enc))
            logging.info("dist: {}".format(dist))

            way = dist[1]
            if way <= 5:
                drive(nano, -speed)
            elif way <= 10:
                nano.set_motors(0, 0)
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
