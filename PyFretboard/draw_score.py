# from tkinter.font import Font
from matplotlib import pyplot as plt
from matplotlib import font_manager
from PyFretboard.definitions import PyFretboard as PF
import math

class DrawScore:
    def __init__(self):
        # Load music font
        font_dirs = ['../']
        font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

        for font_file in font_files:
            font_manager.fontManager.addfont(font_file)

        

    def draw(self, shape, text=PF.TEXT_FUNCTION, fingering=False, shape_name=None, return_fig=False, tab=False):
        fig, ax = plt.subplots(dpi=100)
        alterations={'C': False, 'D': False, 'E': False, 'F': False, 'G': False, 'A': False, 'B': False}
        last_pitch = (-1, -1)
        # TODO: FIx that!!
        position_mult = 0
        length = len(shape.fingers)
        if shape.type == PF.SHAPE_TYPE['ARPEGGIO'] or shape.type == 'ARPEGGIO':
            position_mult = 1
        else:
            length = 3

        factor = self.__create_score__(ax, length, position_mult, tab)
       
        for i, f in enumerate(shape.fingers):
            
            sub_text = ""
            if text == PF.TEXT_FUNCTION and position_mult == 1:
                sub_text = f.function
            sup_text = ""
            if fingering and position_mult == 1:
                sup_text = f.finger
            offset = False
            if position_mult == 0 and last_pitch[1] >= 0:
                if self.__close_pitch__(last_pitch, (f.pitch, f.octave)):
                    offset = True
            x = self.__draw_note__(ax, f.pitch, f.octave-1, i*position_mult, alterations, factor, sub_text, sup_text, offset)
            last_pitch = (f.pitch, f.octave)

            if tab:
                y = PF.STRING_TO_TAB[f.string] - 5
                ax.text(x, y, f.fret, fontsize=(8*factor+position_mult), fontname='DejaVu Sans', weight='bold')



        l = len(shape.fingers)*30 + 27 + 30*position_mult
        ax.plot([l]*2, [0, 40], 'k', )
        ax.plot([l+3]*2, [0, 40], 'k', linewidth=1)
        ax.plot([l+3.25]*2, [0, 40], 'k', linewidth=1)
        ax.plot([l+3.5]*2, [0, 40], 'k', linewidth=1)
        ax.plot([l+3.75]*2, [0, 40], 'k', linewidth=1)
        ax.plot([l+4]*2, [0, 40], 'k', linewidth=1)

        if tab:
            ax.plot([l]*2, [-110, -60], 'k', )
            ax.plot([l+3]*2, [-110, -60], 'k', linewidth=1)
            ax.plot([l+3.25]*2, [-110, -60], 'k', linewidth=1)
            ax.plot([l+3.5]*2, [-110, -60], 'k', linewidth=1)
            ax.plot([l+3.75]*2, [-110, -60], 'k', linewidth=1)
            ax.plot([l+4]*2, [-110, -60], 'k', linewidth=1)
        

        if return_fig:
            return fig
        else:
            plt.show()

    def __close_pitch__(self, pitch1, pitch2):
        semitones1 = PF.NOTES[pitch1[0]] + 12*pitch1[1]
        semitones2 = PF.NOTES[pitch2[0]] + 12*pitch2[1]
        return abs(semitones1 - semitones2) < 3
        
    def __create_score__(self, ax, length=11, mult=1, tab=False):
        for i in range(5):
            ax.plot([0, 60+length*30], [i*10, i*10], 'k')

        ax.plot([0, 10], [80, 80], 'w')

        factor = 100/(math.sqrt(length+1)*30)
        if not tab and length < 5: 
            factor *= 2
        if length <= 10 and length > 5:
            print("Arpeggio!")
            factor *= 1.4
        
        ax.axis('equal')
        ax.axis('off')
        ax.text(10, 0, 'G', fontsize=50*factor, fontname='Musisync')

        if tab:
            for i in range(6):
                ax.plot([0, 60+length*30], [i*10-110, i*10-110], 'k')
            ax.plot([0, 0], [-110, 40], 'k')
            ax.text(10, -75, 'T', fontsize=12*factor, fontname='DejaVu Sans', weight='bold')
            ax.text(10, -90, 'A', fontsize=12*factor, fontname='DejaVu Sans', weight='bold')
            ax.text(10, -105, 'B', fontsize=12*factor, fontname='DejaVu Sans', weight='bold')
            
        return  factor # factor to scale font size

    def __draw_note__(self, ax, note, octave, position, alterations, factor=1, sub_text="", super_text="", offset=False):
        bool_alteration = False
        pitch = {'C': -14, 'D': -9, 'E': -4, 'F': 1, 'G': 6, 'A': 11, 'B': 16}
        text = "w"
        x = 60 + position * 30
        if len(note) > 1: 
            if not offset:
                x -= 12
            if note[1] == 'b':
                text = "bw"
                alterations[note[0]] = True
                bool_alteration = True
            elif note[1] == '#':
                alterations[note[0]] = True
                text = "Bw"
                bool_alteration = True
        elif alterations[note[0]]:
            if not offset:
                x -= 11
            text = "½w"
            alterations[note[0]] = False
            bool_alteration = True
        elif offset:
            x += 14
        y = pitch[note[0]] + octave*35 - 1
        
        # If dditional lines below first one are required
        if y <= -14:
            x_bar = x
            if bool_alteration:
                x_bar += 10
            
            for i in range(-14, y-1, -10):
                ax.plot([x_bar-2, x_bar+18], [i+3.5, i+3.5], 'k')
        
        # If dditional lines over last one are required
        if y >= 45:
            x_bar = x
            if bool_alteration:
                x_bar += 10
            for i in range(46, y+2, 10):
                ax.plot([x_bar-2, x_bar+18], [i+4, i+4], 'k')

        ax.text(x, y, text, fontsize=30*factor, fontname='Musisync')
        
        # Draw sub and super text
        y_sub_text = -20
        if y_sub_text >= (y-20):
            y_sub_text = y-20
        y_super_text = 50
        if y_super_text <= (y+20):
            y_super_text = y+20
        
        x_text = x
        if bool_alteration:
            x_text += 10
    
        ax.text(x_text, y_sub_text, sub_text, fontsize=10*factor, fontname='DejaVu Sans')
        ax.text(x_text, y_super_text, super_text, fontsize=10*factor, fontname='DejaVu Sans')
        return 60 + position * 30
