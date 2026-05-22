import random

import Scale
import Chord

class ChordProgression():

    def __init__(self, scale):
        self._scale = scale

        # Verse will not be in the key of the scale, but rather in a
        # pseudo-relative key; that is, the notes will not change,
        # but the tonic will be moved to that of a non-root triad
        # (which acts as the root for a valid diatonic chord)
        verse_key = None
        while verse_key == None:
            verse_key_pos = min(random.choice([1, 2, 3]), len(self._scale._triads) - 1)
            if self._scale._triads[verse_key_pos] != None:
                verse_key = self._scale._triads[verse_key_pos][0]
        self._verse = self._generate_progression(verse_key)

        # Chorus is just in the key of the song
        chorus_key = self._scale._note_names[0]
        self._chorus = self._generate_progression(chorus_key)

        print("\nVerse, key of ", verse_key, ": ", sep="", end=" ")
        for v in self._verse:
            print(v) 
        print("\nChorus, key of ", chorus_key, ": ", sep="", end=" ")
        for c in self._chorus:
            print(c) 

    def _generate_progression(self, key):
        
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


        # Generate the chords themselves
        chords = []

        # Ensure the first chord is in the key of the section
        first_chord = self._scale._triads[0]
        first_chord_finder = 0
        while first_chord[0] != key:
            first_chord = self._scale._triads[first_chord_finder]
            first_chord_finder += 1
        chords.append(first_chord)
            

        # Rest of the chords
        for i in range(1, sum(harmonic_rhythm)):

            # Generate a random root
            root_degree = random.randrange(self._scale._scale_len)
            root = self._scale._note_names[root_degree]

            # Ensure the previous chord didn't also start with the same root
            while chords[i - 1][0] == root:
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

            chords.append(new_chord)

        progression = []
        pos = 0
        i = 0
        while pos < sum(harmonic_rhythm) and i < duration:

            if harmonic_rhythm[i] == 1:
                progression.append(chords[pos])
                pos += 1
                i += 1
            else:
                progression.append(list([chords[pos], chords[pos + 1]]))
                pos += 2
                i += 1

        return progression
            

if __name__ == "__main__":
    chord_prog = ChordProgression(Scale.Scale())