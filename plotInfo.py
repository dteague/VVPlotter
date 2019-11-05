# -*- coding: utf-8 -*-

info = {
    "HT" : {
        "set_xlabel": "$H_{T}$ (GeV)",
    },
    "Met" : {
        "set_xlabel": "$p_{T}^{miss}$ (GeV)",
    },
    "centrality": {
        "Rebin" :  4,
        "set_xlabel": "Centrality",
    },
    "sphericity" : {
        "Rebin" :  4,
        "set_xlabel": "sphericity",
    },
    "nbjet" : {
        "set_xlim" :  (0, 8),
        "set_xlabel": "$N_{b}$",
        "isMultiplicity" : True,
    },
    "njet" : {
        "set_xlim" :  (0, 12),
        "set_xlabel": '$N_{jets}$',
        "isMultiplicity" : True,
    },
    "nleps" : {
        "set_xlim" :  (0, 5),
        "set_xlabel": '$N_{leps}$',
        "isMultiplicity" : True,
    },
    "ptl1" : {
        "Rebin" :  8,
        "set_xlim" :   (0, 400),
        "set_xlabel": "$p_{T}(\ell_{1})$ (GeV)",
    },
    "ptl2" : {
        "Rebin" :  4,
        "set_xlim" :   (0, 80),
        "set_xlabel": "$p_{T}(\ell_{2})$ (GeV)",
    },
    "ptj1" : {
        "Rebin" : 10,
        "set_xlim" :   (0, 800),
        "set_xlabel": "$p_{T}(j_{1})$ (GeV)",
    },
    "ptj2" : {
        "Rebin" : 10,
        "set_xlim" :   (0, 450),
        "set_xlabel": "$p_{T}(j_{2})$ (GeV)",
    },
    "ptj3" : {
        "Rebin" : 10,
        "set_xlim" :   (0, 300),
        "set_xlabel": "$p_{T}(j_{3})$ (GeV)",
    },
    "etaj1" : {
        "Rebin" :      20,
        "set_xlabel": "η(j_{1})",
    },
    "etaj2" : {
        "Rebin" :      20,
        "set_xlabel": "η(j_{2})",
    },
    "etaj3" : {
        "Rebin" :      20,
        "set_xlabel": "η(j_{3})",
    },
    "ptb1" : {
        "Rebin" : 8,
        "set_xlim" :   (0, 600),
        "set_xlabel": "p_{T}(b_{1}) (GeV)",
    },
    "ptb2" : {
        "Rebin" : 8,
        "set_xlim" :   (0, 300),
        "set_xlabel": "p_{T}(b_{2}) (GeV)",
    },
    "ptb3" : {
        "Rebin" : 4,
        "set_xlim" :   (0, 200),
        "set_xlabel": "p_{T}(b_{3}) (GeV)",
    },
    "etab1" : {
        "Rebin" :      20,
        "set_xlabel": "$η(b_{1})$",
    },
    "etab2" : {
        "Rebin" :      20,
        "set_xlabel": "$η(b_{2})$",
    },
    "etab3" : {
        "Rebin" :      20,
        "set_xlabel": "$η(b_{3})$",
    },
    "ptj1OverHT" : {
        "Rebin" :  4,
        "set_xlabel": "$p_{T}(j_{1})$ / H_{T}",
    },
    "ptb1OverHT" : {
        "Rebin" :  4,
        "set_xlabel": "$p_{T}(b_{1})$ / H_{T}",
    },
    "dphi_l1j1"  : {
        "Rebin" :  25,
        "set_xlabel": "$Δφ(ℓ_{1}, j_{1})$",
    },
    "dphi_l1j2"  : {
        "Rebin" :  25,
        "set_xlabel": "$Δφ(ℓ_{1}, j_{2})$",
    },
    "dphi_l1j3"  : {
        "Rebin" :  25,
        "set_xlabel": "$Δφ(ℓ_{1}, j_{3})$",
    },
}
