from time import sleep
from led_funcs import aufmerksamkeit


def smart(motor):
    motor.roboterl(perc=0.25, speed=-20)
    motor.stop()
    sleep(5)


def bulli(motor):
    motor.stop()
    aufmerksamkeit(motor.nano)
