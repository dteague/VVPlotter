#!/usr/bin/env python
import os
import ROOT as r

from Utilities.InfoGetter import InfoGetter
import Utilities.StyleHelper as style
import Utilities.configHelper as configHelper
from Utilities.makeSimpleHtml import writeHTML
from Utilities.LogFile import LogFile
from DrawObjects.MyCanvas import MyCanvas
from DrawObjects.MyLegend import MyLegend
from DrawObjects.MyRatio import MyRatio
from DrawObjects.MyPaveText import MyPaveText
import datetime
import sys
import time

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

exceptions = ["Rebin"]

# variable setup
### If setting up new run (or added a draw group), set drawObj = None to get new list
# drawObj = None
drawObj = {
           # "ttz"       : "fill-mediumseagreen",
           # "rare"      : "fill-hotpink",
           # "ttXY"      : "fill-cornflowerblue",
           # "ttw"       : "fill-darkgreen",
           # "xg"        : "fill-indigo",
           # "tth"       : "fill-slategray",
           # "2016"      : "fill-red",

          # "ttt"       : "fill-hotpink",
           # "2017"      : "fill-green",
          "ttt_line"  : "nofill-cornflowerblue-thick",
           "tttt_line" : "nofill-hotpink",
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

extraPath = time.strftime("%Y_%m_%d")
if args.path:
    extraPath = args.path+'/'+extraPath


basePath = '/eos/home-{0:1.1s}/{0}/www'.format(os.environ['USER'])
basePath += '/%s/%s/%s_%s' % ('PlottingResults', args.analysis, extraPath, args.drawStyle)
configHelper.checkOrCreateDir('%s' % (basePath))
configHelper.checkOrCreateDir('%s/plots' % (basePath))
configHelper.checkOrCreateDir('%s/logs' % (basePath))
outFile = r.TFile("%s/output.root"%basePath, "UPDATE")

for histName in info.getListOfHists():
    for chan in channels:
        groupHists = configHelper.getNormedHistos(inFile, info, histName, chan)
        if not groupHists or groupHists.values()[0].InheritsFrom("TH2") or not info.isInPlotSpec(histName):
            continue
        for key, hist in groupHists.iteritems():
            if "Rebin" in info.getPlotSpec(histName):
                hist.Rebin(info.getPlotSpec(histName)["Rebin"])
            configHelper.addOverflow(hist, info.getUpBinUser(histName))
        ordHists = configHelper.getDrawOrder(groupHists, drawObj.keys(), info)

        # signal
        if signalName in groupHists:
            signal = groupHists[signalName].Clone()
            style.setStyle(signal, info.getStyleInit("Signal"))
            style.setAttributes(signal, info.getStyleInfo("Signal"))
            del groupHists[signalName]
            del ordHists[[i[0] for i in ordHists].index(signalName)]
        else:
            signal = None
        
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

        maxHeight = configHelper.getMax(stack, signal, data)*1.2
        ####End Setup
        
        if args.drawStyle == 'compare':
            statError = None
            data = None
        if args.drawStyle == 'stack':
            pass

        canvas = MyCanvas(histName)
        canvas.getAndDraw().cd()
        
        legend = MyLegend(ordHists, info, statError, signal, data)
        ratioPlot = MyRatio(args.drawStyle, stack, signal, data)
        cmsText = MyPaveText(info.getLumi())
        
        if args.no_ratio or not ratioPlot.isValid():
            stack.Draw()
            # style.setAttributes(stack, info.getAxisInfo(histName))
            if signal: signal.Draw("same")
            stack.GetHistogram().SetMaximum(maxHeight)
        else:
            rp = ratioPlot.getAndDraw()
            rp.GetUpperPad().cd()
            ratioPlot.setMax(maxHeight)

        style.setAttributes(rp.GetUpperRefObject().GetHistogram(), info.getPlotSpec(histName), exceptions)
        style.setAttributes(rp.GetLowerRefGraph(), info.getPlotSpec(histName), exceptions)
        
        
        if statError: statError.Draw("E2same")
        if data: data.Draw("same")
            
        legend.getAndDraw()
        cmsText.getAndDraw(r.gPad, "Preliminary")
        canvas.writeOut(outFile)
        
        # setup log file
        logger = LogFile(histName, info, basePath+"/logs")
        logger.addMetaInfo(callTime, command)
        logger.addMC(groupHists, drawObj.keys())
        if signal:
            logger.addSignal(signal, signalName)
        logger.writeOut()

        canvas.saveAsPDF(basePath+"/plots")
    
outFile.Close()
writeHTML(basePath, args.analysis)
        
