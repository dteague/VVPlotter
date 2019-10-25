from Utilities.prettytable import PrettyTable
import array
import math

BKG=0
SIGNAL = 1
DATA = 2
TOTAL = 3
def sl(listF):
    newList = tuple()
    for item in listF:
        if isinstance(item, float):
            if item < 1.0:
                item = round(item, 3)
            else:
                item = round(item, 2)
        newList += (item,)
    return newList

class LogFile:
    def __init__(self, name, info):
        self.plotTable = PrettyTable(["Plot Group", "Weighted Events", "Error"])
        self.output = open("%s.txt" % name, "w")
        self.info = info
        self.hists = [None, None, None, None]
        self.callTime = ""
        self.command = ""

    def getBackground(self):
        return self.hists[BKG]

    def getSignal(self):
        return self.hists[SIGNAL]

    def getTotalMC(self):
        return self.hists[TOTAL]

    def getData(self):
        return self.hists[DATA]
        
    def addMC(self, groupHists, drawOrder):
        for groupName in [i for i in drawOrder[::-1] if i in groupHists]:
            hist = groupHists[groupName]
            wEvents, error = self.getIntErr(hist)
            self.plotTable.add_row(sl((groupName, wEvents, error)))
            self.addHist(hist, BKG)
        self.addHist(self.getBackground(), TOTAL)
            
    def addHist(self, hist, dest):
        if not self.hists[dest]:
            self.hists[dest] = hist.Clone()
        else:
            self.hists[dest].Add(hist)

    def addSignal(self, signal, groupName):
        self.addHist(signal, SIGNAL)
        wEvents,error = self.getIntErr(signal)
        self.plotTable.add_row(sl((groupName, wEvents, error)))
        self.addHist(signal, TOTAL)
    
    def addMetaInfo(self, callTime, command):
        self.callTime = callTime
        self.command = command

        
    def getIntErr(self, hist):
        error = array.array('d', [0])
        wEvents = hist.IntegralAndError(0, hist.GetNbinsX(), error)
        return (wEvents, error[0])
        
    def writeOut(self, isLatex=False):
        self.output.write('-'*80 + '\n')
        self.output.write("Script called at %s \n" % self.callTime)
        self.output.write("The command was: %s \n" % self.command)
        self.output.write('-'*80 + '\n')
        self.output.write("Selection: %s/%s\n" % (self.info.getAnalysis(), self.info.getSelection()))
        self.output.write("Luminosity: %0.2f fb^{-1}\n" % (self.info.getLumi()/1000))
        #output.write("\nPlotting branch: %s\n" % branch_name)
        
        if isLatex:
            self.output.write('\n' + self.plotTable.get_latex_string() + '\n'*2)
        else:
            self.output.write('\n' + self.plotTable.get_string() + '\n'*2)

        self.output.write("Total sum of Monte Carlo: %0.2f +/- %0.2f \n" % sl(self.getIntErr(self.getTotalMC())))
        if self.getSignal():
            self.output.write("Total sum of background Monte Carlo: %0.2f +/- %0.2f \n" % sl(self.getIntErr(self.getBackground())))
            self.output.write("Ratio S/(S+B): %0.2f +/- %0.2f \n" % sl(self.getSigBkgRatio()))
            self.output.write("Ratio S/sqrt(S+B): %0.2f +/- %0.2f \n" % sl(self.getLikelihood()))
        if self.getData():
            self.output.write("Number of events in data %d \n" % self.getData.Integral())

        self.output.close()                

    def getSigBkgRatio(self):
        sig, sigErr = self.getIntErr(self.getSignal())
        tot, totErr = self.getIntErr(self.getTotalMC())
        sigbkgd = sig/tot
        sigbkgdErr = sigbkgd*math.sqrt((sigErr/sig)**2 + (totErr/tot)**2)
        return (sigbkgd, sigbkgdErr)

    def getLikelihood(self):
        sig, sigErr = self.getIntErr(self.getSignal())
        tot, totErr = self.getIntErr(self.getTotalMC())
        likelihood = sig/math.sqrt(tot)
        likelihoodErr = likelihood*math.sqrt((sigErr/sig)**2 + (0.5*totErr/tot)**2)
        return (likelihood, likelihoodErr)
