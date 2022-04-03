from song_xml import parse_song_xml
from build_shape import BuildShape
from draw_freatboard import DrawFreatboard


class Song:
    """Song class"""

    def __init__(self, xml_file_path):
        """Parse XML song file into Song Object"""
        t, a, s = parse_song_xml(xml_file_path)
        self.title = t
        self.author = a
        self.sections = s
        self.shapes = Song.__get_shapes__(self.sections)

    def draw_shapes(self, init_freat):
        draw = DrawFreatboard()
        for shape_name, all_shapes in zip(self.shapes.keys(), self.shapes.values()):
            for e, shape in enumerate(all_shapes.all_shapes):
                if shape.valid:
                    min_freat = shape.get_max_min_freat()[1]
                    if min_freat == init_freat or (min_freat + 1) == init_freat:
                        f = draw.draw_shape(shape, shape_name=shape_name, return_fig=True)
                        f.savefig('__{}_{}.png'.format(shape_name, e), bbox_inches='tight')
                    
    def __str__(self):
        return "{} by {}".format(self.title, self.author) + "\n- " + "\n- ".join(str(s) for s in self.sections)

    @staticmethod
    def __get_shapes__(sections):
        """Get all shapes from song"""
        shapes = {}
        for section in sections:
            key = section.root + section.type
            if key not in shapes:
                shapes[key] = BuildShape(section.root, section.type)

            for chord in section.chords:
                key = chord.root + chord.type
                if key not in shapes:
                    shapes[key] = BuildShape(chord.root, chord.type)
        return shapes
    
    # TODO: get_drops from all chords
    
if __name__ == '__main__':
    song = Song("/home/narcis/PyFreatboard/autumn_leaves.xml")
    print(song)
    song.draw_shapes(7)
