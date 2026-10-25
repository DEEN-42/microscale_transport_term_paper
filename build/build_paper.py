"""Builds Term_Paper_Micro_Heat_Pipes_and_Vapour_Chambers.pdf with reportlab.
Run after calc.py:  python -X utf8 build_paper.py
Every number is read from numbers.json (written by calc.py)."""
import json, os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (CondPageBreak, BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table,
                                TableStyle, PageBreak, KeepTogether, NextPageTemplate, HRFlowable)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from refs import REFS

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
FIG = os.path.join(ROOT, "figures")
EQD = os.path.join(HERE, "eq"); os.makedirs(EQD, exist_ok=True)
OUT = os.path.join(ROOT, "Term_Paper_Micro_Heat_Pipes_and_Vapour_Chambers.pdf")
N = json.load(open(os.path.join(HERE, "numbers.json")))

# ------------------------------------------------------------------ fonts
fd = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
for nm, fn in (("Serif", "DejaVuSerif.ttf"), ("Serif-B", "DejaVuSerif-Bold.ttf"),
               ("Serif-I", "DejaVuSerif-Italic.ttf"), ("Serif-BI", "DejaVuSerif-BoldItalic.ttf"),
               ("Sans", "DejaVuSans.ttf"), ("Sans-B", "DejaVuSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(nm, os.path.join(fd, fn)))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")

NAVY = colors.HexColor("#1F3A5F"); GREY = colors.HexColor("#555555"); LIGHT = colors.HexColor("#EEF3F8")
AMBER = colors.HexColor("#FFF6E0"); LINE = colors.HexColor("#B8C4D2")

S = dict(
    body=ParagraphStyle("body", fontName="Serif", fontSize=9.8, leading=14.2, alignment=TA_JUSTIFY, spaceAfter=6),
    h1=ParagraphStyle("h1", fontName="Sans-B", fontSize=14, leading=18, textColor=NAVY, spaceBefore=14, spaceAfter=6, keepWithNext=1),
    h2=ParagraphStyle("h2", fontName="Sans-B", fontSize=11, leading=14, textColor=NAVY, spaceBefore=9, spaceAfter=4, keepWithNext=1),
    cap=ParagraphStyle("cap", fontName="Serif-I", fontSize=8.6, leading=11.5, alignment=TA_JUSTIFY, textColor=GREY, spaceBefore=3, spaceAfter=10),
    bul=ParagraphStyle("bul", fontName="Serif", fontSize=9.8, leading=14, alignment=TA_JUSTIFY, leftIndent=14, bulletIndent=3, spaceAfter=2.5),
    cell=ParagraphStyle("cell", fontName="Serif", fontSize=8.2, leading=10.5, alignment=TA_LEFT),
    cellb=ParagraphStyle("cellb", fontName="Serif-B", fontSize=8.2, leading=10.5, alignment=TA_LEFT),
    box=ParagraphStyle("box", fontName="Serif", fontSize=9.2, leading=13, alignment=TA_JUSTIFY),
    ref=ParagraphStyle("ref", fontName="Serif", fontSize=8.4, leading=11.2, leftIndent=18, firstLineIndent=-18, spaceAfter=3.5, alignment=TA_LEFT),
    title=ParagraphStyle("title", fontName="Sans-B", fontSize=23, leading=29, textColor=NAVY, alignment=TA_CENTER),
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
def BOX(title, text, fill=AMBER):
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
    return _fig_no[0]
_tab_no = [0]
def TABLE(caption, rows, widths, head=True, align_num=False):
    _tab_no[0] += 1
    data = [[Paragraph(str(c), S["cellb"] if (head and i == 0) else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
          ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if head: st.append(("BACKGROUND", (0, 0), (-1, 0), LIGHT))
    t.setStyle(TableStyle(st))
    story.append(KeepTogether([Paragraph(f"<b>Table {_tab_no[0]}.</b> {caption}", S["cap"]), t, Spacer(1, 10)]))
    return _tab_no[0]

_eq_no = [0]; _eq_cache = {}
def EQ(tex, fs=12.5):
    _eq_no[0] += 1
    key = re.sub(r"\W", "", tex)[:40] + str(_eq_no[0])
    path = os.path.join(EQD, key + ".png")
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${tex}$", fontsize=fs, family="DejaVu Serif")
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.04, transparent=True)
    plt.close(fig)
    w, h = PILImage.open(path).size
    k = 72 / 300
    img = Image(path, width=w * k, height=h * k)
    t = Table([[img, Paragraph(f"({_eq_no[0]})", S["body"])]], colWidths=[14.4 * cm, 1.0 * cm])
    t.setStyle(TableStyle([("ALIGN", (0, 0), (0, 0), "CENTER"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ALIGN", (1, 0), (1, 0), "RIGHT")]))
    story.append(KeepTogether([Spacer(1, 2), t, Spacer(1, 2)]))
    return _eq_no[0]

def f(x, n=2):
    return f"{x:.{n}f}"
def g(x, n=3):
    return f"{x:.{n}g}"

# convenient numbers
vc = {int(r["h_um"]): r for r in N["vapour_core"]}
cl = N["cap_limit"]; wk = N["wicks"]
kx = {(int(r["h_um"]), r["Q"]): r for r in N["keff"]}
hi = N["h_interface"]; di = N["dT_interface_5W"]
bp = N["biporous"]; cp = N["coupling"]
mesh, s50, s10 = "Cu mesh (#200)", "Sintered, d = 50 um", "Sintered, d = 10 um"

# ================================================================== COVER
story += [Spacer(1, 0.6 * cm), Paragraph("MICROSCALE TRANSPORT PROCESSES · TERM PAPER", ParagraphStyle("x", parent=S["sub"], fontName="Sans-B", fontSize=9.5, textColor=GREY)),
          Spacer(1, 0.5 * cm),
          Paragraph("Micro Heat Pipes and Vapour Chambers for Smartphone and Chip Cooling", S["title"]),
          Spacer(1, 0.5 * cm),
          Paragraph("A critical review of capillary-driven, two-phase heat transport in sub-millimetre structures: the science, the simplifications and where they fail", S["sub"]),
          Spacer(1, 0.6 * cm), HRFlowable(width="40%", thickness=1, color=NAVY, spaceAfter=14),
          Paragraph("<b>Debanshu Ghosh</b>", S["meta"]), Paragraph("Roll No. 23CH3FP56", S["meta"]),
          Paragraph("Department of Chemical Engineering", S["meta"]), Paragraph("Indian Institute of Technology Kharagpur", S["meta"]),
          Spacer(1, 0.5 * cm), Paragraph("Course: Microscale Transport Processes (S. DasGupta &amp; S. Ganguly)", S["meta"]),
          Paragraph("October 2026", S["meta"]), Spacer(1, 0.6 * cm)]
abs_text = ("<b>Abstract.</b> A modern smartphone processor can produce heat faster than a sealed, fanless body under a centimetre thick can spread it, "
            "and because the user's skin temperature, not the silicon limit, caps performance, thermal throttling can cut the performance of popular applications by up to about a third [2]. "
            "Micro heat pipes and vapour chambers address this passively: a working fluid evaporates at the hot spot, carries heat as latent heat through a sub-millimetre vapour core, "
            "condenses at a cooler region and returns through grooves or porous wicks by capillary pumping, which works in any orientation because surface tension dominates gravity at these scales. "
            "This paper is a critical review of that mechanism built on a single idea, the capillary pressure budget. Using simple, openly stated models (Young–Laplace, Darcy and Poiseuille flow, kinetic-theory evaporation) "
            "it shows that the wick imposes a trade-off between capillary pressure and permeability, that an optimal wick thickness exists when wick and vapour core share a fixed sheet thickness, "
            "and that the vapour-core pressure drop grows as the inverse cube of its thickness, so halving the core makes it eight times more resistive. "
            "It then audits the assumptions of the models used in the literature, shows why reported effective thermal conductivities cannot be compared without their definitions, and discusses how fabrication sets the transport properties and how corrosion and gas generation limit lifetime. "
            "A biporous condenser-side wick, which allows a thicker vapour core, reduced the peak-to-mean skin temperature difference by 37% in a published simulation study [15].")
t = Table([[Paragraph(abs_text, S["abs"])]], colWidths=[15.4 * cm])
t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), LIGHT), ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                       ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
story += [t, PageBreak()]

# ================================================================== 1 INTRODUCTION
H1("1. Introduction and scope")
P("A flagship smartphone puts CPU cores, a GPU, an image processor and a modem on one system-on-a-chip, and the power it draws has grown with every generation. "
  "Unlike a laptop, the phone has no fan and no vents, and the user holds it. The limit that matters is therefore the <i>skin temperature</i> of the case, not the junction temperature of the silicon. "
  "In experiments on a Nexus 6P phone, Bhat et al. found that the system's thermal governor reduced performance by up to 34% in popular Android applications; in one game it cost about 12 frames per second, "
  "while the package temperature reached about 50 °C when throttling was disabled [2]. The heat is produced in a few square millimetres but has to leave through the whole back of the phone, so the real task is <i>spreading</i> heat laterally, quickly, in a body under a millimetre or so of free thickness.")
P("Pumped liquid cooling through etched microchannels is very effective [4] but needs a pump and plumbing that a sealed phone cannot accommodate [3]. A sheet of copper spreads heat by conduction only, and a very thin sheet cannot move much heat sideways (Section 7). "
  "Heat pipes and vapour chambers (VCs) take a different route: they move heat as the <i>latent heat</i> of a fluid that evaporates at the hot spot and condenses elsewhere, with no moving parts. "
  "A <i>micro heat pipe</i> is a channel so small that the capillary pressure of the fluid meniscus is the only pump needed; a <i>vapour chamber</i> is the flat, two-dimensional version of the same idea [5, 7, 8].")
P("<b>What this paper does.</b> It is organised around one idea: the capillary pump has to out-pull every pressure loss in the loop. "
  "Section 2 sets up this pressure budget; Sections 3–5 take its three parts in turn (liquid in the wick, vapour in the thin core, and the phase-change interface); Section 6 turns the budget into operating limits; "
  "Section 7 audits the models used to describe all this; Sections 8–9 connect fabrication and reliability to the physics; Section 10 separates what is established from what is still argued over. "
  "Each section follows the same pattern: the idea in plain words, the one key equation, a worked number, the assumptions made and where they break.")
P("<b>What it deliberately leaves out.</b> Market size, cost and product comparisons are not discussed. The scaling arguments of Lecture 1 of the course (square–cube law, the idea of continuum and slip, dominance of surface effects) "
  "[1] are used as background and are not re-derived; the top-down and bottom-up fabrication routes of Lectures 2 and 3 and the microstructured-heat-exchanger issues of Lecture 4 (wall conduction, pressure loss, fouling) [1] are referred to only where they set a transport property. "
  "Quantities such as the Bond and Knudsen numbers appear only as short checks that decide which physics is needed.")
BOX("How the numbers in this paper were obtained",
    "All calculated values come from one reproducible script (<i>build/calc.py</i>) that uses steam-table properties of saturated water at 60 °C and a deliberately simple geometry: a disc-shaped chamber with the same area as a 60 × 120 mm sheet, "
    "a 10 × 10 mm heat source in the centre and condensation at the rim. The 5 W heat load and the dimensions are <b>illustrative</b>, chosen to be phone-like; they are not measured data from any device. "
    "Where published experiments are quoted, they are cited, and the model is never presented as a validation of them.")

# ================================================================== 2 CYCLE AND PRESSURE BUDGET
H1("2. The cycle and its pressure budget")
H2("2.1 The four steps")
P("Figure 1 shows a vapour chamber in section. Two thin copper walls enclose a sealed, evacuated space holding a small amount of water. Each wall is lined with a porous <i>wick</i>, and between the wicks is the <i>vapour core</i>. "
  "(1) Heat from the chip conducts through the wall and evaporates water from the wick at the hot spot. (2) The vapour, at slightly higher pressure there, flows outward through the core. "
  "(3) Where the wall is cooler, the vapour condenses and releases its latent heat. (4) The liquid returns through the wick to the hot spot, driven by capillary suction. "
  "Because the heat is carried as latent heat (about 2.36 MJ per kg of water at 60 °C), a very small mass flow moves a large amount of heat: for 5 W the water flow is only " + f"{N['mdot_5W_kg_s']*1e6:.1f}" + " mg/s.")
FIG_("f1_cycle.png", "Cross-section of a vapour chamber. Numbers refer to the four steps in the text. The wick on each wall is the capillary pump; the vapour core is the highway for latent heat.", 13.5)
H2("2.2 Capillary pressure: the pump")
P("A curved liquid surface has a pressure jump across it. For a liquid with surface tension σ meeting a pore wall at contact angle θ, a meniscus in a pore of effective radius r<sub>eff</sub> supports the pressure difference")
EQ(r"\Delta P_{cap}=\dfrac{2\,\sigma\cos\theta}{r_{eff}}")
P("This is the Young–Laplace relation. It follows from the fact that the meniscus is a spherical cap of radius r<sub>eff</sub>/cos θ and that the pressure jump across a sphere is 2σ divided by its radius. "
  "The pressure grows as pores shrink, which is the whole reason capillary pumping becomes useful at the microscale: for water at 60 °C (σ = 0.0662 N/m) and complete wetting, a 64 µm pore (woven mesh) gives " + f"{wk[mesh]['p_cap_kPa']:.1f}" +
  " kPa, a 10 µm pore gives about 13 kPa and a 1 µm pore about 130 kPa. "
  "<b>Assumptions:</b> the meniscus is spherical, the contact angle is constant, the pore is a simple, uniform shape and the liquid is pure.")
P("<b>Why orientation does not matter (a short check).</b> The Bond number Bo = ρgh²/σ compares gravity with surface tension on the length scale h of the structure. "
  "For the vapour core it is " + f"{N['Bo']['1000um']:.2f}" + " at h = 1 mm and only " + f"{N['Bo']['200um']:.4f}" + " at 200 µm, so inside the sheet gravity cannot rearrange the liquid. "
  "Gravity still acts over the <i>length</i> of the sheet: if the heat source is at the top of a 100 mm-tall vertical sheet, the liquid must be lifted a hydrostatic head of ρgΔz = " + f"{N['head_100mm_kPa']:.2f}" +
  " kPa. Figure 2 shows that fine wicks cover this easily while coarse mesh wicks are left with only about a factor of two of margin, a point that returns in Sections 3 and 6.")
FIG_("f2_capillary_pressure.png", "Capillary pressure 2σ/r as a function of effective pore radius (full wetting) compared with the gravity head over 100 mm and with the wick-plus-vapour pressure loss at 5 W calculated in this paper. Dots are the three wick types used later.", 12.4)
H2("2.3 The pressure budget")
P("In steady operation the liquid pressure falls as the liquid moves through the wick to the evaporator, and the evaporator meniscus retreats into smaller effective curvature until the pump pressure just balances every loss. The pump can therefore at most provide ΔP<sub>cap</sub>, and the requirement is")
EQ(r"\Delta P_{cap}\;\geq\;\Delta P_{l}+\Delta P_{v}+\Delta P_{g}")
P("where ΔP<sub>l</sub> is the Darcy loss of the liquid in the wick, ΔP<sub>v</sub> the pressure drop of the vapour in its core and ΔP<sub>g</sub> the hydrostatic term. "
  "Phase-change losses (the interface) are treated separately in Section 5 because they appear as a temperature jump rather than a pressure drop. "
  "Both losses are proportional to the mass flow, hence to the heat load Q: ΔP<sub>l</sub> = a<sub>l</sub>Q and ΔP<sub>v</sub> = a<sub>v</sub>Q. Setting equality gives the maximum heat load that capillary action can sustain (the <i>capillary limit</i>):")
EQ(r"Q_{max}=\dfrac{\Delta P_{cap}-\rho_l\,g\,\Delta z}{a_l+a_v}")
P("This single equation is the backbone of the rest of the paper. To raise Q<sub>max</sub>, a design must raise the pump pressure (finer pores), lower the liquid resistance a<sub>l</sub> (bigger, more permeable pores, thicker wick) or lower the vapour resistance a<sub>v</sub> (a thicker vapour core). "
  "These demands conflict, and the next three sections are about how.")
TABLE("Parameters used for the illustrative calculations (saturated water at 60 °C, copper walls).",
      [["Quantity", "Value", "Note"],
       ["Surface tension σ", "0.0662 N/m", "steam-table value"],
       ["Latent heat h<sub>fg</sub>", "2.358 MJ/kg", ""],
       ["Liquid density, viscosity", "983.2 kg/m³, 4.66×10⁻⁴ Pa s", ""],
       ["Vapour density, viscosity", "0.1304 kg/m³, 1.08×10⁻⁵ Pa s", "P<sub>sat</sub> = 19.95 kPa"],
       ["Heat source", "5 W on 10 × 10 mm (R<sub>1</sub> = 5.64 mm)", "illustrative, phone-like"],
       ["Chamber (equal-area disc)", "R<sub>2</sub> = 48 mm", "equivalent to a 60 × 120 mm sheet"],
       ["Wick layers", "2 layers, each 50 µm", "one on each wall"],
       ["Copper walls", "2 × 80 µm", ""],
       ["Orientation", "horizontal, or source on top of a vertical sheet (Δz = 100 mm)", ""]],
      [4.6, 6.2, 4.6])

# ================================================================== 3 WICK
H1("3. Liquid return in the wick")
H2("3.1 Darcy flow and the permeability–pressure trade-off")
P("Liquid flows through the wick as through any porous medium, with a pressure gradient proportional to the velocity (Darcy's law). For radial flow from the rim (R<sub>2</sub>) to the heat source (R<sub>1</sub>) through wick layers of total thickness t<sub>l</sub>, with ṁ = Q/h<sub>fg</sub>:")
EQ(r"\Delta P_{l}=\dfrac{\mu_l\,\dot m\,\ln(R_2/R_1)}{2\pi\,\rho_l\,K\,t_l}")
P("<i>K</i> is the permeability of the wick (m²), which sets how easily liquid moves. For a bed of sintered spheres of diameter d and porosity ε the Kozeny–Carman relation gives")
EQ(r"K=\dfrac{d^{2}\varepsilon^{3}}{150\,(1-\varepsilon)^{2}}\qquad r_{eff}\approx 0.21\,d")
P("(the second relation is a common rule of thumb; mesh and groove wicks have their own correlations [25, 26]). The key observation is that <i>both</i> the pump pressure and the flow resistance depend on the same length d: "
  "pressure goes as 1/d, permeability as d². Finer pores pump harder (good) and resist flow much more (bad). Figure 3 shows this as a sloping line in a K–r<sub>eff</sub> plane. "
  "A useful measure of what a wick can deliver is the ratio K/r<sub>eff</sub>, because for the liquid alone the heat load is proportional to ΔP<sub>cap</sub>·K ∝ K/r<sub>eff</sub>.")
FIG_("f3_wick_tradeoff.png", "Permeability against effective pore radius for sintered-sphere wicks (line) and for a woven mesh (square). Grey lines are constant K/r<sub>eff</sub>: the higher the line, the more liquid the wick can deliver per unit of capillary pressure.", 12.4)
TABLE("The three wick examples used in this paper.",
      [["Wick", "r<sub>eff</sub> (µm)", "K (m²)", "ΔP<sub>cap</sub> (kPa)", "Liquid resistance a<sub>l</sub> (Pa/W)"],
       ["Cu mesh #200", f"{wk[mesh]['r_um']:.0f}", f"{wk[mesh]['K']:.1e}", f"{wk[mesh]['p_cap_kPa']:.1f}", f"{wk[mesh]['a_l_Pa_per_W']:.0f}"],
       ["Sintered powder, d = 50 µm", f"{wk[s50]['r_um']:.1f}", f"{wk[s50]['K']:.1e}", f"{wk[s50]['p_cap_kPa']:.1f}", f"{wk[s50]['a_l_Pa_per_W']:.0f}"],
       ["Sintered powder, d = 10 µm", f"{wk[s10]['r_um']:.1f}", f"{wk[s10]['K']:.1e}", f"{wk[s10]['p_cap_kPa']:.1f}", f"{wk[s10]['a_l_Pa_per_W']:.0f}"]],
      [4.6, 2.4, 2.8, 2.6, 3.0])
P("Table 2 contains the trade-off in numbers. Going from d = 50 µm to d = 10 µm raises the pump pressure five-fold but raises the liquid resistance twenty-five-fold. "
  "The finer wick therefore ends up <i>liquid-limited</i>: it can deliver about " + f"{cl[s10]['100um']['horizontal_W']:.0f}" + " W whatever the vapour core thickness, whereas the coarser powder reaches " +
  f"{cl[s50]['100um']['horizontal_W']:.0f}" + " W at a core thickness of 100 µm (Section 6). Excess pump pressure is simply wasted; the best wick is the coarsest one that still gives enough margin over gravity and other losses.")
H2("3.2 Escaping the trade-off: biporous wicks and thickness optimisation")
P("A <i>biporous</i> wick combines two length scales: fine pores (inside clusters of particles) for pumping pressure and coarse channels between the clusters for easy liquid and vapour passage. "
  "Experiments on such wicks for high heat flux evaporators were reported by Semenic and Catton [18]. In the idealised calculation of Figure 4 (pump pressure from 5 µm pores, permeability from a coarse 100 µm-particle wick) the capillary limit rises from about " +
  f"{list(bp['horizontal'].values())[0]:.0f}" + " W (fine) or " + f"{list(bp['horizontal'].values())[1]:.0f}" + " W (coarse) to about " + f"{list(bp['horizontal'].values())[2]:.0f}" +
  " W. This is an <b>upper bound</b>, not a prediction: it assumes the fine and coarse regions do not interfere, which they do in real structures (coarse channels take up volume and break the conduction path, and the effective permeability of the combined structure is lower than that of the coarse region alone). "
  "The idea, rather than the number, is the lesson: decouple the length scale that sets the pressure from the one that sets the flow.")
FIG_("f8_biporous.png", "Idealised biporous wick (left) and the model capillary limit it gives at a vapour-core thickness of 100 µm (right). The biporous bar is an upper bound.", 14.0)
P("The wick also competes for room. In a phone-thin sheet the total inner thickness is fixed, so every micrometre of wick is taken from the vapour core. "
  "Thicker wicks reduce the liquid resistance (more cross-section) but make the vapour core thinner and raise its resistance (Section 4). "
  "Figure 5 sweeps this trade-off at a fixed inner thickness of " + f"{N['coupling_H_in_um']:.0f}" + " µm. Each wick has an optimum: " +
  f"{cp[s50]['tw_opt_um']:.0f}" + " µm per layer (core " + f"{cp[s50]['h_opt_um']:.0f}" + " µm) for the 50 µm powder, " + f"{cp[mesh]['tw_opt_um']:.0f}" + " µm for the mesh and " + f"{cp[s10]['tw_opt_um']:.0f}" +
  " µm for the fine powder, giving " + f"{cp[s50]['Q_opt']:.0f}" + ", " + f"{cp[mesh]['Q_opt']:.0f}" + " and " + f"{cp[s10]['Q_opt']:.0f}" + " W respectively in this model. "
  "The position of the optimum depends on the wick and not just on the geometry, so a wick cannot be chosen without choosing the thickness split.")
FIG_("f9_coupling.png", "Capillary-limit heat load for a fixed 250 µm inner thickness shared between two wick layers and the vapour core. Dots mark the optimum for each wick.", 11.6)
P("<b>Assumptions and where they break.</b> The wick is treated as a rigid, uniform, isotropic porous medium; the contact angle is the same everywhere; inertia and vapour–liquid shear are ignored; and the liquid is assumed to fill the whole wick thickness. "
  "Real wicks have a distribution of pore sizes (the largest pores set the pump pressure, the smallest set the resistance), anisotropic permeability (in-plane flow differs from through-thickness flow), partial dry-out and a contact angle that changes with oxidation and contamination (Section 9). "
  "Because ΔP<sub>cap</sub> ∝ cos θ, a drift from θ = 0 to 60° halves the pump pressure with no change in geometry.")

# ================================================================== 4 VAPOUR CORE
H1("4. Vapour flow in a thin core")
H2("4.1 Radial Poiseuille flow and the inverse-cube law")
P("In a vapour chamber the vapour leaves the source region and spreads radially in a slit of height h. At radius r the mean velocity is u = ṁ/(ρ<sub>v</sub>·2πrh). "
  "For laminar flow between parallel plates the pressure gradient is dP/dr = −12μ<sub>v</sub>u/h² (plane Poiseuille flow). Substituting u and integrating from R<sub>1</sub> to R<sub>2</sub> gives")
EQ(r"\Delta P_{v}=\dfrac{6\,\mu_v\,\dot m\,\ln(R_2/R_1)}{\pi\,\rho_v\,h^{3}}")
P("The important feature is the h<super>3</super> in the denominator: the pressure drop scales as the inverse cube of the core thickness. Halving the thickness makes the core exactly " + f"{N['ratio_halving']:.0f}" +
  " times more resistive. It is the standard laminar-flow result that follows from the Navier–Stokes equation of Lecture 1, applied to a slit; the new point is what it implies for a vapour. "
  "<b>Assumptions:</b> steady, laminar, incompressible flow; all vapour travels all the way to R<sub>2</sub> (in reality it condenses along the way, so the true pressure drop is lower by a factor of order unity); smooth walls; no pillars or ribs in the core (real chambers have support pillars that add drag).")
H2("4.2 From pressure drop to temperature drop")
P("A vapour pressure drop matters because, in saturated vapour, pressure and temperature are tied together. By the Clausius–Clapeyron relation, a pressure drop ΔP corresponds to a saturation-temperature drop")
EQ(r"\Delta T_{sat}\approx\dfrac{T\,\Delta P}{\rho_v\,h_{fg}}")
P("which for water vapour at 60 °C is about 1.1 K per kPa. So the vapour pressure drop shows up directly as non-uniformity of the chamber temperature, which is exactly what the user feels as a hot spot on the skin. "
  "(The linearised relation is only valid while ΔP is a small fraction of P<sub>sat</sub> = 19.95 kPa; for a core thinner than about " + f"{N['h_invalid_um']['5W']:.0f}" + " µm at 5 W the model leaves its range of validity and the dotted lines in Figure 6 should be read as a warning, not a prediction.)")
rows = [["Core thickness h (µm)", "ΔP at 5 W (Pa)", "ΔT<sub>sat</sub> at 5 W (K)", "ΔT<sub>sat</sub> at 20 W (K)", "Mach no. at 5 W", "Knudsen no. λ/h"]]
for h_ in (400, 200, 100, 50):
    r_ = vc[h_]
    rows.append([f"{h_}", f"{r_['dP_5W_Pa']:.0f}", f"{r_['dT_5W_K']:.2g}" + (" (invalid)" if h_ < 60 else ""), f"{r_['dT_20W_K']:.2g}" if h_ >= 100 else f"{r_['dT_20W_K']:.0f} (invalid)", f"{r_['Ma_5W']:.3f}", f"{r_['Kn']:.3f}"])
TABLE("Vapour-core results from Eqs. (6) and (7) for the geometry of Table 1. Entries marked invalid have a pressure drop above 20% of P<sub>sat</sub>.", rows, [3.2, 2.4, 2.8, 2.9, 2.2, 2.0])
FIG_("f4_vapour_core.png", "Saturation-temperature drop across the vapour core against its thickness for three heat loads. Dotted: beyond the range of the linearised model.", 12.4)
P("Reading Table 3: at a core thickness of 200 µm a 5 W load costs about " + f"{vc[200]['dT_5W_K']:.2f}" + " K across the vapour; at 100 µm it is " + f"{vc[100]['dT_5W_K']:.2f}" +
  " K; at 50 µm the model gives about " + f"{vc[50]['dT_5W_K']:.0f}" + " K, already beyond its range of validity, so only the trend should be read from it. "
  "The consequence is that the advantage of the chamber over solid copper shrinks as the core thins. In the model the whole-chamber temperature drop at 5 W is " + f"{kx[(200,5)]['dT_tot']:.2f}" + " K against " + f"{kx[(200,5)]['dT_copper_plate']:.1f}" +
  " K for a copper plate of the same thickness at a core of 200 µm (a factor of about " + f"{kx[(200,5)]['dT_copper_plate']/kx[(200,5)]['dT_tot']:.0f}" + "), but " + f"{kx[(50,5)]['dT_tot']:.1f}" + " K against " + f"{kx[(50,5)]['dT_copper_plate']:.1f}" + " K at 50 µm (a factor of about " + f"{kx[(50,5)]['dT_copper_plate']/kx[(50,5)]['dT_tot']:.0f}" + "). "
  "The vapour core is a negligible part of the thermal resistance in a thick chamber and the dominant part in an ultra-thin one. This agrees with the finding of Patankar et al. that, at ultra-thin form factors, making room for a thicker vapour core is the lever that matters [15].")
H2("4.3 Compressibility, sonic limit and rarefaction: short checks")
P("The vapour speed at the edge of the source is " + f"{vc[100]['u_5W_m_s']:.1f}" + " m/s at 100 µm, i.e. a Mach number of " + f"{vc[100]['Ma_5W']:.3f}" +
  " (and still only " + f"{vc[50]['Ma_5W']:.2f}" + " at 50 µm), so at phone loads the flow is effectively incompressible. Compressibility and the <i>sonic limit</i> (Q<sub>s</sub> of order " +
  f"{vc[100]['Q_sonic_W']:.0f}" + " W at 100 µm for this geometry, from the standard textbook expression [25, 26]) matter only at much higher loads or in much thinner cores. "
  "The mean free path of water vapour at 60 °C and 19.95 kPa is about " + f"{N['lambda_um']:.2f}" + " µm, so the Knudsen number λ/h in the core is only " + f"{vc[100]['Kn']:.3f}" + " at 100 µm: continuum flow with no slip is a good model. "
  "Inside sub-micron wick pores, however, Kn reaches " + f"{N['Kn_pore_1um']:.2f}" + " for a 1 µm pore, i.e. the vapour near fine nanostructured wicks is no longer a continuum, a limitation of every model in Section 7 that is rarely stated.")

# ================================================================== 5 INTERFACE
H1("5. What happens at the evaporating and condensing surface")
P("So far heat has moved by <i>flow</i>. At the surface of the liquid it must cross a different barrier: molecules have to leave the liquid, and this takes a driving force. "
  "Kinetic theory (the Hertz–Knudsen–Schrage relation) gives the net evaporation flux in terms of how many molecules strike and leave the surface, scaled by an <i>accommodation coefficient</i> σ<sub>a</sub> between 0 and 1. "
  "Linearised around saturation it gives a heat-transfer coefficient for the interface,")
EQ(r"h_i=\dfrac{2\sigma_a}{2-\sigma_a}\;\dfrac{\rho_v\,h_{fg}^{2}}{T}\sqrt{\dfrac{1}{2\pi R_v T}}")
P("For σ<sub>a</sub> = 1 this is " + f"{hi['1.0']/1e6:.1f}" + " MW/m²K, i.e. the interface is practically free. The difficulty is that σ<sub>a</sub> is not known well. Marek and Straub's analysis of published values for water [21] shows how widely the measured coefficients scatter, "
  "and reported values range roughly from 0.01 to 1, with lower values in some older work. Table 4 shows what this does to the interface temperature jump for the 5 W on 1 cm² of the model (a flux of 50 kW/m²): "
  "from about " + f"{di['1.0']*1000:.0f}" + " mK (σ<sub>a</sub> = 1) to about " + f"{di['0.001']:.0f}" + " K (an extreme value of σ<sub>a</sub> = 0.001). Whether the interface matters in a phone-thin chamber therefore depends on a coefficient the community has not pinned down.")
TABLE("Interface temperature jump for 5 W on 1 cm² (50 kW/m²) from Eq. (8) for different accommodation coefficients. The heat flux is taken over the whole source area, which overstates the jump because the real interface area is larger.",
      [["σ<sub>a</sub>", "1", "0.1", "0.03", "0.01", "0.001"],
       ["h<sub>i</sub> (kW/m²K)"] + [(f"{hi[k]/1e3:,.0f}" if hi[k] > 1e5 else f"{hi[k]/1e3:.3g}") for k in ("1.0", "0.1", "0.03", "0.01", "0.001")],
       ["ΔT<sub>i</sub> (K)"] + [f"{di[k]:.3g}" for k in ("1.0", "0.1", "0.03", "0.01", "0.001")]],
      [3.2, 2.4, 2.4, 2.4, 2.4, 2.4])
FIG_("f5_interface.png", "Interface temperature jump against heat flux for five accommodation coefficients. The spread between the curves, two to four orders of magnitude, is the uncertainty in the physics, not a numerical error.", 12.0)
BOX("Going deeper (optional): the thin-film region",
    "In a wick pore the liquid meets the solid wall in a thin wedge. Where the film is only a micrometre or so thick, heat crosses it by conduction at a rate of about k<sub>l</sub>/δ: for δ = 1 µm this is "
    f"{0.653/1e-6/1e3:.0f} kW/m²K, for 10 µm it is {0.653/10e-6/1e3:.0f} kW/m²K, for 100 µm only {0.653/100e-6/1e3:.1f} kW/m²K (k<sub>l</sub> = 0.653 W/m K). "
    "Thin regions near the contact line are therefore where most evaporation happens, as analysed in classical work on the evaporating wetting film [20] and in models of evaporation on grooved structures [19]. "
    "In very thin films, molecular forces between the liquid and the solid (<i>disjoining pressure</i>) change the local equilibrium and set the film's thickness. "
    "The practical consequences are: a thick layer of liquid over the heater is a thermal resistance, and the wick should keep the heater wetted by a <i>thin</i> film; and pore-scale structure, not just wick thickness, controls the evaporator resistance.", LIGHT)
P("Two further mechanisms matter at the interface. First, the conduction path through the wick: for a sintered copper wick the Maxwell mixing estimate for k<sub>eff</sub> at ε = 0.5 is about " +
  f"{N['k_wick_maxwell_eps0.5']:.0f}" + " W/m K, giving only about 0.02 K across a 50 µm wick at 5 W/cm². That is an <i>upper</i> estimate, because real sintered necks and woven-mesh contacts conduct less, and a thick wick over the heater is the evaporator resistance that Hanlon and Ma and Weibel et al. studied for sintered media [13, 14]. "
  "Second, non-condensable gas (air, or hydrogen from slow corrosion) is swept by the vapour to the condenser end and blocks part of the condensing area, and its effect is amplified in a small volume [25, 26].")

# ================================================================== 6 LIMITS
H1("6. Operating limits and start-up")
P("Every limit is a statement of the form <i>this quantity runs out first</i>. The five classical limits of heat pipes [25, 26] are: the <b>capillary limit</b> (the pump pressure is used up, Eq. 2); the <b>sonic limit</b> (the vapour reaches the speed of sound at the evaporator exit); "
  "the <b>entrainment limit</b> (vapour shear tears droplets from the liquid and starves the wick); the <b>boiling limit</b> (vapour bubbles form inside the wick and block liquid access); and the <b>viscous limit</b> (the vapour pressure at start-up is too low to drive flow). "
  "Figure 8 shows the first two, computed from the model, for the three wicks.")
FIG_("f6_limits.png", "Capillary-limit heat load against vapour-core thickness for three wicks (solid: horizontal; dashed: source on top of a vertical sheet) and the sonic limit. The line at 5 W is the illustrative phone load.", 13.0)
P("What the model says: (i) <b>For thick cores the wick sets the limit</b>: the coarse 50 µm powder saturates near 150 W, the mesh near 80 W and the fine 10 µm powder near 30 W, independent of core thickness. "
  "(ii) <b>For thin cores the vapour sets the limit</b>: at 100 µm the powder gives " + f"{cl[s50]['100um']['horizontal_W']:.0f}" + " W and at 50 µm only " + f"{cl[s50]['50um']['horizontal_W']:.0f}" + " W, just above a 5 W load. "
  "(iii) <b>Gravity matters mainly to the coarse wick</b>: the mesh falls from " + f"{cl[mesh]['100um']['horizontal_W']:.0f}" + " W to " + f"{cl[mesh]['100um']['vertical_W']:.1f}" + " W at 100 µm when the source is on top, while the fine powder barely changes. "
  "(iv) The sonic limit lies well above the capillary limit in this range, so it is not the first constraint for a phone.")
P("<b>What the model cannot say.</b> It treats the wick as if the liquid reaches the source uniformly, so it cannot see local dry-out under the hottest spot, entrainment or boiling, which are local, transient and depend on pore-scale details. "
  "Experiments therefore report different limits. Yan et al. measured critical powers up to 60 W for a 0.5 mm chamber with a composite wick [16], and Weibel et al. found that 600–1200 µm sintered wicks handled local fluxes above 500 W/cm² without dry-out [14], but those wicks are many times thicker than phone wicks and the chambers differ. "
  "The closeness of the model's 56 W (50 µm powder, 100 µm core) to the 60 W experimental value is a coincidence of order of magnitude and should not be read as agreement.")
P("<b>Start-up and freezing.</b> A cold chamber begins with the working fluid distributed in the wick and low vapour pressure (viscous limit); start-up can show a temperature overshoot at the evaporator before circulation sets in. "
  "Water also expands by about 9% on freezing, which can deform a sub-millimetre chamber and strand liquid, so freeze–thaw cycling is a real reliability issue for devices used outdoors (Section 9).")

# ================================================================== 7 MODELLING
H1("7. Modelling approaches and their assumptions")
P("The literature uses four broad classes of models. Table 5 lists what each assumes, what it hides and how it fails. The main practical message is that the cheaper models are not worse, only more limited: "
  "which one to trust depends on whether the question is a design sizing, a hot-spot map or a pore-scale mechanism.")
TABLE("Modelling approaches for heat pipes and vapour chambers: assumptions, what each hides and where each breaks down.",
      [["Model", "Main assumptions", "What it hides", "Where it fails"],
       ["Thermal-resistance network (e.g. the conduction-based scheme of Prasher [24])", "Steady; each stage (wall, wick, vapour, condenser) treated as a lumped resistance; vapour core typically nearly isothermal", "Pressure losses, local dry-out, spreading in the vapour", "Thin cores where the vapour drop is not small; high loads near limits"],
       ["Analytical 1-D/2-D flow models (as in Sections 2–6 of this paper)", "Laminar, incompressible, uniform wick, constant properties, all vapour to the rim", "Pillars, non-uniform condensation, pore-size distribution, transients", "Local hot-spot flux; fine nanostructured wicks (Kn not small); transient start-up"],
       ["3-D continuum porous-medium models (e.g. Vadakkan et al. [22])", "Wick as porous continuum with effective K and k<sub>eff</sub>; vapour core solved with flow equations; interface via mass-flux balance", "Interface physics reduced to one assumed coefficient; real pore structure averaged out", "Accuracy depends on K, k<sub>eff</sub> and σ<sub>a</sub>, which are rarely known independently"],
       ["Wick-microstructure models (e.g. Ranjan et al. [23])", "Wick microstructure (particle size, packing) enters the model explicitly, not only through K", "Computational cost; idealised particle packings", "Large devices; uncertain contact angle, contamination"]],
      [3.8, 4.4, 3.5, 3.7])
H2("7.1 Why 'effective thermal conductivity' needs a definition")
P("Vapour chambers are often rated by an <i>effective thermal conductivity</i> k<sub>eff</sub>, defined by comparing the chamber's temperature drop with that of a solid conductor carrying the same heat. For the radial geometry of this paper")
EQ(r"k_{eff}=\dfrac{Q\,\ln(R_2/R_1)}{2\pi\,H\,\Delta T}")
P("with H the total thickness and ΔT the total temperature drop (vapour, wick and interface). The trouble is that there is more than one way to define the geometry. "
  "Taking the same data and treating the chamber as a strip of width equal to the source width gives a number " + f"{kx[(200,5)]['keff_strip']/kx[(200,5)]['keff_radial']:.0f}" + " times larger: at h = 200 µm, "
  f"{kx[(200,5)]['keff_radial']/1e3:.0f}" + "×10³ W/m K (radial) against " + f"{kx[(200,5)]['keff_strip']/1e3:.0f}" + "×10³ W/m K (strip), from the same temperature drop (Figure 9). "
  "Also, k<sub>eff</sub> is not a material property: it falls as the core thins (" + f"{kx[(100,5)]['keff_radial']/1e3:.1f}" + "×10³ W/m K at 100 µm and " + f"{kx[(50,5)]['keff_radial']:.0f}" + " W/m K at 50 µm in this model) and in experiments it depends on load and orientation.")
FIG_("f7_keff.png", "Apparent effective thermal conductivity from the model for two definitions of the geometry, as a function of vapour-core thickness at 5 W. The factor-of-eleven gap between the lines comes only from the definition. Dotted: beyond model validity.", 12.0)
P("This matters when papers are compared. Zhang et al. report 3473–3837 W/m K for a 0.39 mm chamber with a composite mesh wick [17] while Yan et al. report 11,817 W/m K at 50 W against gravity for a 0.5 mm chamber with a different composite wick [16]. "
  "These devices differ in size, thickness, load and orientation, and the definition of k<sub>eff</sub> and the reference length in each paper has to be checked before concluding that one is better; "
  "the values are not interchangeable. The same experiment [17] also reports that k<sub>eff</sub> <i>fell</i> as the diameter of the support columns increased, a direct reminder that pillars that stiffen the thin shell also block the vapour and conduct heat the wrong way.")
story.append(CondPageBreak(10 * cm))
H2("7.2 Audit of the assumptions in this paper's own model")
TABLE("Assumption audit of the model of Sections 2–6.",
      [["Assumption", "Why it was made", "Effect on results", "When it fails"],
       ["Fluid properties at a single temperature (60 °C)", "Simplicity", "Small, a few percent", "Large spreading (ΔT of tens of K); P<sub>sat</sub> changes strongly with T"],
       ["Disc geometry, central source, all vapour to rim", "Closed-form solutions", "Overestimates ΔP<sub>v</sub> by an order-one factor", "Multiple sources, corners, distributed condensation"],
       ["Uniform wick, K from Kozeny–Carman, r<sub>eff</sub> = 0.21 d", "Standard correlations", "K and r<sub>eff</sub> uncertain by a factor of 2 or more", "Real pore-size distributions, anisotropy, partial saturation"],
       ["θ = 0 (full wetting)", "Best case", "Overestimates ΔP<sub>cap</sub> (halved at 60°)", "Oxidised or contaminated surfaces (Section 9)"],
       ["Laminar, incompressible vapour; Kn small", "Checked in Section 4.3", "Negligible at phone loads", "Very high loads; core thinner than a few µm"],
       ["Linear Clausius–Clapeyron", "Converts ΔP to ΔT in closed form", "Valid while ΔP < 20% P<sub>sat</sub>", "Cores thinner than about 60 µm (5 W)"],
       ["Steady state only", "Limits are defined at steady state", "Misses dry-out and start-up behaviour", "Fast power transients typical of mobile workloads"],
       ["No non-condensable gas, no pillars", "Clean idealisation", "Optimistic", "Real chambers contain both"]],
      [4.2, 3.2, 3.9, 4.1])

# ================================================================== 8 FABRICATION
H1("8. How fabrication sets the transport physics")
P("The processes themselves are the subject of Lectures 2 and 3 and the reviews of ultra-thin heat pipes and vapour chambers [10–12]; they are not repeated here. What matters for transport is which property each route fixes, summarised in Table 7.")
TABLE("Fabrication routes translated into transport properties (generic mechanisms; process details in [10–12]).",
      [["Structure", "What it fixes", "Consequence for transport", "Typical weakness"],
       ["Sintered copper powder", "Particle size d (so r<sub>eff</sub> and K), porosity, neck size", "Strong pump (small d) or high K (large d); neck conduction for evaporation", "Thick layer wastes core height; sintering can leave closed pores"],
       ["Woven copper mesh (layers)", "Wire diameter and mesh count", "Coarse r<sub>eff</sub>, moderate K, thin and flexible", "Lower pump pressure; weak anti-gravity capability (Section 6)"],
       ["Etched grooves or pillars (top-down, as in Lectures 2–3)", "Channel width and depth, regular geometry", "Well-defined, directional K; analysable (compare [6, 19])", "In-plane anisotropy; sensitive to burrs and contamination"],
       ["Nanostructured / oxidised copper surfaces (bottom-up)", "Sub-micron roughness, contact angle", "Higher pump pressure, thin-film evaporation, better wetting", "Ageing of wetting; Kn not small in pores"],
       ["Bonding and sealing (diffusion bonding, brazing, welding)", "Hermeticity, residual gas", "Leak-free life; sets non-condensable gas level", "A weak seal is a slow loss of the working fluid"],
       ["Support pillars in the core", "Mechanical stiffness of the thin shell", "Prevents collapse under vacuum or pressure", "Obstructs vapour and adds conduction paths [17]"]],
      [3.6, 3.7, 4.3, 3.8])

# ================================================================== 9 RELIABILITY
H1("9. Reliability science")
BUL(["<b>Compatibility.</b> Copper and water is the standard compatible pair for such chambers [25, 26]; copper and water are chemically compatible over long times and do not generate gas to a significant extent when clean. Aluminium in contact with water, in contrast, generates hydrogen, a non-condensable gas, and is not used for water chambers.",
     "<b>Non-condensable gas.</b> Even small amounts of gas accumulate at the condenser, where the vapour sweeps them, and shut off part of the area; the chamber then runs hotter at the same load. Gas comes from the manufacturing process, from permeation through the seal and from slow corrosion.",
     "<b>Wetting ageing.</b> Oxidation, contamination and surface changes alter the contact angle. Because ΔP<sub>cap</sub> ∝ cos θ, a change from 0° to 60° halves the pump pressure. This lowers the capillary limit of Section 6 with no change in geometry; surface treatments can be used to restore wetting, but whether they last is a question this review could not settle from the sources used.",
     "<b>Fouling and deposition.</b> Dissolved or leached species concentrate at the evaporator and can block the finest pores, the same fouling mechanism that Lecture 4 raises for microstructured heat exchangers [1]; here it affects the pump pressure and not just the heat transfer.",
     "<b>Mechanical and thermal cycling.</b> The saturation pressure of water at 60 °C is about 20 kPa, well below atmospheric, so a sealed chamber sits under a net external load and relies on pillars and wick for stiffness. Freezing (a volume increase of about 9%) and repeated thermal cycles can deform thin walls and lift the wick."])

# ================================================================== 10 SYNTHESIS
H1("10. Critical synthesis")
H2("10.1 What is well established")
BUL(["The cycle is limited by a pressure budget in which capillary pressure rises as 1/r<sub>eff</sub> and flow resistance rises faster, so every wick is a compromise [5, 25, 26].",
     "In ultra-thin chambers the vapour core, whose resistance goes as 1/h³, eventually dominates, and the geometry of the vapour space is as important as the wick [15].",
     "Biporous and patterned wicks, which separate the length scale that sets pressure from the one that sets flow, improve performance in both experiments and simulation [15, 18]."])
H2("10.2 What is still argued over")
BUL(["<b>The interface.</b> The accommodation coefficient of water is uncertain by orders of magnitude [21], yet it sets the interface resistance of Eq. (8); how much it matters in practice is unclear.",
     "<b>Comparability of reported performance.</b> k<sub>eff</sub> and 'maximum power' depend on definitions, load, orientation and dry-out criteria; many papers define them differently (Section 7.1).",
     "<b>Predictive power of simple models.</b> The Darcy–Poiseuille picture predicts trends well but not the absolute limit; it ignores local dry-out and boiling, which are what experiments often see first.",
     "<b>Long-term behaviour.</b> In the sources used here, steady-state thermal performance is documented far more than lifetime data on wetting ageing, gas generation and fouling at these scales."])
H2("10.3 Limits of this review")
P("The calculations are for one fluid, one geometry and steady state; the numbers are illustrative and not design values. The simplified models are used to <i>explain trends</i>, and wherever a published experiment is quoted the devices differ from the model. "
  "Some quantities (wick correlations, the rule r<sub>eff</sub> ≈ 0.21 d, interface properties) come from textbooks and review papers and are used at face value.")

# ================================================================== 11 CONCLUSIONS
H1("11. Conclusions")
BUL(["A vapour chamber is a capillary pump that must beat the sum of wick, vapour and gravity losses; the capillary limit Q<sub>max</sub> = (ΔP<sub>cap</sub> − ρgΔz)/(a<sub>l</sub> + a<sub>v</sub>) organises the whole design problem.",
     "In the wick the pump pressure goes as 1/d and permeability as d²: finer pores give " + f"{wk[s10]['p_cap_kPa']/wk[s50]['p_cap_kPa']:.0f}" + "× the pressure but " + f"{wk[s10]['a_l_Pa_per_W']/wk[s50]['a_l_Pa_per_W']:.0f}" + "× the liquid resistance in this comparison (d = 10 µm against 50 µm), so the best wick is the coarsest one that leaves enough margin; biporous structures try to escape this trade-off.",
     "Sharing a fixed thickness between wick and vapour core creates an optimum wick thickness that depends on the wick (50 µm per layer for the 50 µm powder in this model).",
     "The vapour-core pressure drop grows as 1/h³, so halving the core makes it " + f"{N['ratio_halving']:.0f}" + " times more resistive; at about 100 µm and below it controls the temperature uniformity and the 5 W model gives a drop of " + f"{vc[100]['dT_5W_K']:.1f}" + " K at 100 µm and several kelvin at 50 µm.",
     "The interface adds a temperature jump that depends on a poorly known coefficient, and the effective conductivity used to rate chambers has no unique definition.",
     "Fabrication fixes pore size, porosity, contact angle and hermeticity; reliability is governed by wetting ageing, gas generation, fouling and thermal cycling, which are less documented than steady-state thermal performance."])
P("Taken together, the field has a good first-order picture of <i>why</i> thin vapour chambers work, and weaker quantitative tools for predicting <i>exactly</i> how well and for how long. The open problems are the interface, the standardisation of performance metrics and long-term wetting.")

# ================================================================== REFERENCES
H1("References")
for i, (txt, url) in enumerate(REFS, 1):
    story.append(Paragraph(f"[{i}] {txt}" + (f" {url}" if url else ""), S["ref"]))
P("<i>Note on the references.</i> Items [2]–[24] with a DOI were checked against the Crossref database for title, authors, year, volume and pages. "
  "Items [25] and [26] are standard textbooks, cited for classical correlations and the standard operating limits; [1] is the course material. "
  "The quoted figures were verified against the original sources: the 34% loss and the 12 frames per second [2], the 37% reduction [15], the 60 W, 11,817 W/m K and 0.5 mm [16], and the 3473–3837 W/m K, 0.39 mm and the effect of column diameter [17].", "cap")

# ================================================================== BUILD
def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Sans", 7.5); canvas.setFillColor(GREY)
    canvas.drawString(2.5 * cm, 1.4 * cm, "Debanshu Ghosh · 23CH3FP56 · Microscale Transport Processes term paper")
    canvas.drawRightString(A4[0] - 2.5 * cm, 1.4 * cm, f"{doc.page}")
    canvas.restoreState()
def nofooter(canvas, doc): pass

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm, topMargin=2.2 * cm, bottomMargin=2.2 * cm,
                      title="Micro Heat Pipes and Vapour Chambers for Smartphone and Chip Cooling", author="Debanshu Ghosh",
                      subject="Microscale Transport Processes term paper")
fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="cover", frames=[fr], onPage=nofooter, autoNextPageTemplate="main"),
                      PageTemplate(id="main", frames=[fr], onPage=footer)])
doc.build(story)
print("written", OUT, os.path.getsize(OUT) // 1024, "KB")
