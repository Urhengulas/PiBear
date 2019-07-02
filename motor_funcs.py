def drive(nano, speed, tolerance=6, cor=5):
    enc = nano.get_encoders()

    left = enc[0]
    right = enc[1]

    if (left - right) > tolerance:
        # adjust to right
        nano.set_motors(speed, speed + cor)
    elif (right - left) > tolerance:
        # adjust to left
        nano.set_motors(speed + cor, speed)
    else:
        # do nothing
        nano.set_motors(speed, speed)


def kurve(nano, speed, perc=1, dic="left"):
    if dic == "right":
        nano.set_motors(speed, -speed)
    elif dic == "left":
        nano.set_motors(-speed, speed)
    else:
        return

    while True:
        enc = nano.get_encoders()

        if abs(enc[0] - enc[1]) > perc*290:
            break

    nano.set_motors(0, 0)
    nano.reset_encoders()
