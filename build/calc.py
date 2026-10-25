"""
Order-of-magnitude model of an ultra-thin vapour chamber (VC).

All numbers quoted in the term paper, slides and study guide come from this file.
Run:  python -X utf8 calc.py     -> writes numbers.json and ../figures/f*.png

The model is deliberately simple (see section 7 of the paper for its assumptions):
 - saturated water at 60 C, copper walls, a disc-shaped chamber of equal area to a phone-size sheet
 - one heat source in the centre (radius R1), condensation at the outer radius R2 (conservative)
 - radial Darcy flow in the wick, radial Poiseuille flow in the vapour slit
"""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "..", "figures")
os.makedirs(FIG, exist_ok=True)

# ---------------------------------------------------------------- properties
# Saturated water at 60 C (rounded steam-table values)
T = 333.15            # K
rho_l = 983.2         # kg/m3
rho_v = 0.1304        # kg/m3
mu_l = 4.66e-4        # Pa s
mu_v = 1.08e-5        # Pa s
sigma = 0.0662        # N/m
hfg = 2.358e6         # J/kg
k_l = 0.653           # W/m K
P_sat = 19.95e3       # Pa
R_v = 461.5           # J/kg K (steam)
gamma = 1.33
g = 9.81
k_cu = 400.0
kB = 1.381e-23
d_mol = 2.6e-10       # kinetic diameter of H2O, m (rough)

# Geometry (illustrative)
Q_base = 5.0                      # W, full-load phone SoC (illustrative)
A_src = 10e-3 * 10e-3             # 10 mm x 10 mm source
R1 = math.sqrt(A_src / math.pi)   # equivalent radius, 5.64 mm
R2 = 48e-3                        # disc of the same area as 60 x 120 mm sheet
t_wall = 0.08e-3                  # each copper wall
t_w = 0.05e-3                     # each wick layer
dz_vert = 0.10                    # m, source at the top of a vertical sheet
lnR = math.log(R2 / R1)

out = {"props": dict(T=T, rho_l=rho_l, rho_v=rho_v, mu_l=mu_l, mu_v=mu_v, sigma=sigma, hfg=hfg,
                     P_sat=P_sat), "geom": dict(R1=R1, R2=R2, lnR=lnR, t_w=t_w, t_wall=t_wall, Q=Q_base)}

# ---------------------------------------------------------------- formulas
def p_cap(r_eff, theta_deg=0.0):
    return 2 * sigma * math.cos(math.radians(theta_deg)) / r_eff

def mdot(Q):
    return Q / hfg

def a_liquid(K, tw=t_w):
    """dP_l = a_l * Q : radial Darcy flow through two wick layers (thickness 2*tw)."""
    return mu_l * lnR / (hfg * 2 * math.pi * rho_l * K * (2 * tw))

def a_vapour(h):
    """dP_v = a_v * Q : radial Poiseuille flow in a slit of height h, all vapour reaching R2."""
    return 6 * mu_v * lnR / (hfg * math.pi * rho_v * h ** 3)

def dT_from_dP(dP):
    """Clausius-Clapeyron: temperature equivalent of a vapour pressure drop (ideal-gas vapour)."""
    return dP * T / (rho_v * hfg)

def q_max(pcap, K, h, vertical=False, tw=t_w):
    head = rho_l * g * dz_vert if vertical else 0.0
    avail = pcap - head
    return max(avail, 0.0) / (a_liquid(K, tw) + a_vapour(h))

def q_sonic(h):
    A = 2 * math.pi * R1 * h
    return rho_v * hfg * A * math.sqrt(gamma * R_v * T / (2 * (gamma + 1)))

def mean_free_path():
    return kB * T / (math.sqrt(2) * math.pi * d_mol ** 2 * P_sat)

def h_interface(sig_acc):
    """Schrage/Hertz-Knudsen linearised interface coefficient, W/m2K."""
    return (2 * sig_acc / (2 - sig_acc)) * (hfg ** 2 * rho_v / T) * math.sqrt(1 / (2 * math.pi * R_v * T))

