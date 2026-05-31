import random
import numpy as np

import Scale
import ntom

SIGNATURE = 4

class Melody(Scale.Scale):

    def __init__(self, length: int = 4):

        super().__init__()
        
        random.seed()
        self._8th_note_grid = self._gen_rhythm(length)
        self._num_notes = 0
        for i in self._8th_note_grid:
            if i != 0:
                self._num_notes += 1

        #print(self._8th_note_grid)

        self._pitches = self._gen_pitches()
        self._pitch_index = 0
        #print(self._pitches)

        self.simple_grid = []
        for i in range(len(self._8th_note_grid)):
            if self._8th_note_grid[i] == 2:
                self.simple_grid.append(1)
            elif self._8th_note_grid[i] == 3:
                self.simple_grid.append(0)
            else:
                self.simple_grid.append(self._8th_note_grid[i])

    def _gen_rhythm(self, measures: int = 4):
        # Grid of eighth notes
        grid = []
        for i in range(measures * SIGNATURE * 2):
            grid.append(0)

        # Limit the number of phrases proportionally to the duration of the melody
        num_phrases = [random.choice([measures // 2, measures // 2 + 1]), random.choice([(measures * 3) // 2 - 1, (measures * 3) // 2])]
        min_phrase_offset = SIGNATURE * 2

        # First go through and generate the "seeds" of phrases, denoted as ones.
        seeds = 0
        pos = 0
        previous_seed_pos = random.randrange(0, 4)  # Starting note
        new_seed_chance = 33        # 0-100
        grid[previous_seed_pos] = 1
        while pos < len(grid) and (seeds < num_phrases[0] or seeds > num_phrases[1]):

            # If valid position for a seed to generate
            if abs(pos - previous_seed_pos) > min_phrase_offset:

                # More likely if on a downbeat
                rhythm_chance = -2
                if (pos % 2) == 0:
                    rhythm_chance = 0
                elif (pos % 4) == 0:
                    rhythm_chance = 2
                elif (pos % 8) == 0:
                    rhythm_chance = 4
                else:
                    rhythm_chance = -2

                # Attempt to generate a seed, 
                if random.randrange(0, 100) < new_seed_chance + (rhythm_chance * 10):
                    grid[pos] = 1

                # If succeeded, update trackers
                if grid[pos] == 1:
                    seeds += 1
                    previous_seed_pos = pos
                    new_seed_chance = 0

                # If failed, increase chance for a seed next time
                else:
                    new_seed_chance += 10

            # Always slightly increment
            new_seed_chance += 3

            # Update position
            pos += 1
            # If end has been reached with no success, wrap around
            if pos >= len(grid) and (seeds < num_phrases[0] or seeds > num_phrases[1]):
                pos = 0

        # print("\n\nSEED POSITIONS:", grid)

        # Now generate the rhythm for each phrase
        # print("\n\nADDITIONAL NOTES")
        for i in range(len(grid)):
            # print()
            # print()
            # print("==========", i, "==========")
            if grid[i] == 0:
                pass
            if grid[i] == 2:
                # print("Added note at index", i)
                pass
            elif grid[i] == 1:
                pos_start = i
                while pos_start < len(grid) and grid[pos_start] != 1:
                    pos_start += 1
                pos_end = int(min(pos + 1, len(grid)))
                while  pos_end < len(grid) and grid[pos_end] != 1:
                    pos_end += 1
                phrase_len = int(min(10, max(pos_end - pos_start, 2)))

                num_notes_in_phrase = random.randrange(2, max(3, phrase_len // 2))
                # print("This phrase contains", num_notes_in_phrase, "notes")
                within_phrase_positions = []
                new_pos = None
                num_notes_so_far = 1    # Count the first note when considering density
                    
                attempts = 0
                while num_notes_so_far < num_notes_in_phrase and num_notes_so_far < len(grid) - i:
                    new_pos = i + random.randrange(1, phrase_len)
                    # print("Attempting to generate an index of a new note:", new_pos)
                    while ((new_pos in within_phrase_positions) or (new_pos > pos_end) or (grid[new_pos] != 0)) and attempts < 20:
                        offset_1 = random.randrange(1, phrase_len)
                        offset_2 = random.randrange(1, phrase_len + 1)
                        new_pos = min((len(grid) - offset_1), int(i + offset_2))
                        attempts += 1
                        # print("Attempting to generate an index of a new note:", new_pos)
                    within_phrase_positions.append(new_pos)
                    # print("Adding note at index", new_pos)
                    num_notes_so_far += 1
                        
                # Additional new notes in the phrase are denoted as twos
                for j in within_phrase_positions:
                    grid[j % len(grid)] = 2


        # Generate time until release from each played note
        # print("\n\nHOLD TIMING")
        for i in range(1, len(grid)):
            # print()
            # print()
            # print("==========", i, "==========")
            if grid[i] != 0:
                # print("Not empty: grid[i] =", grid[i])
                pass
            if grid[i] == 0 and (grid[i % len(grid) - 1] != 0):
                # Held notes are denoted as threes
                # print(i % len(grid), grid[i % len(grid)], )
                weight = 0.3
                # print("initial weight:", weight)
                # Notes that have a long time until the next note are more likely to be held
                until_next_note = 1
                while[i % len(grid) + until_next_note] == 0:
                    until_next_note += 1
                # print("additional weight given due to length bonus:", until_next_note * 0.1, "due to having", until_next_note, "notes until the next")
                weight += until_next_note * 0.1

                # Notes that previously had an initial value rather than a continued sustain
                # should be weighted higher, but only slightly
                if grid[i % len(grid) - 1] != 3:
                    # print("2 branch taken, adding 0.2 to weight. Weight:", weight)
                    weight += 0.2

                # print("resulting weight:", weight)
                if weight > 1:
                    # print("Capping weight to 1")
                    weight = 1

                control_val = random.randrange(1, 100)
                likelihood = weight * 100
                if control_val < likelihood and i < len(grid):
                    # print("Weight check passed:", likelihood, ">", control_val)
                    grid[i] = 3
                else:
                    pass
                    # print("Weight check failed:", likelihood, "<", control_val)
            else:
                pass
                # print("No previous note")

        return grid

    def _gen_pitches(self):
        pitches = []
        root = -1
        match self._note_names[0]:
            case "A":
                root = ntom.AB_VALUES[2]
                if root < 45:
                    root = ntom.AB_VALUES[3]
            case "Bb" | "A#":
                root = ntom.BB_VALUES[2]
                if root < 45:
                    root = ntom.BB_VALUES[3]
            case "B":
                root = ntom.B_VALUES[2]
                if root < 45:
                    root = ntom.B_VALUES[3]
            case "C":
                root = ntom.C_VALUES[2]
                if root < 45:
                    root = ntom.C_VALUES[3]
            case "Db" | "C#":
                root = ntom.DB_VALUES[2]
                if root < 45:
                    root = ntom.DB_VALUES[3]
            case "D":
                root = ntom.D_VALUES[2]
                if root < 45:
                    root = ntom.DB_VALUES[3]
            case "Eb" | "D#":
                root = ntom.EB_VALUES[2]
                if root < 45:
                    root = ntom.EB_VALUES[3]
            case "E":
                root = ntom.E_VALUES[2]
                if root < 45:
                    root = ntom.E_VALUES[3]
            case "F":
                root = ntom.F_VALUES[2]
                if root < 45:
                    root = ntom.F_VALUES[3]
            case "Gb" | "F#":
                root = ntom.GB_VALUES[2]
                if root < 45:
                    root = ntom.GB_VALUES[3]
            case "G":
                root = ntom.G_VALUES[2]
                if root < 45:
                    root = ntom.G_VALUES[3]
            case "Ab" | "G#":
                root = ntom.AB_VALUES[2]
                if root < 45:
                    root = ntom.AB_VALUES[3]
            case _:
                print("Cannot convert value to MIDI:", self._note_names[0])
        
        # Each melody should lean on a couple notes in the scale to give 
        # it more cohesive ideas.
        favorite_notes = [root + self._notes[random.randrange(self._scale_len - 1)], root + self._notes[random.randrange(self._scale_len - 1)]]
        while favorite_notes[1] == favorite_notes[0]:
            favorite_notes[1] = root + self._notes[random.randrange(self._scale_len - 1)]

        # Generate the notes   
        num_favs = 0   
        num_diatonic = 0
        pitch_pos = 0
        for i in range(len(self._8th_note_grid)):
            if self._8th_note_grid[i] != 0:

                favorite_weight = int((1 - ((num_favs * 2) / self._num_notes)) * 100)
                if len(pitches) > 1 and pitches[pitch_pos - 1] in favorite_notes:
                    favorite_weight -= 30
                diatonic_weight = int((1 - ((num_diatonic / 2) / self._num_notes)) * 100)

                # First check for favorite notes
                if random.randrange(100) < favorite_weight:
                    pitches.append(favorite_notes[random.randrange(0,1)])
                    num_favs += 1
                    num_diatonic += 1

                # Next, likely to generate a diatonic note
                elif random.randrange(100) < diatonic_weight:
                    pitches.append(root + self._notes[random.randrange(self._scale_len - 1)])
                    num_diatonic += 1

                # Else generate a random note that is within 2 half-steps of a favorite note
                else:
                    offset = random.choice([-2, -1, 1, 2])
                    pitches.append(favorite_notes[random.randrange(0,1)] + offset)

                pitch_pos += 1
            
        # Last check, if melody is too low just raise it all up by an octave
        if np.average(pitches) < 53:
            for p in pitches:
                p += 12

        return pitches
               


if __name__ == "__main__":

    sum = 0
    melody = Melody()