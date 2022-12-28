from PIL import Image
import numpy as np
from PyFretboard.song import Song
from PyFretboard.draw_shape import DrawShape
from PyFretboard.definitions import PyFretboard as PF
from PyFretboard.draw_score import DrawScore

def get_first_black_pixel(data):
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j] != 255:
                print(data[i,j])
                return i

def get_last_black_pixel(data):
    for i in range(data.shape[0]-1, 0, -1):
        for j in range(data.shape[1]):
            if data[i, j] != 255:
                return i

def crop_image(name):
    img = Image.open(name).convert('L')
    data = np.array(img)
    first = get_first_black_pixel(data)
    last = get_last_black_pixel(data)
    img1 = img.crop((0, first, data.shape[1], last))
    img1.save("crop_" + name)

# Draw chords
def get_chord(chord_root, chord_type, use_drop2=False, use_drop3=False):
    draw = DrawShape()
    chords = Song("/home/narcis/PyFretboard/shapes_xml/chords.xml")
    shapes = chords.chord_shapes
    if use_drop2:
        drop2_chords = Song("/home/narcis/PyFretboard/shapes_xml/drop2.xml")
        shapes.update(drop2_chords.chord_shapes)
    if use_drop3:
        drop3_chords = Song("/home/narcis/PyFretboard/shapes_xml/drop3.xml")
        shapes.update(drop3_chords.chord_shapes)
    
        
    ds = DrawScore()
    idx = 0
    for i, k in enumerate(shapes.keys()):
        s = chords.chord_shapes[k]
        root = s[0]
        type = s[1]
        shape = s[2]
        if type == chord_type:
            interval = shape.get_interval(root, chord_root)
            shape.transpose(interval)
            f = draw.draw_vertical(shape, text=PF.TEXT_FUNCTION, return_fig=True)
            f.savefig("chord_{}_{}_{}.png".format(chord_root, chord_type, idx), dpi=300, bbox_inches='tight', pad_inches=0)
            fs = ds.draw(shape, fingering=False, return_fig=True, tab=False)
            fs.savefig("score_chord_{}_{}_{}.png".format(chord_root, chord_type, idx), dpi=600, bbox_inches='tight', pad_inches=0)
            crop_image("score_chord_{}_{}_{}.png".format(chord_root, chord_type, idx))
            idx += 1