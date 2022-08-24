class PyFreatboard:
    STRINGS = ['e', 'B', 'G', 'D', 'A', 'E']
    STRINGS_REVERSE = ['E', 'A', 'D', 'G', 'B', 'e']
    NOTE_NAME = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']
    NOTES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'Fb': 4, 'E#': 5, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A':9, 'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11, 'B#': 0}
    TEXT_NONE = 0
    TEXT_FUNCTION = 1
    TEXT_FINGER = 2
    TEXT_PITCH = 3
    SHAPE_TYPE = {'ARPEGGIO': 0, 'STRUM': 1}
    SHAPE_TYPE_INV = ['arpeggio', 'strum']
    STRING_TO_TAB={'E':-110, 'A': -100, 'D': -90, 'G': -80, 'B':-70, 'e': -60}
    def __init__(self):
        pass
