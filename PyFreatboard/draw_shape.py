from matplotlib import pyplot as plt, patches
from PyFreatboard.definitions import PyFreatboard as PF

class DrawShape:
    
    def __init__(self, min_freats=3, freat_size=20, string_separation=10):
        self.min_freats = min_freats
        self.freat_size = freat_size
        self.string_separation = string_separation
        self.dot_size = 4.4
        self.font_size = 14

    def draw(self, shape, text=PF.TEXT_FUNCTION, shape_name=None, init_freat=None, show_string_names=True, return_fig=False, show_extension=True):
        self.text = text
        figure, axes = plt.subplots(dpi=100)
        max_f, min_f = shape.get_max_min_freat()
        if init_freat is not None:
            min_f = init_freat    
        self.__draw_freatboard__(axes, max_f - min_f, min_f, shape_name, show_string_names)
        for f in shape.fingers:
            x = (f.freat - min_f)*self.freat_size + self.freat_size/2
            y = 5*self.string_separation - PF.STRINGS.index(f.string)*self.string_separation
            if f.function == '1':
                if f.visual == 0:
                    circle = plt.Circle((x, y), self.dot_size, color='tomato', fill=True, zorder=2)
                else:
                    circle = plt.Circle((x, y), self.dot_size, color='pink', fill=True, zorder=2)        
            else:
                if f.visual == 0:
                    circle = plt.Circle((x, y), self.dot_size, color='k', fill=True, zorder=2)
                else:
                    circle = plt.Circle((x, y), self.dot_size, color='gray', fill=True, zorder=2)
                    
            axes.add_artist(circle)
            if show_extension:
                if f.finger in ['1s', '4s']:
                    circle = plt.Circle((x, y), self.dot_size+0.5, color='r', fill=False, zorder=2)
                axes.add_artist(circle)
            self.__add_finger_text__(axes, shape, x, y, f)
        if return_fig:
            return figure
        else:
            plt.show()
       
    def draw_vertical(self, shape, text=PF.TEXT_FUNCTION, shape_name=None, init_freat=None, show_string_names=False, return_fig=False):
        self.min_freats = 2
        self.dot_size = 5
        self.string_separation = 13
        self.font_size = 18
        self.text = text
        crosses_strings = [True]*6
        figure, axes = plt.subplots(dpi=100)
        max_f, min_f = shape.get_max_min_freat()
        if init_freat is not None:
            min_f = init_freat    
        freats = max_f - min_f
        if freats < self.min_freats:
            freats = self.min_freats
        self.__draw_freatboard_vertical__(axes, freats, min_f, shape_name, show_string_names)
        self.__draw_barrel__(shape, min_f, axes)
        for f in shape.fingers:
            crosses_strings[PF.STRINGS.index(f.string)] = False
            y = (f.freat - min_f)*self.freat_size + self.freat_size/2
            x = 5*self.string_separation - PF.STRINGS.index(f.string)*self.string_separation
            if f.function == '1':
                circle = plt.Circle((x, y), self.dot_size*1.2, color='tomato', fill=True, zorder=2)
            else:
                circle = plt.Circle((x, y), self.dot_size*1.2, color='k', fill=True, zorder=2)
            axes.add_artist(circle)
            self.__add_finger_text__(axes, shape, x, y, f, is_vertical=True)
            if self.text != PF.TEXT_FINGER:
                axes.text(x - 2, self.freat_size*(freats + 1.4), f.finger, fontsize=self.font_size)
    
        for e, c in enumerate(crosses_strings):
            if c:
                x = 5*self.string_separation - e*self.string_separation
                axes.text(x - 2, -2, 'X', fontsize=self.font_size)
    
        if return_fig:
            return figure
        else:
            plt.show()

    def __draw_barrel__(self, shape, min_f, axes):
        barrel_fingers = []
        for f in shape.fingers:
            if f.barrel:
                barrel_fingers.append(f)
        min_pos = [999, 999]
        max_pos = [-999, -999]
        if len(barrel_fingers) >= 2:
            for f in barrel_fingers:
                y = (f.freat - min_f)*self.freat_size + self.freat_size/2
                x = 5*self.string_separation - PF.STRINGS.index(f.string)*self.string_separation
                if x < min_pos[0]:
                    min_pos[0] = x
                if x > max_pos[0]:
                    max_pos[0] = x
                if y < min_pos[1]:
                    min_pos[1] = y
                if y > max_pos[1]:
                    max_pos[1] = y
            circle = plt.Circle(min_pos, self.dot_size*1.4, color='darkgray', fill=True, zorder=2)
            axes.add_artist(circle)
            circle = plt.Circle(max_pos, self.dot_size*1.4, color='darkgray', fill=True, zorder=2)
            axes.add_artist(circle)
            rect = patches.Rectangle((min_pos[0], min_pos[1] - self.dot_size*1.45), max_pos[0]-min_pos[0], self.dot_size*2.8 , color='darkgray', zorder=2)
            axes.add_patch(rect)

    def __draw_freatboard__(self, axes, freats, init_freat, shape_name, show_string_names):
        if freats < self.min_freats:
            freats = self.min_freats
        

        for s in range(6): # strings
            axes.plot([0, freats*self.freat_size + self.freat_size], [s*self.string_separation, s*self.string_separation], '-', color='gray')
        for f in range(freats + 1): # freats
            axes.plot([self.freat_size*f, self.freat_size*f], [0, self.string_separation*5], 'k-')
        if show_string_names:
            for e, t in enumerate(PF.STRINGS): # string names
                axes.text(-self.string_separation + (self.string_separation/5), self.string_separation*5-(self.string_separation/10) - e*self.string_separation, t, fontsize=self.font_size)
        if init_freat <= 1: # if initial freat draw double line
            axes.plot([1, 1], [0, self.string_separation*5], 'k-')
        axes.axis('off')
        
        # Draw freat symbols
        freat_symbols = [3, 5, 7, 9, 12, 15, 17]
        for s in freat_symbols:
            x = (s - init_freat)*self.freat_size + self.freat_size/2
            if x > 0 and x < (freats + 1)*self.freat_size:
                if s == 12:
                    y = 1.5*self.string_separation
                    circle = plt.Circle((x, y), self.dot_size/2, color='silver', fill=True)
                    axes.add_artist(circle)
                    y = 3.5*self.string_separation
                    circle = plt.Circle((x, y), self.dot_size/2, color='silver', fill=True)
                    axes.add_artist(circle)
                else:
                    y = 2.5*self.string_separation
                    circle = plt.Circle((x, y), self.dot_size/2, color='silver', fill=True)
                    axes.add_artist(circle)

        # Add starting fret
        plt.text(4, -self.string_separation*1.2, str(init_freat)+" fr", fontsize=self.font_size)
        axes.set_aspect(1)
        axes.set_xlim(-self.freat_size/4, (freats+1)*self.freat_size)
        axes.set_ylim(-self.freat_size, self.string_separation*7)

        # Add shape name
        if shape_name is not None:
            axes.text(0, self.string_separation*6, shape_name, fontsize=self.font_size)

    def __draw_freatboard_vertical__(self, axes, freats, init_freat, shape_name, show_string_names):    
        for s in range(6): # strings
            axes.plot([s*self.string_separation, s*self.string_separation], [0, (freats + 1) * self.freat_size], '-', color='gray')
        for f in range(freats + 1): # freats
            axes.plot([0, self.string_separation*5], [self.freat_size*f, self.freat_size*f], 'k-')
        if show_string_names:
            for e, t in enumerate(PF.STRINGS_REVERSE): # string names
                axes.text(e*self.string_separation - 2 , -2, t, fontsize=self.font_size)
        if init_freat <= 1: # if initial freat draw double line
            axes.plot([0, self.string_separation*5], [1, 1], 'k-')
        axes.axis('off')
        
        # Draw freat symbols
        freat_symbols = [3, 5, 7, 9, 12, 15, 17]
        for s in freat_symbols:
            if (s - init_freat) >= 0 and (s - init_freat) < (freats + 1):
                y = (s - init_freat)*self.freat_size + self.freat_size/2
                if s == 12:
                    x = 1.5*self.string_separation
                    circle = plt.Circle((x, y), self.dot_size/2, color='lightgray', fill=True)
                    axes.add_artist(circle)
                    x = 3.5*self.string_separation
                    circle = plt.Circle((x, y), self.dot_size/2, color='lightgray', fill=True)
                    axes.add_artist(circle)
                else:
                    x = 2.5*self.string_separation
                    circle = plt.Circle((x, y), self.dot_size/2, color='lightgray', fill=True)
                    axes.add_artist(circle)

        # Add starting fret
        plt.text(self.string_separation * 5.6, self.freat_size/1.5, str(init_freat) + " fr", fontsize=self.font_size)
        axes.set_aspect(1)
        axes.set_xlim(-self.string_separation, self.string_separation*7)
        axes.set_ylim((freats+1)*self.freat_size, -self.freat_size/4)
    
        # Add shape name
        if shape_name is not None:
            axes.text(0, -self.freat_size/2, shape_name, fontsize=self.font_size*1.2) #1.5
    
    def __add_finger_text__(self, axes, shape, x, y, f, is_vertical=False):
        if is_vertical:
            y_offset = -1.5 - (self.font_size - 12) * 0.1
        else:
            y_offset = 1.5 + (self.font_size - 12) * 0.1
        
        len1 = 1.75 + (self.font_size - 12) * 0.14
        len2 = 3.5 + (self.font_size - 12) * 0.14
        len3 = 3.5 + (self.font_size - 12) * 0.14

        size = self.font_size
        l = len1
        if len(f.function) == 2:
            l = len2
        elif len(f.function) == 3:
            l = len3
            size = self.font_size * 0.8

        if self.text == PF.TEXT_FUNCTION:
            axes.text(x-l, y-y_offset, f.function, fontsize=size, color='white')
        elif self.text == PF.TEXT_FINGER:
            axes.text(x-l, y-y_offset, f.finger, fontsize=size, color='white')
        elif self.text == PF.TEXT_PITCH:
            note = f.pitch
            axes.text(x-l, y-y_offset, note, fontsize=size, color='white')
           