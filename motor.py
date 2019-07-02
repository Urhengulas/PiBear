import _thread
import logging

from led_funcs import blink


class Motor:

    def __init__(self, nano, base_speed=40):
        self.nano = nano
        self.base_speed = base_speed

    def drive(self, speed=None, tol=4, cor=5):
        if speed is None:
            speed = self.base_speed

        enc = self.nano.get_encoders()

        left = enc[0]
        right = enc[1]

        speed_l, speed_r = correct_speed(nano=self.nano, speed=speed, tol=tol, cor=cor)

        self.nano.set_motors(speed_l, speed_r)

    def stop(self):
        self.nano.set_motors(0, 0)

    def kurve(self, dir, speed=None, perc=1):
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

        while True:
            enc = self.nano.get_encoders()

            if abs(enc[0] - enc[1]) > perc * 290:
                break

        self.nano.reset_encoders()

    def roboterl(self, perc=1.0, speed=None):
        if speed is None:
            speed = self.base_speed

        enc0 = self.nano.get_encoders()[1]

        while True:
            self.drive(speed=speed)

            enc1 = self.nano.get_encoders()[1]

            if abs(enc0 - enc1) > perc * 270:
                break

    def ausscheren(self):
        self.kurve("left")

        while True:
            self.drive()

            dist = self.nano.get_distances()
            way = dist[2]

            if way > 15:
                break
            else:
                pass

        self.roboterl(perc=0.5)
        self.kurve("right")
        self.roboterl(perc=1)

    def einscheren(self):
        logging.info("EINSCHEREN: {}".format(self.nano.get_encoders()))

        self.roboterl(perc=0.5)
        self.kurve("right")

        while True:
            self.drive()

            dtb = self.nano.get_distances()[2]

            if dtb < 15:
                self.stop()
                break
            else:
                pass

        self.roboterl(perc=0.2)
        self.kurve("left")


def correct_speed(nano, speed, tol, cor):
    enc = nano.get_encoders()

    left = enc[0]
    right = enc[1]

    if (left - right) > tol:
        return speed, speed + cor  # adjust to right
    elif (right - left) > tol:
        return speed + cor, speed  # adjust to left
    else:
        return speed, speed  # do nothing
