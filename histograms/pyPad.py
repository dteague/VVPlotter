from matplotlib import gridspec

class pyPad:
    """Documentation for pyPad

    """
    def __init__(self, plot, makeRatio=True, ratio=(3, 1)):
        total = ratio[0] + ratio[1]
        self.makeRatio = makeRatio
        self.gs = gridspec.GridSpec(total, 1)
        self.gs.update(hspace=0.1)
        self.up = None
        self.down = None
        if self.makeRatio:
            self.up = plot.subplot(self.gs[0:ratio[0], 0])
            self.down = plot.subplot(self.gs[ratio[0]:total, 0])
            self._setup_ticks(self.down)
            self.up.xaxis.set_major_formatter(plot.NullFormatter())
            self.down.tick_params(direction="in")
            self.up.get_shared_x_axes().join(self.up, self.down)
        else:
            self.up = plot.gca()

        self._setup_ticks(self.up)

    def _setup_ticks(self, pad):
        pad.minorticks_on()
        pad.tick_params(direction="in", length=9, top=True, right=True)
        pad.tick_params(direction="in", length=4, which='minor', top=True,
                        right=True)

    def __call__(self, sub_pad=False):
        if sub_pad:
            return self.down
        else:
            return self.up
    
    def setLegend(self, plotSpecs):
        if "legendLoc" in plotSpecs:
            self.up.legend(loc=plotSpecs["legendLoc"])
        else:
            self.up.legend()

    def getXaxis(self):
        if self.down:
            return self.down
        else:
            return self.up

    def axisSetup(self, info):
        axis = self.getXaxis()

        # Defaults
        self.up.set_ylim(bottom=0.)
        self.up.set_ylabel("Events/bin")
        # axis.set_xlim(defRange)
        self._right_align_label(self.up.get_yaxis(), True)
        self._right_align_label(axis.get_xaxis())
        if self.down:
            self.down.set_ylabel("Signal/MC")
            self.down.set_ylim(top=2.0, bottom=0)

        # user specified
        for key, val in info.items():
            try:
                if "_y" in key:
                    getattr(self.up, key)(val)
                else:
                    getattr(axis, key)(val)
            except:
                pass

    def _right_align_label(self, axis, isYaxis=False):
        label = axis.get_label()
        x_lab_pos, y_lab_pos = label.get_position()
        if isYaxis:
            label.set_position([x_lab_pos, 1.0])
        else:
            label.set_position([1.0, y_lab_pos])
        label.set_horizontalalignment('right')
        axis.set_label(label)
