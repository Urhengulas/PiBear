def drive(nano, speed, correct=True, correct_val=5):
    nano.set_motors(speed[0], speed[1])

    if correct == True:
        enc = nano.get_encoders()

        left = enc[0]
        right = enc[1]

        if (left - right) > correct_val:
            pass  # adjust to right
        elif (right - left) > correct_val:
            pass  # adjust to left
        else:
            pass  # do nothing
