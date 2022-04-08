class Section:
    def __init__(self):
        self.scale = []
        self.chord = []
    
    def add_scale(self, scale):
        self.scale.append(scale)

    def add_chord(self, chord):
        self.chord.append(chord)
    
    def __str__(self):
        return ", ".join(str(s) for s in self.scale) + "[" + ", ".join(str(c) for c in self.chord) + "]"

class Scale:
    def __init__(self, root, type):
        self.root = root
        self.type = type
        self.shape = {}

    def __str__(self):
        return "{} {}: ".format(self.root, self.type) + ", ".join(str(s) for s in self.shape)

class Chord:
    def __init__(self, root, type, duration, bass=None):
        self.root = root
        self.bass = bass
        self.type = type
        self.duration = duration
        self.melody = {}
        self.shape = {}
    
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