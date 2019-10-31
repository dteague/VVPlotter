#!/usr/bin/env python
import os
import ROOT as r

from Utilities.InfoGetter import InfoGetter
import Utilities.StyleHelper as style
import Utilities.configHelper as config
from Utilities.pyHist import pyHist
from Utilities.pyStack import pyStack
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import datetime
import sys
import time

# run time variables
callTime = str(datetime.datetime.now())
command = ' '.join(sys.argv)

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

channels = args.channels.split(',')

colorList = ["thistle", "mediumorchid", "darkviolet", "darkorchid", "indigo", "blueviolet", "rebeccapurple"]

for histName in info.getListOfHists():
    if not info.isInPlotSpec(histName): continue
    
    for chan in channels:
        groupHists = config.getNormedHistos(inFile, info, histName, chan)
        pyGroupHists = dict()
        if not groupHists or groupHists.values()[0].InheritsFrom("TH2"):
            continue

        drawOrder = config.getDrawOrder(groupHists, drawObj, info)
        
        stacker = pyStack(drawOrder)
        stacker.setColors(drawObj)

        gs = gridspec.GridSpec(4, 1)
        up = plt.subplot(gs[0:3, 0])
        down = plt.subplot(gs[3:4, 0])
        up.xaxis.set_major_formatter(plt.NullFormatter())
        up.tick_params(direction="in")
        down.tick_params(direction="in")
        up.get_shared_x_axes().join(up,down)
        
        
        n, bins, patches = up.hist(**stacker.getInputs())
        stacker.applyPatches(plt, patches)
        
        plt.show()
        
        
        plt.clf()
        plt.cla()
        plt.close()



