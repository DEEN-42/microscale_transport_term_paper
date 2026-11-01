"""Illustrations and plots for the focused paper and 3-minute deck, in the user's four-colour palette.
Figures are drawn at their slide size in inches, so the font sizes here are the sizes seen on the slide.
Run after focused_model.py:  python -X utf8 figs_focused.py   -> writes ../figures/g*.png"""
import math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Arc, Polygon, Wedge
from focused_model import *

FIG = os.path.join(HERE, "..", "figures")
plt.rcParams.update({"font.family": ["Calibri", "DejaVu Sans"], "mathtext.fontset": "cm", "text.color": INK, "axes.edgecolor": INK,
                     "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK, "savefig.dpi": 260})

def save(fig, name, transparent=False):
    fig.savefig(os.path.join(FIG, name), transparent=transparent, facecolor="none" if transparent else "white")
    plt.close(fig)

def canvas(w, h, xmax, ymax):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, xmax); ax.set_ylim(0, ymax); ax.axis("off")
    return fig, ax

def arrow(ax, a, b, color=PINE, lw=3, ms=20, **kw):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw, shrinkA=0, shrinkB=0, **kw))

def badge(ax, x, y, n, r=0.27, fc=PINE, fs=14):
    ax.add_patch(Circle((x, y), r, fc=fc, ec="white", lw=1.5, zorder=8))
    ax.text(x, y - 0.01, str(n), ha="center", va="center", fontsize=fs, fontweight="bold", color="white", zorder=9)

def spheres(ax, x0, y0, x1, y1, d, fc=PINE, jitter=0.0, seed=2, alpha=1.0, zorder=3):
    """Hexagonal packing clipped to a rectangle, so the pore size visibly follows the particle size."""
    rng = np.random.default_rng(seed)
    clip = Rectangle((x0, y0), x1 - x0, y1 - y0, transform=ax.transData)
    row, y = 0, y0 + d * 0.5
    while y < y1 + d:
        x = x0 + (d * 0.5 if row % 2 else 0)
        while x < x1 + d:
            c = Circle((x + rng.normal(0, jitter), y + rng.normal(0, jitter)), d * 0.44, fc=fc, ec="none", alpha=alpha, zorder=zorder)
            ax.add_patch(c); c.set_clip_path(clip)
            x += d
        y += d * 0.866; row += 1

# ---------------------------------------------------------------- G1 the loop: half section, centre line at the left, rim at the right
fig = plt.figure(figsize=(12.1, 3.75)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 12.1); ax.set_ylim(-0.3, 3.45); ax.axis("off")
x0, x1, xr1 = 0.1, 10.1, 2.1                                                    # centre line, rim (R2), chip edge (R1)
ax.add_patch(Rectangle((x0, 2.72), x1 - x0, 0.14, fc=INK, ec="none"))           # top wall
ax.add_patch(Rectangle((x0, 0.62), x1 - x0, 0.14, fc=INK, ec="none"))           # bottom wall
ax.add_patch(Rectangle((x0, 2.32), x1 - x0, 0.40, fc=SAGE, ec="none"))          # top wick
ax.add_patch(Rectangle((x0, 0.76), x1 - x0, 0.40, fc=SAGE, ec="none"))          # bottom wick
ax.add_patch(Rectangle((x0, 1.16), x1 - x0, 1.16, fc=TINT, ec="none"))          # vapour core
ax.add_patch(Rectangle((2.3, 1.16), 0.4, 1.16, fc=SAGE, ec="none"))             # wick column joining the two wicks
arrow(ax, (2.5, 2.2), (2.5, 1.3), color=PINE, lw=3, ms=16)
ax.add_patch(Rectangle((x0, 0.26), xr1 - x0, 0.36, fc=INK, ec="none"))          # chip under the centre
ax.text(1.1, 0.44, "chip (hot spot)", ha="center", va="center", color="white", fontsize=13.5, fontweight="bold")
ax.plot([x0, x0], [0.26, 2.86], color=INK, lw=1.4, ls=(0, (4, 3)))
ax.text(0.2, 3.3, "centre line", fontsize=12, va="center")
for x in (0.6, 1.1, 1.6):                                                        # evaporation above the chip
    arrow(ax, (x, 1.16), (x, 1.5), color=FERN, lw=2.2, ms=14)
