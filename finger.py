class Finger:
    guitar_strings = ['e', 'B', 'G', 'D', 'A', 'E']
    strings_semitones = [24, 19, 15, 10, 5, 0]

    def __init__(self, semitone, function, string, freat, finger=""):
        self.semitone = semitone
        self.function = function
        self.string = string
        self.freat = freat
        self.finger = finger
        
    def dist(self, f):
        s_num = Finger.guitar_strings.index(self.string)
        f_num = Finger.guitar_strings.index(f.string)
        return (Finger.strings_semitones[s_num] + self.freat) - (Finger.strings_semitones[f_num] + f.freat)
        
    def __eq__(self, f):
        return self.freat == f.freat and self.string == f.string and self.finger == f.finger

    def __str__(self):
        return "{} ({}) --> [{}/{}]({})".format(self.semitone, self.function, self.string, self.freat, self.finger)
