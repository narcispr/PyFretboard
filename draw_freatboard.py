from matplotlib import pyplot as plt

class DrawFreatboard:
    STRINGS = ['e', 'B', 'G', 'D', 'A', 'E']
    TEXT_NONE = 0
    TEXT_FUNCTION = 1
    TEXT_FINGER = 2
    
    def __init__(self, shape, init_freat=None, min_freats=4, text=1):
        self.min_freats = min_freats
        self.figure, self.axes = plt.subplots(dpi=80)
        self.freat_size = 20
        self.string_separation = 10
        self.text = text
        self.__draw_shape__(shape, init_freat)
        
    def __draw_freatboard__(self, freats, init_freat):
        if freats < self.min_freats:
            freats = self.min_freats
        for s in range(6): # strings
            self.axes.plot([0, freats*self.freat_size + self.freat_size], [s*self.string_separation, s*self.string_separation], '-', color='gray')
        for f in range(freats + 1): # freats
            self.axes.plot([self.freat_size*f, self.freat_size*f], [0, self.string_separation*5], 'k-')
        for e, t in enumerate(DrawFreatboard.STRINGS): # string names
            self.axes.text(-self.string_separation + (self.string_separation/5), self.string_separation*5-(self.string_separation/10) - e*self.string_separation, t, fontsize=12)
        if init_freat <= 1: # if initial freat draw double line
            self.axes.plot([1, 1], [0, self.string_separation*5], 'k-')
        plt.axis('off')
        # Draw freat symbols
        freat_symbols = [3, 5, 7, 9, 12, 15, 17]
        for s in freat_symbols:
            x = (s - init_freat)*self.freat_size + self.freat_size/2
            if x > 0 and x < (freats + 1)*self.freat_size:
                if s == 12:
                    y = 1.5*self.string_separation
                    circle = plt.Circle((x, y), self.freat_size/10, color='lightgray', fill=True)
                    self.axes.add_artist(circle)
                    y = 3.5*self.string_separation
                    circle = plt.Circle((x, y), self.freat_size/10, color='lightgray', fill=True)
                    self.axes.add_artist(circle)
                else:
                    y = 2.5*self.string_separation
                    circle = plt.Circle((x, y), self.freat_size/10, color='lightgray', fill=True)
                    self.axes.add_artist(circle)

        # Add starting fret
        plt.text(8, -self.string_separation, str(init_freat), fontsize=12)
        self.axes.set_aspect(1)
        self.axes.set_xlim(-self.freat_size/4, (freats+1)*self.freat_size)
        self.axes.set_ylim(-self.freat_size, self.string_separation*7)
        
    def __draw_shape__(self, shape, init_freat=None):
        max_f, min_f = shape.get_max_min_freat()
        if init_freat is not None:
            min_f = init_freat    
        self.__draw_freatboard__(max_f - min_f, min_f)
        for f in shape.fingers:
            x = (f.freat - min_f)*self.freat_size + self.freat_size/2
            y = 5*self.string_separation - DrawFreatboard.STRINGS.index(f.string)*self.string_separation
            if f.function == '1':
                circle = plt.Circle((x, y), self.freat_size/5, color='r', fill=True, zorder=2)
            else:
                circle = plt.Circle((x, y), self.freat_size/5, color='k', fill=True, zorder=2)
            self.axes.add_artist(circle)
            self.__add_finger_text__(shape, x, y, f)
        plt.show()

    def __add_finger_text__(self, shape, x, y, f):
        if self.text == DrawFreatboard.TEXT_FUNCTION:
            if len(f.function) == 2:
                self.axes.text(x-2.75, y-1.5, f.function, fontsize=11, color='white')
            else:
                self.axes.text(x-1.75, y-1.5, f.function, fontsize=11, color='white')
        elif self.text == DrawFreatboard.TEXT_FINGER:
            if len(f.finger) == 2:
                self.axes.text(x-2.75, y-1.5, f.finger, fontsize=11, color='white')
            else:
                self.axes.text(x-1.75, y-1.5, f.finger, fontsize=11, color='white')
                