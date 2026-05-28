import Harmonizer
import Scale
import Melody
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
        self._melody = Melody.Melody(4) # FIXME duration shouldn't be this arbitrary

        self._chords = Synth.Synth()
        self._chords.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=1))
        self._chords.handleMessage(mido.Message('control_change', control=consts.RELEASE_CC, value=64))
        self._chords.handleMessage(mido.Message('control_change', control=consts.SUSTAIN_CC, value=1))
        self._chords.handleMessage(mido.Message('control_change', control=consts.DECAY_CC, value=100))
        self._chords.handleMessage(mido.Message('control_change', control=consts.ATTACK_CC, value=32))
        self._chords.handleMessage(mido.Message('control_change', control=consts.REVERB_CC, value=127))

        self._lead = Synth.Synth()
        self._lead.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=64))
        self._lead.handleMessage(mido.Message('control_change', control=consts.RELEASE_CC, value=8))
        self._lead.handleMessage(mido.Message('control_change', control=consts.SUSTAIN_CC, value=1))
        self._lead.handleMessage(mido.Message('control_change', control=consts.DECAY_CC, value=32))
        self._lead.handleMessage(mido.Message('control_change', control=consts.ATTACK_CC, value=8))
        self._lead.handleMessage(mido.Message('control_change', control=consts.REVERB_CC, value=32))


    def play(self):

        # FIXME crude demo implmentation
        print(self._verse._midi, self._verse._rhythm)

        measure = 1
        next_measure = False
        chord = 1
        for i in range(4):

            for i in range(len(self._melody._8th_note_grid)):

                # New chord time yay
                if i % 8 == 0:

                    print("Measure #", measure, "\t\tChord: ", self._verse._midi[chord - 1], sep="")

                    chord = chord % len(self._verse._midi)
                    measure = measure % len(self._verse._rhythm)

                    for n in self._verse._midi[chord - 1]:
                        self._chords.handleMessage(mido.Message(type='note_on', note=n))
                
                    if chord > 1:
                        for n in self._verse._midi[chord - 2]:
                            self._chords.handleMessage(mido.Message('note_off', note=n))

                    if self._verse._rhythm[measure - 1] == 1:
                        measure += 1
                    elif next_measure:
                        measure += 1
                        next_measure = False
                    else:
                        next_measure = True 
                    chord += 1


                last_note = -1
                holding = False
                if self._melody._8th_note_grid[i] == 0:
                    if holding and (last_note > 0 or last_note == self._melody._pitches[self._melody._pitch_index]):
                        self._lead.handleMessage(mido.Message(type='note_off', note=last_note))
                        holding = False
                if self._melody._8th_note_grid[i] == 1 or self._melody._8th_note_grid[i] == 2: 
                    if self._melody._pitch_index >= len(self._melody._pitches):
                        self._melody._pitch_index = 0
                    self._lead.handleMessage(mido.Message(type='note_on', note=self._melody._pitches[self._melody._pitch_index]))
                    last_note = self._melody._pitches[self._melody._pitch_index]
                    self._melody._pitch_index += 1
                if self._melody._8th_note_grid[i] == 3:
                    if not holding:
                        self._melody._pitch_index += 1
                        if self._melody._pitch_index >= len(self._melody._pitches):
                            self._melody._pitch_index = 0
                    holding = True


                time.sleep(BEAT_INTERVAL / 2)
                
                
                




if __name__ == "__main__":
    player = Player()
    player.play()