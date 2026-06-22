#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Centrifugal-pump selection program  (Project Part 3-b)
------------------------------------------------------
Given a required volumetric flow rate Q [m^3/h] and head H [m], the program
recommends a suitable PUMPIRAN ETA pump (2900 rpm) from the digitized catalog,
together with the impeller diameter, efficiency at the duty point and the
required electric-motor power.  Method follows the catalog's own worked
example (catalog p.5): locate the model whose H-Q field contains the duty
point, trim the impeller so its curve passes through (Q,H), read efficiency
from the efficiency field, then size the motor.
Usage:
    python pump_selector.py            # runs the demo duty points
    python pump_selector.py 20 25      # Q=20 m3/h , H=25 m
"""
import sys, math
from pumpiran_catalog_2900 import CATALOG_2900, model_a

RHO, G = 997.0, 9.81                      # water 25 C
IEC_MOTORS = [0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37]


def required_diameter(m, Q, H):
    """smallest impeller (mm) whose curve passes through (Q,H); None if impossible"""
    a = model_a(m)
    r2 = (H + a * Q ** 2) / m["H0"]       # r = D/Dmax from H_r(Q)=r^2 H0 - a Q^2
    if r2 <= 0:
        return None
    r = math.sqrt(r2)
    D = r * m["Dmax"]
    if D > m["Dmax"] * 1.002 or D < m["Dmin"] * 0.998:
        return None                       # outside available trim range
    if Q > m["Qmax"] * r + 1e-6:          # beyond end of curve
        return None
    return max(m["Dmin"], min(m["Dmax"], D)), r


def efficiency(m, Q):
    e = m["eta"] * (1 - ((Q - m["Qbep"]) / m["Qbep"]) ** 2)
    return max(e, 1.0)


def motor_size(P_shaft_kW):
    P = P_shaft_kW * 1.15                  # 15 % safety margin
    for s in IEC_MOTORS:
        if s >= P:
            return s
    return P_shaft_kW


def select_pump(Q, H, verbose=True):
    """Q [m3/h], H [m] -> list of feasible pumps sorted by efficiency."""
    cand = []
    for name, m in CATALOG_2900.items():
        res = required_diameter(m, Q, H)
        if res is None:
            continue
        D, r = res
        eta = efficiency(m, Q)
        P_hyd = RHO * G * (Q / 3600.0) * H / 1000.0    # kW
        P_shaft = P_hyd / (eta / 100.0)                # kW
        motor = motor_size(P_shaft)
        cand.append(dict(model=name, D=round(D), eta=round(eta, 1),
                         P_hyd=round(P_hyd, 2), P_shaft=round(P_shaft, 2),
                         motor=motor))
    cand.sort(key=lambda c: -c["eta"])
    if verbose:
        print(f"\nDuty point :  Q = {Q} m3/h ,  H = {H} m   (2900 rpm)")
        if not cand:
            print("  -> No catalog pump in the small-pump range matches this duty.")
        else:
            print(f"  Recommended : ETA {cand[0]['model']}  |  impeller "
                  f"D = {cand[0]['D']} mm  |  eff = {cand[0]['eta']} %  |  "
                  f"motor = {cand[0]['motor']} kW")
            print("  All feasible options:")
            print(f"    {'model':<8}{'D(mm)':>7}{'eta%':>7}{'P_hyd':>8}{'P_shaft':>9}{'motor':>8}")
            for c in cand:
                print(f"    {c['model']:<8}{c['D']:>7}{c['eta']:>7}"
                      f"{c['P_hyd']:>8}{c['P_shaft']:>9}{c['motor']:>8}")
    return cand


if __name__ == "__main__":
    if len(sys.argv) == 3:
        select_pump(float(sys.argv[1]), float(sys.argv[2]))
    else:
        for Q, H in [(20, 25), (30, 18), (12, 30), (35, 12), (25, 20)]:
            select_pump(Q, H)
