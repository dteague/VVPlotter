from matplotlib import colors as clr
from Utilities.pyUproot import GenericHist
import numpy as np

class pyErrors:
    def __init__(self, name, hist, color, isTH1=True, isMult=False):
        self.name = name
        self.x = list()
        self.y = list()
        self.yerr = list()
        self.xerr = list()
        
        self.color = color
        self.edgecolor = self._darkenColor(self.color)
        # self.align = 'left' if isMult else "mid"
        self.align = 'mid'

        if not isinstance(hist, GenericHist):
            hist = GenericHist(hist)
        
        self.setupTH1(hist, isMult)
                    
        self.bottom = [y - yerr for y, yerr in zip(self.y, self.yerr)]
        self.errors = [2*yerr for yerr in self.yerr]
                
                        
    def setupTH1(self, hist, isMult):
        self.bins = hist.bins
        self.y = hist.hist
        self.yerr = np.sqrt(hist.histErr2)
        width = np.array([self.bins[i+1]-self.bins[i] for i in xrange(len(self.bins)-1)])
        self.xerr = width/2
        self.x = self.bins[:-1] if isMult else self.xerr + self.bins[:-1]

    def _darkenColor(self, color):
        cvec = clr.to_rgba(color)
        dark = 0.3
        return tuple([i - dark if i > dark else 0.0 for i in cvec])

    def getInputs(self, **kwargs):
        return dict({"weights":self.errors, "x":self.x, "bins":self.bins, 'bottom':self.bottom, "histtype":'stepfilled', "color":self.color, 'align':self.align, 'stacked':True}, **kwargs)

