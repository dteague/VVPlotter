# -*- coding: utf-8 -*-

info = {
    "HT" : {
        "Column": "Event_variables/Event_HT",
        "set_xlabel": "$H_{T}$ (GeV)",
        "Binning"     :  1,
        "set_xlim"  :  (0, 1200)
    },
    "Met" : {
        "Column": "Event_MET/MET_pt",
        "set_xlabel": "$p_{T}^{miss}$ (GeV)",
        "Binning"     :  10,
        "set_xlim"  :  (0, 350)
    },
    "NJets" : {
        "Column": "Jets/Jet_pt",
        "Modify" : "ak.count({}, axis=-1)",
        "set_xlabel": "$N_{j}$",
        "Binning"     :  10,
        "set_xlim"  :  (0, 10)
    },
}
