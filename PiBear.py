from pibot.lcd import LCD

from motor import Motor
from utilities import setup

class PiBear:

    def __init__(self, base_speed):
        self.nano = setup()
        self.motor = Motor(nano=self.nano, base_speed=base_speed)
        self.lcd = LCD()