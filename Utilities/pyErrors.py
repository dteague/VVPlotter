from matplotlib import colors as clr
from Utilities.pyUproot import GenericHist
import numpy as np


class pyErrors:
    def __init__(self, name, hist, color, isMult=False):
        self.name = name
        self.hist = hist
        self.color = color
        self.edgecolor = self._darkenColor(self.color)
        self.align = 'left' if isMult else "mid"
        # self.align = 'mid'
        self.bottom = self.hist.hist - np.sqrt(self.hist.histErr2)
        
    def _darkenColor(self, color):
        cvec = clr.to_rgba(color)
        dark = 0.3
        return tuple([i - dark if i > dark else 0.0 for i in cvec])

    def getInputs(self, **kwargs):
        return dict({"weights": 2*np.sqrt(self.hist.histErr2),
                     "x": self.hist.bins[:-1], "bins": self.hist.bins,
                     'bottom': self.bottom,"histtype": 'stepfilled',
                     "color": self.color,'align': self.align, 'stacked': True},
                    **kwargs)
