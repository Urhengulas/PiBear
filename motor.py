import _thread
import logging

from utilities import setup
from led_funcs import blink
from time import sleep


class Motor:

    def __init__(self, base_speed=30):
        self.nano = setup()
        self.base_speed = base_speed

    def drive(self, speed=None, tol=4, cor=5):
        if speed is None:
            speed = self.base_speed

        speed_l, speed_r = correct_speed(nano=self.nano, speed=speed, tol=tol, cor=cor)

        self.nano.set_motors(speed_l, speed_r)

    def stop(self):
        self.nano.set_motors(0, 0)

    def kurve(self, dir, speed=None, perc=1.0):
        if speed is None:
            speed = self.base_speed

        if dir == "right":
            _thread.start_new_thread(blink, ("right",))
            self.nano.set_motors(speed, -speed)
        elif dir == "left":
            _thread.start_new_thread(blink, ("left",))
            self.nano.set_motors(-speed, speed)
        else:
            return

        quarter_turn = 290
        while True:
            enc = self.nano.get_encoders()

            if abs(enc[0] - enc[1]) > perc * quarter_turn:
                break

        self.nano.reset_encoders()

    def roboterl(self, perc=1.0, speed=None):
        if speed is None:
            speed = self.base_speed

        enc0 = self.nano.get_encoders()[1]

        while True:
            self.drive(speed=speed)

            enc1 = self.nano.get_encoders()[1]

            if abs(enc0 - enc1) > perc * 290:
                break

    def ausscheren(self):
        logging.info("AUSSCHEREN beginnt")
        self.kurve("left")

        while True:
            self.drive()

            dtb = self.nano.get_distances()[2]

            if dtb > 15:
                sleep(0.06)
                dtb = self.nano.get_distances()[2]
                if dtb > 15:
                    break
            else:
                pass

        self.roboterl(perc=0.6)
        self.kurve("right", perc=1)
        self.roboterl(perc=1)

    def einscheren(self):
        logging.info("EINSCHEREN beginnt")

        self.roboterl(perc=0.8)
        self.kurve("right")

        while True:
            self.drive()

            dtb = self.nano.get_distances()[2]

            if dtb < 20:
                dtb = self.nano.get_distances()[2]
                if dtb < 20:
                    break
            else:
                pass

        self.roboterl(perc=0.35)  # alt 0.7
        self.kurve("left", perc=1.1)

    def correct_wall(self, dist_r):
        # dtw means distance to wall
        dtw = dist_r

        if dtw <= 7:
            self.nano.set_motors(self.base_speed, self.base_speed + 15)
        elif 15 <= dtw <= 25:
            self.nano.set_motors(self.base_speed + 10, self.base_speed)


def correct_speed(nano, speed, tol, cor):
    enc = nano.get_encoders()

    enc_l = enc[0]
    enc_r = enc[1]

    if (enc_l - enc_r) > tol:
        return speed, speed + cor  # adjust to right
    elif (enc_r - enc_l) > tol:
        return speed + cor, speed  # adjust to left
    else:
        return speed, speed  # do nothing
