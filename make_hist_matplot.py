#!/usr/bin/env python

import os
import ROOT as r

from Utilities.InfoGetter import InfoGetter
import Utilities.StyleHelper as style
import Utilities.configHelper as config
from Utilities.pyHist import pyHist
from Utilities.pyStack import pyStack
from Utilities.pyPad import pyPad
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
           "tttt_line" : "red",

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
if args.drawStyle == 'compare':
    info.setLumi(-1)
else:
    info.setLumi(args.lumi*1000)

if not drawObj:
    print("you have no list of drawObjs, paste this into the code to continue\n")
    groups = info.getGroups()
    print("drawObj = {")
    for group in groups:
        print( '           %-12s: "%s",' % ('"'+group+'"', info.getStyle(group)))
    print("}")
    exit()


if args.signal and args.signal not in drawObj:
    print( "signal not in list of groups!")
    print( drawObj.keys())
    exit(1)
signalName = args.signal
channels = args.channels.split(',')

# HTML setup
extraPath = time.strftime("%Y_%m_%d")
if args.path:
    extraPath = args.path+'/'+extraPath

basePath = '/eos/home-{0:1.1s}/{0}/www'.format(os.environ['USER'])
basePath += '/%s/%s/%s_%s' % ('PlottingResults', args.analysis, extraPath, args.drawStyle)
config.checkOrCreateDir('%s' % (basePath))
config.checkOrCreateDir('%s/plots' % (basePath))
config.checkOrCreateDir('%s/logs' % (basePath))

for histName in info.getListOfHists():
    if not info.isInPlotSpec(histName): continue
    
    for chan in channels:
        signal = None
        data = None
        ratio = None
        
        groupHists = config.getNormedHistos(inFile, info, histName, chan)
        if not groupHists or groupHists.values()[0].InheritsFrom("TH2"):
            continue

        exclude = []
        # signal
        if signalName in groupHists:
            signal = pyHist(info.getLegendName(signalName), groupHists[signalName], drawObj[signalName])
            exclude.append(signalName)
                    
        # data
        if False:
            data = pyHist("Data", groupHists['data'], 'black')
            exclude.append('data')
                    
        drawOrder = config.getDrawOrder(groupHists, drawObj, info, ex=[signalName])
        stacker = pyStack(drawOrder)
        stacker.setColors(drawObj)
        stacker.setLegendNames(info)

        # ratio
        if signal:
            divide = r.TGraphAsymmErrors(signal.getRHist(), stacker.getRHist(), "pois")
            ratio = pyHist("Ratio", divide, "black", isTH1=False)
                                                        
        pad = pyPad(plt, ratio!=None)
        
        n, bins, patches = pad.getMainPad().hist(**stacker.getInputs())
        stacker.applyPatches(plt, patches)

        if signal:
            pad.getMainPad().errorbar(**signal.getInputs())
        if data:
            pad.getMainPad().errorbar(**data.getInputs())

        pad.setLegend()
        pad.axisSetup(info.getPlotSpec(histName))

        if ratio:
            pad.getSubMainPad().errorbar(**ratio.getInputs())

        fig = plt.gcf()
        fig.set_size_inches(8,8)
                
        plt.savefig("%s/plots/%s.png" % (basePath, histName), format="png", bbox_inches='tight')
        plt.savefig("%s/plots/%s.pdf" % (basePath, histName), format="pdf", bbox_inches='tight')
        plt.clf()
        plt.cla()
        plt.close()


writeHTML(basePath, args.analysis)

