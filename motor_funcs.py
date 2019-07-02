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


def kurve(nano, speed, dic="left", perc=1):
    if dic == "right":
        nano.set_motors(speed, -speed)
    elif dic == "left":
        nano.set_motors(-speed, speed)
    else:
        return

    while True:
        enc = nano.get_encoders()

        if abs(enc[0] - enc[1]) > perc * 290:
            break

    nano.set_motors(0, 0)
    nano.reset_encoders()


def ausscheren(nano, speed):
    kurve(nano, speed, "left")
    drive(nano, speed)

    while True:
        dist = nano.get_distances()
        way = dist[2]
        if way > 15:
            break
        else:
            pass

    roboterl(nano, speed, perc=0.4)
    kurve(nano, speed, "right")


def einscheren(nano, speed):
    drive(nano, speed)

    while True:
        dist = nano.get_distances()
        way = dist[2]
        if way > 15:
            break
        else:
            pass

    roboterl(nano, speed, perc=0.8)
    kurve(nano, speed, "right")
    roboterl(nano, speed, perc=1.1)
    kurve(nano, speed, "left")


def roboterl(nano, speed, perc=1):
    enc0 = nano.get_encoders()[1]

    drive(nano, speed)

    while True:
        enc = nano.get_encoders()[1]

        if abs(enc0 - enc) > perc * 270:
            break
