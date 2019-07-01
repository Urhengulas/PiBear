from pibot import leds, constants as c


def clean_up(nano):
    stop_motors(nano)
    nano.reset_nano(nano)
    stop_leds()


def stop_motors(nano):
    nano.set_motors(0, 0)


def stop_leds():
    led_list = [c.LED_RIGHT, c.LED_MID, c.LED_LEFT, c.LED_FRONT_LEFT, c.LED_FRONT_RIGHT]

    for led in led_list:
        leds.set_led(led, c.OFF)
