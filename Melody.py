import random
import numpy as np

import Scale

SIGNATURE = 4

class Melody(Scale.Scale):
    def __init__(self, len: int = 4):
        random.seed()
        self._8th_note_grid = self._gen_rhythm(len)
        print(self._8th_note_grid)

        self._pitches = self._gen_pitches()
        self._pitch_index = 0
        print(self._pitches)

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

                # Attempt to generate a seed
                if random.randrange(0, 100) < new_seed_chance:
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
                    
                while num_notes_so_far < num_notes_in_phrase:
                    new_pos = i + random.randrange(1, phrase_len)
                    # print("Attempting to generate an index of a new note:", new_pos)
                    while (new_pos in within_phrase_positions) or (new_pos > pos_end) or (grid[new_pos] != 0):
                        offset_1 = random.randrange(1, phrase_len)
                        offset_2 = random.randrange(1, phrase_len + 1)
                        new_pos = min((len(grid) - offset_1), int(i + offset_2))
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
        for i in range(len(self._8th_note_grid)):

            if self._8th_note_grid[i] != 0:
                # FIXME just to test
                pitches.append(65)

        return pitches
               


if __name__ == "__main__":

    sum = 0
    melody = Melody()