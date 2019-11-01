from matplotlib import gridspec

class pyPad:
    """Documentation for pyPad

    """
    def __init__(self, plot, makeRatio=True, ratio=(3,1)):
        total = ratio[0] + ratio[1]
        self.makeRatio = makeRatio
        self.gs = gridspec.GridSpec(total, 1)
        self.gs.update(hspace=0.1)
        self.up = None
        self.down = None
        if self.makeRatio:
            self.up = plot.subplot(self.gs[0:ratio[0], 0])
            self.down = plot.subplot(self.gs[ratio[0]:total, 0])
            self.setupTicks(self.down)
            self.up.xaxis.set_major_formatter(plot.NullFormatter())
            self.down.tick_params(direction="in")
            self.up.get_shared_x_axes().join(self.up,self.down)
        else:
            self.up = plot.gca()
            
        self.setupTicks(self.up)

    def setupTicks(self, pad):
        pad.minorticks_on()
        pad.tick_params(direction="in", length=9, top=True, right=True)
        pad.tick_params(direction="in", length=4, which='minor',top=True,right=True)
        
    def getMainPad(self):
        return self.up

    def getSubMainPad(self):
        return self.down

    
    def setLegend(self):
        self.up.legend()

    def getXaxis(self):
        if self.down:
            return self.down
        else:
            return self.up

    def axisSetup(self, info, defRange):
        axis = self.getXaxis()

        # Defaults
        self.up.set_ylim(bottom=0.)
        self.up.set_ylabel("Events/bin")
        axis.set_xlim(defRange)
        self.rightAlignLabel(self.up.get_yaxis(), True)
        self.rightAlignLabel(axis.get_xaxis())
        if self.down:
            self.down.set_ylabel("Signal/MC")
            self.down.set_ylim(top=2.0, bottom=0)

        # user specified
        for key, val in info.iteritems():
            try:
                getattr(axis, key)(val)
            except:
                pass
        
        
 
    def rightAlignLabel(self, axis, isYaxis=False):
        label = axis.get_label()
        x_lab_pos, y_lab_pos = label.get_position()
        if isYaxis:
            label.set_position([x_lab_pos, 1.0])
        else:
            label.set_position([1.0, y_lab_pos])
        label.set_horizontalalignment('right')
        axis.set_label(label)



        
