import boost_histogram as bh
import numpy as np
import os
import json
import imp
import glob

class InfoGetter:
    def __init__(self, analysis, selection, group2color, plotInfo="plotInfo_default.py"):
        try:
            adm_path = os.environ['ADM_PATH']
        except:
            print('The Analysis Dataset Manager is found by the variable ADM_PATH')
            print('Please set this path and consider setting it in your .bashrc')
            exit(1)
        #adm_path = '
        
        self.analysis = analysis
        self.selection = selection
        self.groupInfo = self.readAllInfo("{}/PlotGroups/{}.py"
                                          .format(adm_path, analysis))
        self.group2MemberMap = {group: self.groupInfo[group]["Members"]
                                for group in group2color.keys()}
        self.group2color = group2color
        self.plotSpecs = self.readAllInfo(plotInfo)
        self.lumi = 35900  #default
        
    def readAllInfo(self, file_path):
        info = {}
        for info_file in glob.glob(file_path):
            file_info = self.readInfo(info_file)
            if file_info:
                info.update(file_info)
        return info

    def readInfo(self, file_path):
        if ".py" not in file_path[-3:] and ".json" not in file_path[-5:]:
            if os.path.isfile(file_path + ".py"):
                file_path = file_path + ".py"
            elif os.path.isfile(file_path + ".json"):
                file_path = file_path + ".json"
            else:
                return
        if ".py" in file_path[-3:]:
            file_info = imp.load_source("info_file", file_path)
            info = file_info.info
        else:
            info = self.readJson(file_path)
        return info

    def readJson(self, json_file_name):
        json_info = {}
        with open(json_file_name) as json_file:
            try:
                json_info = json.load(json_file)
            except ValueError as err:
                print("Error reading JSON file {}. The error message was:"
                      .format(json_file_name))
                print(err)
        return json_info

    def __getattr__(self, name):
        return {h: (vals[name] if name in vals else None) for h, vals in self.plotSpecs.items()}

    def get_hists(self):
        return self.plotSpecs.keys()

    def get_binning(self, histname):
        bins = np.array(self.Binning[histname], dtype=float)
        if self.Discrete[histname]:
            bins[1:] = bins[1:] - 0.5
        return bh.axis.Regular(int(bins[0]), *bins[1:])

    def get_color(self, group):
        return self.group2color[group]

    def setupGraphSpecs(self, input):
        return_map = dict()
        for action, dic in input.items():
            for hist, value in dict.items():
                if hist not in return_map:
                    return_map[hist] = dict()
                return_map[hist][action] = value
        return return_map

    def getLegendName(self, group):
        return self.groupInfo[group]['Name']

    def getAnalysis(self):
        return self.analysis, self.selection

    def getGroups(self):
        return self.groupInfo.keys()

    def getPlotSpec(self, histName):
        return self.plotSpecs[histName]

    def isDiscreteGraph(self, histName):
        if "isMultiplicity" in self.plotSpecs[histName]:
            return self.plotSpecs[histName]["isMultiplicity"]
        else:
            return False
        
    def setLumi(self, lumi):
        self.lumi = lumi
