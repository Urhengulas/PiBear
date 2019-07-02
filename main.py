import logging

from utilities import setup, clean_up
from motor import Motor
from actions import smart, bulli

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    dist = nano.get_distances()
    enc = nano.get_encoders()

    global ausgeschert

    logging.info("enc: {} – dist: {} – asg: {}".format(enc, dist, ausgeschert))

    # ultrasonic distances
    dist_l = dist[0]
    dist_m = dist[1]
    dist_r = dist[2]

    stop_val = 16
    if dist_l <= stop_val and dist_m <= stop_val and dist_r <= stop_val:
        motor.stop()
    else:
        if ausgeschert is False:
            if dist_m <= 10:
                motor.ausscheren() # hier fährt er raus
                ausgeschert = True
        elif ausgeschert is True:
            if dist_r > 15:
                lov = nano.get_encoders()[0]

                motor.einscheren() # hier fährt er rein
                ausgeschert = False

                if lov < 700:
                    logging.info("SMART")
                    smart(motor)
                elif lov > 700 and lov < 900:
                    logging.info("BULLI")
                    bulli(motor)
                else:
                    pass

        motor.drive()

    nano.set_buzzer(100, 5)

    # blink()


if __name__ == "__main__":
    nano = setup()
    motor = Motor(nano=nano, base_speed=30)
    ausgeschert = False

    #  nano.set_buzzer(50, 1000)  # hz, ms

    while True:
        try:
            main()
        except KeyboardInterrupt:
            clean_up(nano)
            logging.error("Keyboard Interupt. Stop motors. Reset Nano. Reset LED's")
            break
