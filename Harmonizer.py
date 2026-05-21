import random

import Scale

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
        print(verse_key)
        self._verse = self._generate_progression(verse_key)

        # Chorus is just in the key of the song
        chorus_key = self._scale._note_names[0]
        self._chorus = self._generate_progression(chorus_key)

    def _generate_progression(self, key):
        
        # Each progression is either 4 or 8 measures
        duration = random.choice([4, 8])

        # Each progression has the first measure be a single chord.
        # After this, some measures may contain two chords.
        harmonic_rhythm = [1]
        num_doubles = 0
        for i in range(1, duration):
            half_note_chance = (1 - (num_doubles / duration))
            whole_note_chance = 1 - half_note_chance
            num_chords_in_this_measure = int(random.choices([1, 2], weights=(whole_note_chance, half_note_chance), k=1)[0])
            if num_chords_in_this_measure > 1:
                num_doubles += 1
            harmonic_rhythm.append(num_chords_in_this_measure)
        random.shuffle(harmonic_rhythm[1:])

        print(harmonic_rhythm)

if __name__ == "__main__":
    chord_prog = ChordProgression(Scale.Scale())