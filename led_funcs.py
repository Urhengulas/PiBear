from time import sleep

from pibot import leds, constants as c


def blink(sleep_time=0.5):
    blink_list = [(c.LED_RIGHT, c.RED), (c.LED_MID, c.YELLOW), (c.LED_LEFT, c.GREEN)]

    for led, col in blink_list:
        leds.set_led(led, col)
        sleep(sleep_time)
        leds.set_led(led, c.OFF)
