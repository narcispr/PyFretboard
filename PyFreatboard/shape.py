import copy
from PyFreatboard.draw_freatboard import DrawFreatboard

class Shape:
    def __init__(self, fingers):
        self.fingers = fingers
        self.valid = True

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
    
    def get_extensions(self):
        assert len(self.fingers) > 0
        if self.fingers[0].finger == '':
            self.set_fingering()
        num_extensions = 0
        for f in self.fingers:
            if f.finger == '1s' or f.finger == '4s':
                num_extensions += 1
        return num_extensions

    def __lt__(self, shape):
        return self.get_max_min_freat()[1] < shape.get_max_min_freat()[1]
