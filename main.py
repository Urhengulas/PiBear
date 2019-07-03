import logging

from utilities import setup, clean_up
from motor import Motor
from actions import smart, bulli
from led_funcs import tunnel_licht
from pibot.camera import Camera

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    global ausgeschert
    global in_tunnel

    dist = nano.get_distances()
    enc = nano.get_encoders()

    # ultrasonic distances
    dist_l = dist[0]
    dist_m = dist[1]
    dist_r = dist[2]

    # encoder values
    enc_l = enc[0]
    enc_r = enc[1]

    logging.info("enc: {} – dist: {} – asg: {}".format(enc, dist, ausgeschert))

    stop_val = 13
    tunnel_val = 12

    if dist_l * 0.1 <= stop_val and dist_m <= stop_val and dist_r <= stop_val:
        motor.stop()
        return True
    else:
        if ausgeschert is False:
            if dist_m <= 10:
                motor.ausscheren()
                ausgeschert = True
            elif dist_l * 0.1 <= tunnel_val and dist_r <= tunnel_val:
                in_tunnel = True
            else:
                in_tunnel = False

        elif ausgeschert is True:
            if dist_r > 15:
                lov = (enc_l + enc_r) / 2  # length of vehicle

                motor.einscheren()
                ausgeschert = False

                smart_l = 750
                bulli_l = 950

                if lov <= smart_l:
                    logging.info("SMART")
                    smart(motor)
                elif smart_l < lov <= bulli_l:
                    logging.info("BULLI")
                    bulli(motor)
                else:
                    pass

        tunnel_licht(in_tunnel)

        motor.correct_wall(dist_r)
        motor.drive()

        return False


if __name__ == "__main__":
    nano = setup()
    motor = Motor(nano=nano, base_speed=25)

    ausgeschert = False
    in_tunnel = False

    while True:
        try:
            end = main()

            #  if end is True:
            #      break

        except KeyboardInterrupt:
            clean_up(motor)
            logging.error("Keyboard Interupt. Stop motors. Reset Nano. Reset LED's")
            break