def k_maxwell(eps, ks=k_cu, kl=k_l):
    r = kl / ks
    return ks * (2 + r - 2 * eps * (1 - r)) / (2 + r + eps * (1 - r))

# ---------------------------------------------------------------- wick families
def kozeny_sphere(d, eps=0.5):
    return d ** 2 * eps ** 3 / (150 * (1 - eps) ** 2)

wicks = {
    "Cu mesh (#200)":       dict(r=64e-6, K=2.8e-11),
    "Sintered, d = 50 um":  dict(r=0.21 * 50e-6, K=kozeny_sphere(50e-6)),
    "Sintered, d = 10 um":  dict(r=0.21 * 10e-6, K=kozeny_sphere(10e-6)),
}
out["wicks"] = {}
for n, w in wicks.items():
    out["wicks"][n] = dict(r_um=w["r"] * 1e6, K=w["K"], p_cap_kPa=p_cap(w["r"]) / 1e3,
                           a_l_Pa_per_W=a_liquid(w["K"]))

# ---------------------------------------------------------------- scaling numbers
lam = mean_free_path()
out["lambda_um"] = lam * 1e6
out["head_100mm_kPa"] = rho_l * g * dz_vert / 1e3
out["mdot_5W_kg_s"] = mdot(Q_base)
out["Qv_5W_m3_s"] = mdot(Q_base) / rho_v
out["Bo"] = {f"{h*1e6:.0f}um": rho_l * g * h ** 2 / sigma for h in (1e-3, 400e-6, 200e-6, 100e-6, 50e-6)}
out["Kn_vapour"] = {f"{h*1e6:.0f}um": lam / h for h in (200e-6, 100e-6, 50e-6, 20e-6, 5e-6)}
out["Kn_pore_1um"] = lam / 1e-6
out["Kn_pore_10um"] = lam / 10e-6

# vapour core table
rows = []
for h in (400e-6, 200e-6, 100e-6, 50e-6, 25e-6):
    d = dict(h_um=h * 1e6)
    for Q in (5, 20, 50):
        dP = a_vapour(h) * Q
        d[f"dP_{Q}W_Pa"] = dP
        d[f"dT_{Q}W_K"] = dT_from_dP(dP)
    d["Q_sonic_W"] = q_sonic(h)
    u = (mdot(5) / rho_v) / (2 * math.pi * R1 * h)
    d["u_5W_m_s"] = u
    d["Ma_5W"] = u / math.sqrt(gamma * R_v * T)
    d["Kn"] = lam / h
    rows.append(d)
out["vapour_core"] = rows
# thickness below which the linear model is invalid (dP = 0.2 P_sat)
out["h_invalid_um"] = {f"{Q}W": ((a_vapour(1.0) * Q / (0.2 * P_sat)) ** (1 / 3)) * 1e6 for Q in (5, 20, 50)}
# loss at 5 W for the Fig. 2 line
out["loss5_sinter50_h100_Pa"] = (a_liquid(kozeny_sphere(50e-6)) + a_vapour(100e-6)) * Q_base
# the 1/h^3 statement
out["ratio_halving"] = a_vapour(50e-6) / a_vapour(100e-6)

# capillary limit table
cl = {}
for n, w in wicks.items():
    cl[n] = {}
    for h in (200e-6, 100e-6, 50e-6):
        cl[n][f"{h*1e6:.0f}um"] = dict(horizontal_W=q_max(p_cap(w["r"]), w["K"], h),
                                       vertical_W=q_max(p_cap(w["r"]), w["K"], h, vertical=True))
out["cap_limit"] = cl

