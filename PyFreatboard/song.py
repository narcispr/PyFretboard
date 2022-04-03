from PyFreatboard.song_xml import parse_song_xml
from PyFreatboard.build_shape import BuildShape
from PyFreatboard.draw_freatboard import DrawFreatboard
from os.path import join

class Song:
    """Song class"""

    def __init__(self, xml_file_path):
        """Parse XML song file into Song Object"""
        self.title, self.author, self.sections = parse_song_xml(xml_file_path)
        self.scale_shapes = Song.__get_scales__(self.sections)
        self.arpeggio_shapes = Song.__get_arpeggios__(self.sections)
        self.drop2_shapes = Song.__get_drops2__(self.sections)
        
    def get_scales(self):
        return self.scale_shapes
    
    def get_arpeggios(self):
        return self.arpeggio_shapes
    
    def get_drops2(self):
        return self.drop2_shapes

    def get_melody(self, melody_id):
        melody = []
        for s in self.sections:
            for c in s.chords:
                for m in c.melody.keys():
                    if m == melody_id:
                        melody += c.melody[m]
        return melody
    
    def __str__(self):
        return "{} by {}".format(self.title, self.author) + "\n- " + "\n- ".join(str(s) for s in self.sections)

    
    @staticmethod
    def __get_scales__(sections):
        """Get all scale shapes from song"""
        shapes = {}
        for section in sections:
            key = section.root + section.type
            if key not in shapes:
                shapes[key] = BuildShape(section.root, section.type).all_shapes
        return shapes

    @staticmethod
    def __get_arpeggios__(sections):
        """Get all shapes from song"""
        shapes = {}
        for section in sections:
            for chord in section.chords:
                key = chord.root + chord.type
                if key not in shapes:
                    shapes[key] = BuildShape(chord.root, chord.type).all_shapes
        return shapes
    
    @staticmethod
    def __get_drops2__(sections):
        shapes = {}
        for section in sections:
            for chord in section.chords:
                key = chord.root + chord.type
                if key not in shapes:
                    sh = BuildShape(chord.root, chord.type)
                    shapes[key] = sh.build_drop(drop=2, bass_string='D')
        return shapes

    @staticmethod
    def draw_shapes(shapes, path='.', init_freat=None, vertical=False):
        draw = DrawFreatboard()
        for shape_name, all_shapes in zip(shapes.keys(), shapes.values()):
            for e, shape in enumerate(all_shapes):
                if shape.valid:
                    min_freat = shape.get_max_min_freat()[1]
                    if init_freat is None or min_freat == init_freat or (min_freat + 1) == init_freat:
                        if vertical:
                            f = draw.draw_shape_vertical(shape, shape_name=shape_name, return_fig=True)
                        else:
                            f = draw.draw_shape(shape, shape_name=shape_name, return_fig=True)
                        f.savefig(join(path, '__{}_{}.png'.format(shape_name, e)), bbox_inches='tight')
