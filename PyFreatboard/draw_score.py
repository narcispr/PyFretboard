from matplotlib import pyplot as plt, patches
from matplotlib import font_manager
from PyFreatboard.definitions import PyFreatboard as PF
import time

class DrawScore:
    def __init__(self):
        font_dirs = ['../']
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)

        # set font
        plt.rcParams['font.family'] = 'Musisync'
    

    def draw(self, shape, text=PF.TEXT_FUNCTION, fingering=False, shape_name=None, return_fig=False):
        fig, ax = plt.subplots(dpi=100)
        
        factor = self.__create_score__(ax, len(shape.fingers))

        for i, f in enumerate(shape.fingers):
            position_mult = 0
            # TODO: FIx that!!
            if shape.type == PF.SHAPE_TYPE['ARPEGGIO'] or shape.type == 'ARPEGGIO':
                position_mult = 1
            self.__draw_note__(ax, f.pitch, f.octave-1, i*position_mult, factor)
        if return_fig:
            return fig
        else:
            plt.show()

    def __create_score__(self, ax, length=11):
        for i in range(5):
            ax.plot([0, 60+length*30], [i*10, i*10], 'k')

        factor = 400/(60+length*30)
        ax.axis('equal')
        ax.axis('off')
        ax.text(10, 0, 'G', fontsize=50*factor)
        return  factor # factor to scale font size

    def __draw_note__(self, ax, note, octave, position, factor=1):

        pitch = {'C': -14, 'D': -9, 'E': -4, 'F': 1, 'G': 6, 'A': 11, 'B': 16}
        text = "w"
        x = 60 + position * 30
        if len(note) > 1: 
            x -= 9
            if note[1] == 'b':
                text = "bw"
            elif note[1] == '#':
                text = "Bw"
        y = pitch[note[0]] + octave*35

        if y <= -14:
            x_bar = x
            if len(note) > 1:
                x_bar += 10
            
            for i in range(-14, y-1, -10):
                ax.plot([x_bar-2, x_bar+15], [i+3.5, i+3.5], 'k')

        ax.text(x, y, text, fontsize=30*factor)
    
    def __del__(self):
        time.sleep(2)
        plt.rcParams['font.family'] = 'sans-serif'
        