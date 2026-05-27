import random
import Scale

SIGNATURE = 4

class Melody(Scale.Scale):
    def __init__(self, len: int = 4):
        self._8th_note_grid = self._gen_rhythm(len)

    def _gen_rhythm(self, measures: int = 4):
        # Grid of eighth notes
        grid = []
        for i in range(measures * SIGNATURE * 2):
            grid.append([0])

        # Limit the number of phrases proportionally to the duration of the melody
        num_phrases = [measures // 2, (measures * 3) // 2]
        min_phrase_offset = SIGNATURE * 2

        # First go through and generate the "seeds" of phrases
        seeds = 0
        pos = 0
        previous_seed_pos = random.randrange(0, 3)
        new_seed_chance = 33        # 0-100


        # FIXME infinite recursion here sometimes??
        grid[previous_seed_pos] = 1
        while pos < len(grid) and (seeds < num_phrases[0] or seeds > num_phrases[1]):

            # If valid position for a seed to generate
            if abs(pos - previous_seed_pos) > min_phrase_offset:

                print(pos, new_seed_chance)

                # Attempt to generate a seed
                if random.randrange(0, 100) > new_seed_chance:
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

        print(grid)
                


if __name__ == "__main__":
    melody = Melody()