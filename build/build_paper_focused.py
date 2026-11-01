"""Builds Term_Paper_Micro_Heat_Pipes_and_Vapour_Chambers_Focused.pdf with reportlab: the paper cut down to three topics
(liquid return in the wick and biporous wicks, wick-thickness optimisation, vapour flow in a thin core).
Run after focused_model.py and figs_focused.py:  python -X utf8 build_paper_focused.py"""
import os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (CondPageBreak, BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table,
                                TableStyle, PageBreak, KeepTogether, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from refs import REFS
from focused_model import *

ROOT = os.path.join(HERE, ".."); FIG = os.path.join(ROOT, "figures")
EQD = os.path.join(HERE, "eq_focused"); os.makedirs(EQD, exist_ok=True)
OUT = os.path.join(ROOT, "Term_Paper_Micro_Heat_Pipes_and_Vapour_Chambers_Focused.pdf")

# ------------------------------------------------------------------ fonts and styles
fd = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
for nm, fn in (("Serif", "DejaVuSerif.ttf"), ("Serif-B", "DejaVuSerif-Bold.ttf"),
               ("Serif-I", "DejaVuSerif-Italic.ttf"), ("Serif-BI", "DejaVuSerif-BoldItalic.ttf"),
               ("Sans", "DejaVuSans.ttf"), ("Sans-B", "DejaVuSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(nm, os.path.join(fd, fn)))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")

HEAD = colors.HexColor(PINE); GREY = colors.HexColor(INK); LIGHT = colors.HexColor(TINT); LINE = colors.HexColor(SAGE)
S = dict(
    body=ParagraphStyle("body", fontName="Serif", fontSize=9.8, leading=14.2, alignment=TA_JUSTIFY, spaceAfter=6),
    h1=ParagraphStyle("h1", fontName="Sans-B", fontSize=14, leading=18, textColor=HEAD, spaceBefore=14, spaceAfter=6, keepWithNext=1),
    h2=ParagraphStyle("h2", fontName="Sans-B", fontSize=11, leading=14, textColor=HEAD, spaceBefore=9, spaceAfter=4, keepWithNext=1),
    cap=ParagraphStyle("cap", fontName="Serif-I", fontSize=8.6, leading=11.5, alignment=TA_JUSTIFY, textColor=GREY, spaceBefore=3, spaceAfter=10),
    bul=ParagraphStyle("bul", fontName="Serif", fontSize=9.8, leading=14, alignment=TA_JUSTIFY, leftIndent=14, bulletIndent=3, spaceAfter=2.5),
    cell=ParagraphStyle("cell", fontName="Serif", fontSize=8.2, leading=10.5, alignment=TA_LEFT),
    cellb=ParagraphStyle("cellb", fontName="Serif-B", fontSize=8.2, leading=10.5, alignment=TA_LEFT),
    box=ParagraphStyle("box", fontName="Serif", fontSize=9.2, leading=13, alignment=TA_JUSTIFY),
    ref=ParagraphStyle("ref", fontName="Serif", fontSize=8.4, leading=11.2, leftIndent=18, firstLineIndent=-18, spaceAfter=3.5, alignment=TA_LEFT),
    title=ParagraphStyle("title", fontName="Sans-B", fontSize=23, leading=29, textColor=HEAD, alignment=TA_CENTER),
    sub=ParagraphStyle("sub", fontName="Serif-I", fontSize=12, leading=17, textColor=GREY, alignment=TA_CENTER),
    meta=ParagraphStyle("meta", fontName="Serif", fontSize=11, leading=17, alignment=TA_CENTER),
    abs=ParagraphStyle("abs", fontName="Serif", fontSize=9.0, leading=12.6, alignment=TA_JUSTIFY),
)
story = []
def P(t, st="body"): story.append(Paragraph(t, S[st]))
def H1(t): story.append(CondPageBreak(4.5 * cm)); story.append(Paragraph(t, S["h1"])); story.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceAfter=5))
def H2(t): story.append(CondPageBreak(3.5 * cm)); story.append(Paragraph(t, S["h2"]))
def BUL(items):
    for t in items: story.append(Paragraph(t, S["bul"], bulletText="•"))
    story.append(Spacer(1, 4))
def BOX(title, text, fill=LIGHT):
    t = Table([[Paragraph(f"<b>{title}</b>", S["box"])], [Paragraph(text, S["box"])]], colWidths=[15.4 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fill), ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story.append(KeepTogether([t, Spacer(1, 8)]))
_fig_no = [0]
def FIG_(name, caption, width=13.0):
    _fig_no[0] += 1
    path = os.path.join(FIG, name)
    w, h = PILImage.open(path).size
    img = Image(path, width=width * cm, height=width * cm * h / w)
    story.append(KeepTogether([img, Paragraph(f"<b>Figure {_fig_no[0]}.</b> {caption}", S["cap"])]))
_tab_no = [0]
def TABLE(caption, rows, widths):
    _tab_no[0] += 1
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("BACKGROUND", (0, 0), (-1, 0), LIGHT)]))
    story.append(KeepTogether([Paragraph(f"<b>Table {_tab_no[0]}.</b> {caption}", S["cap"]), t, Spacer(1, 10)]))
