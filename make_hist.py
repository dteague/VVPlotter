#!/usr/bin/env python

import os
import ROOT as r

from Utilities.InfoGetter import InfoGetter
import Utilities.configHelper as config
from Utilities.pyHist import pyHist
from Utilities.pyStack import pyStack
from Utilities.pyErrors import pyErrors
from Utilities.pyPad import pyPad
from Utilities.LogFile import LogFile

from Utilities.makeSimpleHtml import writeHTML
import numpy as np
import matplotlib.pyplot as plt
import datetime
import sys
import time

# run time variables
callTime = str(datetime.datetime.now())
command = ' '.join(sys.argv)
r.gErrorIgnoreLevel=r.kError

font = {'family' : 'sans',
        'weight' : 'normal',
        }

plt.rc('font', **font)

SMALL_SIZE = 12
MEDIUM_SIZE = 16
plt.rc('font', size=SMALL_SIZE) 
plt.rc('axes', titlesize=SMALL_SIZE) 
plt.rc('axes', labelsize=MEDIUM_SIZE) 
plt.rc('xtick', labelsize=MEDIUM_SIZE) 
plt.rc('ytick', labelsize=MEDIUM_SIZE) 
plt.rc('legend', fontsize=SMALL_SIZE) 

# Setup
args = config.getComLineArgs()

drawObj = {
           "ttz"       : "mediumseagreen",
           "rare"      : "hotpink",
           "ttXY"      : "cornflowerblue",
           "ttw"       : "darkgreen",
           "xg"        : "indigo",
           "tth"       : "slategray",
           "tttt"      : "red",

          # "ttt"       : "fill-hotpink",
           # "2017"      : "fill-green",
          # "ttt_line"  : "nofill-cornflowerblue-thick",
          #  "tttt_line" : "nofill-hotpink",
           # "other"     : "fill-hotpink",
}

# In out
inFile = r.TFile(args.infile)

anaSel = args.analysis.split('/')
if len(anaSel) == 1:
    anaSel.append('')

info = InfoGetter(anaSel[0], anaSel[1], inFile)
info.setLumi(args.lumi*1000)
info.setDrawStyle(args.drawStyle)

if not drawObj:
    config.printDrawObjAndExit(info)

if args.signal and args.signal not in drawObj:
    print( "signal not in list of groups!")
    print( drawObj.keys())
    exit(1)
signalName = args.signal
channels = args.channels.split(',')



basePath = config.setupPathAndDir(args.analysis, args.drawStyle, args.path)

for histName in info.getListOfHists():
    if not info.isInPlotSpec(histName): continue
    print "Processing %s" % histName
    isDcrt = info.isDiscreteGraph(histName)
    
    for chan in channels:
        signal, data, ratio, band, error = None, None, None, None, None
                                
        groupHists = config.getNormedHistos(inFile, info, histName, chan)
        if not groupHists or groupHists.values()[0].InheritsFrom("TH2"):
            continue

        exclude = []
        # signal
        if signalName in groupHists:
            signal = pyHist(info.getLegendName(signalName), groupHists[signalName], drawObj[signalName], isMult=isDcrt)
            exclude.append(signalName)

        # data
        if False:
            data = pyHist("Data", groupHists['data'], 'black', isMult=isDcrt)
            exclude.append('data')
                    
        drawOrder = config.getDrawOrder(groupHists, drawObj, info, ex=[signalName])
        stacker = pyStack(drawOrder, isMult=isDcrt)
        stacker.setColors(drawObj)
        stacker.setLegendNames(info)
        error = pyErrors("Stat Errors", stacker.getRHist(), "plum", isMult=isDcrt)
        
        # ratio
        if signal:
            divide = r.TGraphAsymmErrors(signal.getRHist(), stacker.getRHist(), "pois")
            stack_divide = r.TGraphAsymmErrors(stacker.getRHist(), stacker.getRHist(), "pois")
            ratio = pyHist("Ratio", divide, "black", isTH1=False, isMult=isDcrt)
            band = pyErrors("Ratio", stack_divide, "plum", isTH1=False, isMult=isDcrt)
                                                        
        pad = pyPad(plt, ratio!=None)
        
        n, bins, patches = pad.getMainPad().hist(**stacker.getInputs())
        stacker.applyPatches(plt, patches)

        if signal:
            pad.getMainPad().errorbar(**signal.getInputs(fmt='o', markersize=4))
        if data:
            pad.getMainPad().errorbar(**data.getInputs(fmt='o', markersize=4))
        if error:
            pad.getMainPad().hist(**error.getInputs(hatch='//', alpha=0.4,label="Stat Error"))
        if ratio:
            pad.getSubMainPad().errorbar(**ratio.getInputs(fmt='o', markersize=4))
            pad.getSubMainPad().hist(**band.getInputs(hatch='//', alpha=0.4,))

        pad.setLegend()
        pad.axisSetup(info.getPlotSpec(histName), stacker.getRange())

        
        fig = plt.gcf()
        fig.set_size_inches(8,8)

        plt.savefig("%s/plots/%s.png" % (basePath, histName), format="png", bbox_inches='tight')
        plt.savefig("%s/plots/%s.pdf" % (basePath, histName), format="pdf", bbox_inches='tight')
        plt.close()

        # setup log file
        logger = LogFile(histName, info, basePath+"/logs")
        logger.addMetaInfo(callTime, command)
        logger.addMC(drawOrder)
        if signal:
            logger.addSignal(groupHists[signalName], signalName)
        logger.writeOut()

        

writeHTML(basePath, args.analysis)
userName = os.environ['USER']
htmlPath = basePath[basePath.index(userName)+len(userName)+1:]
if 'hep.wisc.edu' in os.environ['HOSTNAME']:
    print "https://www.hep.wisc.edu/~{0}/{1}".format(os.environ['USER'], htmlPath[12:])
else:
    print "https://{0}.web.cern.ch/{0}/{1}".format(os.environ['USER'], htmlPath[4:])    


