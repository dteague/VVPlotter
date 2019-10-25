info = {
    "HT" : {
        "Attributes" : {
            "GetXaxis.SetTitle" :      "H_{T} (GeV)",
        }
    },
    "Met" : {
        "Attributes" : {
            "GetXaxis.SetTitle" :      "p_{T}^{miss} (GeV)",
        }
    },
    
    "centrality" : {
        "Rebin" : 2,
        "Attributes" : {
            "GetXaxis.SetTitle"         : "Centrality",
        }
    },
    "nbjet" : {
        "Attributes" : {
            "GetXaxis.SetTitle"         : "N_{b}",
            "GetXaxis.SetRangeUser"     : (0, 8),
        }
    },
    "njet" : {
        "Attributes" : {
            "GetXaxis.SetTitle" :      "N_{jets}",
            "GetXaxis.SetRangeUser"     : (0, 12),
        }
    },
    "nleps" : {
        "Attributes" : {
            "GetXaxis.SetTitle" :      "N_{leps}",
            "GetXaxis.SetRangeUser"     : (0, 5),
        }
    },
    "ptl1" : {
          "Rebin" : 2,
        "Attributes" : {
            "GetXaxis.SetTitle" :      "p_{T}(\ell_{1})\ (GeV)",
        }
    },
    "ptl2" : {
        "Rebin" : 3,
        "Attributes" : {
            "GetXaxis.SetTitle" :      "p_{T}(\ell_{2})\ (GeV)",
            "GetXaxis.SetRangeUser"     : (0, 200),
        }
    },
    "sphericity" : {
        "Rebin" : 2,
        "Attributes" : {
            "GetXaxis.SetTitle" :      "sphericity",
        }
    },
    "SR" : {
        "Attributes": {
            "GetXaxis.SetRangeUser"     : (0, 8),},
    }
}
