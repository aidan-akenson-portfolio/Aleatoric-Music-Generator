import random

class Scale():

    def __init__(self):

        # Scale size
        random.seed()
        self._scale_len = random.randrange(5, 8)

        # Generate a key
        self._root = random.choice(['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab'])

        # Generate the scale in terms of intervals from the root note
        self._notes = self._generate_scale()

        self._notes.sort()
        # FIXME checking sanity
        print(self._notes)

    # Generates a scale that:
    #   - Avoids large clusters of notes
    #   - Contains enough traditionally harmonic content 
    #       for at least a couple chords and melodic ideas
    def _generate_scale(self):

        notes = []
        valid_scale = False
        while not valid_scale:

            notes = []

            # Always include the 1
            notes.append(0)

            # Generate the scale
            for i in range(self._scale_len - 1):

                # Generate the note
                new_note = 0
                while new_note in notes:
                    new_note = random.randrange(1, 12)
                notes.append(new_note)


            # Check for "clumps" 
            # No more than 2 notes should be sequential
            for i in range(1, self._scale_len):

                # Reset search counter
                search_attempts = 0
                
                while (
                    notes[i] - 1 in notes and notes[i] + 1 in notes
                    ) or (
                    notes[i] - 1 in notes and notes[i] - 2 in notes
                    ) or (
                    notes[i] + 1 in notes and notes[i] + 2 in notes
                    ): 

                    # Generate a candidate note not already in the list
                    candidate = random.randrange(1, 12)
                    while candidate in notes:
                        candidate = random.randrange(1, 12)
                    notes[i] = candidate

                    search_attempts += 1

                    # If a scale has gotten stuck, randomly change one of the values by 1 and try again
                    if search_attempts >= (11 - self._scale_len):
                        note_mod_pos = random.randrange(1, self._scale_len)
                        offset = random.choice([-1, 1])
                        while (notes[note_mod_pos] + offset) in notes:
                            note_mod_pos = random.randrange(1, self._scale_len)
                            offset = random.choice([-1, 1])
                        notes[note_mod_pos] += offset
                        search_attempts = 0
            
            # Scales as-is are unlikely to lend themselves to 
            # nice chords or comfortable melodies. We'll normalize
            # a bit in the following ways:

            # Ensure each scale has at least two perfect fifths somewhere
            num_fifths = 0
            for n in notes:
                if (n + 7) % 12 in notes:
                    num_fifths += 1
            
            if num_fifths < 2:
                # Always add the perfect fifth up from the root for simplicity
                notes.append(7)
                
                # If another is required, generate a random one
                if num_fifths < 1:
                    notes.sort()
                    new_base = random.choice(notes[1:])
                    new_note = (new_base + 7) % 12
                    while new_note in notes:
                        new_base = random.choice(notes[1:])
                        new_note = (new_base + 7) % 12
                    notes.append(new_note)

            # Ensure each scale has at least three thirds somewhere
            num_thirds = 0
            for n in notes:
                if (n + 3) % 12 in notes or (n + 4) % 12 in notes:
                    num_thirds += 1
            
            if num_thirds < 3:
                # Always add either the major or minor third up from the root for simplicity
                offset = random.choice([0,1])
                if 8 + offset not in notes:
                    notes.append(3 + offset)
                else:
                    notes.append(3) if offset else notes.append(9)
                
                # If more are required, generate random ones
                if num_thirds < 2:
                    notes.sort()
                    new_third = (random.choice(notes[1:]) + random.choice([3, 4])) % 12
                    while new_third in notes:
                        new_third = (random.choice(notes[1:]) + random.choice([3, 4])) % 12
                    notes.append(new_third)
                if num_thirds < 1:
                    notes.sort()
                    new_third = (random.choice(notes[1:]) + random.choice([3, 4])) % 12
                    while new_third in notes:
                        new_third = (random.choice(notes[1:]) + random.choice([3, 4])) % 12
                    notes.append(new_third)

            # Ensure each scale has at least three sixths somewhere
            num_sixths = 0
            for n in notes:
                if (n + 8) % 12 in notes or (n + 49) % 12 in notes:
                    num_sixths += 1
            
            if num_sixths < 3:
                # Always add either the major or minor sixth up from the root for simplicity
                offset = random.choice([0,1])
                if 8 + offset not in notes:
                    notes.append(8 + offset)
                else:
                    notes.append(8) if offset else notes.append(9)
                
                # If more are required, generate random ones
                if num_sixths < 2:
                    notes.sort()
                    new_sixth = (random.choice(notes[1:]) + random.choice([8, 9])) % 12
                    while new_sixth in notes:
                        new_sixth = (random.choice(notes[1:]) + random.choice([8, 9])) % 12
                    notes.append(new_sixth)
                if num_sixths < 1:
                    notes.sort()
                    new_sixth = (random.choice(notes[1:]) + random.choice([8, 9])) % 12
                    while new_sixth in notes:
                        new_sixth = (random.choice(notes[1:]) + random.choice([8, 9])) % 12
                    notes.append(new_sixth)

            # These operations have a good chance of creating a scale
            # whose root makes more sense on a note other than 0. To
            # account for this, we find a candidate root and shift the
            # other values in accordance.
            likely_root = 0
            for n in notes:
                
                # Start by making sure the note in question is the root of a valid
                # major or minor chord, as we want our tonic to have that feature.
                if ((((n + 3) % 12) in notes) or (((n + 4) % 12) in notes)) and (
                    ((n + 7) % 12) in notes):

                    # As a tiebreaker, we'll check if the dominant of n is in the scale and
                    # itself is the root of a valid major or minor chord.
                    # This should happen rarely enough to not need further tiebreakers, so
                    # this loop will arbitrarily select the highest value for which this is true.
                    if (((n + 7) % 12) in notes) and (
                        (((n + 7 + 3) % 12) in notes) or (((n + 7 + 4) % 12) in notes)) and (
                        ((n + 7 + 7) % 12) in notes):
                        likely_root = n

            # Rotate if needed
            if likely_root != 0:
                for i in range(self._scale_len):
                    notes[i] -= likely_root
                    if notes[i] < 0:
                        notes[i] = 12 + notes[i]

            # Make sure some common issues have been resolved
            if (notes[0] == 0) and (                         
                ((3 in notes) or (4 in notes)) and (7 in notes)      
            ): 
                valid_scale = True
        return notes

if __name__ == "__main__":
    scale_test = Scale()
    scale_test = Scale()
    scale_test = Scale()
    scale_test = Scale()
    scale_test = Scale()
    scale_test = Scale()
    scale_test = Scale()
    scale_test = Scale()
    scale_test = Scale()
    scale_test = Scale()