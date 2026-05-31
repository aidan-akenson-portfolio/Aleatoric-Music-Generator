import random

import Scale
import Chord
import ntom

class ChordProgression():

    def __init__(self, scale):
        self._scale = scale

        self._key = None
        key_pos = 0
        while self._key == None or self._scale._triads[key_pos] == None:
            key_pos = min(random.choice([1, 2, 3]), len(self._scale._triads) - 1)
            if self._scale._triads[key_pos] != None:
                self._key = self._scale._triads[key_pos][0]
        self._rhythm = self._harmonic_rhythm()
        self._prog = self._generate_progression(self._key, self._rhythm)
        self._midi = self._to_midi(self._prog)

    def _harmonic_rhythm(self):
        # Each progression is either 4 or 8 measures
        duration = random.choice([4, 8])

        # Each progression has the first measure be a single chord.
        # After this, some measures may contain two chords.
        harmonic_rhythm = [1]
        num_doubles = 0
        for i in range(1, duration):
            half_note_chance = (1 - (num_doubles / duration)) * 0.25
            whole_note_chance = 1 - half_note_chance
            num_chords_in_this_measure = int(random.choices([1, 2], weights=(whole_note_chance, half_note_chance), k=1)[0])
            if num_chords_in_this_measure > 1:
                num_doubles += 1
            harmonic_rhythm.append(num_chords_in_this_measure)
        random.shuffle(harmonic_rhythm[1:])

        return harmonic_rhythm

    def _generate_progression(self, key, harmonic_rhythm):

        chords = []

        # Ensure the first chord is in the key of the section
        first_chord = self._scale._triads[0]
        first_chord_finder = 0
        while (first_chord == None) or (first_chord[0] != key):
            first_chord = self._scale._triads[first_chord_finder]
            first_chord_finder += 1
        chords.append(first_chord) 
            

        # Rest of the chords
        for i in range(1, sum(harmonic_rhythm)):

            # Generate a random root
            root_degree = random.randrange(self._scale._scale_len)
            root = self._scale._note_names[root_degree]

            # Ensure the previous chord didn't also start with the same root
            # and that the first and last chords don't share a root
            while chords[i - 1][0] == root:

                root_degree = random.randrange(self._scale._scale_len)
                root = self._scale._note_names[root_degree]

                if (i == sum(harmonic_rhythm) - 1) and root == key:
                    root_degree = random.randrange(self._scale._scale_len)
                    root = self._scale._note_names[root_degree]
                    


            # Attempt to use a diatonic chord
            new_chord = self._scale._triads[root_degree]
            if self._scale._sevenths[root_degree] != None:
                new_chord = self._scale._sevenths[root_degree]
            if self._scale._ninths[root_degree] != None:
                new_chord = self._scale._ninths[root_degree]

            # Else we'll randomly generate either a major or minor chord
            # FIXME make this behaviour more sophisticated once basic functionality is working
            if new_chord is None:
                new_chord = random.choice([Chord.major(root), Chord.minor(root)])


            # With a 50% chance, make the last chord in the progression a 7
            if (i == sum(harmonic_rhythm) - 1) and (random.randrange(0,1) == 1):
                new_chord = Chord.dominant7(root)

            chords.append(new_chord)

        progression = []
        pos = 0
        i = 0
        while pos < sum(harmonic_rhythm) and i < len(harmonic_rhythm):

            if harmonic_rhythm[i] == 1:
                progression.append(chords[pos])
                pos += 1
                i += 1
            else:
                progression.append(list([chords[pos], chords[pos + 1]]))
                pos += 2
                i += 1

        return progression
            
    def _to_midi(self, progression):

        min_interval = [7, 3, 2, 2, 1]

        # Attempt with the given inversions
        midi_prog = []
        for i in range(len(progression)):
            chord = progression[i]
            midi_vals = []
            for i in range(len(chord)):

                match chord[i]:
                    case "A":
                        if i == 0:
                            midi_vals.append(ntom.A_VALUES[2])
                        else:
                            j = 0
                            while ntom.A_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.A_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.A_VALUES[j])
                    case "Bb" | "A#":
                        if i == 0:
                            midi_vals.append(ntom.BB_VALUES[2])
                        else:
                            j = 0
                            while ntom.BB_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.BB_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.BB_VALUES[j])
                    case "B":
                        if i == 0:
                            midi_vals.append(ntom.B_VALUES[2])
                        else:
                            j = 0
                            while ntom.B_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.B_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.B_VALUES[j])
                    case "C":
                        if i == 0:
                            midi_vals.append(ntom.C_VALUES[2])
                        else:
                            j = 0
                            while ntom.C_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.C_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.C_VALUES[j])
                    case "Db" | "C#":
                        if i == 0:
                            midi_vals.append(ntom.DB_VALUES[2])
                        else:
                            j = 0
                            while ntom.DB_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.DB_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.DB_VALUES[j])
                    case "D":
                        if i == 0:
                            midi_vals.append(ntom.D_VALUES[2])
                        else:
                            j = 0
                            while ntom.D_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.D_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.D_VALUES[j])
                    case "Eb" | "D#":
                        if i == 0:
                            midi_vals.append(ntom.EB_VALUES[2])
                        else:
                            j = 0
                            while ntom.EB_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.EB_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.EB_VALUES[j])
                    case "E":
                        if i == 0:
                            midi_vals.append(ntom.E_VALUES[2])
                        else:
                            j = 0
                            while ntom.E_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.E_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.E_VALUES[j])
                    case "F":
                        if i == 0:
                            midi_vals.append(ntom.F_VALUES[2])
                        else:
                            j = 0
                            while ntom.F_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.F_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.F_VALUES[j])
                    case "Gb" | "F#":
                        if i == 0:
                            midi_vals.append(ntom.GB_VALUES[2])
                        else:
                            j = 0
                            while ntom.GB_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.GB_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.GB_VALUES[j])
                    case "G":
                        if i == 0:
                            midi_vals.append(ntom.G_VALUES[2])
                        else:
                            j = 0
                            while ntom.G_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.G_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.G_VALUES[j])
                    case "Ab" | "G#":
                        if i == 0:
                            midi_vals.append(ntom.AB_VALUES[2])
                        else:
                            j = 0
                            while ntom.AB_VALUES[j] < midi_vals[i - 1] + min_interval[i]:
                                j += 1
                            if ntom.AB_VALUES[j] > 70:
                                j -= 1
                            midi_vals.append(ntom.AB_VALUES[j])
                    case _:
                        # Multiple chords in the same measure
                        multi_chord_midi = []
                        for m in range(len(chord[i])):
                            match chord[i][m]:
                                case "A":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.A_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.A_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.A_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.A_VALUES[j])
                                case "Bb" | "A#":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.BB_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.BB_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.BB_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.BB_VALUES[j])
                                case "B":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.B_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.B_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.B_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.B_VALUES[j])
                                case "C":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.C_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.C_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.C_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.C_VALUES[j])
                                case "Db" | "C#":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.DB_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.DB_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.DB_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.DB_VALUES[j])
                                case "D":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.D_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.D_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.D_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.D_VALUES[j])
                                case "Eb" | "D#":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.EB_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.EB_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.EB_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.EB_VALUES[j])
                                case "E":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.E_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.E_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.E_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.E_VALUES[j])
                                case "F":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.F_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.F_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.F_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.F_VALUES[j])
                                case "Gb" | "F#":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.GB_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.GB_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.GB_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.GB_VALUES[j])
                                case "G":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.G_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.G_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.G_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.G_VALUES[j])
                                case "Ab" | "G#":
                                    if m == 0:
                                        multi_chord_midi.append(ntom.AB_VALUES[2])
                                    else:
                                        j = 0
                                        while ntom.AB_VALUES[j] < multi_chord_midi[m - 1] + min_interval[i]:
                                            j += 1
                                        if ntom.AB_VALUES[j] > 70:
                                            j -= 1
                                        multi_chord_midi.append(ntom.AB_VALUES[j])
                                case _:
                                    print("Cannot convert value to MIDI:", chord[i][m])
                        midi_prog.append(multi_chord_midi)
            if midi_vals != [] and midi_vals is not None:
                midi_prog.append(midi_vals)

        # Fix some clustering issues
        for i in midi_prog:

            # If the root is not the lowest note, raise the lower note
            if i[0] > i[1]:
                i[1] += 12
            if i[0] > i[2]:
                i[2] += 12

            # Check all min intervals and raise an octave where needed
            needs_raise = [False] * len(i)
            for j in range(1, len(i)):
                if i[j] - i[j - 1] < min_interval[j - 1]:
                    needs_raise[j] = True
            for j in range(len(i)):
                if needs_raise[j]:
                    i[j] += 12


        return midi_prog
    
if __name__ == "__main__":
    chord_prog = ChordProgression(Scale.Scale())