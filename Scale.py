import random

from Synth.lib import mtof

class Scale():

    def __init__(self):

        # Scale size
        random.seed()
        self._scale_len = random.randrange(5, 8)

        # Generate a key
        self._root = random.choice(['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab'])

        self._notes = []

        