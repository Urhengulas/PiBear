import logging
import pickle

from pibot.lcd import LCD

from utilities import setup, clean_up
from motor import Motor
from actions import smart, bulli
from led_funcs import tunnel_licht, wait_for_start

from camera_funcs import MyCamera

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    global ausgeschert
    global in_tunnel

    dist = motor.nano.get_distances()
    enc = motor.nano.get_encoders()

    # ultrasonic distances
    dist_l = dist[0]
    dist_m = dist[1]
    dist_r = dist[2]

    # encoder values
    enc_l = enc[0]
    enc_r = enc[1]

    logging.info("enc: {} – dist: {} – asg: {}".format(enc, dist, ausgeschert))

    stop_val = 18
    tunnel_val = 16

    # SACKGASSE
    if 0 < dist_l <= stop_val and 0 < dist_m * 0.75 <= stop_val and 0 < dist_r <= stop_val:
        logging.info("SACKGASSE 1 - dist: {}".format(dist))
        dist = motor.nano.get_distances()
        logging.info("SACKGASSE 2 - dist: {}".format(dist))

        dist_l = dist[0]
        dist_m = dist[1]
        dist_r = dist[2]

        if 0 < dist_l <= stop_val and 0 < dist_m * 0.75 <= stop_val and 0 < dist_r <= stop_val:
            motor.stop()

            """for _ in range(5):
                farbe = my_camera.check_for_balls()
                logging.info("BALL_FARBE: {}".format(farbe))"""

            return True
        else:
            logging.info("no")
    # NORMAL
    else:
        if ausgeschert is False:
            if 0 < dist_m <= 10:
                dist_m = motor.nano.get_distances()[1]

                if 0 < dist_m <= 10:
                    motor.ausscheren()
                    ausgeschert = True
            elif dist_l <= tunnel_val and dist_r <= tunnel_val:
                in_tunnel = True
            else:
                in_tunnel = False

        elif ausgeschert is True:
            if dist_r > 15:
                dist_r = motor.nano.get_distances()[2]

                if dist_r > 15:
                    lov = (enc_l + enc_r) / 2  # length of vehicle

                    motor.einscheren()
                    ausgeschert = False

                    smart_l = 700
                    bulli_l = 950

                    if lov <= smart_l:
                        logging.info("SMART - lov: {} - enc: {}".format(lov, enc))
                        lcd.print(["SMART", "hey hey"])
                        smart(motor)
                    elif smart_l < lov <= bulli_l:
                        logging.info("BlULLI - lov: {} - enc: {}".format(lov, enc))
                        lcd.print(["BULLI", "You look cool"])
                        bulli(motor)
                    else:
                        logging.info("LKW - lov: {} - enc: {}".format(lov, enc))
                        lcd.print(["LKW", "woom"])

        tunnel_licht(in_tunnel)

        motor.correct_wall(dist_r)
        motor.drive()

        return False


if __name__ == "__main__":
    motor = Motor(base_speed=28)
    my_camera = MyCamera()
    lcd = LCD()
    lcd.clear()

    ausgeschert = False
    in_tunnel = False

    normal = True

    if normal is True:
        logging.info("READY")
        lcd.print(["READY"])
        wait_for_start()
    elif normal is False:
        my_camera.BLUE_LOWER = (0, 0, 125)
        my_camera.BLUE_UPPER = (255, 255, 200)
        tunnel_licht(True)
        foto = my_camera.capture_image()
        my_camera.view_image(foto, "johann")
        is_ball, new_image = my_camera.check_for_ball(image=foto, color="blue", radius=60)
        logging.info("is_ball: {}".format(is_ball))
        my_camera.view_image(new_image, "paul")

        for _ in range(5):
            red_ball, blue_ball = my_camera.check_for_balls()
            logging.info("FARBE: red: {}, blue: {}".format(red_ball, blue_ball))

        tunnel_licht(False)

    while True:
        try:
            if normal is True:
                end = main()
            if normal is False:
                pass

            #  if end is True:
            #      break

        except KeyboardInterrupt:
            clean_up(motor)

            logging.error("Keyboard Interupt. Stop motors. Reset Nano. Reset LED's")
            break