_eq_no = [0]
def EQ(tex, fs=12.5):
    _eq_no[0] += 1
    path = os.path.join(EQD, f"eq{_eq_no[0]}.png")
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${tex}$", fontsize=fs, math_fontfamily="cm", color=INK)
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.04, transparent=True)
    plt.close(fig)
    w, h = PILImage.open(path).size
    img = Image(path, width=w * 72 / 300, height=h * 72 / 300)
    t = Table([[img, Paragraph(f"({_eq_no[0]})", S["body"])]], colWidths=[14.0 * cm, 1.4 * cm])
    t.setStyle(TableStyle([("ALIGN", (0, 0), (0, 0), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (1, 0), (1, 0), "RIGHT")]))
    story.append(KeepTogether([Spacer(1, 2), t, Spacer(1, 2)]))

# ------------------------------------------------------------------ references: only what this version cites, numbered by first use
_ORIG = dict(course=1, bhat=2, garimella=3, faghri12=5, weibel13=8, zhou=10, peterson=25, faghri95=26, semenic=18, patankar=15,
             hanlon=13, weibel10=14, yan=16, zhang=17)
_order = ["course"]
def c(*keys):
    for k in keys:
        if k not in _order: _order.append(k)
    return "[" + ", ".join(str(_order.index(k) + 1) for k in keys) + "]"

# convenient numbers
vc = {int(r["h_um"]): r for r in N["vapour_core"]}; cl = N["cap_limit"]; wk = N["wicks"]; bp = N["biporous"]
kx = {(int(r["h_um"]), r["Q"]): r for r in N["keff"]}; opt = out["wick"]; ex = out["split_examples"]
bh, bv = list(bp["horizontal"].values()), list(bp["vertical"].values())
o50, oM, o10 = opt[S50], opt[MESH], opt[S10]

# ================================================================== COVER
story += [Spacer(1, 0.6 * cm), Paragraph("MICROSCALE TRANSPORT PROCESSES · TERM PAPER", ParagraphStyle("x", parent=S["sub"], fontName="Sans-B", fontSize=9.5, textColor=GREY)),
          Spacer(1, 0.5 * cm),
          Paragraph("Micro Heat Pipes and Vapour Chambers for Smartphone and Chip Cooling", S["title"]),
          Spacer(1, 0.5 * cm),
          Paragraph("Liquid return in the wick, wick-thickness optimisation and vapour flow in a thin core", S["sub"]),
          Spacer(1, 0.6 * cm), HRFlowable(width="40%", thickness=1, color=HEAD, spaceAfter=14),
          Paragraph("<b>Debanshu Ghosh</b>", S["meta"]), Paragraph("Roll No. 23CH3FP56", S["meta"]),
          Paragraph("Department of Chemical Engineering", S["meta"]), Paragraph("Indian Institute of Technology Kharagpur", S["meta"]),
          Spacer(1, 0.5 * cm), Paragraph("Course: Microscale Transport Processes (S. DasGupta &amp; S. Ganguly)", S["meta"]),
          Paragraph("November 2026", S["meta"]), Spacer(1, 0.6 * cm)]
abs_text = ("<b>Abstract.</b> A vapour chamber spreads heat passively: water evaporates at a hot spot, flows as vapour through a sub-millimetre core, condenses, and returns through a porous wick by capillary suction. "
            "This paper examines the three transport questions that decide how far such a chamber can be thinned. "
            "First, liquid return: capillary pressure and wick permeability both depend on the same particle size, so going from a 50 µm to a 10 µm powder gives "
            f"{wk[S10]['p_cap_kPa']/wk[S50]['p_cap_kPa']:.0f} times the pump pressure but {wk[S10]['a_l_Pa_per_W']/wk[S50]['a_l_Pa_per_W']:.0f} times the liquid resistance, and biporous wicks try to escape this by giving each job its own length scale. "
            "Second, thickness optimisation: wick and vapour core share a fixed thickness, so there is a best split, for which this paper derives the closed-form condition h²/t = 12√(K ν<sub>v</sub>/ν<sub>l</sub>). "
            "Third, vapour flow: radial Poiseuille flow gives a pressure drop proportional to 1/h³, so halving the core makes it eight times more resistive, and Clausius–Clapeyron turns that pressure drop into a temperature non-uniformity of about 1.1 K per kPa. "
            f"All calculations use simple, openly stated models with water at 60 °C and an illustrative 5 W phone-like geometry. A published simulation found that a biporous condenser-side wick, by allowing a thicker core, reduced the peak-to-mean condenser surface temperature difference by 37% {c('patankar')}.")
