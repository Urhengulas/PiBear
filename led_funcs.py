from pibot import leds, constants as c
from time import sleep


def blink(dir_b, times=3):
    if dir_b == "left":
        led = c.LED_LEFT
    elif dir_b == "right":
        led = c.LED_RIGHT

    for _ in range(times):
        leds.set_led(led, c.RED)
        sleep(0.3)
        leds.set_led(led, c.OFF)
        sleep(0.3)


def aufmerksamkeit(nano):
    sleep(0.1)

    for _ in range(3):
        leds.set_led(c.LED_RIGHT, c.GREEN)
        nano.set_buzzer(100, 400)
        sleep(0.3)
        leds.set_led(c.LED_RIGHT, c.OFF)
        sleep(0.3)


def tunnel_licht(in_tunnel: bool):
    if in_tunnel is True:
        zustand = c.ON
    else:
        zustand = c.OFF

    for led in [c.LED_FRONT_LEFT, c.LED_FRONT_RIGHT]:
        leds.set_led(led, zustand)