# interface
out["h_interface"] = {f"{s}": h_interface(s) for s in (1.0, 0.1, 0.03, 0.01, 0.001)}
q_flux = Q_base / A_src
out["q_flux_5W_W_m2"] = q_flux
out["dT_interface_5W"] = {f"{s}": q_flux / h_interface(s) for s in (1.0, 0.1, 0.03, 0.01, 0.001)}
out["k_wick_maxwell_eps0.5"] = k_maxwell(0.5)

# ---------------------------------------------------------------- effective conductivity
def total_dT(Q, h, K=None, sig_acc=0.1, kwick=None):
    kw = kwick or k_maxwell(0.5)
    dTv = dT_from_dP(a_vapour(h) * Q)
    dTw = (Q / A_src) * t_w / kw
    dTi = (Q / A_src) / h_interface(sig_acc)
    return dTv, dTw, dTi

def keff_radial(Q, H, dT):
    return Q * lnR / (2 * math.pi * H * dT)

def keff_strip(Q, H, dT):
    return Q * (R2 - R1) / (dT * H * 2 * R1)

keff = []
for h in (400e-6, 200e-6, 100e-6, 50e-6, 25e-6):
    H = h + 2 * t_w + 2 * t_wall
    for Q in (5, 20, 50):
        dTv, dTw, dTi = total_dT(Q, h)
        dT = dTv + dTw + dTi
        keff.append(dict(h_um=h * 1e6, H_mm=H * 1e3, Q=Q, dT_v=dTv, dT_w=dTw, dT_i=dTi, dT_tot=dT,
                         keff_radial=keff_radial(Q, H, dT), keff_strip=keff_strip(Q, H, dT),
                         dT_copper_plate=Q * lnR / (2 * math.pi * k_cu * H)))
out["keff"] = keff

# biporous idealisation: fine pores set pressure, coarse channels set permeability
bip = dict(r_fine=5e-6, K_coarse=kozeny_sphere(100e-6), r_coarse=0.21 * 100e-6, K_fine=kozeny_sphere(23e-6))
h_ref = 100e-6
bip_res = {
    "fine monoporous (r=5 um)":     q_max(p_cap(bip["r_fine"]), bip["K_fine"], h_ref),
    "coarse monoporous (r=21 um)":  q_max(p_cap(bip["r_coarse"]), kozeny_sphere(100e-6), h_ref),
    "biporous (r=5 um, K of coarse)": q_max(p_cap(bip["r_fine"]), bip["K_coarse"], h_ref),
}
bip_res_v = {
    "fine monoporous (r=5 um)":     q_max(p_cap(bip["r_fine"]), bip["K_fine"], h_ref, vertical=True),
    "coarse monoporous (r=21 um)":  q_max(p_cap(bip["r_coarse"]), kozeny_sphere(100e-6), h_ref, vertical=True),
    "biporous (r=5 um, K of coarse)": q_max(p_cap(bip["r_fine"]), bip["K_coarse"], h_ref, vertical=True),
}
out["biporous"] = dict(horizontal=bip_res, vertical=bip_res_v, K_fine=bip["K_fine"], K_coarse=bip["K_coarse"])

# ---------------------------------------------------------------- figures
C = dict(blue="#0072B2", orange="#E69F00", green="#009E73", red="#D55E00", purple="#CC79A7",
         sky="#56B4E9", grey="#555555", light="#DDDDDD")
plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.25, "figure.dpi": 100, "savefig.dpi": 220,
                     "font.family": "DejaVu Sans"})

def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, name), bbox_inches="tight")
    plt.close(fig)

