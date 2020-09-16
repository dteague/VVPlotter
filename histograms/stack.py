from .histogram import Histogram

from matplotlib import colors as clr
import numpy as np

class Stack(Histogram):
    def __init__(self, bin_info):
        super().__init__("", "", bin_info)
        self.stack = list()
        self.options = {"stacked": True, "histtype": "stepfilled"}
        # if isMult:
        #     self.bins = self.bins - 0.5
        # #self.align = 'left' if isMult else "mid"
        # self.align = "mid"

    def __add__(self, right):
        idx = self._get_index(right.integral())
        self.stack.insert(idx, right)
        return super().__add__(right)

    def _darkenColor(self, color):
        cvec = clr.to_rgb(color)
        dark = 0.3
        return [i - dark if i > dark else 0.0 for i in cvec]

    def _get_index(self, integral):
        if not self.stack:
            return 0
        else:
            return np.argmax(np.array([s.integral() for s in self.stack]) < integral)

    def applyPatches(self, plot, patches):
        edgecolors = [self._darkenColor(h.color) for h in self.stack]
        for p, ec in zip(patches, edgecolors):
            plot.setp(p, edgecolor=ec)

    def getInputs(self, **kwargs):
        stack = [h.vals for h in self.stack]
        base_vals = [self.axis.centers for _ in range(len(stack))]
        fancyNames = [h.name for h in self.stack]
        colors = [h.color for h in self.stack]
        rDict = dict({"weights": stack, "bins": self.axis.edges,
                      "x": base_vals, "color": colors, "label": fancyNames
                      # , 'align': self.align,
                      }, **self.options)
        rDict.update(kwargs)
        return rDict

#     def setDrawType(self, drawtype):
#         if drawtype == "compare":
#             self.options["stacked"] = False
#             self.options["histtype"] = "step"
#             self.edgecolors = self.colors
