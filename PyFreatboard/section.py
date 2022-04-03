class Section:
    def __init__(self, root, type):
        self.root = root
        self.type = type
        self.chords = []
    
    def add_chord(self, chord):
        self.chords.append(chord)
    
    def __str__(self):
        return "{} {}: ".format(self.root, self.type) + ", ".join(str(c) for c in self.chords)


class Chord:
    def __init__(self, root, type, duration):
        self.root = root
        self.type = type
        self.duration = duration
        self.melody = {}
    
    def add_melody(self, id, notes):
        self.melody[id] = notes

    def __str__(self):
        return "{}{} ({})".format(self.root, self.type, self.duration)
class Note:
    def __init__(self, pitch, duration, octave):
        self.pitch = pitch
        self.duration = duration
        self.octave = octave
    
    def __str__(self):
        return "{}/{}({})".format(self.pitch, self.octave, self.duration)