_abs_ref = abs_text
t = Table([[Paragraph(abs_text, S["abs"])]], colWidths=[15.4 * cm])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                       ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [t, PageBreak()]

# ================================================================== 1 OVERVIEW
H1("1. Overview: one pressure budget, three questions")
P("A smartphone processor makes its heat in a few square millimetres, but the heat has to leave through the whole back of a sealed, fanless body, and the user's skin temperature caps performance. "
  f"In experiments on a Nexus 6P, the thermal governor reduced performance by up to 34% in popular applications {c('bhat')}. The task is therefore to <i>spread</i> heat sideways in a body with under a millimetre of free thickness. "
  f"Pumped microchannels need plumbing that a sealed phone cannot hold {c('garimella')}. A vapour chamber instead moves heat as the latent heat of a fluid, with no moving parts {c('faghri12', 'weibel13', 'zhou')}.")
P(f"Figure 1 shows the cycle as a half section through the centre of a disc-shaped chamber, the geometry used in the calculations: the dashed left edge is the centre line, the chip sits under the centre (radius R<sub>1</sub>) and the rim is at R<sub>2</sub>. Heat from the chip evaporates water from the wick. Vapour flows outward through the core and condenses over the cooler surface, where the heat leaves. The condensate returns through the top wick, passes down wick columns to the bottom wick, and is pulled back to the evaporator by capillary suction. "
  f"At 2.36 MJ/kg of latent heat, a load of 5 W needs a water flow of only {N['mdot_5W_kg_s']*1e6:.1f} mg/s.")
FIG_("g1_cycle.png", "Half section through a disc-shaped vapour chamber, with the three topics of this paper marked: (1) liquid return in the wick, (2) the split of a fixed thickness between wick (t) and core (h), (3) vapour flow in the thin core. The vapour arrow narrows because vapour condenses along the way.", 15.4)
P("Around this closed loop only the meniscus raises pressure; everything else loses it. The capillary pressure must therefore at least balance the liquid loss in the wick, the vapour loss in the core and the hydrostatic head:")
EQ(r"\Delta P_{cap}\;\geq\;\Delta P_{l}+\Delta P_{v}+\Delta P_{g}")
P("Both flow losses are laminar, so each is proportional to the mass flow ṁ = Q/h<sub>fg</sub> and hence to the heat load: ΔP<sub>l</sub> = a<sub>l</sub>Q and ΔP<sub>v</sub> = a<sub>v</sub>Q, with a<sub>l</sub> and a<sub>v</sub> flow resistances in Pa/W. Setting equality gives the largest load that capillary action can sustain, the <i>capillary limit</i>:")
EQ(r"Q_{max}=\dfrac{\Delta P_{cap}-\rho_l\,g\,\Delta z}{a_l+a_v}")
P("The three topics of this paper are the three parts of this equation. Section 2 asks how the wick sets ΔP<sub>cap</sub> and a<sub>l</sub>, and how a biporous wick can improve on the trade-off between them. "
  "Section 3 asks how a fixed thickness should be shared between a<sub>l</sub> and a<sub>v</sub>. Section 4 asks what a<sub>v</sub> does as the core thins, and what it costs in temperature.")
P(f"<b>Scope.</b> This version deals only with these three topics. Interface kinetics, the other operating limits, fabrication and reliability are outside its scope and are mentioned only where they change how a result here should be read. The scaling, continuum and slip arguments of the course {c('course')} are used as background and are not re-derived.")
BOX("How the numbers in this paper were obtained",
    "All values come from one reproducible script, using steam-table properties of saturated water at 60 °C and a deliberately simple geometry (Table 1). The 5 W load and the dimensions are <b>illustrative</b>, chosen to be phone-like; they are not measured data from any device. "
    "Published experiments are cited where quoted, and the model is not presented as a validation of them.")
TABLE("Parameters used for the calculations (saturated water at 60 °C).",
      [["Quantity", "Value", "Note"],
       ["Surface tension σ", "0.0662 N/m", "steam-table value"],
       ["Latent heat h<sub>fg</sub>", "2.358 MJ/kg", ""],
       ["Liquid density, viscosity", "983.2 kg/m³, 4.66×10⁻⁴ Pa s", "ν<sub>l</sub> = 4.74×10⁻⁷ m²/s"],
       ["Vapour density, viscosity", "0.1304 kg/m³, 1.08×10⁻⁵ Pa s", f"ν<sub>v</sub> = 8.28×10⁻⁵ m²/s; ν<sub>v</sub>/ν<sub>l</sub> = {nu_ratio:.0f}"],
       ["Saturation pressure P<sub>sat</sub>", "19.95 kPa", "T = 333.15 K"],
       ["Heat source", "5 W on 10 × 10 mm (R<sub>1</sub> = 5.64 mm)", "illustrative, phone-like"],
       ["Chamber (equal-area disc)", "R<sub>2</sub> = 48 mm", "same area as a 60 × 120 mm sheet"],
       ["Wick layers", "2 layers, t = 50 µm each, unless varied", "one on each wall"]],
      [4.6, 6.0, 4.8])

