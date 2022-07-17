import copy
from PyFreatboard.finger import Finger
from PyFreatboard.definitions import PyFreatboard

class Shape:
    
    # TODO: Move all definitions to definitions file!
    # SHAPE_TYPE = {'ARPEGGIO': 0, 'STRUM': 1}
    # SHAPE_TYPE_INV = ['arpeggio', 'strum']
    
    # TODO: Missing several augmented and diminished
    # INTERVAL = {'2m': (1, 1), '2M': (1, 2), '3m': (2, 3), '3M': (2, 4), '4dism': (3, 4), '4': (3, 5), '4aug': (3, 6), '5dism': (4, 6), '5': (4, 7), '5aug': (4, 8), '6m': (5, 8), '6M': (5, 9), '7m': (6, 10), '7M': (6, 11)} # 'Interval name': (notes, semitones)
   
    def __init__(self, fingers, shape_type=PyFreatboard.SHAPE_TYPE['ARPEGGIO']):
        self.fingers = fingers
        self.valid = True
        self.type = shape_type

    def __add__(self, a):
        return Shape(self.fingers + a)

    def get_max_min_freat(self):
        min_f = 100
        max_f = -100
        for f in self.fingers:
            min_f = min(min_f, f.freat)
            max_f = max(max_f, f.freat)
        return max_f, min_f

    def set_fingering(self):
        self.__set_fingering__(False)
        if not self.valid:
            self.__set_fingering__(True)
        
        return copy.deepcopy(self)
    
    def get_extensions(self):
        assert len(self.fingers) > 0
        if self.fingers[0].finger == '':
            self.set_fingering()
        num_extensions = 0
        for f in self.fingers:
            if f.finger == '1s' or f.finger == '4s':
                num_extensions += 1
        return num_extensions


    def transpose(self, interval):
        over_12_freat = True
        for f in self.fingers:
            f.freat += interval[1]
            if f.freat <= 12:
                over_12_freat = False
        if over_12_freat:
            for f in self.fingers:
                f.freat -= 12

        for f in self.fingers:
            f.pitch = Shape.__transpose_pitch__(f.pitch, interval)
            f.semitone = Finger.NOTES[f.pitch]

    def to_xml(self):
        return "   <shape>\n    <type>{}</type>\n    <fingers>\n{}\n    </fingers>\n   </shape>".format(PyFreatboard.SHAPE_TYPE_INV[self.type], '\n'.join([f.to_xml() for f in self.fingers]))
    
    @staticmethod
    def get_interval(pitch1, pitch2):
        pitch1_note = Finger.NOTES7.index(pitch1[0])
        pitch2_note = Finger.NOTES7.index(pitch2[0])
        note_interval = (pitch2_note - pitch1_note) % 7
        semitones1 = Finger.NOTES[pitch1]
        semitones2 = Finger.NOTES[pitch2]
        semitones_interval = (semitones2 - semitones1) % 12
        return (note_interval, semitones_interval)

    @staticmethod
    def __transpose_pitch__(pitch, interval):
        pitch_note = Finger.NOTES7.index(pitch[0])
        base_note = Finger.NOTES7[(pitch_note + interval[0])%7]
        semitones = (Finger.NOTES[pitch] + interval[1]) % 12
        for k, s in zip(Finger.NOTES.keys(), Finger.NOTES.values()):
            if s == semitones:
                if k[0] == base_note:
                    return k
        print("Error: Could not transpose pitch")
        return None

    def __set_fingering__(self, priority_4s):
        self.valid = True
        max_f, min_f = self.get_max_min_freat()
        last_finger = '0'
        
        if max_f - min_f <= 3:
            # one finger per freat
            for f in self.fingers:
                f.finger = str(f.freat - min_f + 1)

        elif (max_f - min_f == 4) and priority_4s:
            # 4th finger extension
            for f in self.fingers:
                f.finger = str(f.freat - min_f + 1)
                if f.finger == '5':
                    f.finger = "4s"
                    if last_finger == '4' or last_finger == '4s' or last_finger == '1s':
                        self.valid = False
                if f.finger == '1' and last_finger =='1s':
                    self.valid = False
                last_finger = f.finger
        
        elif (max_f - min_f == 4) and not priority_4s:
            # 4th finger extension
            for f in self.fingers:
                f.finger = str(f.freat - min_f)
                if f.finger == '0':
                    f.finger = "1s"
                    if last_finger == '1' or last_finger == '1s' or last_finger == '4s':
                        self.valid = False
                if f.finger == '1' and last_finger =='1s':
                    self.valid = False
                last_finger = f.finger
        
        elif max_f - min_f == 5:
            # 4th finger and 1st finger extensions
            for f in self.fingers:
                f.finger = str(f.freat - min_f)
                if f.finger == '5':
                    f.finger = "4s"
                    if last_finger == '4' or last_finger == '4s' or last_finger == '1s':
                        self.valid = False
                elif f.finger == '0':
                    f.finger = '1s'
                    if last_finger == '1' or last_finger == '1s' or last_finger == '4s':
                        self.valid = False
                if f.finger == '1' and last_finger =='1s':
                    self.valid = False
                last_finger = f.finger
        else:
            self.valid = False

    def __lt__(self, shape):
        return self.get_max_min_freat()[1] < shape.get_max_min_freat()[1]
