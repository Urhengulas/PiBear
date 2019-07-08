from pibot.camera import Camera


class MyCamera(Camera):

    def check_for_balls(self):
        bild = self.capture_image()

        red_ball = self.check_one_ball(bild=bild, farbe="red")
        blue_ball = self.check_one_ball(bild=bild, farbe="blue")

        """if red_ball is True:
            return "red"
        elif blue_ball is True:
            return "blue"
        else:
            return None"""
        return red_ball, blue_ball

    def check_one_ball(self, bild, farbe, start=50, end=150, step=10):
        for rad in range(start, end, step):
            is_ball, new_image = self.check_for_ball(image=bild, color=farbe, radius=rad)

            if is_ball is True:
                return True

        return False
