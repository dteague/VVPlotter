# -*- coding: utf-8 -*-

info = {
    "HT" : {
        "set_xlabel": "$H_{T}$ (GeV)",
        "Rebin"     :  10,
        "set_xlim"  :  (0, 1200)
    },
    "Met" : {
        "set_xlabel": "$p_{T}^{miss}$ (GeV)",
        "Rebin"     :  10,
        "set_xlim"  :  (0, 350)
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
    "nloosebjet" : {
        "set_xlim" :  (0, 8),
        "set_xlabel": "$N_{bloose}$",
        "isMultiplicity" : True,
    },
    "ntightbjet" : {
        "set_xlim" :  (0, 8),
        "set_xlabel": "$N_{btight}$",
        "isMultiplicity" : True,
    },
    "njet" : {
        "set_xlim" :  (0, 12),
        "set_xlabel": '$N_{jets}$',
        "isMultiplicity" : True,
    },
    "nlooseleps" : {
        "set_xlim" :  (0, 5),
        "set_xlabel": '$N_{leps}$',
        "isMultiplicity" : True,
    },
    "ptl1" : {
        "Rebin" :  4,
        "set_xlim" :   (0, 400),
        "set_xlabel": "$p_{T}(\ell_{1})$ (GeV)",
    },
    "ptl2" : {
        "Rebin" :  2,
        "set_xlim" :   (0, 200),
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
    "ptj4" : {
        "Rebin" : 10,
        "set_xlim" :   (0, 300),
        "set_xlabel": "$p_{T}(j_{4})$ (GeV)",
    },
    "ptj5" : {
        "Rebin" : 10,
        "set_xlim" :   (0, 300),
        "set_xlabel": "$p_{T}(j_{5})$ (GeV)",
    },
    "ptj6" : {
        "Rebin" : 10,
        "set_xlim" :   (0, 300),
        "set_xlabel": "$p_{T}(j_{6})$ (GeV)",
    },
    "ptj7" : {
        "Rebin" : 10,
        "set_xlim" :   (0, 300),
        "set_xlabel": "$p_{T}(j_{7})$ (GeV)",
    },
    "ptj8" : {
        "Rebin" : 10,
        "set_xlim" :   (0, 300),
        "set_xlabel": "$p_{T}(j_{8})$ (GeV)",
    },
    "etaj1" : {
        "Rebin" :      20,
        "set_xlabel": "$\eta(j_{1})$",
    },
    "etaj2" : {
        "Rebin" :      20,
        "set_xlabel": "$\eta(j_{2})$",
    },
    "etaj3" : {
        "Rebin" :      20,
        "set_xlabel": "$\eta(j_{3})$",
    },
    "ptb1" : {
        "Rebin" : 8,
        "set_xlim" :   (0, 600),
        "set_xlabel": "$p_{T}(b_{1})$ (GeV)",
    },
    "ptb2" : {
        "Rebin" : 8,
        "set_xlim" :   (0, 300),
        "set_xlabel": "$p_{T}(b_{2})$ (GeV)",
    },
    "ptb3" : {
        "Rebin" : 4,
        "set_xlim" :   (0, 200),
        "set_xlabel": "$p_{T}(b_{3})$ (GeV)",
    },
    "ptb4" : {
        "Rebin" : 4,
        "set_xlim" :   (0, 200),
        "set_xlabel": "$p_{T}(b_{4})$ (GeV)",
    },
    "etab1" : {
        "Rebin" :      20,
        "set_xlabel": u"$η(b_{1})$",
    },
    "etab2" : {
        "Rebin" :      20,
        "set_xlabel": u"$η(b_{2})$",
    },
    "etab3" : {
        "Rebin" :      20,
        "set_xlabel": u'$η(b_{3})$',
    },
    "ptj1OverHT" : {
        "Rebin" :  4,
        "set_xlabel": "$p_{T}(j_{1}) / H_{T}$",
    },
    "ptb1OverHT" : {
        "Rebin" :  4,
        "set_xlabel": "$p_{T}(b_{1}) / H_{T}$",
    },
    "dphi_l1j1"  : {
        "Rebin" :  25,
        "set_xlabel": u"$Δφ(ℓ_{1}, j_{1})$",
    },
    "dphi_l1j2"  : {
        "Rebin" :  25,
        "set_xlabel": u"$Δφ(ℓ_{1}, j_{2})$",
    },
    "dphi_l1j3"  : {
        "Rebin" :  25,
        "set_xlabel": u"$Δφ(ℓ_{1}, j_{3})$",
    },
    "dilepCharge" : {
        "set_xlabel": "$q(\ell_{1})\times q(\ell_{2})$"
    },
    "DRjet" : {
        "set_xlabel": "$\Delta R(j_{1}, j_{2})$",
        "Rebin"      : 2,
    },
    "DRLep" : {
        "set_xlabel" : "$\Delta R(\ell_{1}, \ell_{2})$",
        "Rebin"      : 2,
    },
    "dijetMass" : {
        "set_xlabel" : "$M(j_{1}, j_{2})$",
        "set_xlim"   :  (0,60)
    },
    "dilepMass" : {
        "set_xlabel": "$M(\ell_{1}, \ell_{2})$",
        "set_xlim"  :  (0, 600),
        "Rebin"     :  10,
    },
    "jetpt" : {
        "set_xlabel": "$p_{T}$(all jets) (GeV)",
        "Rebin" :      8,
    },
    "bjetpt" : {
        "set_xlabel": "$p_{T}$(all bs) (GeV)",
        "Rebin":       8,
    },
    "Shape1" : {
        "set_xlabel": "shape1",
        "Rebin":      4
    },
    "Shape2" : {
        "set_xlabel": "shape2",
        "Rebin":      4
    },
    "LepCos" : {
        "set_xlabel": "$cos(\ell_{1}, \ell_{2})",
        "Rebin":      4,
    },
    "JLep1Cos" : {
        "set_xlabel": "$cos(j_{1}, \ell_{1})$",
        "Rebin":      4,
    },
    "JLep2Cos" : {
        "set_xlabel": "$cos(j_{1}, \ell_{2})$",
        "Rebin":      4,
    },
    "JBCos" : {
        "set_xlabel": "$cos(j_{1}, b_{1})$",
        "Rebin":      4,
        
    },
    "DRjb" : {
        "set_xlabel": "$\Delta R(j_{1}, b_{1})$",
        "set_xlim":   (0.4, 6),
    },
    "etaj" : {
        "set_xlabel": "$eta(j)$",
        "Rebin":      8
    },
    "etab" : {
        "set_xlabel": "$\eta(b)$",
        "Rebin":      8,
        "set_xlim":   (-2.5, 2.5)
    },
    "detaj12" : {
        "set_xlabel": "$\Delta\eta(j_{1},j_{2})$",
        "Rebin":      8,
        "set_xlim":   (0, 6)
    },
    "detaj13" : {
        "set_xlabel": "$\Delta\eta(j_{1},j_{3})$",
        "Rebin":      8,
        "set_xlim":   (0, 6)
    },
    "detaj23" : {
        "set_xlabel": "$\Delta\eta(j_{2},j_{3})$",
        "Rebin":      8,
        "set_xlim":   (0, 6)
    },
}
