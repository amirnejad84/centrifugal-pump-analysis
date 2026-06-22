# -*- coding: utf-8 -*-
"""
Digitized performance data for PUMPIRAN ETA centrifugal pumps (EN733/DIN24255)
at n = 2900 rpm, read from the company catalog (ETA.pdf) performance charts.
For every model the following anchors were digitized from its 2900-rpm chart:
  Dmax, Dmin : largest / smallest impeller trim on the chart  [mm]
  H0         : shut-off head of the LARGEST impeller (Q=0)     [m]
  Qbep,Hbep  : flow / head at best-efficiency point (max imp.) [m^3/h, m]
  eta_max    : peak (best) efficiency                          [%]
  Qmax       : end-of-curve flow of the largest impeller       [m^3/h]
H-Q model (largest impeller):   H(Q) = H0 - a*Q^2 ,  a=(H0-Hbep)/Qbep^2
Impeller trimming (affinity)  :  D->r=D/Dmax  =>  H_r(Q) = r^2*H0 - a*Q^2
Efficiency model              :  eta(Q) = eta_max*(1-((Q-Qbep)/Qbep)^2), >=0
These are engineering approximations of the catalog curves and may be refined
with finer digitization if higher accuracy is required.
"""
CATALOG_2900 = {
    #  model :   Dmax Dmin   H0    Qbep  Hbep  eta   Qmax
    "32-125": dict(Dmax=139, Dmin=110, H0=21.5, Qbep=14, Hbep=16.0, eta=63.5, Qmax=26),
    "32-160": dict(Dmax=169, Dmin=130, H0=33.0, Qbep=19, Hbep=24.0, eta=62.0, Qmax=35),
    "32-200": dict(Dmax=209, Dmin=170, H0=50.0, Qbep=13, Hbep=40.0, eta=45.0, Qmax=18),
    "40-125": dict(Dmax=139, Dmin=110, H0=22.0, Qbep=30, Hbep=16.0, eta=70.0, Qmax=45),
    "40-160": dict(Dmax=169, Dmin=130, H0=36.0, Qbep=30, Hbep=26.0, eta=67.8, Qmax=45),
    "40-200": dict(Dmax=209, Dmin=170, H0=60.0, Qbep=25, Hbep=45.0, eta=57.0, Qmax=40),
    "50-160": dict(Dmax=169, Dmin=130, H0=37.0, Qbep=55, Hbep=28.0, eta=78.0, Qmax=80),
    "50-200": dict(Dmax=209, Dmin=170, H0=60.0, Qbep=55, Hbep=45.0, eta=73.0, Qmax=90),
    "65-160": dict(Dmax=169, Dmin=130, H0=40.0, Qbep=110, Hbep=30.0, eta=80.0, Qmax=180),
    "65-200": dict(Dmax=209, Dmin=170, H0=60.0, Qbep=120, Hbep=45.0, eta=80.0, Qmax=160),
}


def model_a(m):
    """quadratic coefficient a of H(Q)=H0-a Q^2 for the largest impeller"""
    return (m["H0"] - m["Hbep"]) / (m["Qbep"] ** 2)