# ================================================================== 2 WICK
H1("2. Liquid return in the wick")
H2("2.1 The pump: capillary pressure")
P("A curved liquid surface carries a pressure jump. For a spherical interface of radius R the jump is 2σ/R (Young–Laplace). In a pore of effective radius r<sub>eff</sub> the meniscus meets the wall at contact angle θ (Figure 2), so geometry gives R = r<sub>eff</sub>/cos θ and")
EQ(r"\Delta P_{cap}=\dfrac{2\,\sigma\cos\theta}{r_{eff}}")
P(f"The pressure grows as pores shrink, which is why capillary pumping becomes useful at the microscale: with full wetting, a 64 µm mesh pore gives {wk[MESH]['p_cap_kPa']:.1f} kPa and a 10 µm pore about 13 kPa. "
  "Because ΔP<sub>cap</sub> ∝ cos θ, a drift from θ = 0° to 60° through oxidation or contamination halves the pump pressure with no change in geometry.")
FIG_("g2_wick.png", "Left: the meniscus in one pore, which is the pump. Right: a coarse wick is a weak pump with easy flow, and a fine wick a strong pump with hard flow.", 10.5)
H2("2.2 The loss: radial Darcy flow")
P("Liquid moves through the wick under Darcy's law, dP/dr = μ<sub>l</sub>u/K, where K is the permeability. Mass conservation across a cylinder of radius r, through a total wick thickness t<sub>l</sub> = 2t (one layer per wall), gives ṁ = ρ<sub>l</sub>u(2πr t<sub>l</sub>). Eliminating u and integrating from the rim R<sub>2</sub> to the source R<sub>1</sub>, with ∫dr/r = ln(R<sub>2</sub>/R<sub>1</sub>), gives")
EQ(r"\Delta P_{l}=\dfrac{\mu_l\,\dot m\,\ln(R_2/R_1)}{2\pi\,\rho_l\,K\,t_l}")
P("For a bed of sintered spheres of diameter d and porosity ε, the Kozeny–Carman relation treats the pores as tubes with a hydraulic diameter proportional to εd/(1−ε), which gives")
EQ(r"K=\dfrac{d^{2}\varepsilon^{3}}{150\,(1-\varepsilon)^{2}}\qquad r_{eff}\approx 0.21\,d")
P(f"The second relation is a common rule of thumb; mesh and groove wicks have their own correlations {c('peterson', 'faghri95')}.")
H2("2.3 The trade-off")
P("Both the pump and the resistance depend on the same length d: ΔP<sub>cap</sub> ∝ 1/d, but K ∝ d². Figure 3 shows this as a line in the K–r<sub>eff</sub> plane, and Table 2 puts numbers on it for the three wicks used in this paper.")
FIG_("g7_tradeoff.png", "Permeability against effective pore radius for sintered spheres (line), with the three wicks of Table 2 marked.", 11.6)
TABLE("The three example wicks, for two layers of t = 50 µm each.",
      [["Wick", "r<sub>eff</sub> (µm)", "K (m²)", "ΔP<sub>cap</sub> (kPa)", "a<sub>l</sub> (Pa/W)"],
       ["Cu mesh #200", f"{wk[MESH]['r_um']:.0f}", f"{wk[MESH]['K']:.1e}", f"{wk[MESH]['p_cap_kPa']:.1f}", f"{wk[MESH]['a_l_Pa_per_W']:.0f}"],
       ["Sintered powder, d = 50 µm", f"{wk[S50]['r_um']:.1f}", f"{wk[S50]['K']:.1e}", f"{wk[S50]['p_cap_kPa']:.1f}", f"{wk[S50]['a_l_Pa_per_W']:.0f}"],
       ["Sintered powder, d = 10 µm", f"{wk[S10]['r_um']:.1f}", f"{wk[S10]['K']:.1e}", f"{wk[S10]['p_cap_kPa']:.1f}", f"{wk[S10]['a_l_Pa_per_W']:.0f}"]],
      [5.4, 2.2, 2.6, 2.6, 2.6])
P(f"Going from d = 50 µm to d = 10 µm raises the pump pressure {wk[S10]['p_cap_kPa']/wk[S50]['p_cap_kPa']:.0f}-fold but the liquid resistance {wk[S10]['a_l_Pa_per_W']/wk[S50]['a_l_Pa_per_W']:.0f}-fold. With a 100 µm core, the 50 µm powder reaches {cl[S50]['100um']['horizontal_W']:.0f} W, while the finer powder is held by its own wick to {cl[S10]['100um']['horizontal_W']:.0f} W. "
  f"For the liquid alone, Q ∝ ΔP<sub>cap</sub>·K ∝ d, so a finer wick always delivers less. Excess pump pressure is wasted: the best uniform wick is the coarsest one that leaves enough margin over gravity (a {N['head_100mm_kPa']:.2f} kPa head for a 100 mm rise) and other losses.")