# F1: cycle schematic
fig, ax = plt.subplots(figsize=(7.2, 3.3))
ax.set_xlim(0, 12.6); ax.set_ylim(-1.0, 5.4); ax.axis("off")
ax.add_patch(Rectangle((0.5, 0.4), 11, 0.35, fc="#B87333", ec="k", lw=0.8))      # bottom wall
ax.add_patch(Rectangle((0.5, 4.2), 11, 0.35, fc="#B87333", ec="k", lw=0.8))      # top wall
ax.add_patch(Rectangle((0.5, 0.75), 11, 0.55, fc="#BFE0F5", ec="k", lw=0.5))     # bottom wick
ax.add_patch(Rectangle((0.5, 3.65), 11, 0.55, fc="#BFE0F5", ec="k", lw=0.5))     # top wick
ax.add_patch(Rectangle((0.5, 1.3), 11, 2.35, fc="#FFF8E1", ec="none"))            # vapour
for x in np.arange(0.8, 11.3, 0.28):
    ax.plot([x, x], [0.8, 1.25], color=C["sky"], lw=0.6); ax.plot([x, x], [3.7, 4.15], color=C["sky"], lw=0.6)
ax.text(6, 2.5, "vapour core (height h)", ha="center", va="center", fontsize=9, color=C["grey"])
ax.text(11.65, 1.02, "wick", fontsize=8, va="center"); ax.text(11.65, 3.92, "wick", fontsize=8, va="center")
ax.add_patch(Rectangle((0.5, -0.55), 2.0, 0.4, fc=C["red"], ec="none"))
ax.text(1.5, -0.85, "heat source (evaporator)", ha="center", fontsize=8, color=C["red"])
ax.annotate("", xy=(1.5, 0.4), xytext=(1.5, -0.15), arrowprops=dict(arrowstyle="-|>", color=C["red"], lw=1.8))
ax.annotate("", xy=(7.3, 5.1), xytext=(7.3, 4.58), arrowprops=dict(arrowstyle="-|>", color=C["blue"], lw=1.6))
ax.text(7.3, 5.15, "heat out (condenser)", ha="center", va="bottom", fontsize=8, color=C["blue"])
for (x0, x1, y) in ((1.5, 5.4, 2.1), (1.5, 5.4, 2.9)):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y), arrowstyle="-|>", mutation_scale=11, color=C["orange"], lw=1.5))
ax.text(1.7, 3.25, "(2) vapour flows outward", color=C["orange"], fontsize=8)
ax.add_patch(FancyArrowPatch((9.6, 3.9), (3.6, 3.9), arrowstyle="-|>", mutation_scale=11, color=C["green"], lw=1.5))
ax.add_patch(FancyArrowPatch((9.6, 1.0), (3.6, 1.0), arrowstyle="-|>", mutation_scale=11, color=C["green"], lw=1.5))
ax.text(9.5, 2.6, "(4) liquid returns through\nthe wick by capillary suction", color=C["green"], fontsize=8, va="center", ha="center")
ax.text(1.5, 1.55, "(1) evaporation", color=C["red"], fontsize=8, ha="center")
ax.text(7.3, 3.3, "(3) condensation", color=C["blue"], fontsize=8, ha="center")
save(fig, "f1_cycle.png")

# F2: capillary pressure vs pore radius, with the pressures it has to beat
r = np.logspace(-7, -4, 200)
fig, ax = plt.subplots(figsize=(6.2, 3.6))
ax.loglog(r * 1e6, 2 * sigma / r / 1e3, color=C["blue"], lw=2, label=r"capillary pressure $2\sigma/r$ ($\theta=0$)")
ax.axhline(rho_l * g * dz_vert / 1e3, color=C["red"], ls="--", label="gravity head, 100 mm (source on top)")
loss5 = (a_liquid(wicks["Sintered, d = 50 um"]["K"]) + a_vapour(100e-6)) * Q_base
ax.axhline(loss5 / 1e3, color=C["green"], ls=":", lw=1.5, label="wick + vapour loss at 5 W, h = 100 um (sintered 50 um)")
for n, w in wicks.items():
    ax.plot(w["r"] * 1e6, p_cap(w["r"]) / 1e3, "o", color=C["orange"], ms=6)
    ax.annotate(n, (w["r"] * 1e6, p_cap(w["r"]) / 1e3), textcoords="offset points", xytext=(6, 5), fontsize=7)
