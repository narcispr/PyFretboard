import csv
import copy
import sys

from shape import Shape
from finger import Finger
from draw_freatboard import DrawFreatboard


class BuildShape:
    SHAPES_FILE = 'shapes.csv'
    NOTES = {'C': 0, 'C#': 1, 'D': 2, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A':9, 'Bb': 10, 'B': 11}
    INTERVALS = {'1': 0, 'b2': 1, '2': 2, '#2': 3, 'b3': 3, '3': 4, '#3': 5, 'b4': 4, '4': 5, '#4': 6, 'b5': 6, '5': 7, '#5': 8, 'b6': 8, '6': 9, '#6': 10, 'b7': 10, '7': 11, 'b9': 12, '9': 13, '#9': 14, 'b11': 14, '11': 15, '#11': 16, 'b13': 16, '13': 17, '#13': 18}

    def __init__(self, root, shape_type, plot_type=1):
        self.root = root
        self.shape_type = shape_type
        self.plot_type = plot_type
        self.all_shapes = self.scale_to_freatboard()

        # Set fingering for each shape
        shapes_with_fingers = []
        for i in range(len(self.all_shapes)):
            shapes_with_fingers.append(self.all_shapes[i].set_fingering())
        self.all_shapes = shapes_with_fingers

        # Filter not_valid or redundant shapes
        self.filter_shapes()

    def plot(self):
        for s in self.all_shapes:
            if not s.not_valid:
                s.plot(self.plot_type)

    def scale_to_freatboard(self):
        all_shapes = []
        scale, harmony = self.create_shape()
        fingers = self.__semitone_to_freat__(scale, harmony, Finger.guitar_strings)
            
        for r in fingers:
            if r.string == 'E':
                shape = Shape([r])
                self.fill_shape(shape, harmony, (harmony.index(r.function) + 1) % len(harmony), fingers, all_shapes, r.freat, r.freat)
            
        return all_shapes

    def create_shape(self):
        shapes_file = self.__load_shape_file__(BuildShape.SHAPES_FILE)
        harmony = shapes_file[self.shape_type]
        shape_notes = []
        for note in harmony:
            shape_notes.append((BuildShape.NOTES[self.root] + BuildShape.INTERVALS[note]) % 12)
        return shape_notes, harmony


    def fill_shape(self, shape, harmony, pointer, fingers, all_shapes, min_freat, max_freat, depth=0):
        valid_fingers = []
        for f in fingers:
            if f.function == harmony[pointer] and f.dist(shape.fingers[-1]) > 0 and f.dist(shape.fingers[-1]) < 12 and abs(f.freat - shape.fingers[-1].freat) < 5:
                valid_fingers.append(f)
        if len(valid_fingers) > 0:
            for f in valid_fingers:
                new_min = min(min_freat, f.freat)
                new_max = max(max_freat, f.freat)
                if new_max - new_min < 5 and new_min > 0:
                    self.fill_shape(shape + [f], harmony, (pointer + 1)%len(harmony), fingers, all_shapes, new_min, new_max, depth+1)
                elif shape.fingers[-1].string == 'e':
                    all_shapes.append(shape)
        else:
            all_shapes.append(shape)
            
    def __semitone_to_freat__(self, semitone, function, guitar_strings):
        fingers = []
        if not isinstance(semitone, list):
            semitone = [semitone]
        for n, h in zip(semitone, function):
            for string in guitar_strings:
                freat = n - BuildShape.NOTES[string.upper()]
                if freat < 0:
                    freat += 12
                fingers.append(Finger(n, h, string, freat, None))
                if freat < 5:
                    fingers.append(Finger(n, h, string, freat + 12, None))    
        return fingers

    def __load_shape_file__(self, filename):
        shapes_file = {}
        with open(filename, newline='') as csv_file:
            shapes_reader = csv.reader(csv_file, delimiter=',', quotechar='#')
            for row in shapes_reader:
                harmony = []
                name = ""
                first = True
                for item in row:
                    if first:  
                        name = item.strip()
                        first = False
                    else:
                        harmony.append(item.strip())
                shapes_file[name] = harmony
        return shapes_file

    def filter_shapes(self):
        self.all_shapes.sort()
        for i, s in enumerate(self.all_shapes):
            extensions = s.get_extensions()
            if extensions >= 4:
                s.not_valid = True
            if not s.not_valid:
                # Remove same position with less notes in 6th string
                last_finger = s.fingers[-1]
                for j, s2 in enumerate(self.all_shapes[i+1:]):
                    if not s2.not_valid and s2.fingers[-1] == last_finger and len(s2.fingers) != len(s.fingers):
                        same_shape = True
                        k = 1
                        while same_shape and k < min(len(s.fingers), len(s2.fingers)):
                            index = -1 - k
                            if s.fingers[index] == s2.fingers[index]:
                                k += 1
                            else:
                                same_shape = False
                        if same_shape:
                            if len(s2.fingers) < len(s.fingers):
                                s2.not_valid = True
                            else:
                                s.not_valid = True

                # Remove same position with more extensions
                first_finger = s.fingers[0]
                for j, s2 in enumerate(self.all_shapes[i+1:]):
                    if not s2.not_valid and s2.fingers[0] == first_finger:
                        if s2.get_extensions() >= extensions:
                            s2.not_valid = True
                        else:
                            s.not_valid = True
        
if __name__ == "__main__":
    plot_type = DrawFreatboard.TEXT_FINGER
    if len(sys.argv) == 3:
        BuildShape(sys.argv[1], sys.argv[2], plot_type=plot_type).plot()
    elif len(sys.argv) == 4:
        shapes = BuildShape(sys.argv[1], sys.argv[2])
        for s in shapes.all_shapes:
            f_max, f_min = s.get_max_min_freat()
            if not s.not_valid and int(sys.argv[3]) >= f_min and int(sys.argv[3]) <= f_max:
                s.plot(plot_type)
    else:
        print("Usage: python3 {} <root> <shape_type> [<freat_value>]".format(sys.argv[0]))