H2("2.4 Escaping the trade-off: biporous wicks")
P(f"A biporous wick gives each job its own length scale: fine pores inside clusters of particles set the capillary pressure, while coarse channels between the clusters carry the liquid (Figure 4). Semenic and Catton studied such wicks experimentally for high heat flux evaporators {c('semenic')}. In the terms of Eq. (2), the idealised capillary limit is")
EQ(r"Q_{max}=\dfrac{2\sigma/r_{fine}}{a_l(K_{coarse})+a_v}")
FIG_("g4_biporous.png", "A biporous wick (schematic): clusters of fine particles provide small pores and a strong pump, and the coarse channels between clusters provide an easy path for the liquid.", 10.5)
P(f"For a 100 µm core, taking r<sub>fine</sub> = 5 µm from a 23 µm powder and K<sub>coarse</sub> from a 100 µm powder, the limit rises from about {bh[0]:.0f} W (fine) or {bh[1]:.0f} W (coarse) to about {bh[2]:.0f} W (Figure 5). "
  "This is an <b>upper bound</b>, not a prediction. It assumes the two regions do not interfere, whereas coarse channels take up volume and break the conduction path. It also borrows K from 100 µm particles, which would not fit inside the 50 µm layer used here, so the bar stands for the principle and not for a buildable wick.")
FIG_("g8_biporous_bars.png", "Model capillary limit at a vapour-core thickness of 100 µm for fine, coarse and idealised biporous wicks. The biporous bars are upper bounds.", 11.4)
P(f"The biporous idea also matters for the vapour core. Patankar et al. used a 3-D numerical model to show that a biporous <i>condenser-side</i> wick allows a thicker vapour core, reducing the peak-to-mean condenser surface temperature difference by 37% relative to a monolithic wick {c('patankar')}. "
  f"Composite wicks are also the route taken in recent ultra-thin experiments, such as a 0.5 mm chamber with critical powers up to 60 W {c('yan')}; those devices differ from the model here, so this is context and not a validation.")
P(f"<b>Assumptions and where they break.</b> The wick is treated as rigid, uniform and isotropic, fully saturated, with one contact angle, and with inertia and vapour–liquid shear ignored. Real wicks have a distribution of pore sizes, in-plane and through-plane permeabilities that differ, and partial dry-out {c('hanlon', 'weibel10')}. "
  "Darcy's law and Kozeny–Carman are also continuum descriptions that need a layer many particles thick: a 50 µm layer of 50 µm powder is about one particle deep, so that case is an order-of-magnitude estimate only.")

# ================================================================== 3 THICKNESS
H1("3. Wick-thickness optimisation")
H2("3.1 The problem")
P(f"In a phone-thin sheet the inner thickness H is fixed, so every micrometre of wick is taken from the vapour core: H = 2t + h. A thicker wick lowers the liquid resistance, and a thinner core raises the vapour resistance. Figure 6 shows the effect at H = {H_in*1e6:.0f} µm for the 50 µm powder: "
  f"{ex[0]['Q']:.0f} W with a thin wick, {ex[1]['Q']:.0f} W at the best split and {ex[2]['Q']:.0f} W with a thin core.")
FIG_("g5_split.png", "Three ways of sharing a fixed 250 µm inner thickness, drawn to scale, for the 50 µm powder.", 11.0)
H2("3.2 Derivation of the optimum")
P("Since ΔP<sub>cap</sub> does not depend on t, maximising Q<sub>max</sub> in the horizontal case means minimising the total flow resistance. From Eq. (4) with t<sub>l</sub> = 2t, and from Eq. (11) in Section 4, the two resistances are")
EQ(r"a_l+a_v=\dfrac{A}{t}+\dfrac{B}{h^{3}},\quad A=\dfrac{\mu_l\ln(R_2/R_1)}{4\pi\rho_l K h_{fg}},\quad B=\dfrac{6\mu_v\ln(R_2/R_1)}{\pi\rho_v h_{fg}}")
P("With h = H − 2t, so that dh/dt = −2, setting the derivative to zero gives")
EQ(r"\dfrac{d}{dt}\left(\dfrac{A}{t}+\dfrac{B}{h^{3}}\right)=-\dfrac{A}{t^{2}}+\dfrac{6B}{h^{4}}=0\quad\Rightarrow\quad\dfrac{h^{4}}{t^{2}}=\dfrac{6B}{A}=144\,K\,\dfrac{\nu_v}{\nu_l}")
P("where ν = μ/ρ is the kinematic viscosity. The second derivative is positive, so this is a minimum of the resistance. Taking the square root gives the result:")
EQ(r"\dfrac{h^{2}}{t}=12\sqrt{K\,\dfrac{\nu_v}{\nu_l}}")
P(f"Writing G for the right-hand side and substituting h = H − 2t gives a quadratic in t, (H − 2t)² = Gt, which has one physically possible root. For water at 60 °C, ν<sub>v</sub>/ν<sub>l</sub> = {nu_ratio:.0f}, so for the 50 µm powder (K = 8.33×10⁻¹² m²) G = {o50['G_um']:.0f} µm, and H = 250 µm gives t = {o50['t_um']:.1f} µm and h = {o50['h_um']:.0f} µm. "
  "Table 3 shows that this agrees with a direct numerical sweep of Eq. (2) (Figure 7) for all three wicks. The derivation is this paper's own, a direct consequence of the model; it has not been compared with a published optimum.")
