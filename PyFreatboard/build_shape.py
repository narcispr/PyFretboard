from PyFreatboard.shape import Shape
from PyFreatboard.finger import Finger
from PyFreatboard.draw_freatboard import DrawFreatboard


class BuildShape:
    SHAPES = {
        'TriadMaj' : ['1', '3', '5'],
        'TriadMin' : ['1', 'b3', '5'],
        'TriadAug' : ['1', '3', '#5'],
        'TriadDism' : ['1', 'b3', 'b5'],
        '7' : ['1', '3', '5', 'b7'],
        '7b9' : ['b2', '3', '5', 'b7'],
        '6' : ['1', '3', '5', '6'],
        '-6' : ['1', 'b3', '5', '6'],
        '-7' : ['1', 'b3', '5', 'b7'],
        'Maj7' : ['1', '3', '5', '7'],
        '-7b5' : ['1', 'b3', 'b5', 'b7'],
        'º7' : ['1', 'b3', 'b5', '6'],
        'dism' : ['1', 'b3', 'b5', '6'],
        'Major' : ['1', '2', '3', '4', '5', '6', '7'],
        'Minor' : ['1', '2', 'b3', '4', '5', 'b6', 'b7'],
        'Harmonic' : ['1', '2', 'b3', '4', '5', 'b6', '7'],
        'Pentatonic' : ['1', 'b3', '4', '5', 'b7'],
        'PentatonicMaj' : ['1', '2', '3', '5', '6'],
        'Diminished' : ['1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7'],
        'Whole-half' : ['1', '2', 'b3', 'b4', 'b5', 'b6', 'b7'],
        'Ionian' : ['1', '2', '3', '4', '5', '6', '7'],
        'Dorian' : ['1', '2', 'b3', '4', '5', '6', 'b7'],
        'Phrygian' : ['1', 'b2', 'b3', '4', '5', 'b6', 'b7'],
        'Lydian' : ['1', '2', '3', '#4', '5', '6', '7'],
        'Mixolydian' : ['1', '2', '3', '4', '5', '6', 'b7'],
        'Aeolian' : ['1', '2', 'b3', '4', '5', 'b6', 'b7'],
        'Locrian' : ['1', 'b2', 'b3', '4', 'b5', 'b6', 'b7'],
        'Mixolydianb9#9b13' : ['1', 'b2', '#2', '3', '4', '5', 'b6', 'b7']
    }

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

        # Filter invalid or redundant shapes
        self.all_shapes = self.filter_shapes(self.all_shapes)
                
    def scale_to_freatboard(self):
        all_shapes = []
        scale, harmony = self.get_shape_notes_and_harmony()
        fingers = self.__semitone_to_finger__(scale, harmony, Finger.guitar_strings)
            
        for r in fingers:
            if r.string == 'E':
                shape = Shape([r])
                self.fill_shape(shape, harmony, (harmony.index(r.function) + 1) % len(harmony), fingers, all_shapes, r.freat, r.freat)
            
        return all_shapes

    def get_shape_notes_and_harmony(self):
        shapes_file = BuildShape.SHAPES
        harmony = shapes_file[self.shape_type]
        shape_notes = []
        for note in harmony:
            shape_notes.append((Finger.NOTES[self.root] + Finger.INTERVALS[note]) % 12)
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
            
    def __semitone_to_finger__(self, semitone, function, guitar_strings):
        fingers = []
        if not isinstance(semitone, list):
            semitone = [semitone]
        for n, h in zip(semitone, function):
            for string in guitar_strings:
                freat = n - Finger.NOTES[string.upper()]
                if freat < 0:
                    freat += 12
                fingers.append(Finger(n, h, string, freat, None))
                if freat < 5:
                    fingers.append(Finger(n, h, string, freat + 12, None))    
        return fingers

    def filter_shapes(self, shapes):
        shapes.sort()
        for i, s in enumerate(shapes):
            extensions = s.get_extensions()
            if extensions >= 4:
                s.valid = False
            if s.valid:
                # Remove same position with less notes in 6th string
                last_finger = s.fingers[-1]
                for j, s2 in enumerate(shapes[i+1:]):
                    if s2.valid and s2.fingers[-1] == last_finger and len(s2.fingers) != len(s.fingers):
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
                                s2.valid = False
                            else:
                                s.valid = False

                # Remove same position with more extensions
                first_finger = s.fingers[0]
                for j, s2 in enumerate(shapes[i+1:]):
                    if s2.valid and s2.fingers[0] == first_finger:
                        if s2.get_extensions() >= extensions:
                            s2.valid = False
                        else:
                            s.valid = False
        return shapes

    def build_drop(self, drop=2, bass_string='D'):
        notes, harmony = self.get_shape_notes_and_harmony()
        assert drop > 1 and drop < len(notes)
        all_drops = []
        
        for i in range(len(notes)):
            # get inversion
            inv_notes = notes[i:] + notes[:i]
            inv_h = harmony[i:] + harmony[:i]
            # apply drop
            bass = [inv_notes[-drop]]
            bass_h = [inv_h[-drop]]
            pre_drop = inv_notes[:-drop]
            pre_drop_h = inv_h[:-drop]
            post_drop = inv_notes[-(drop-1):]
            post_drop_h = inv_h[-(drop-1):]
            if isinstance(pre_drop, int):
                pre_drop = [pre_drop]
                pre_drop_h = [pre_drop_h]
            if isinstance(post_drop, int):
                post_drop = [post_drop]
                post_drop_h = [post_drop_h]
            
            drop_notes = bass + pre_drop + post_drop
            drop_h = bass_h + pre_drop_h + post_drop_h
            fingers = self.__semitone_to_finger__(drop_notes, drop_h, Finger.guitar_strings)
            all_drops_tmp = []    
            for r in fingers:
                if r.string == bass_string:
                    shape = Shape([r])
                    self.fill_shape(shape, drop_h, (drop_h.index(r.function) + 1) % len(drop_h), fingers, all_drops_tmp, r.freat, r.freat)
                
            all_drops += all_drops_tmp

        # Set fingering for each shape
        shapes_with_fingers = []
        for i in range(len(all_drops)):
            shapes_with_fingers.append(all_drops[i].set_fingering())
        all_drops = shapes_with_fingers

        # Filter invalid or redundant shapes
        # all_drops = self.filter_shapes(all_drops)
        all_drops = self.filter_drops(all_drops, len(notes))
        all_drops.sort()
        return all_drops
        
    def filter_drops(self, drops, length):
        for d in drops:
            if d.valid:
                max, min = d.get_max_min_freat()
                if max - min > 3:
                    d.valid = False
                if min == 0:
                    d.valid = False
                if len(d.fingers) < length:
                    d.valid = False
                elif len(d.fingers) > length:
                    d.fingers = d.fingers[:length]
                
                for f1 in range(len(d.fingers)):
                    for f2 in range(f1+1, len(d.fingers)):
                        if d.fingers[f1].string == d.fingers[f2].string:
                            d.valid = False
                
                for f in range(len(d.fingers) - 1):
                    if Finger.guitar_strings.index(d.fingers[f].string) != (Finger.guitar_strings.index(d.fingers[f+1].string) + 1):
                        d.valid = False
        return drops

if __name__ == "__main__":
    drop = BuildShape('D', '-7', 1)
    drops = drop.build_drop(drop=2, bass_string="A")
    for d in drops:
        if d.valid:
           d.plot(plot_type=DrawFreatboard.TEXT_NOTE)
