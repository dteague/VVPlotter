import os
import json
import imp
import glob
import uproot

class InfoGetter:
    def __init__(self, analysis, selection, infilename, plotInfo="plotInfo.py"):
        try:
            adm_path = os.environ['ADM_PATH']
        except:
            print('The Analysis Dataset Manager is found by the variable ADM_PATH')
            print('Please set this path and consider setting it in your .bashrc')
            exit(1)
        #adm_path = '

        inFile = uproot.open(infilename)
        self.analysis = analysis
        self.selection = selection
        self.groupInfo = self.readAllInfo("{}/PlotGroups/{}.py"
                                          .format(adm_path, analysis))
        self.mcInfo = self.readAllInfo(
            "{}/FileInfo/montecarlo/montecarlo_2016.py".format(adm_path))
        self.member2GroupMap = self.setupMember2GroupMap()
        self.listOfHists = self.setupListOfHists(inFile)
        self.sumweights = self.setupSumWeight(inFile)
        self.plotSpecs = self.readAllInfo(plotInfo)
        self.lumi = 35900  #default
        
        # if os.path.isfile("%s/PlotObjects/%s/%s.json" % (adm_path, analysis, selection)):
        #     self.objectInfo = self.readAllInfo("%s/PlotObjects/%s/%s.json" % (adm_path, analysis, selection))
        # else:
        #     self.objectInfo = self.readAllInfo("%s/PlotObjects/%s.json" % (adm_path, analysis))
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

    def setupMember2GroupMap(self):
        return_map = dict()
        for key, val in self.groupInfo.items():
            for bkg in val['Members']:
                if bkg not in return_map:
                    return_map[bkg] = list()
                return_map[bkg].append(key)
        return return_map

    def setupGraphSpecs(self, input):
        return_map = dict()
        for action, dic in input.items():
            for hist, value in dict.items():
                if hist not in return_map:
                    return_map[hist] = dict()
                return_map[hist][action] = value
        return return_map

    def setupListOfHists(self, inFile):
        return_list = []
        for histName in inFile[inFile.keys()[0]].keys():
            histName = histName.decode()
            if histName == 'sumweights':
                continue
            baseName = histName[:histName.rfind('_')]
            if baseName not in return_list:
                return_list.append(baseName)
        return return_list

    def setupSumWeight(self, inFile):
        return_dict = dict()
        for dirName, dir in inFile.items():
            if "sumweights" not in dir:
                print("sumweight not in {}".format(dir))
            dirName = dirName.decode().strip(";1")
            return_dict[dirName] = sum(dir['sumweights'].values)
        return return_dict

    def setDrawStyle(self, drawStyle):
        if drawStyle == "compare":
            self.lumi = -1
            
    def getListOfHists(self):
        return self.listOfHists

    def getGroupName(self, member):
        return self.member2GroupMap[member]

    def getXSec(self, member):
        return self.mcInfo[member]['cross_section']

    def getSumweight(self, member):
        return self.sumweights[member]

    def getStyle(self, group):
        return self.groupInfo[group]['Style']

    def getLumi(self):
        return self.lumi

    def getLegendName(self, group):
        return self.groupInfo[group]['Name']

    def getSelection(self):
        return self.selection

    def getAnalysis(self):
        return self.analysis

    def getGroups(self):
        return self.groupInfo.keys()

    def getPlotSpec(self, histName):
        return self.plotSpecs[histName]

    def getUpBinUser(self, histName):
        if "set_xlim" in self.plotSpecs[histName]:
            return self.plotSpecs[histName]["set_xlim"][1]
        else:
            return None

    def isInPlotSpec(self, histName):
        return histName in self.plotSpecs

    def isDiscreteGraph(self, histName):
        if "isMultiplicity" in self.plotSpecs[histName]:
            return self.plotSpecs[histName]["isMultiplicity"]
        else:
            return False
        
    def setLumi(self, lumi):
        self.lumi = lumi