TABLE("Optimum split of a fixed 250 µm inner thickness: closed form (Eqs. 7–9) against the numerical sweep on a 2 µm grid.",
      [["Wick", "G (µm)", "t, closed form (µm)", "t, sweep (µm)", "h (µm)", "Q<sub>max</sub> (W)", "a<sub>l</sub>/a<sub>v</sub> = 6t/h"]] +
      [[SHORT[n], f"{opt[n]['G_um']:.0f}", f"{opt[n]['t_um']:.1f}", f"{opt[n]['tw_sweep_um']:.0f}", f"{opt[n]['h_um']:.0f}", f"{opt[n]['Q_opt']:.0f}", f"{opt[n]['al_over_av']:.1f}"] for n in (MESH, S50, S10)],
      [4.2, 1.5, 2.4, 1.9, 1.5, 1.7, 2.2])
FIG_("g9_sweep.png", "Capillary limit for a fixed 250 µm inner thickness shared between two wick layers and the core. Markers show the closed-form optimum of Eq. (9).", 11.8)
H2("3.3 What the result says")
BUL(["<b>What sets the optimum.</b> Only the permeability and the fluid. Q, σ, θ and R<sub>2</sub>/R<sub>1</sub> have all cancelled, so a contact-angle drift lowers the limit but does not move the best split.",
     f"<b>Permeability moves it.</b> Lower K pushes the optimum towards a thicker wick: from {oM['t_um']:.0f} µm for the mesh to {o10['t_um']:.0f} µm for the 10 µm powder. A wick therefore cannot be chosen without also choosing the split.",
     f"<b>The losses are not shared equally.</b> Combining the condition with the resistances gives a<sub>l</sub>/a<sub>v</sub> = 6t/h at the optimum, which is {o50['al_over_av']:.1f} for the 50 µm powder. Equalising the two losses would not be optimal.",
     f"<b>The coarsest wick does not win.</b> The 50 µm powder ({o50['Q_opt']:.0f} W) beats both the coarser mesh ({oM['Q_opt']:.0f} W) and the finer powder ({o10['Q_opt']:.0f} W), because the pump and the resistance trade off as in Section 2."])
P(f"<b>Limits of this result.</b> It maximises the capillary limit only, not the thermal performance at the working load. At these ceiling loads, the vapour drop is no longer small: {o50['dP_v_at_Qopt_kPa']:.1f} kPa for the 50 µm powder ({o50['dP_v_at_Qopt_kPa']*1e3/P_sat*100:.0f}% of P<sub>sat</sub>) and {o10['dP_v_at_Qopt_kPa']:.1f} kPa for the 10 µm powder ({o10['dP_v_at_Qopt_kPa']*1e3/P_sat*100:.0f}%), so constant vapour properties become rough and the watts should be read as trends. "
  f"A thicker wick also adds conduction resistance, and support pillars take up core area; Zhang et al. report that effective conductivity fell as support-column diameter increased {c('zhang')}.")

# ================================================================== 4 VAPOUR
H1("4. Vapour flow in a thin core")
H2("4.1 Radial Poiseuille flow and the inverse-cube law")
P("The vapour leaves the source region and spreads radially in a slit of height h (Figure 8). For laminar flow between parallel plates, the mean velocity is u = (h²/12μ<sub>v</sub>)(−dP/dr), so")
EQ(r"-\dfrac{dP}{dr}=\dfrac{12\,\mu_v\,u}{h^{2}},\qquad u=\dfrac{\dot m}{\rho_v\,2\pi r h}")
P("The second relation is mass conservation, since the flow area at radius r is 2πrh. Substituting and integrating from R<sub>1</sub> to R<sub>2</sub> gives")
EQ(r"\Delta P_{v}=\dfrac{6\,\mu_v\,\dot m\,\ln(R_2/R_1)}{\pi\,\rho_v\,h^{3}}")
FIG_("g6_vapour.png", "Left: radial vapour flow from the source to the rim. Right: the Poiseuille profile in the slit. The h³ comes from one power in the velocity and two in the wall shear, so halving h multiplies the gradient by 2 × 4 = 8.", 12.0)
P(f"The pressure drop scales as the inverse cube of the thickness: halving h makes the core exactly {N['ratio_halving']:.0f} times more resistive. One power of h comes from the velocity (a thinner slit must carry the same flow faster) and two from the wall shear (the same velocity is sheared over a shorter distance). "
  "<b>Assumptions:</b> steady, laminar, incompressible flow; smooth walls; and all vapour travelling to R<sub>2</sub>. In reality the vapour condenses along the way, so the true drop is lower by a factor of order one, while support pillars add drag.")
