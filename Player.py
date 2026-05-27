import Harmonizer
import Scale
import ntom
from Synth import Synth
from Synth.lib import consts

import time
import random
import mido

BPM = random.randrange(90, 174)
BEAT_INTERVAL = 1 / (BPM / 60)
SIGNATURE = 4

class Player():

    def __init__(self):
        self._scale = Scale.Scale()
        self._verse = Harmonizer.ChordProgression(self._scale)

        self._chords = Synth.Synth()
        self._chords.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=1))
        self._chords.handleMessage(mido.Message('control_change', control=consts.RELEASE_CC, value=64))
        self._chords.handleMessage(mido.Message('control_change', control=consts.SUSTAIN_CC, value=1))
        self._chords.handleMessage(mido.Message('control_change', control=consts.DECAY_CC, value=100))
        self._chords.handleMessage(mido.Message('control_change', control=consts.ATTACK_CC, value=32))

        self._lead = Synth.Synth()
        self._chords.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=2))
        self._chords.handleMessage(mido.Message('control_change', control=consts.RELEASE_CC, value=16))
        self._chords.handleMessage(mido.Message('control_change', control=consts.SUSTAIN_CC, value=64))
        self._chords.handleMessage(mido.Message('control_change', control=consts.DECAY_CC, value=100))
        self._chords.handleMessage(mido.Message('control_change', control=consts.ATTACK_CC, value=3))


    def play(self):

        # FIXME crude demo implmentation
        print(self._verse._midi, self._verse._rhythm)
        for i in range(4):

            measure = 1
            next_measure = False
            chord = 1

            while measure <= len(self._verse._rhythm) and chord <= len(self._verse._midi):

                print("Measure #", measure, "\t\tChord: ", self._verse._midi[chord - 1], sep="")

                for n in self._verse._midi[chord - 1]:
                    self._chords.handleMessage(mido.Message('note_on', note=n))
                time.sleep(BEAT_INTERVAL * (SIGNATURE / self._verse._rhythm[measure - 1]))
                for n in self._verse._midi[chord - 1]:
                    self._chords.handleMessage(mido.Message('note_off', note=n))

                if self._verse._rhythm[measure - 1] == 1:
                    measure += 1
                elif next_measure:
                    measure += 1
                    next_measure = False
                else:
                    next_measure = True
                
                chord += 1




if __name__ == "__main__":
    player = Player()
    player.play()