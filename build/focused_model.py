"""Shared model for the focused paper and the 3-minute deck (wick, thickness split, vapour core).

Properties and geometry are read from numbers.json (written by calc.py), so both versions of the paper
use the same inputs. Adds the closed-form optimum wick thickness, which calc.py only found by sweeping.
Run:  python -X utf8 focused_model.py   -> writes numbers_focused.json
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
N = json.load(open(os.path.join(HERE, "numbers.json")))
_p, _g = N["props"], N["geom"]
T, rho_l, rho_v, mu_l, mu_v = _p["T"], _p["rho_l"], _p["rho_v"], _p["mu_l"], _p["mu_v"]
sigma, hfg, P_sat = _p["sigma"], _p["hfg"], _p["P_sat"]
R1, R2, lnR, t_w = _g["R1"], _g["R2"], _g["lnR"], _g["t_w"]
g_acc, dz = 9.81, 0.10
gamma, R_v = 1.33, 461.5
H_in = 250e-6
MESH, S50, S10 = "Cu mesh (#200)", "Sintered, d = 50 um", "Sintered, d = 10 um"

# User palette, plus tints of it for fills
SAGE, FERN, PINE, INK = "#9CB080", "#618764", "#2B5748", "#273338"
TINT, MIST = "#EEF2E8", "#D9E2CC"

def kozeny(d, eps=0.5): return d ** 2 * eps ** 3 / (150 * (1 - eps) ** 2)
def p_cap(r, theta_deg=0.0): return 2 * sigma * math.cos(math.radians(theta_deg)) / r
def a_l(K, tw=t_w): return mu_l * lnR / (hfg * 2 * math.pi * rho_l * K * (2 * tw))
def a_v(h): return 6 * mu_v * lnR / (hfg * math.pi * rho_v * h ** 3)
def dT_from_dP(dP): return dP * T / (rho_v * hfg)
def q_max(pc, K, h, tw=t_w, vertical=False):
    return max(pc - (rho_l * g_acc * dz if vertical else 0.0), 0.0) / (a_l(K, tw) + a_v(h))

WICKS = {MESH: dict(r=64e-6, K=2.8e-11), S50: dict(r=0.21 * 50e-6, K=kozeny(50e-6)), S10: dict(r=0.21 * 10e-6, K=kozeny(10e-6))}
SHORT = {MESH: "Cu mesh #200", S50: "Sintered, d = 50 µm", S10: "Sintered, d = 10 µm"}
nu_ratio = (mu_v / rho_v) / (mu_l / rho_l)

def optimum(K, H=H_in):
    """Minimise a_l(t) + a_v(h) with h = H - 2t. Stationary point: h^2/t = G = 12*sqrt(K*nu_v/nu_l)."""
    G = 12 * math.sqrt(K * nu_ratio)
    t = ((4 * H + G) - math.sqrt((4 * H + G) ** 2 - 16 * H ** 2)) / 8
    return dict(G_um=G * 1e6, t_um=t * 1e6, h_um=(H - 2 * t) * 1e6)

TWS = [t * 1e-6 for t in range(10, 101, 2)]
out = dict(H_in_um=H_in * 1e6, nu_ratio=nu_ratio, wick={}, sweep=dict(tw_um=[round(t * 1e6) for t in TWS]))
for n, w in WICKS.items():
    pc, K = p_cap(w["r"]), w["K"]
    o = optimum(K)
    t, h = o["t_um"] * 1e-6, o["h_um"] * 1e-6
    sweep = [q_max(pc, K, H_in - 2 * x, tw=x) for x in TWS]
    i = max(range(len(sweep)), key=sweep.__getitem__)
    o.update(Q_opt=q_max(pc, K, h, tw=t), al_over_av=a_l(K, t) / a_v(h), tw_sweep_um=TWS[i] * 1e6, Q_sweep=sweep[i],
             dP_v_at_Qopt_kPa=a_v(h) * q_max(pc, K, h, tw=t) / 1e3)
    # the closed form must land on the swept optimum (2 um grid) and on calc.py's result
    assert abs(o["t_um"] - TWS[i] * 1e6) <= 2.0, (n, o)
    assert abs(N["coupling"][n]["tw_opt_um"] - TWS[i] * 1e6) < 1e-6
    out["wick"][n] = o
    out["sweep"][n] = sweep

# vapour chamber against a solid copper sheet of the same total thickness, 5 W, same source and rim (from calc.py's keff table)
_kx = {(int(r["h_um"]), r["Q"]): r for r in N["keff"]}
out["vs_copper"] = [dict(h_um=h, H_mm=_kx[(h, 5)]["H_mm"], vc=_kx[(h, 5)]["dT_tot"], cu=_kx[(h, 5)]["dT_copper_plate"],
                         factor=_kx[(h, 5)]["dT_copper_plate"] / _kx[(h, 5)]["dT_tot"],
                         vapour=_kx[(h, 5)]["dT_v"], wick=_kx[(h, 5)]["dT_w"], interface=_kx[(h, 5)]["dT_i"]) for h in (400, 200, 100, 50)]

# thickness comparison used on the split illustration (50 um powder)
w = WICKS[S50]
out["split_examples"] = [dict(t_um=t, h_um=H_in * 1e6 - 2 * t, Q=q_max(p_cap(w["r"]), w["K"], H_in - 2 * t * 1e-6, tw=t * 1e-6)) for t in (20, 50, 90)]
# what halving the gap does at the optimum and away from it, and the 5 W vapour drop at the optimum core
out["dT_5W_h150"] = dT_from_dP(a_v(150e-6) * 5)
out["K_per_kPa"] = dT_from_dP(1000.0)

if __name__ == "__main__":
    with open(os.path.join(HERE, "numbers_focused.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "sweep"}, indent=1))
