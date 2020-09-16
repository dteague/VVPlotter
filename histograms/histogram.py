import boost_histogram as bh
import awkward1 as ak
import numpy as np
from scipy.stats import beta
import math

class Histogram:
    def __init__(self, name, color, args):
        self.hist = bh.Histogram(args)
        self.sumw2 = bh.Histogram(args)
        self.name = r'${}$'.format(name) if '\\' in name else name
        self.color = color
        self.draw_sc = 1.

    def __add__(self, right):
        if isinstance(right, Histogram):
            self.hist += right.hist
            self.sumw2 += right.sumw2
        elif isinstance(right, ak.Array):
            histName = (set(right.columns) - {"scale_factor"}).pop()
            self.hist.fill(right[histName], weight=right.scale_factor)
            self.sumw2.fill(right[histName], weight=right.scale_factor**2)
        return self

    def __truediv__(self, denom):
        p_raw = (self.hist*self.hist/self.sumw2).to_numpy()[0]
        t_raw = (denom.hist*denom.hist/denom.sumw2).to_numpy()[0]
        ratio = (self.sumw2*denom.hist/(self.hist*denom.sumw2)).to_numpy()[0]
        hist = (self.hist/denom.hist).to_numpy()[0]

        alf = (1-0.682689492137)/2
        lo = np.array([beta.ppf(alf, p, t+1) for p, t in zip(p_raw, t_raw)])
        hi = np.array([beta.ppf(1 - alf, p+1, t) for p, t in zip(p_raw, t_raw)])
        errLo = hist - ratio*lo/(1-lo)
        errHi = ratio*hi/(1-hi) - hist
        hist[np.isnan(hist)], errLo[np.isnan(errLo)], errHi[np.isnan(errHi)] = 0, 0, 0

        return_obj = Histogram("", "", self.hist.axes[0])
        return_obj.hist[...] = hist
        return_obj.sumw2[...] = (errLo**2 + errHi**2)/2
        return return_obj

    def __bool__(self):
        return not self.hist.empty()

    def __getattr__(self, attr):
        if attr == 'axis':
            return self.hist.axes[0]
        elif attr == 'vals':
            return self.hist.view()
        elif attr == 'err':
            return np.sqrt(self.sumw2.view())
        else:
            raise Exception()

    def scale(self, scale, forPlot=False):
        if forPlot:
            self.draw_sc *= scale
            self.name = self.name.split(" x")[0] + " x {}".format(int(self.draw_sc))
        else:
            self.hist *= scale
            self.sumw2 *= scale**2

    def integral(self):
        return self.hist.sum(flow=True)

    def getInputs(self, **kwargs):
        return dict({"x": self.axis.centers, "xerr": self.axis.widths/2,
                "y": self.draw_sc*self.vals, "ecolor": self.color,
                "yerr": self.draw_sc*self.err, 'fmt': 'o',
                "color": self.color, "barsabove": True, "label": self.name,
                'markersize': 4}, **kwargs)

    def getInputsHist(self, **kwargs):
        # bins = self.bins - 0.5 if self.isMult else self.bins
        return dict({"weights": self.draw_sc*self.vals,
                "bins": self.axis.edges, "x": self.axis.centers,
                "color": self.color, # 'align': "mid"
                "histtype": "step"},
                    **kwargs)

    def getInputsError(self, **kwargs):
        # bins = self.bins - 0.5 if self.isMult else self.bins
        bottom = self.vals - self.err
        return dict({"weights": 2*self.err, "x": self.axis.centers,
                "bins": self.axis.edges, 'bottom': bottom,
                "histtype": 'stepfilled', "color": self.color,
                'align': 'mid', 'stacked': True, "hatch": '//',
                "alpha": 0.4, "label":self.name}, **kwargs)
