#!/usr/bin/env python
import os
import ROOT as r

from Utilities.InfoGetter import InfoGetter
import Utilities.StyleHelper as style
import Utilities.configHelper as configHelper
from Utilities.LogFile import LogFile
from DrawObjects.MyCanvas import MyCanvas
from DrawObjects.MyLegend import MyLegend
from DrawObjects.MyRatio import MyRatio
from DrawObjects.MyPaveText import MyPaveText
import datetime
import sys

# run time variables
callTime = str(datetime.datetime.now())
command = ' '.join(sys.argv)

# Setup
args = configHelper.getComLineArgs()
r.gROOT.SetBatch(True)
r.gStyle.SetOptTitle(0)
r.gErrorIgnoreLevel=r.kError
r.gROOT.LoadMacro("tdrstyle.C")

r.setTDRStyle()
r.gStyle = r.tdrStyle
r.gROOT.ForceStyle()

# variable setup
### If setting up new run (or added a draw group), set drawObj = None to get new list
# drawObj = None
drawObj = {
           # "ttz"       : "fill-mediumseagreen",
           # "rare"      : "fill-hotpink",
           # "ttXY"      : "fill-cornflowerblue",
           # "ttw"       : "fill-darkgreen",
           # "xg"        : "fill-indigo",
           # "ttt"       : "fill-hotpink",
           "ttt_line"  : "nofill-cornflowerblue-thick",
           # "tth"       : "fill-slategray",
           # "2017"      : "fill-green",
           # "2016"      : "fill-red",
           "tttt_line" : "nofill-hotpink",
           # "other"     : "fill-hotpink",
}

# In out
inFile = r.TFile(args.infile)
outFile = r.TFile(args.outfile, "RECREATE")

info = InfoGetter(args.analysis, args.selection, inFile)
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

for histName in info.getListOfHists():
    for chan in channels:
        groupHists = configHelper.getNormedHistos(inFile, info, histName, chan)
        for hist in groupHists.values(): configHelper.addOverflow(hist)
        if not groupHists or groupHists.values()[0].InheritsFrom("TH2"):
            continue

        # signal
        if signalName in groupHists:
            signal = groupHists[signalName].Clone()
            style.setStyle(signal, info.getStyleInit("Signal"))
            style.setAttributes(signal, info.getStyleInfo("Signal"))
            del groupHists[signalName]
        else:
            signal = None
        
        ordHists = configHelper.getDrawOrder(groupHists, drawObj.keys(), info)

        # stack
        stack = r.THStack("%s_%s" % (histName, chan), "")
        for group, hist in ordHists:
            style.setStyle(hist, drawObj[group])
            stack.Add(hist)
        if args.stack_signal:
            stack.Add(signal)
            signal = None

        # data
        data = None

        # error bars
        statError = configHelper.getHistTotal(ordHists)
        style.setStyle(statError, info.getStyleInit("ErrorBars"))

        maxHeight = configHelper.getMax(stack, signal, data)
        ####End Setup
        
        if args.drawStyle == 'compare':
            statError = None
            data = None
        if args.drawStyle == 'stack':
            pass

            
        canvas = MyCanvas(histName)
        curPad = canvas.getAndDraw()
        curPad.cd()
        
        legend = MyLegend(ordHists, info, statError, signal, data)
        ratioPlot = MyRatio(args.drawStyle, stack, signal, data)
        cmsText = MyPaveText(info.getLumi())
        
        if args.no_ratio or not ratioPlot.isValid():
            stack.Draw()
            style.setAttributes(stack, info.getAxisInfo(histName))
            if signal: signal.Draw("same")
            stack.GetHistogram().SetMaximum(maxHeight*1.3)
        else:
            rp = ratioPlot.getAndDraw()
            curPad = rp.GetUpperPad()
            curPad.cd()
            rp.GetLowerRefYaxis().SetNdivisions(505)
            ratioPlot.setMax(maxHeight)
            
        if statError: statError.Draw("E2same")
        if data: data.Draw("same")
            
        legend.getAndDraw()
        cmsText.getAndDraw(curPad, "Preliminary")
        canvas.writeOut(outFile)

        # # setup log file
        # logger = LogFile(histName, info)
        # logger.addMetaInfo(callTime, command)
        # logger.addMC(groupHists, drawOrder)
        # if signal:
        #     logger.addSignal(signal, signalName)
        # logger.writeOut()

        
        
        
