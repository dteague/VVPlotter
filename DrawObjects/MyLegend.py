import ROOT as r
from MyObject import MyObject

class MyLegend(MyObject, object):
    def __init__(self, ordHists, info, statError=None, signal=None, data=None):
        super(MyLegend,self).__init__()

        x = 0.9 - 0.05*(len(ordHists) + self.legInc(statError) + self.legInc(signal) + self.legInc(data))
        self.myObj = r.TLegend(0.75, x , 0.9, 0.9)
        
        for group, hist in ordHists[::-1]:
            self.myObj.AddEntry(hist, info.getLegendName(group), 'f')
        if statError:
            self.myObj.AddEntry(statError, "statError", "f")
        if signal:
            self.myObj.AddEntry(signal, info.getLegendName(signal.GetName()), "f")
        if data:
            self.myObj.AddEntry(data, "data", "f")


    def setAttributes(self):
        self.myObj.SetBorderSize(0)

    def legInc(self, obj):
        return 1 if obj else 0
                


