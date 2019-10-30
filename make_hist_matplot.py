#!/usr/bin/env python
import os
import ROOT as r

from Utilities.InfoGetter import InfoGetter
import Utilities.StyleHelper as style
import Utilities.configHelper as configHelper
from Utilities.pyHist import pyHist
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, colors
import datetime
import sys
import time

# run time variables
callTime = str(datetime.datetime.now())
command = ' '.join(sys.argv)

# Setup
args = configHelper.getComLineArgs()

drawObj = {
           "ttz"       : "mediumseagreen",
           "rare"      : "hotpink",
           "ttXY"      : "cornflowerblue",
           "ttw"       : "darkgreen",
           "xg"        : "indigo",
           "tth"       : "slategray",
           "2016"      : "red",

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

channels = args.channels.split(',')

colorList = ["thistle", "mediumorchid", "darkviolet", "darkorchid", "indigo", "blueviolet", "rebeccapurple"]

for histName in info.getListOfHists():
    for chan in channels:
        nbins = 0
        width = 0
        groupHists = configHelper.getNormedHistos(inFile, info, histName, chan)
        pyGroupHists = dict()
        if not groupHists or groupHists.values()[0].InheritsFrom("TH2"):
            continue
        i=0
        for key, hist in groupHists.iteritems():
            if key not in drawObj: continue
            
            pyGroupHists[key] = pyHist(info.getLegendName(key), hist, drawObj[key])
            if nbins == 0:
                nbins = pyGroupHists[key].nBins
                width = pyGroupHists[key].width
            i+=1
        gs = gridspec.GridSpec(4, 1)
        up = plt.subplot(gs[0:3, 0])
        up.xaxis.set_major_formatter(plt.NullFormatter())
        up.tick_params(direction="in")
        down = plt.subplot(gs[3:4, 0])
        down.tick_params(direction="in")
        
        total = np.zeros(nbins)
        i= 0
        for hist in pyGroupHists.values():
            if i >= len(colorList):
                break

            up.bar(bottom=total, **hist.barVars())
            total = np.add(total, hist.getValues())
            i+= 1
            
        plt.show()
        
        
        plt.clf()
        plt.cla()
        plt.close()


# N = 7
# OECD = (242, 244, 255, 263, 269, 276, 285)
# NonOECD = (282, 328, 375, 417, 460, 501, 535)
# extra = (282, 328, 375, 417, 460, 501, 535)
# ind = np.arange(N)


# p1 = plt.bar(ind, NonOECD, width = 1.0, color = 'r')
# p2 = plt.bar(ind, OECD, width = 1.0, color = 'b', bottom = NonOECD)
# p3 = plt.bar(ind, extra, width = 1.0, color = 'g', bottom = np.add(OECD, NonOECD))

# plt.ylabel('Quadrillion Btu')
# plt.title('World Total Energy Consumption 2010 - 2040')
# plt.xticks(ind+width/2., ('2010', '2015', '2020', '2025', '2030', '2035', '2040'))
# plt.yticks(np.arange(0, 1001, 200))
# plt.legend((p1[0], p2[0], p3[0]), ('Non - OECD', 'OECD', "extra"), loc = 2, frameon = False)
# plt.tick_params(top = 'off', bottom = 'off', right = 'off')
# plt.grid(axis = 'y', linestyle = '-')

