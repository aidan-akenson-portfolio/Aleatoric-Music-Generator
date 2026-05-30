import Harmonizer
import Scale
import Melody
import ntom
from Synth import Synth
from Synth.lib import consts

import time
import random
import mido

BPM = random.randrange(80, 150)
BEAT_INTERVAL = 1 / (BPM / 60)
SIGNATURE = 4

class Player():

    def __init__(self):
        self._scale = Scale.Scale()
        self._verse_progression = Harmonizer.ChordProgression(self._scale)
        self._verse_melody = Melody.Melody(4) # FIXME duration shouldn't be this arbitrary

        self._chords = Synth.Synth()
        self._chords.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=1))
        self._chords.handleMessage(mido.Message('control_change', control=consts.RELEASE_CC, value=16))
        self._chords.handleMessage(mido.Message('control_change', control=consts.SUSTAIN_CC, value=1))
        self._chords.handleMessage(mido.Message('control_change', control=consts.DECAY_CC, value=100))
        self._chords.handleMessage(mido.Message('control_change', control=consts.ATTACK_CC, value=32))
        self._chords.handleMessage(mido.Message('control_change', control=consts.REVERB_CC, value=127))

        self._lead = Synth.Synth()
        self._lead.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=64))
        self._lead.handleMessage(mido.Message('control_change', control=consts.RELEASE_CC, value=16))
        self._lead.handleMessage(mido.Message('control_change', control=consts.SUSTAIN_CC, value=0))
        self._lead.handleMessage(mido.Message('control_change', control=consts.DECAY_CC, value=32))
        self._lead.handleMessage(mido.Message('control_change', control=consts.ATTACK_CC, value=8))
        self._lead.handleMessage(mido.Message('control_change', control=consts.REVERB_CC, value=64))
        self._lead.handleMessage(mido.Message('control_change', control=consts.CUTOFF_CC, value=80))


    def play_section(self, synth_device, progression, melody, repetitions: int = 4):

        # FIXME crude demo implmentation
        print(progression._midi, progression._rhythm)

        measure = 1
        chord = 1
        until_next_chord = 0

        for i in range(repetitions):

            for i in range(len(melody._8th_note_grid)):

                # New chord time yay
                if until_next_chord == 0:

                    print("Measure #", measure, "\t\tChord: ", progression._midi[chord - 1], sep="")

                    chord = chord % len(progression._midi)
                    measure = measure % len(progression._rhythm)

                    for n in progression._midi[chord - 1]:
                        synth_device.handleMessage(mido.Message(type='note_on', note=n))
                
                    if chord > 1:
                        for n in progression._midi[chord - 2]:
                            synth_device.handleMessage(mido.Message('note_off', note=n))

                    chord += 1
                    until_next_chord = 2 * SIGNATURE / progression._rhythm[measure - 1]

                    if ((i % 8 == 0) and (progression._rhythm[measure - 1] == 1)
                        ) or (
                        (i % 4 == 0) and (i % 8 != 0) and (progression._rhythm[measure - 1] == 2)):

                        measure += 1

                last_note = -1
                holding = False

                if melody._8th_note_grid[i] == 0:
                    if holding and (last_note > 0 or last_note == melody._pitches[melody._pitch_index]):
                        self._lead.handleMessage(mido.Message(type='note_off', note=last_note))
                        holding = False
                if melody._8th_note_grid[i] == 1 or melody._8th_note_grid[i] == 2: 
                    if holding:
                        self._lead.handleMessage(mido.Message(type='note_off', note=last_note))
                        holding = False
                    if melody._pitch_index >= len(melody._pitches):
                        melody._pitch_index = 0
                    self._lead.handleMessage(mido.Message(type='note_on', note=melody._pitches[melody._pitch_index]))
                    last_note = melody._pitches[melody._pitch_index]
                    melody._pitch_index += 1
                if melody._8th_note_grid[i] == 3:
                    if not holding:
                        melody._pitch_index += 1
                        if melody._pitch_index >= len(melody._pitches):
                            melody._pitch_index = 0
                    holding = True

                until_next_chord -= 1

                time.sleep(BEAT_INTERVAL / 2)

    def play(self):
        self.play_section(self._chords, self._verse_progression, self._verse_melody)       
                
                




if __name__ == "__main__":
    player = Player()
    player.play()