H2("4.2 From pressure drop to temperature drop")
P("A vapour pressure drop matters because pressure and temperature are tied together in saturated vapour. The Clausius–Clapeyron relation is dP/dT = h<sub>fg</sub>/(T v<sub>fg</sub>). With v<sub>fg</sub> ≈ 1/ρ<sub>v</sub>, a small pressure drop corresponds to a saturation-temperature drop")
EQ(r"\Delta T_{sat}\approx\dfrac{T\,\Delta P}{\rho_v\,h_{fg}}")
P(f"which for water vapour at 60 °C is {out['K_per_kPa']:.2f} K per kPa. The vapour pressure drop thus appears directly as non-uniformity in the chamber temperature, which is what the user feels as a hot spot on the skin. "
  f"The linear relation only holds while ΔP is a small fraction of P<sub>sat</sub> = 19.95 kPa. Taking 20% as the limit, this means a core no thinner than about {N['h_invalid_um']['5W']:.0f} µm at 5 W, so the dotted lines of Figure 9 are a warning and not a prediction.")
rows = [["Core thickness h (µm)", "ΔP<sub>v</sub> at 5 W (Pa)", "ΔT<sub>sat</sub> at 5 W (K)", "ΔT<sub>sat</sub> at 20 W (K)", "Mach no. at 5 W", "Knudsen no. λ/h"]]
for h_ in (400, 200, 100, 50):
    r_ = vc[h_]
    rows.append([f"{h_}", f"{r_['dP_5W_Pa']:.0f}", f"{r_['dT_5W_K']:.2g}" + (" (invalid)" if h_ < 60 else ""), f"{r_['dT_20W_K']:.2g}" if h_ >= 100 else f"{r_['dT_20W_K']:.0f} (invalid)", f"{r_['Ma_5W']:.3f}", f"{r_['Kn']:.3f}"])
TABLE("Vapour-core results from Eqs. (11) and (12). Entries marked invalid have a pressure drop above 20% of P<sub>sat</sub>.", rows, [3.2, 2.4, 2.8, 2.9, 2.2, 2.0])
FIG_("g10_vapour_dT.png", "Saturation-temperature drop across the vapour core against its thickness for three heat loads. Dotted: beyond the range of the linearised model.", 11.6)
H2("4.3 When the core becomes the bottleneck")
P(f"At 5 W, the drop across the vapour is {vc[200]['dT_5W_K']:.2f} K at h = 200 µm and {vc[100]['dT_5W_K']:.2f} K at 100 µm. At 50 µm the model gives about {vc[50]['dT_5W_K']:.0f} K, already beyond its range, so only the trend should be read from it. "
  f"The advantage over solid copper shrinks accordingly (Figure 10). In the model, the whole-chamber drop at 5 W (vapour, wick and interface, the last with an assumed accommodation coefficient of 0.1) is {kx[(200,5)]['dT_tot']:.2f} K against {kx[(200,5)]['dT_copper_plate']:.1f} K for a copper plate of the same total thickness at h = 200 µm, a factor of about {kx[(200,5)]['dT_copper_plate']/kx[(200,5)]['dT_tot']:.0f}. At h = 50 µm it is {kx[(50,5)]['dT_tot']:.1f} K against {kx[(50,5)]['dT_copper_plate']:.1f} K, a factor of about {kx[(50,5)]['dT_copper_plate']/kx[(50,5)]['dT_tot']:.0f}.")
FIG_("g12_vs_copper.png", "Temperature drop at 5 W for the vapour chamber (stacked: vapour, interface, wick) against a solid copper sheet of the same total thickness H, same source and rim, for four core thicknesses. * The 50 µm vapour value is beyond the range of the linearised model.", 11.8)
P(f"The capillary limit shows the same change of control (Figure 11). For a thick core a<sub>v</sub> is negligible and the wick sets the limit, so each curve flattens. For a thin core a<sub>v</sub> takes over and the curves bend down towards Q<sub>max</sub> ∝ h³: the 50 µm powder gives {cl[S50]['100um']['horizontal_W']:.0f} W at 100 µm but only {cl[S50]['50um']['horizontal_W']:.0f} W at 50 µm. "
  f"This agrees with the finding of Patankar et al. that, at ultra-thin form factors, making room for a thicker vapour core is the lever that matters {c('patankar')}.")