ax.set_xlabel(r"effective pore radius $r_{eff}$ ($\mu$m)"); ax.set_ylabel("pressure (kPa)")
ax.legend(fontsize=7, loc="upper right"); ax.set_ylim(0.05, 3000)
save(fig, "f2_capillary_pressure.png")

# F3: trade-off, K versus r_eff with iso-lines of K * p_cap (liquid-limited transport capacity)
fig, ax = plt.subplots(figsize=(6.2, 3.8))
dd = np.logspace(math.log10(2e-6), math.log10(300e-6), 100)
ax.loglog(0.21 * dd * 1e6, [kozeny_sphere(d) for d in dd], color=C["blue"], lw=2, label="sintered spheres (Kozeny-Carman, $\\epsilon=0.5$)")
ax.plot([64], [2.8e-11], "s", color=C["orange"], ms=7, label="Cu mesh #200")
rr = np.logspace(-6.5, -3.5, 50)
for m in (1e-7, 1e-6, 1e-5):  # lines of constant K/r (m) ~ transport capacity per unit pressure
    ax.plot(rr * 1e6, m * rr, color=C["light"], lw=1)
    ax.text(rr[-1] * 1e6 * 0.95, m * rr[-1], f"K/r = {m:.0e} m", fontsize=6.5, color=C["grey"], ha="right", va="bottom")
ax.set_xlabel(r"effective pore radius $r_{eff}$ ($\mu$m)"); ax.set_ylabel(r"permeability $K$ (m$^2$)")
ax.annotate("fine pores:\nhigh pumping pressure,\nhigh flow resistance", (0.7, 3e-15), fontsize=7.5, color=C["grey"])
ax.annotate("coarse pores:\nlow pumping pressure,\neasy flow", (30, 1e-9), fontsize=7.5, color=C["grey"])
ax.legend(fontsize=7, loc="lower right"); ax.set_xlim(0.3, 400); ax.set_ylim(1e-15, 1e-8)
save(fig, "f3_wick_tradeoff.png")

# F4: vapour core pressure drop / temperature drop vs thickness
h = np.logspace(math.log10(30e-6), math.log10(600e-6), 120)
valid_dP = 0.2 * P_sat      # linearised Clausius-Clapeyron only sensible while dP << P_sat
fig, ax = plt.subplots(figsize=(6.2, 3.8))
for Q, c in ((5, C["blue"]), (20, C["orange"]), (50, C["red"])):
    dT = np.array([dT_from_dP(a_vapour(x) * Q) for x in h])
    ok = np.array([a_vapour(x) * Q <= valid_dP for x in h])
    ax.loglog(h[ok] * 1e6, dT[ok], color=c, lw=2, label=f"{Q} W")
    ax.loglog(h[~ok] * 1e6, dT[~ok], color=c, lw=1.2, ls=":")
ax.axhline(1.0, color=C["grey"], ls=":", lw=1); ax.text(32, 1.1, "1 K reference", fontsize=7, color=C["grey"])
ax.set_xlabel(r"vapour core thickness $h$ ($\mu$m)"); ax.set_ylabel("saturation-temperature drop across vapour core (K)")
ax.text(32, 0.004, "dotted: pressure drop > 20% of P$_{sat}$,\nlinear model no longer valid", fontsize=7, color=C["grey"], va="bottom")
ax.legend(title="heat load", fontsize=7, title_fontsize=7, loc="upper right")
ax.set_xlim(30, 600)
save(fig, "f4_vapour_core.png")

# F5: interface resistance, accommodation coefficient
fig, ax = plt.subplots(figsize=(6.2, 3.4))
qq = np.logspace(3, 6, 100)
for s, c in ((1.0, C["blue"]), (0.1, C["green"]), (0.03, C["orange"]), (0.01, C["red"]), (0.001, C["purple"])):
    ax.loglog(qq / 1e4, qq / h_interface(s), color=c, lw=2, label=f"accommodation coeff. = {s:g}")
