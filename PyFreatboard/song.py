from PyFreatboard.song_xml import parse_song_xml
from PyFreatboard.build_shape import BuildShape
from PyFreatboard.draw_shape import DrawShape
from os.path import join

class Song:
    """Song class"""

    def __init__(self, xml_file_path, autogen_shapes=False):
        """Parse XML song file into Song Object"""
        self.title, self.author, self.sections = parse_song_xml(xml_file_path)
        if autogen_shapes:
            self.scale_shapes = Song.__gen_scales__(self.sections)
            self.arpeggio_shapes = Song.__gen_arpeggios__(self.sections)
            self.drop2_shapes = Song.__gen_drops2__(self.sections)
        else:
            self.scale_shapes = Song.__get_scales__(self.sections)
            self.chord_shapes = Song.__get_chords__(self.sections)
            # self.arpeggio_shapes = []
            # self.drop2_shapes = []

    def get_scales(self):
        return self.scale_shapes
    
    def get_arpeggios(self):
        return self.arpeggio_shapes
    
    def get_drops2(self):
        return self.drop2_shapes

    def get_melody(self, melody_id):
        melody = []
        for s in self.sections:
            for c in s.chord:
                for m in c.melody.keys():
                    if m == melody_id:
                        melody += c.melody[m]
        return melody
    
    def __str__(self):
        return "{} by {}".format(self.title, self.author) + "\n- " + "\n- ".join(str(s) for s in self.sections)

    
    @staticmethod
    def __gen_scales__(sections):
        """Get all scale shapes from song"""
        shapes = {}
        for section in sections:
            for scale in section.scale:
                key = scale.root + scale.type
                if key not in shapes:
                    shapes[key] = BuildShape(scale.root, scale.type).all_shapes
        return shapes

    @staticmethod
    def __gen_arpeggios__(sections):
        """Get all shapes from song"""
        shapes = {}
        for section in sections:
            for chord in section.chord:
                key = chord.root + chord.type
                if key not in shapes:
                    shapes[key] = BuildShape(chord.root, chord.type).all_shapes
        return shapes
    
    @staticmethod
    def __gen_drops2__(sections):
        shapes = {}
        for section in sections:
            for chord in section.chord:
                key = chord.root + chord.type
                if key not in shapes:
                    sh = BuildShape(chord.root, chord.type)
                    shapes[key] = sh.build_drop(drop=2, bass_string='D')
        return shapes

    @staticmethod
    def __get_chords__(sections):
        shapes = {}
        for section in sections:
            for chord in section.chord:
                for shape_id in chord.shape.keys():
                    if chord.bass is not None:
                        key = "{}/{} {} {}".format(chord.root, chord.bass, chord.type, shape_id)
                    else:
                        key = "{} {} {}".format(chord.root, chord.type, shape_id)

                    if key not in shapes:
                        shapes[key] = chord.shape[shape_id]
        return shapes 
    
    @staticmethod
    def __get_scales__(sections):
        shapes = {}
        for section in sections:
            for scale in section.scale:
                for shape_id in scale.shape.keys():
                    key = "{} {} {}".format(scale.root, scale.type, shape_id)
                    if key not in shapes:
                        shapes[key] = scale.shape[shape_id]
        return shapes 

    @staticmethod
    def draw_shapes(shapes, path='.', init_freat=None, vertical=False):
        draw = DrawShape()
        for shape_name, all_shapes in zip(shapes.keys(), shapes.values()):
            for e, shape in enumerate(all_shapes):
                if shape.valid:
                    min_freat = shape.get_max_min_freat()[1]
                    if init_freat is None or min_freat == init_freat or (min_freat + 1) == init_freat:
                        if vertical:
                            f = draw.draw_vertical(shape, shape_name=shape_name, return_fig=True)
                        else:
                            f = draw.draw(shape, shape_name=shape_name, return_fig=True)
                        f.savefig(join(path, '__{}_{}.png'.format(shape_name, e)), bbox_inches='tight')