FIG_("g11_limit.png", "Capillary limit against vapour-core thickness for the three wicks, with t = 50 µm. The wick sets the limit for thick cores, and the vapour for thin ones.", 11.6)
H2("4.4 Are the flow assumptions valid?")
P(f"<b>Compressibility.</b> The vapour speed at the edge of the source at 5 W is {vc[100]['u_5W_m_s']:.1f} m/s for h = 100 µm, a Mach number of {vc[100]['Ma_5W']:.3f} (still only {vc[50]['Ma_5W']:.2f} at 50 µm), so the flow is effectively incompressible. "
  f"<b>Rarefaction.</b> The mean free path of water vapour at 60 °C and 19.95 kPa is about {N['lambda_um']:.2f} µm, so the Knudsen number λ/h is {vc[100]['Kn']:.3f} at 100 µm, and continuum no-slip flow is a good model in the core. Inside a 1 µm wick pore, however, Kn reaches {N['Kn_pore_1um']:.2f}, so these flow models should not be carried over to nanostructured wicks. "
  f"<b>Laminarity.</b> The Reynolds number based on the slit is Re = 2ṁ/(2πR<sub>1</sub>μ<sub>v</sub>) ≈ {2*N['mdot_5W_kg_s']/(2*math.pi*R1*mu_v):.0f} at 5 W and is independent of h, well within the laminar range.")

# ================================================================== 5 CONCLUSIONS
H1("5. Conclusions")
BUL([f"<b>Liquid return.</b> The pump pressure goes as 1/d and the permeability as d²: a 10 µm powder gives {wk[S10]['p_cap_kPa']/wk[S50]['p_cap_kPa']:.0f}× the pressure but {wk[S10]['a_l_Pa_per_W']/wk[S50]['a_l_Pa_per_W']:.0f}× the liquid resistance of a 50 µm powder. A uniform wick should be the coarsest that leaves enough margin. Biporous wicks aim to escape this by giving each job its own length scale; the idealised estimate here is an upper bound.",
     f"<b>Thickness optimisation.</b> With a fixed thickness, the best split satisfies h²/t = 12√(K ν<sub>v</sub>/ν<sub>l</sub>), which depends only on the permeability and the fluid and agrees with a numerical sweep. For a 250 µm space and a 50 µm powder it gives t ≈ {o50['t_um']:.0f} µm and h ≈ {o50['h_um']:.0f} µm, with the liquid taking about {o50['al_over_av']:.0f} times the vapour's share of the loss.",
     f"<b>Vapour flow.</b> The pressure drop grows as 1/h³, so halving the core makes it {N['ratio_halving']:.0f} times more resistive, at a cost of about 1.1 K per kPa. At 5 W, the drop goes from {vc[200]['dT_5W_K']:.1f} K at 200 µm to {vc[100]['dT_5W_K']:.1f} K at 100 µm, and below about {N['h_invalid_um']['5W']:.0f} µm the simple model no longer applies."])
P("All of this comes from simple models with one fluid, one geometry and steady state. The numbers are illustrative and are meant to explain trends; they are not design values and have not been validated against a device. Within those limits, the three topics give one consistent picture: as a chamber thins, the design problem moves from the wick to the vapour core, and the wick and the core must be designed together.")

# ================================================================== REFERENCES
H1("References")
for i, k in enumerate(_order, 1):
    txt, url = REFS[_ORIG[k] - 1]
    story.append(Paragraph(f"[{i}] {txt}" + (f" {url}" if url else ""), S["ref"]))
P(f"<i>Note on the references.</i> Entries with a DOI were checked against the Crossref database. Items {c('peterson')} and {c('faghri95')} are standard textbooks, cited for classical correlations; {c('course')} is the course material, used as background for scaling, continuum and slip arguments.", "cap")

# ================================================================== BUILD
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5); canvas.setFillColor(GREY)
    canvas.drawString(2.5 * cm, 1.4 * cm, "Debanshu Ghosh · 23CH3FP56 · Microscale Transport Processes term paper")
    canvas.drawRightString(A4[0] - 2.5 * cm, 1.4 * cm, f"{doc.page}")
    canvas.restoreState()
def nofooter(canvas, doc): pass

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm, topMargin=2.2 * cm, bottomMargin=2.2 * cm,
                      title="Micro Heat Pipes and Vapour Chambers for Smartphone and Chip Cooling: liquid return, wick thickness and vapour flow", author="Debanshu Ghosh",
                      subject="Microscale Transport Processes term paper")
fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="cover", frames=[fr], onPage=nofooter, autoNextPageTemplate="main"),
                      PageTemplate(id="main", frames=[fr], onPage=footer)])
doc.build(story)
print("written", OUT, os.path.getsize(OUT) // 1024, "KB;", _fig_no[0], "figures,", _tab_no[0], "tables,", _eq_no[0], "equations,", len(_order), "references")
print("order:", _order)
