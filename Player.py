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
        self._chord_prog = Harmonizer.ChordProgression(self._scale)

        self._chords = Synth.Synth()
        #self._chords.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=1))

    def play(self):

        # FIXME crude demo implmentation
        print(self._chord_prog._verse_midi, self._chord_prog._verse_rhythm)
        for i in range(4):

            measure = 1
            next_measure = False
            chord = 1

            while measure <= len(self._chord_prog._verse_rhythm) and chord <= len(self._chord_prog._verse_midi):

                print("Measure #", measure, "\t\tChord: ", self._chord_prog._verse_midi[chord - 1], sep="")

                for n in self._chord_prog._verse_midi[chord - 1]:
                    self._chords.handleMessage(mido.Message('note_on', note=n))
                time.sleep(BEAT_INTERVAL * (SIGNATURE / self._chord_prog._verse_rhythm[measure - 1]))
                for n in self._chord_prog._verse_midi[chord - 1]:
                    self._chords.handleMessage(mido.Message('note_off', note=n))

                if self._chord_prog._verse_rhythm[measure - 1] == 1:
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