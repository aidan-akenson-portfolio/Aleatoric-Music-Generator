NOTE_NAMES = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab']
NOTE_NAMES_SHARPS = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
NOTE_NAMES_FLATS = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

MAJOR_ROOTS = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
SHARP_ROOTS_MAJOR = ['A', 'B', 'D', 'E', 'C', 'G']
FLAT_ROOTS_MAJOR = ['Bb', 'Db', 'Eb', 'F', 'G', 'Ab']

MINOR_ROOTS = ['A', 'Bb', 'B', 'C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab']
SHARP_ROOTS_MINOR = ['A', 'B', 'C#', 'E', 'F#']
FLAT_ROOTS_MINOR = ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'Ab']


def major(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MAJOR_ROOTS[root_pos] != root:
        root_pos += 1

    major_chord = [root]

    if root in SHARP_ROOTS_MAJOR:
        major_chord.append(NOTE_NAMES_SHARPS[(root_pos + 4) % 12])
        major_chord.append(NOTE_NAMES_SHARPS[(root_pos + 7) % 12])
    else:
        major_chord.append(NOTE_NAMES_FLATS[(root_pos + 4) % 12])
        major_chord.append(NOTE_NAMES_FLATS[(root_pos + 7) % 12])

    match inversion:
        case "root":
            pass
        case "first" | "1st":
            major_chord = major_chord[-1:] + major_chord[:-1]
        case "second" | "2nd":
            major_chord = major_chord[-2:] + major_chord[:-2]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return major_chord
def minor(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MINOR_ROOTS[root_pos] != root:
        root_pos += 1

    minor_chord = [root]

    if root in SHARP_ROOTS_MINOR:
        minor_chord.append(NOTE_NAMES_SHARPS[(root_pos + 3) % 12])
        minor_chord.append(NOTE_NAMES_SHARPS[(root_pos + 7) % 12])
    else:
        minor_chord.append(NOTE_NAMES_FLATS[(root_pos + 3) % 12])
        minor_chord.append(NOTE_NAMES_FLATS[(root_pos + 7) % 12])

    match inversion:
        case "root":
            pass
        case "first" | "1st":
            minor_chord = minor_chord[-1:] + minor_chord[:-1]
        case "second" | "2nd":
            minor_chord = minor_chord[-2:] + minor_chord[:-2]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return minor_chord
def diminished(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MINOR_ROOTS[root_pos] != root:
        root_pos += 1

    dim_chord = [root]

    if root in SHARP_ROOTS_MINOR:
        dim_chord.append(NOTE_NAMES_SHARPS[(root_pos + 3) % 12])
        dim_chord.append(NOTE_NAMES_SHARPS[(root_pos + 6) % 12])
    else:
        dim_chord.append(NOTE_NAMES_FLATS[(root_pos + 3) % 12])
        dim_chord.append(NOTE_NAMES_FLATS[(root_pos + 6) % 12])

    match inversion:
        case "root":
            pass
        case "first" | "1st":
            dim_chord = dim_chord[-1:] + dim_chord[:-1]
        case "second" | "2nd":
            dim_chord = dim_chord[-2:] + dim_chord[:-2]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return dim_chord
def augmented(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MAJOR_ROOTS[root_pos] != root:
        root_pos += 1

    aug_chord = [root]

    if root in SHARP_ROOTS_MAJOR:
        aug_chord.append(NOTE_NAMES_SHARPS[(root_pos + 4) % 12])
        aug_chord.append(NOTE_NAMES_SHARPS[(root_pos + 8) % 12])
    else:
        aug_chord.append(NOTE_NAMES_FLATS[(root_pos + 4) % 12])
        aug_chord.append(NOTE_NAMES_FLATS[(root_pos + 8) % 12])

    match inversion:
        case "root":
            pass
        case "first" | "1st":
            aug_chord = aug_chord[-1:] + aug_chord[:-1]
        case "second" | "2nd":
            aug_chord = aug_chord[-2:] + aug_chord[:-2]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return aug_chord

def dominant7(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MAJOR_ROOTS[root_pos] != root:
        root_pos += 1

    seven_chord = major(root)

    if root in SHARP_ROOTS_MAJOR:
        seven_chord.append(NOTE_NAMES_SHARPS[(root_pos + 10) % 12])
    else:
        seven_chord.append(NOTE_NAMES_FLATS[(root_pos + 10) % 12])


    match inversion:
        case "root":
            pass
        case "first" | "1st":
            seven_chord = seven_chord[-1:] + seven_chord[:-1]
        case "second" | "2nd":
            seven_chord = seven_chord[-2:] + seven_chord[:-2]
        case "third" | "3rd":
            seven_chord = seven_chord[-3:] + seven_chord[:-3]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return seven_chord
def major7(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MAJOR_ROOTS[root_pos] != root:
        root_pos += 1

    seven_chord = major(root)

    if root in SHARP_ROOTS_MAJOR:
        seven_chord.append(NOTE_NAMES_SHARPS[(root_pos + 11) % 12])
    else:
        seven_chord.append(NOTE_NAMES_FLATS[(root_pos + 11) % 12])


    match inversion:
        case "root":
            pass
        case "first" | "1st":
            seven_chord = seven_chord[-1:] + seven_chord[:-1]
        case "second" | "2nd":
            seven_chord = seven_chord[-2:] + seven_chord[:-2]
        case "third" | "3rd":
            seven_chord = seven_chord[-3:] + seven_chord[:-3]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return seven_chord
def minor7(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MINOR_ROOTS[root_pos] != root:
        root_pos += 1

    seven_chord = minor(root)

    if root in SHARP_ROOTS_MINOR:
        seven_chord.append(NOTE_NAMES_SHARPS[(root_pos + 10) % 12])
    else:
        seven_chord.append(NOTE_NAMES_FLATS[(root_pos + 10) % 12])


    match inversion:
        case "root":
            pass
        case "first" | "1st":
            seven_chord = seven_chord[-1:] + seven_chord[:-1]
        case "second" | "2nd":
            seven_chord = seven_chord[-2:] + seven_chord[:-2]
        case "third" | "3rd":
            seven_chord = seven_chord[-3:] + seven_chord[:-3]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return seven_chord
def half_dim7(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MINOR_ROOTS[root_pos] != root:
        root_pos += 1

    seven_chord = diminished(root)

    if root in SHARP_ROOTS_MINOR:
        seven_chord.append(NOTE_NAMES_SHARPS[(root_pos + 10) % 12])
    else:
        seven_chord.append(NOTE_NAMES_FLATS[(root_pos + 10) % 12])


    match inversion:
        case "root":
            pass
        case "first" | "1st":
            seven_chord = seven_chord[-1:] + seven_chord[:-1]
        case "second" | "2nd":
            seven_chord = seven_chord[-2:] + seven_chord[:-2]
        case "third" | "3rd":
            seven_chord = seven_chord[-3:] + seven_chord[:-3]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return seven_chord
def dim7(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MINOR_ROOTS[root_pos] != root:
        root_pos += 1

    seven_chord = diminished(root)

    if root in SHARP_ROOTS_MINOR:
        seven_chord.append(NOTE_NAMES_SHARPS[(root_pos + 9) % 12])
    else:
        seven_chord.append(NOTE_NAMES_SHARPS[(root_pos + 9) % 12])


    match inversion:
        case "root":
            pass
        case "first" | "1st":
            seven_chord = seven_chord[-1:] + seven_chord[:-1]
        case "second" | "2nd":
            seven_chord = seven_chord[-2:] + seven_chord[:-2]
        case "third" | "3rd":
            seven_chord = seven_chord[-3:] + seven_chord[:-3]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return seven_chord

def dominant9(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MAJOR_ROOTS[root_pos] != root:
        root_pos += 1

    nine_chord = dominant7(root)

    if root in SHARP_ROOTS_MAJOR:
        nine_chord.append(NOTE_NAMES_SHARPS[(root_pos + 14) % 12])
    else:
        nine_chord.append(NOTE_NAMES_FLATS[(root_pos + 14) % 12])

    match inversion:
        case "root":
            pass
        case "first" | "1st":
            nine_chord = nine_chord[-1:] + nine_chord[:-1]
        case "second" | "2nd":
            nine_chord = nine_chord[-2:] + nine_chord[:-2]
        case "third" | "3rd":
            nine_chord = nine_chord[-3:] + nine_chord[:-3]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return nine_chord
def seven_flat_9(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MAJOR_ROOTS[root_pos] != root:
        root_pos += 1

    nine_chord = dominant7(root)

    if root in SHARP_ROOTS_MAJOR:
        nine_chord.append(NOTE_NAMES_SHARPS[(root_pos + 13) % 12])
    else:
        nine_chord.append(NOTE_NAMES_FLATS[(root_pos + 13) % 12])

    match inversion:
        case "root":
            pass
        case "first" | "1st":
            nine_chord = nine_chord[-1:] + nine_chord[:-1]
        case "second" | "2nd":
            nine_chord = nine_chord[-2:] + nine_chord[:-2]
        case "third" | "3rd":
            nine_chord = nine_chord[-3:] + nine_chord[:-3]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return nine_chord
def minor9(root: str = "C", inversion: str = "root"):
    root = root.capitalize()
    inversion = inversion.lower()
    root_pos = 0
    while MINOR_ROOTS[root_pos] != root:
        root_pos += 1

    nine_chord = minor7(root)

    if root in SHARP_ROOTS_MINOR:
        nine_chord.append(NOTE_NAMES_SHARPS[(root_pos + 14) % 12])
    else:
        nine_chord.append(NOTE_NAMES_FLATS[(root_pos + 14) % 12])

    match inversion:
        case "root":
            pass
        case "first" | "1st":
            nine_chord = nine_chord[-1:] + nine_chord[:-1]
        case "second" | "2nd":
            nine_chord = nine_chord[-2:] + nine_chord[:-2]
        case "third" | "3rd":
            nine_chord = nine_chord[-3:] + nine_chord[:-3]
        case _:
            print("Unknown inversion specification provided, returning root inversion.")

    return nine_chord

# Only triads and 7 chords currently
def test_chords():
    print()
    for n in MAJOR_ROOTS:
        print(n, "MAJOR")
        print(major(n))
        print(major(n, "1st"))
        print(major(n, "2nd"))
    
    print()
    for n in MAJOR_ROOTS:
        print(n, "AUGMENTED")
        print(augmented(n))
        print(augmented(n, "1st"))
        print(augmented(n, "2nd"))
    
    print()
    for n in MINOR_ROOTS:
        print(n, "MINOR")
        print(minor(n))
        print(minor(n, "1st"))
        print(minor(n, "2nd"))
    
    print()
    for n in MINOR_ROOTS:
        print(n, "DIMINISHED")
        print(diminished(n))
        print(diminished(n, "1st"))
        print(diminished(n, "2nd"))
    
    print()
    for n in MAJOR_ROOTS:
        print(n, "7")
        print(dominant7(n))
        print(dominant7(n, "1st"))
        print(dominant7(n, "2nd"))
        print(dominant7(n, "3rd"))
    
    print()
    for n in MAJOR_ROOTS:
        print(n, "MAJOR 7")
        print(major7(n))
        print(major7(n, "1st"))
        print(major7(n, "2nd"))
        print(major7(n, "3rd"))
    
    print()
    for n in MINOR_ROOTS:
        print(n, "MINOR 7")
        print(minor7(n))
        print(minor7(n, "1st"))
        print(minor7(n, "2nd"))
        print(minor7(n, "3rd"))
    
    print()
    for n in MINOR_ROOTS:
        print(n, "ø 7")
        print(half_dim7(n))
        print(half_dim7(n, "1st"))
        print(half_dim7(n, "2nd"))
        print(half_dim7(n, "3rd"))
    
    print()
    for n in MINOR_ROOTS:
        print(n, "DIMINISHED 7")
        print(dim7(n))
        print(dim7(n, "1st"))
        print(dim7(n, "2nd"))
        print(dim7(n, "3rd"))

if __name__ == "__main__":
    
    test_chords()