ax.axvline(q_flux / 1e4, color=C["grey"], ls=":"); ax.text(q_flux / 1e4 * 1.05, 2e-4, "5 W on 1 cm$^2$", fontsize=7, color=C["grey"])
ax.set_xlabel("heat flux through the interface (W/cm$^2$)"); ax.set_ylabel("interface temperature jump (K)")
ax.legend(fontsize=7); ax.set_ylim(1e-4, 1e3)
save(fig, "f5_interface.png")

# F6: capillary limit versus core thickness
fig, ax = plt.subplots(figsize=(6.4, 3.8))
for (n, w), c in zip(wicks.items(), (C["orange"], C["blue"], C["green"])):
    ax.loglog(h * 1e6, [q_max(p_cap(w["r"]), w["K"], x) for x in h], color=c, lw=2, label=n + ", horizontal")
    ax.loglog(h * 1e6, [q_max(p_cap(w["r"]), w["K"], x, vertical=True) if q_max(p_cap(w["r"]), w["K"], x, vertical=True) > 0 else np.nan for x in h],
              color=c, lw=1.4, ls="--")
ax.loglog(h * 1e6, [q_sonic(x) for x in h], color=C["grey"], lw=1.5, ls=":", label="sonic limit")
ax.axhline(5, color=C["red"], lw=0.8); ax.text(580, 5.6, "5 W phone load", fontsize=7, color=C["red"], ha="right")
ax.set_xlabel(r"vapour core thickness $h$ ($\mu$m)"); ax.set_ylabel("maximum heat load, capillary limit (W)")
ax.text(580, 2.2e4, "solid: horizontal   dashed: source on top of vertical sheet", fontsize=7, ha="right", color=C["grey"])
ax.legend(fontsize=7, loc="upper left"); ax.set_ylim(1, 6e4)
save(fig, "f6_limits.png")

# F7: effective conductivity is not a property
fig, ax = plt.subplots(figsize=(6.2, 3.6))
hs = np.array([400, 300, 200, 150, 100, 75, 50, 35]) * 1e-6
for fn, lab, c in ((keff_radial, "radial definition (source in the centre)", C["blue"]),
                   (keff_strip, "strip definition (same data, source width as area)", C["orange"])):
    ks, ok = [], []
    for x in hs:
        dTv, dTw, dTi = total_dT(5, x)
        ks.append(fn(5, x + 2 * t_w + 2 * t_wall, dTv + dTw + dTi)); ok.append(a_vapour(x) * 5 <= valid_dP)
    ks, ok = np.array(ks), np.array(ok)
    ax.semilogy(hs[ok] * 1e6, ks[ok], "o-", color=c, lw=2, label=lab)
    ax.semilogy(hs[~ok] * 1e6, ks[~ok], "o:", color=c, lw=1.2)
ax.axhline(k_cu, color=C["grey"], ls="--"); ax.text(36, k_cu * 1.25, "solid copper, 400 W/m K", fontsize=7, color=C["grey"])
ax.set_xlabel(r"vapour core thickness $h$ ($\mu$m)"); ax.set_ylabel(r"apparent $k_{eff}$ (W/m K), 5 W")
ax.legend(fontsize=7, loc="lower left"); ax.set_ylim(150, 3e5); ax.invert_xaxis()
save(fig, "f7_keff.png")

# F8: biporous idea
fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.1), gridspec_kw=dict(width_ratios=[1, 1.25]))
a = axs[0]; a.set_xlim(0, 10); a.set_ylim(-0.8, 6.8); a.set_aspect("equal"); a.axis("off")
rng = np.random.default_rng(3)
a.add_patch(Rectangle((0.3, 0.3), 9.4, 5.4, fc="#FBE9D5", ec="k"))

centres = []
for i in range(9):
    for j in range(7):
        cx, cy = 0.9 + i * 1.0 + rng.normal(0, .05), 0.9 + j * 0.75 + rng.normal(0, .05)
        a.add_patch(plt.Circle((cx, cy), 0.36, fc="#B87333", ec="#7a4a1d", lw=0.6))
