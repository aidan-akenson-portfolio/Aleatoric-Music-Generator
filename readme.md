## This project will randomly generate a song with the following features:  
- The song will be broken up into some combination of verses, choruses, and bridges. Some songs may not include a bridge. 
- Two scales will be generated, one for the verse, and one for the chorus. The bridge will pick one of these scales to use. Each scale includes 5-7 notes, and is generated in such a way as to ensure a certain number of triads exist for use in harmony. 
- As a result of the scale generation method, the chord progression generation has been altered. Rather than picking one of a set list of chord progressions, each section will generate a random chord progression from its scale. Generation logic includes provisions such as: progressions will always start on the tonic, two consecutive chords should not share a root, chords will attempt to be diatonic (but if a suitable diatonic chord is not found, it will generate as major or minor), and final chords in progressions have a chance to be a 7 chord.   
- Each progression is either 4 or 8 measures, and generates with an associated harmonic rhythm. Measures may contain one or two chords, in which case they will be spaced out equally. Each song section repeats the progression 2 or 4 times, meaning that a song section has a minimum length of 8 measures, and a maximum length of 32 measures.
- Each song section has its own melody. Melodies are generated on an eighth-note grid using a "phrase seeding" method. A number of phrases per melody are determined, and the starting points for these melodies are dispersed throughout the grid. From there, each phrase generates a random number of notes at nearby positions after the seed. The duration each note is held is also randomized. Seeds are more likely to generate on beat 1, less so on beat 3, less still on beats 2 and 4, and even less on the ands.
- The pitches for each melody are generated primarily, but not completely, from the associated scale. First, two "favorite" notes are chosen, so that the melody has more cohesion than pure randomness. Then, weights are assigned to probabilities of choosing a favorite, diatonic, or non-diatonic note. The weights are generated inversely proportional to the amount of notes of its type that have already been generated.
- The melody and harmony play on independent synths. The synth for the chords will be a sine wave with moderately slow attack, reverb at 100% wet, and a lowpass filter. The synth for the melody is a saw wave with faster attack, reverb at 50% wet, and a lowpass filter with a higher cutoff than that of the chords.
- Tempo is randomized between 80 and 160 BPM.


## TO-DO:
- Allow for .wav writing directly from the program


## Limitations:
- The melody generation is weak. No contour logic exists, so melodies still feel a bit aimless. Additionally, pitches are generated sequentially, meaning that the favorite notes tend to be frontloaded, producing unnatural repetition in many outputs.
- The scales, despite attempts to the contrary, seem to generate with augmented chords for a tonic on several occasions. Line 229 of Scale.py seems to expressly prohibit this, so I'm not sure why this is the case.
- No bass or rhythm instruments have been implemented.
- Time signature is locked to 4/4