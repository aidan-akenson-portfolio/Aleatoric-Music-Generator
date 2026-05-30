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

        random.seed()

        self._scale = Scale.Scale()
        self._verse_progression = Harmonizer.ChordProgression(self._scale)
        self._verse_melody = Melody.Melody()

        time.sleep(0.05)

        self._chorus_progression = Harmonizer.ChordProgression(self._scale)
        self._chorus_melody = Melody.Melody()

        time.sleep(0.05)

        self._bridge_progression = Harmonizer.ChordProgression(self._scale)
        self._bridge_melody = Melody.Melody()

        time.sleep(0.05)

        self._song_structure = self._gen_structure()

        self._chords = Synth.Synth(ir="1")
        self._chords.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=1))
        self._chords.handleMessage(mido.Message('control_change', control=consts.RELEASE_CC, value=16))
        self._chords.handleMessage(mido.Message('control_change', control=consts.SUSTAIN_CC, value=1))
        self._chords.handleMessage(mido.Message('control_change', control=consts.DECAY_CC, value=60))
        self._chords.handleMessage(mido.Message('control_change', control=consts.ATTACK_CC, value=32))
        self._chords.handleMessage(mido.Message('control_change', control=consts.REVERB_CC, value=127))
        self._chords.handleMessage(mido.Message('control_change', control=consts.CUTOFF_CC, value=50))
        self._chords.handleMessage(mido.Message('control_change', control=consts.Q_CC, value=64))

        self._lead = Synth.Synth(ir="2")
        self._lead.handleMessage(mido.Message('control_change', control=consts.WAVE_CC, value=64))
        self._lead.handleMessage(mido.Message('control_change', control=consts.RELEASE_CC, value=64))
        self._lead.handleMessage(mido.Message('control_change', control=consts.SUSTAIN_CC, value=64))
        self._lead.handleMessage(mido.Message('control_change', control=consts.DECAY_CC, value=64))
        self._lead.handleMessage(mido.Message('control_change', control=consts.ATTACK_CC, value=8))
        self._lead.handleMessage(mido.Message('control_change', control=consts.REVERB_CC, value=64))
        self._lead.handleMessage(mido.Message('control_change', control=consts.CUTOFF_CC, value=100))
        self._lead.handleMessage(mido.Message('control_change', control=consts.Q_CC, value=64))

    def _gen_structure(self):
        song_structure = []
        num_sections = random.randrange(3, 8)
        verse_chance = 0.8
        chorus_chance = 0.2
        bridge_chance = 0.0
        for i in range(num_sections):

            # Prevents ending on a bridge
            success = False
            while not success:

                verse_roll = verse_chance * random.randrange(100)
                chorus_roll = chorus_chance * random.randrange(100)
                bridge_roll = bridge_chance * random.randrange(100)

                if verse_roll >= chorus_roll and verse_roll >= bridge_roll:
                    song_structure.append([self._verse_progression, self._verse_melody, random.choices([2, 4], weights=[0.8, 0.2])[0], "\n============VERSE============"])
                    verse_chance -= 0.8
                    chorus_chance += 0.3
                    bridge_chance += 0.4 * (i / num_sections)   # Bridges weighted towards later in the song
                    success = True
                elif chorus_roll >= bridge_roll:
                    song_structure.append([self._chorus_progression, self._chorus_melody, random.choices([2, 4], weights=[0.8, 0.2])[0], "\n============CHORUS============"])
                    verse_chance += 0.3
                    chorus_chance -= 0.8
                    bridge_chance += 0.4 * (i / num_sections)   # Bridges weighted towards later in the song
                    success = True
                elif i < num_sections - 1:
                    song_structure.append([self._bridge_progression, self._bridge_melody, random.choices([1, 2])[0], "\n============BRIDGE============"])
                    verse_chance += 0.1
                    chorus_chance += 0.6
                    bridge_chance -= 0.8
                    success = True

        return song_structure

    def _play_section(self, progression, melody, repetitions):

        print("Chords:", progression._midi, "\nHarmonic Rhythm:", progression._rhythm)
        print("Melody:", melody._pitches, "\nMelodic Rhythm:", melody.simple_grid, "\n")

        measure = 1
        chord = 1
        until_next_chord = 0
        last_note = -1

        for i in range(repetitions):
            melody._pitch_index = 0

            for i in range(len(melody._8th_note_grid)):

                # Chord performance
                if until_next_chord == 0:

                    chord = chord % len(progression._midi)
                    measure = measure % len(progression._rhythm)

                    for n in progression._midi[chord - 1]:
                        self._chords.handleMessage(mido.Message(type='note_on', note=n))
                
                    if chord > 1:
                        for n in progression._midi[chord - 2]:
                            self._chords.handleMessage(mido.Message('note_off', note=n))

                    chord += 1
                    until_next_chord = 2 * SIGNATURE / progression._rhythm[measure - 1]

                    if ((i % 8 == 0) and (progression._rhythm[measure - 1] == 1)
                        ) or (
                        (i % 4 == 0) and (i % 8 != 0) and (progression._rhythm[measure - 1] == 2)):

                        measure += 1


                # Melody performance
                if melody._8th_note_grid[i] == 0:
                    if last_note > 0:
                        self._lead.handleMessage(mido.Message(type='note_off', note=last_note))
                        last_note = -1

                if melody._8th_note_grid[i] == 1 or melody._8th_note_grid[i] == 2: 
                    if last_note > 0:
                        self._lead.handleMessage(mido.Message(type='note_off', note=last_note))

                    self._lead.handleMessage(mido.Message(type='note_on', note=melody._pitches[melody._pitch_index]))
                    last_note = melody._pitches[melody._pitch_index]

                    melody._pitch_index += 1

                until_next_chord -= 1

                time.sleep(BEAT_INTERVAL / 2)

    def play(self):
        for i in range(len(self._song_structure)):
            print(self._song_structure[i][3])
            self._play_section(self._song_structure[i][0], self._song_structure[i][1], self._song_structure[i][2])    
                
                




if __name__ == "__main__":
    player = Player()
    player.play()