a.add_patch(Rectangle((4.65, 0.3), 0.7, 5.4, fc="#BFE0F5", ec="none", alpha=0.9))
a.text(5.0, 5.85, "coarse channel", ha="center", fontsize=7.5, color=C["blue"])
a.text(5.0, -0.2, "fine pores between particles set the pressure", ha="center", fontsize=7.5, color=C["grey"])
a.set_title("idealised biporous wick (schematic)", fontsize=8)
b = axs[1]
labels = ["fine\nmonoporous", "coarse\nmonoporous", "biporous\n(ideal)"]
vals_h = [bip_res["fine monoporous (r=5 um)"], bip_res["coarse monoporous (r=21 um)"], bip_res["biporous (r=5 um, K of coarse)"]]
vals_v = [bip_res_v["fine monoporous (r=5 um)"], bip_res_v["coarse monoporous (r=21 um)"], bip_res_v["biporous (r=5 um, K of coarse)"]]
xx = np.arange(3)
b.bar(xx - 0.19, vals_h, 0.36, color=C["blue"], label="horizontal")
b.bar(xx + 0.19, vals_v, 0.36, color=C["orange"], label="source on top, vertical")
b.set_xticks(xx); b.set_xticklabels(labels, fontsize=8); b.set_ylabel("capillary-limit heat load (W)")
b.legend(fontsize=7); b.set_title("model result at $h$ = 100 um", fontsize=8)
for i, (u, v) in enumerate(zip(vals_h, vals_v)):
    b.text(i - 0.19, u + 3, f"{u:.0f}", ha="center", fontsize=7); b.text(i + 0.19, v + 3, f"{v:.0f}", ha="center", fontsize=7)
save(fig, "f8_biporous.png")


# F9: design coupling - fixed inner thickness shared between wick and vapour core
H_in = 250e-6
tws = np.linspace(10e-6, 100e-6, 46)
def coupling(wk):
    res = []
    for tw in tws:
        hh = H_in - 2 * tw
        res.append(q_max(p_cap(wk["r"]), wk["K"], hh, tw=tw))
    return np.array(res)
fig, ax = plt.subplots(figsize=(6.2, 3.6))
cpl = {}
for (n, wk), c in zip(wicks.items(), (C["orange"], C["blue"], C["green"])):
    v = coupling(wk)
    ax.plot(tws * 1e6, v, color=c, lw=2, label=n)
    i = int(np.argmax(v))
    ax.plot(tws[i] * 1e6, v[i], "o", color=c)
    cpl[n] = dict(tw_opt_um=tws[i] * 1e6, h_opt_um=(H_in - 2 * tws[i]) * 1e6, Q_opt=v[i])
ax.set_xlabel(r"thickness of each wick layer $t_w$ ($\mu$m)   [vapour core $h$ = 250 - 2$t_w$]")
ax.set_ylabel("capillary-limit heat load (W)")
ax.legend(fontsize=7); ax.set_ylim(0, None)
save(fig, "f9_coupling.png")
out["coupling_H_in_um"] = H_in * 1e6
out["coupling"] = cpl

with open(os.path.join(HERE, "numbers.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps({k: out[k] for k in ("lambda_um", "head_100mm_kPa", "Bo", "Kn_vapour", "ratio_halving", "wicks", "h_interface", "dT_interface_5W", "k_wick_maxwell_eps0.5", "biporous")}, indent=1))
print(out["h_invalid_um"], out["loss5_sinter50_h100_Pa"])
print("VAPOUR CORE"); [print({k: round(v, 4) for k, v in r_.items()}) for r_ in out["vapour_core"]]
print("CAP LIMIT"); print(json.dumps(out["cap_limit"], indent=1))
print("KEFF"); [print({k: round(v, 3) for k, v in r_.items()}) for r_ in out["keff"]]
