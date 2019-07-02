from pibot import leds, constants as c
from time import sleep


def blink(dir_b, times=5):
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
    nano.set_buzzer(100, 3000)
    for _ in range(3):
        leds.set_led(c.LED_RIGHT, c.GREEN)
        sleep(0.3)
        leds.set_led(c.LED_RIGHT, c.OFF)
        sleep(0.3)