ax.text(1.1, 1.72, "evaporation", ha="center", va="center", fontsize=13.5, color=PINE, fontweight="bold")
ys = 1.7                                                                         # vapour narrows as it condenses on the way
ax.add_patch(Polygon([(2.95, ys + 0.16), (8.7, ys + 0.03), (8.7, ys - 0.03), (2.95, ys - 0.16)], fc=FERN, ec="none"))
ax.add_patch(Polygon([(8.7, ys + 0.14), (9.1, ys), (8.7, ys - 0.14)], fc=FERN, ec="none"))
xs = [x for x in np.arange(0.6, 9.3, 0.8) if not 2.0 <= x <= 2.9]
for x in xs:                                                                     # condensation, and heat out through the whole cooler surface
    arrow(ax, (x, 2.0), (x, 2.32), color=FERN, lw=2.2, ms=14)
for x in np.arange(0.6, 9.3, 0.8):
    arrow(ax, (x, 2.9), (x, 3.12), color=INK, lw=2.2, ms=14)
ax.text(5.0, 3.3, "heat out through the whole cooler surface", ha="center", va="center", fontsize=13.5, fontweight="bold")
arrow(ax, (9.7, 0.96), (1.9, 0.96), color=PINE, lw=3.5, ms=22)                   # liquid back to the evaporator
arrow(ax, (9.7, 2.52), (2.7, 2.52), color=PINE, lw=3.5, ms=22)
badge(ax, 3.2, 1.36, 3, r=0.2, fs=12)
ax.text(3.5, 1.36, "Vapour flow in a thin core", va="center", fontsize=14.5, color=PINE, fontweight="bold")
ax.text(7.55, 1.36, "condensation", va="center", ha="center", fontsize=13.5, color=PINE, fontweight="bold")
badge(ax, 3.0, 0.42, 1, r=0.2, fs=12)
ax.text(3.3, 0.42, "Liquid return in the wick, through wick columns", fontsize=14.5, color=PINE, fontweight="bold", va="center")
ax.annotate("", xy=(10.25, 1.16), xytext=(10.25, 2.32), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
ax.text(10.33, 1.74, "h", fontsize=15, style="italic", va="center")
ax.annotate("", xy=(10.25, 0.76), xytext=(10.25, 1.16), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
ax.text(10.33, 0.96, "$t$", fontsize=16, va="center")
badge(ax, 11.3, 2.15, 2, r=0.2, fs=12)
ax.text(11.3, 1.5, "Wick and core\nshare a fixed\nthickness", ha="center", va="center", fontsize=13.5, color=PINE, fontweight="bold")
ax.plot([x0, x1], [0.06, 0.06], color=INK, lw=1.2)                               # radial scale: 0, R1, R2
for xt, lab in ((x0, "0"), (xr1, "$R_1$"), (x1, "$R_2$")):
    ax.plot([xt, xt], [0.0, 0.12], color=INK, lw=1.2); ax.text(xt, -0.16, lab, ha="center", va="center", fontsize=14)
ax.text(6.2, -0.16, "radial distance from the centre line", ha="center", va="center", fontsize=12)
save(fig, "g1_cycle.png")

# ---------------------------------------------------------------- G0 title-slide motif (on dark background)
fig, ax = canvas(13.333, 2.6, 13.333, 2.6)
ax.add_patch(Rectangle((0, 2.2), 13.333, 0.12, fc=SAGE, ec="none"))
ax.add_patch(Rectangle((0, 0.28), 13.333, 0.12, fc=SAGE, ec="none"))
ax.add_patch(Rectangle((0, 1.86), 13.333, 0.34, fc=FERN, ec="none"))
ax.add_patch(Rectangle((0, 0.40), 13.333, 0.34, fc=FERN, ec="none"))
ax.add_patch(Rectangle((0, 0.74), 13.333, 1.12, fc=PINE, ec="none"))
for x in np.arange(0.9, 12.6, 2.9):
    arrow(ax, (x, 1.30), (x + 1.8, 1.30), color=SAGE, lw=4, ms=24)
for y in (0.57, 2.03):
    for x in np.arange(12.0, 0.6, -2.3):
        arrow(ax, (x, y), (x - 1.2, y), color=INK, lw=2.2, ms=14)
save(fig, "g0_title_band.png", transparent=True)

# ---------------------------------------------------------------- G2 meniscus zoom + coarse vs fine wick
fig, ax = canvas(6.3, 4.75, 6.3, 4.75)
# meniscus in one pore (left)
wx0, wx1, ybot, ytop = 0.65, 2.45, 0.85, 4.0
th = math.radians(35); r = (wx1 - wx0) / 2; xc = (wx0 + wx1) / 2; R = r / math.cos(th)
y_contact = 2.85; yc = y_contact + R * math.sin(th)
xs = np.linspace(wx0, wx1, 80); ys = yc - np.sqrt(R ** 2 - (xs - xc) ** 2)
ax.add_patch(Polygon(list(zip(xs, ys)) + [(wx1, ybot), (wx0, ybot)], fc=SAGE, ec="none"))
ax.plot(xs, ys, color=PINE, lw=2.5)
for x_ in (wx0 - 0.14, wx1):
    ax.add_patch(Rectangle((x_, ybot), 0.14, ytop - ybot, fc=INK, ec="none"))
ax.annotate("", xy=(wx0, 1.15), xytext=(xc, 1.15), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
ax.text((wx0 + xc) / 2, 1.24, "$r_{eff}$", ha="center", fontsize=15)
ax.text(xc, 3.55, "vapour\n$P_v$", ha="center", va="center", fontsize=14.5)
ax.text(xc + 0.36, 1.82, "liquid\n$P_l$", ha="center", va="center", fontsize=14.5, color=INK)
# contact angle: between the wall (pointing down into the liquid) and the meniscus tangent
ax.add_patch(Arc((wx0, y_contact), 0.9, 0.9, angle=0, theta1=270, theta2=270 + math.degrees(th), color=INK, lw=1.4))
ax.text(wx0 + 0.20, y_contact - 0.66, r"$\theta$", fontsize=16)
ax.text(1.5, 0.48, "meniscus = the pump", ha="center", fontsize=14.5, fontweight="bold", color=PINE)
ax.text(1.5, 4.32, "One pore", ha="center", fontsize=15.5, fontweight="bold")
# coarse and fine strips (right)
for (y0, d, title, s1, s2) in ((2.62, 0.62, "Coarse wick (large d)", "weak pump: low $\\Delta P_{cap}$", "easy flow: high $K$"),
                               (0.28, 0.20, "Fine wick (small d)", "strong pump: high $\\Delta P_{cap}$", "hard flow: low $K$")):
    xa, xb, h_ = 3.1, 6.05, 1.02
    ax.text(xa, y0 + h_ + 0.58, title, fontsize=15.5, fontweight="bold")
    ax.add_patch(Rectangle((xa, y0 + 0.48), xb - xa, h_, fc=SAGE, ec="none", zorder=1))
    spheres(ax, xa, y0 + 0.48, xb, y0 + 0.48 + h_, d, fc=PINE)
    arrow(ax, (xb - 0.15, y0 + 0.48 + h_ / 2), (xa + 0.15, y0 + 0.48 + h_ / 2), color="white", lw=3.5, ms=22, zorder=6)
    ax.text(xa, y0 + 0.24, s1, fontsize=14, va="center")
    ax.text(xa, y0 + 0.0, s2, fontsize=14, va="center")
save(fig, "g2_wick.png")

# ---------------------------------------------------------------- G4 biporous structure
fig, ax = canvas(6.3, 4.05, 6.3, 4.05)
xa, xb, ya, yb = 0.2, 6.1, 0.92, 3.5
ax.add_patch(Rectangle((xa, ya), xb - xa, yb - ya, fc=SAGE, ec="none", zorder=1))
clip = Rectangle((xa, ya), xb - xa, yb - ya, transform=ax.transData)
rng = np.random.default_rng(5)
RC, r_small = 0.54, 0.066
centres = []
for row, yy in enumerate(np.arange(ya + 0.2, yb + 0.5, 1.26)):
    for xx in np.arange(xa + (0.0 if row % 2 == 0 else 0.68), xb + 0.7, 1.36):
        centres.append((xx, yy))
for (cx, cy) in centres:
    for ax_x in np.arange(cx - RC, cx + RC, r_small * 2.0):
        for ax_y in np.arange(cy - RC, cy + RC, r_small * 1.75):
            if (ax_x - cx) ** 2 + (ax_y - cy) ** 2 <= RC ** 2:
                c = Circle((ax_x + rng.normal(0, .006), ax_y + rng.normal(0, .006)), r_small * 0.92, fc=PINE, ec="none", zorder=3)
                ax.add_patch(c); c.set_clip_path(clip)
# liquid threading the coarse channels between clusters
for y_ in (1.75, 3.01):
    arrow(ax, (xb - 0.1, y_), (xa + 0.1, y_), color="white", lw=4.5, ms=26, zorder=6)
ax.text(3.15, 3.8, "Clusters of fine particles, with coarse channels between them", ha="center", fontsize=14, fontweight="bold")
ax.plot([1.56, 1.56], [0.8, 1.12], color=INK, lw=1.2, zorder=7); ax.plot(1.56, 1.12, "o", ms=6, mfc="white", mec=INK, zorder=8)
ax.text(0.2, 0.62, "inside a cluster: fine pores", fontsize=14, fontweight="bold", color=PINE, va="center")
ax.text(0.2, 0.32, "small $r_{eff}$, strong pump", fontsize=14, va="center")
ax.plot([4.96, 4.96], [0.8, 1.6], color=INK, lw=1.2, zorder=7); ax.plot(4.96, 1.6, "o", ms=6, mfc="white", mec=INK, zorder=8)
ax.text(3.45, 0.62, "between: coarse channels", fontsize=14, fontweight="bold", color=PINE, va="center")
ax.text(3.45, 0.32, "high $K$, easy liquid flow", fontsize=14, va="center")
save(fig, "g4_biporous.png")

# ---------------------------------------------------------------- G5 fixed-thickness split, three cases to scale
ex = out["split_examples"]
fig, ax = canvas(5.75, 2.5, 5.75, 2.5)
titles = ("thin wick", "best split", "thin core")
scale = 1.25 / 250
for i, e in enumerate(ex):
    x = 0.1 + i * 1.93; w_ = 1.65; y = 0.63
    tw_, h_ = e["t_um"] * scale, e["h_um"] * scale
    ax.add_patch(Rectangle((x, y), w_, tw_, fc=SAGE, ec="none"))
    ax.add_patch(Rectangle((x, y + tw_), w_, h_, fc=TINT, ec=SAGE, lw=0.6))
    ax.add_patch(Rectangle((x, y + tw_ + h_), w_, tw_, fc=SAGE, ec="none"))
    for yy in (y - 0.05, y + 1.25):
        ax.add_patch(Rectangle((x, yy), w_, 0.05, fc=INK, ec="none"))
    lw_ = 1.2 + 4.0 * (e["h_um"] / 210)
    arrow(ax, (x + 0.25, y + tw_ + h_ / 2), (x + w_ - 0.25, y + tw_ + h_ / 2), color=FERN, lw=lw_, ms=10 + 12 * e["h_um"] / 210)
    best = i == 1
    ax.text(x + w_ / 2, 2.2, titles[i], ha="center", fontsize=14.5, fontweight="bold", color=PINE if best else INK)
    ax.text(x + w_ / 2, 0.39, f"$t$ = {e['t_um']:.0f} µm, $h$ = {e['h_um']:.0f} µm", ha="center", fontsize=13.5)
    ax.text(x + w_ / 2, 0.12, f"{e['Q']:.0f} W", ha="center", fontsize=15.5, fontweight="bold", color=PINE if best else INK)
save(fig, "g5_split.png")

# ---------------------------------------------------------------- G6 radial flow (top view) + slit profile (side view)
fig, ax = canvas(6.3, 2.95, 6.3, 2.95)
cx, cy, Ro, Ri = 1.42, 1.66, 1.2, 0.32
ax.add_patch(Circle((cx, cy), Ro, fc=TINT, ec=SAGE, lw=2))
ax.add_patch(Circle((cx, cy), Ri, fc=INK, ec="none"))
for a in np.arange(0, 360, 45):
    c_, s_ = math.cos(math.radians(a)), math.sin(math.radians(a))
    arrow(ax, (cx + (Ri + .07) * c_, cy + (Ri + .07) * s_), (cx + (Ro - .1) * c_, cy + (Ro - .1) * s_), color=FERN, lw=2.2, ms=13)
ax.text(cx, cy, "$R_1$", ha="center", va="center", color="white", fontsize=15.5)
ax.text(cx + 0.88, cy + 0.86, "$R_2$", fontsize=15.5, va="bottom")
ax.text(cx, 0.1, "top view: flow area $2\\pi r h$", ha="center", fontsize=13.5, va="bottom", fontweight="bold")
# slit side view
xa, xb, ya, yb = 3.25, 6.0, 1.05, 2.25
for yy in (ya - 0.13, yb):
    ax.add_patch(Rectangle((xa, yy), xb - xa, 0.13, fc=SAGE, ec="none"))
zz = np.linspace(ya, yb, 60); xi = (zz - ya) / (yb - ya); prof = 4 * xi * (1 - xi) * 1.45
ax.fill_betweenx(zz, xa + 0.42, xa + 0.42 + prof, color=MIST, lw=0)
ax.plot(xa + 0.42 + prof, zz, color=PINE, lw=2.2)
ax.plot([xa + 0.42] * 2, [ya, yb], color=INK, lw=1)
for z_ in np.linspace(ya + .17, yb - .17, 5):
    xi_ = (z_ - ya) / (yb - ya)
    arrow(ax, (xa + 0.42, z_), (xa + 0.42 + 4 * xi_ * (1 - xi_) * 1.45, z_), color=PINE, lw=1.4, ms=9)
ax.annotate("", xy=(xa + 0.18, ya), xytext=(xa + 0.18, yb), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
ax.text(xa + 0.05, (ya + yb) / 2, "$h$", fontsize=16, ha="right", va="center")
ax.text((xa + xb) / 2, 2.62, "side view: Poiseuille profile", ha="center", fontsize=13.5, fontweight="bold")
ax.text(xa - 0.14, 0.55, "halve $h$:  $u$ ×2  and  $1/h^2$ ×4", fontsize=14, va="center")
ax.text(xa - 0.14, 0.2, "so $dP/dr$ rises ×8", fontsize=14.5, va="center", fontweight="bold", color=PINE)
save(fig, "g6_vapour.png")

# ---------------------------------------------------------------- data plots used in the paper
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": MIST, "grid.linewidth": 0.7})
def plain_x(ax):
    """Thickness axis as plain micrometre values rather than 3 x 10^1."""
    ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([30, 50, 100, 200, 400, 600]))
    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter()); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
STY = {MESH: dict(color=SAGE, ls="-", marker="s"), S50: dict(color=PINE, ls="-", marker="o"), S10: dict(color=INK, ls="--", marker="^")}

# G7 K vs r_eff
fig, ax = plt.subplots(figsize=(6.4, 3.5))
dd = np.logspace(math.log10(2e-6), math.log10(300e-6), 100)
ax.loglog(0.21 * dd * 1e6, [kozeny(d) for d in dd], color=PINE, lw=2.2, label=r"sintered spheres: Kozeny–Carman, $\varepsilon = 0.5$")
for n, w in WICKS.items():
    ax.plot(w["r"] * 1e6, w["K"], STY[n]["marker"], color=STY[n]["color"], mec=INK, ms=8, ls="none", label=SHORT[n], zorder=5)
ax.set_xlabel(r"effective pore radius $r_{eff}$ (µm)"); ax.set_ylabel(r"permeability $K$ (m$^2$)")
ax.annotate("fine pores: strong pump,\nhigh flow resistance", (1.3, 1.6e-14), fontsize=9)
ax.annotate("coarse pores: weak pump,\neasy flow", (2.2, 1.5e-10), fontsize=9)
ax.legend(fontsize=8.5, loc="lower right", frameon=False); ax.set_xlim(0.4, 100); ax.set_ylim(1e-14, 1e-9)
fig.tight_layout(); save(fig, "g7_tradeoff.png")

# G8 biporous bars
bh, bv = N["biporous"]["horizontal"], N["biporous"]["vertical"]
labs = ["Fine\nmonoporous\n($r_{eff}$ = 5 µm)", "Coarse\nmonoporous\n($r_{eff}$ = 21 µm)", "Biporous\n(ideal upper bound)"]
fig, ax = plt.subplots(figsize=(6.0, 3.3)); xx = np.arange(3)
hb = ax.bar(xx - .19, list(bh.values()), .36, color=PINE, label="horizontal")
vb = ax.bar(xx + .19, list(bv.values()), .36, color=SAGE, label="source on top, vertical sheet")
ax.bar_label(hb, fmt="%.0f", fontsize=9, padding=2); ax.bar_label(vb, fmt="%.0f", fontsize=9, padding=2)
ax.set_xticks(xx); ax.set_xticklabels(labs, fontsize=9); ax.set_ylabel("capillary limit (W)"); ax.grid(axis="x", visible=False)
ax.legend(fontsize=8.5, frameon=False, loc="upper left"); ax.set_ylim(0, 190)
fig.tight_layout(); save(fig, "g8_biporous_bars.png")

# G9 thickness sweep with the closed-form optimum
fig, ax = plt.subplots(figsize=(6.4, 3.6))
tws = out["sweep"]["tw_um"]
for n in WICKS:
    o = out["wick"][n]
    ax.plot(tws, out["sweep"][n], color=STY[n]["color"], ls=STY[n]["ls"], lw=2.2, label=SHORT[n])
    ax.plot(o["t_um"], o["Q_opt"], STY[n]["marker"], color=STY[n]["color"], mec=INK, ms=9, zorder=5)
    ax.annotate(f"{o['t_um']:.0f} µm, {o['Q_opt']:.0f} W", (o["t_um"], o["Q_opt"]), textcoords="offset points", xytext=(0, 9), ha="center", fontsize=9)
ax.set_xlabel(r"thickness of each wick layer $t$ (µm), with $h = 250 - 2t$"); ax.set_ylabel("capillary limit (W)")
ax.legend(fontsize=8.5, frameon=False); ax.set_ylim(0, 125); ax.set_xlim(10, 100)
fig.tight_layout(); save(fig, "g9_sweep.png")

# G10 vapour temperature drop against core thickness
h = np.logspace(math.log10(30e-6), math.log10(600e-6), 150)
fig, ax = plt.subplots(figsize=(6.4, 3.5))
for Q, c, ls in ((5, PINE, "-"), (20, FERN, "-"), (50, INK, "-")):
    d = np.array([dT_from_dP(a_v(x) * Q) for x in h]); ok = np.array([a_v(x) * Q <= 0.2 * P_sat for x in h])
    ax.loglog(h[ok] * 1e6, d[ok], color=c, lw=2.2, label=f"{Q} W")
    ax.loglog(h[~ok] * 1e6, d[~ok], color=c, lw=1.2, ls=":")
ax.set_xlabel(r"vapour core thickness $h$ (µm)"); ax.set_ylabel("saturation-temperature drop (K)")
ax.text(32, 0.0035, "dotted: $\\Delta P_v$ > 20% of $P_{sat}$,\nlinearised model not valid", fontsize=8.5)
ax.legend(title="heat load", fontsize=8.5, title_fontsize=8.5, frameon=False); ax.set_xlim(30, 600); plain_x(ax)
fig.tight_layout(); save(fig, "g10_vapour_dT.png")

# G11 capillary limit against core thickness: who sets the limit
fig, ax = plt.subplots(figsize=(6.4, 3.5))
for n, w in WICKS.items():
    ax.loglog(h * 1e6, [q_max(p_cap(w["r"]), w["K"], x) for x in h], color=STY[n]["color"], ls=STY[n]["ls"], lw=2.2, label=SHORT[n])
ax.axhline(5, color=INK, lw=0.9, ls=":"); ax.text(590, 5.5, "5 W illustrative load", fontsize=8.5, ha="right")
ax.set_xlabel(r"vapour core thickness $h$ (µm), with $t$ = 50 µm"); ax.set_ylabel("capillary limit (W)")
ax.legend(fontsize=8.5, frameon=False, loc="upper left"); ax.set_xlim(30, 600); ax.set_ylim(1, 400); plain_x(ax)
fig.tight_layout(); save(fig, "g11_limit.png")
# G12 vapour chamber against a solid copper sheet of the same thickness, 5 W
vs = out["vs_copper"]; xx = np.arange(len(vs)); w = 0.36
fig, ax = plt.subplots(figsize=(6.4, 3.7))
ax.bar(xx - w / 2, [v["cu"] for v in vs], w, color=SAGE, label="solid copper sheet, same total thickness")
bot = np.zeros(len(vs))
for key, col, lab in (("vapour", PINE, "vapour core"), ("interface", FERN, "evaporating interface ($\\sigma_a$ = 0.1)"), ("wick", INK, "wick conduction")):
    vals = np.array([v[key] for v in vs]); ax.bar(xx + w / 2, vals, w, bottom=bot, color=col, label="vapour chamber: " + lab); bot += vals
for i, v in enumerate(vs):
    ax.text(i - w / 2, v["cu"] + 0.3, f"{v['cu']:.1f}", ha="center", fontsize=9)
    ax.text(i + w / 2, v["vc"] + 0.3, f"{v['vc']:.1f}" + ("*" if v["h_um"] < 60 else ""), ha="center", fontsize=9)
ax.set_xticks(xx); ax.set_xticklabels([f"h = {v['h_um']:.0f} µm\nH = {v['H_mm']:.2f} mm\n" + (f"{v['factor']:.0f}× better" if v["h_um"] >= 100 else f"≈{v['factor']:.0f}× better*") for v in vs], fontsize=9)
ax.set_ylabel("temperature drop at 5 W (K)"); ax.set_ylim(0, 18); ax.grid(axis="x", visible=False)
ax.legend(fontsize=8, frameon=False, loc="upper left")
fig.tight_layout(); save(fig, "g12_vs_copper.png")
print("figures written")
