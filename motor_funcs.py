def drive(nano, speed, correct=True, correct_val=5, cor=3):
    if correct == True:
        enc = nano.get_encoders()

        left = enc[0]
        right = enc[1]

        if (left - right) > correct_val:
            # adjust to right
            nano.set_motors(speed[0], speed[1] + cor)
        elif (right - left) > correct_val:
            # adjust to left
            nano.set_motors(speed[0] + cor, speed[1])
        else:
            # do nothing
            nano.set_motors(speed[0], speed[1])
