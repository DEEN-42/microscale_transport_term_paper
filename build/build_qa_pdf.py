"""Builds two PDFs: Viva_Prep_QA_Sources_and_Contribution.pdf (Q&A, sources, contribution) and Calculations_How_the_Numbers_Are_Calculated.pdf.
Part A: likely questions for the 2-minute Q&A, with answers. Part B: how every number is calculated. Part C: what comes from
the literature, what is textbook theory, what was assumed. Part D: what the contribution is, stated honestly.
Numbers are read from numbers.json / focused_model.py, so they match the slides. Run after focused_model.py:
    python -X utf8 build_qa_pdf.py"""
import math, os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table, TableStyle,
                                KeepTogether, CondPageBreak, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from focused_model import *
from talk_script import _bar

ROOT = os.path.join(HERE, ".."); OUT = os.path.join(ROOT, "Viva_Prep_QA_Sources_and_Contribution.pdf"); OUT_CALC = os.path.join(ROOT, "Calculations_How_the_Numbers_Are_Calculated.pdf")
EQD = os.path.join(HERE, "eq_qa"); os.makedirs(EQD, exist_ok=True)

fd = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
for nm, fn in (("Serif", "DejaVuSerif.ttf"), ("Serif-B", "DejaVuSerif-Bold.ttf"), ("Serif-I", "DejaVuSerif-Italic.ttf"),
               ("Serif-BI", "DejaVuSerif-BoldItalic.ttf"), ("Sans", "DejaVuSans.ttf"), ("Sans-B", "DejaVuSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(nm, os.path.join(fd, fn)))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")

PINEc, FERNc, SAGEc, INKc, TINTc, MISTc = (colors.HexColor(x) for x in (PINE, FERN, SAGE, INK, TINT, MIST))
S = dict(
    title=ParagraphStyle("title", fontName="Sans-B", fontSize=22, leading=27, textColor=PINEc, spaceAfter=4),
    sub=ParagraphStyle("sub", fontName="Serif-I", fontSize=10.5, leading=15, textColor=INKc, spaceAfter=8),
    part=ParagraphStyle("part", fontName="Sans-B", fontSize=15, leading=19, textColor=colors.white),
    h2=ParagraphStyle("h2", fontName="Sans-B", fontSize=11.5, leading=15, textColor=PINEc, spaceBefore=10, spaceAfter=4),
    lab=ParagraphStyle("lab", fontName="Sans-B", fontSize=8, leading=10.5, textColor=FERNc, spaceBefore=5, spaceAfter=2),
    body=ParagraphStyle("body", fontName="Serif", fontSize=9.8, leading=14, textColor=INKc, spaceAfter=4),
    q=ParagraphStyle("q", fontName="Serif-B", fontSize=10.6, leading=14.5, textColor=INKc),
    ans=ParagraphStyle("ans", fontName="Serif", fontSize=10, leading=14.4, textColor=INKc),
    bul=ParagraphStyle("bul", fontName="Serif", fontSize=9.8, leading=13.6, leftIndent=14, bulletIndent=2, spaceAfter=2.5, textColor=INKc),
    cell=ParagraphStyle("cell", fontName="Serif", fontSize=8.8, leading=11.6, textColor=INKc),
    cellb=ParagraphStyle("cellb", fontName="Serif-B", fontSize=8.8, leading=11.6, textColor=INKc),
    cap=ParagraphStyle("cap", fontName="Serif-I", fontSize=8.8, leading=12, textColor=INKc, spaceAfter=6),
)
def fmt(t):
    """Escape for reportlab, turn X_y into subscripts and **bold** into bold."""
    t = re.sub(r"([A-Za-zΔνμρσθε]+)_([A-Za-z0-9]+)", r"\1<sub>\2</sub>", escape(t))
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    return t.replace("★", '<font name="Sans">★</font>')
def P(t, st="body"): return Paragraph(fmt(t), S[st])
def C(t, bold=False): return Paragraph(fmt(t), S["cellb" if bold else "cell"])
def bullets(items): return [Paragraph(fmt(b), S["bul"], bulletText="•") for b in items]

_n = [0]
def eqimg(tex, width_max=14.5, fs=15):
    _n[0] += 1; path = os.path.join(EQD, f"e{_n[0]}.png")
    fig = plt.figure(figsize=(0.01, 0.01)); fig.text(0, 0, f"${tex}$", fontsize=fs, math_fontfamily="cm", color=INK)
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.03, transparent=True); plt.close(fig)
    w, h = PILImage.open(path).size; wc, hc = w * 72 / 300 / 28.35, h * 72 / 300 / 28.35
    if wc > width_max: hc *= width_max / wc; wc = width_max
    return Image(path, width=wc * cm, height=hc * cm, hAlign="LEFT")

def table(rows, widths, head=True, zebra=False):
    t = Table([[c if not isinstance(c, str) else C(c, bold=(head and i == 0)) for c in r] for i, r in enumerate(rows)], colWidths=[w * cm for w in widths], repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, SAGEc), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if head: st.append(("BACKGROUND", (0, 0), (-1, 0), TINTc))
    t.setStyle(TableStyle(st)); return t

def part_bar(text):
    t = Table([[Paragraph(fmt(text), S["part"])]], colWidths=[16.6 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PINEc), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t

def box(flow, fill=TINTc):
    t = Table([[flow]], colWidths=[16.6 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fill), ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t

# ---------------------------------------------------------------- numbers (all from the model)
o50, o10, oM = out["wick"][S50], out["wick"][S10], out["wick"][MESH]
wk = N["wicks"]; vc = {int(r["h_um"]): r for r in N["vapour_core"]}; cu = {int(v["h_um"]): v for v in out["vs_copper"]}
bh, bv = N["biporous"]["horizontal"], N["biporous"]["vertical"]; bhv, bvv = list(bh.values()), list(bv.values())
rp = wk[S10]["p_cap_kPa"] / wk[S50]["p_cap_kPa"]; rr = wk[S10]["a_l_Pa_per_W"] / wk[S50]["a_l_Pa_per_W"]
mdot5 = 5 / hfg; av100 = a_v(100e-6); Kfine, Kcoarse = N["biporous"]["K_fine"], N["biporous"]["K_coarse"]
kx = {(int(r["h_um"]), r["Q"]): r for r in N["keff"]}
hi01 = N["h_interface"]["0.1"]; kw = N["k_wick_maxwell_eps0.5"]; q_flux = N["q_flux_5W_W_m2"]
Q_50_100 = q_max(p_cap(WICKS[S50]["r"]), WICKS[S50]["K"], 100e-6)

story = []
# ================================================================== cover
story += [Paragraph("Viva preparation: Q&A, sources and contribution", S["title"]),
          P("Micro heat pipes and vapour chambers · 3-minute talk (slides only) with a 2-minute Q&A · Debanshu Ghosh, 23CH3FP56. "
            "Written for you, the presenter. Everything here is about what is on the slides. The step-by-step calculations are in the separate PDF “Calculations_How_the_Numbers_Are_Calculated”.", "sub")]
story.append(table([[C("Part", True), C("What it gives you", True)],
                    [C("A"), C("25 likely questions with answers. The ten marked ★ (shaded) are the most likely, and one of them is “what is your innovation?”. Each answer is sized to fit in 20 seconds.")],
                    [C("B"), C("What came from research papers, what is textbook theory, and what was assumed.")],
                    [C("C"), C("Your contribution slide by slide, the innovation stated honestly, what is not new, and one sentence to say it in.")]], [1.3, 15.3]))
story.append(Spacer(1, 8))
story.append(box([P("**How to survive a 2-minute Q&A**"),
    *bullets(["Expect 3 to 5 questions. Answer in 15 to 20 seconds: the number or the one-line reason first, the explanation second.",
              "Your numbers are for water at 60 °C and an illustrative 5 W phone-like disc. Say “in my model” before a number. Nobody can fault that; they can fault a number presented as a measurement.",
              "If you do not know: say what you do know, then “that is outside my model; I would check it in the literature.” Do not guess a value.",
              "Easy exits: “that is an assumption, stated on the slide”; “that is an upper bound, not a prediction”; “that is a simulation result from Patankar, not mine”.",
              "Slides 3, 4 and 5 hold your three biggest results: 5× and 25×; 50, 38 and 161 W; 27×, 28×, 12× and about 2×. For the calculation behind any of them, see the calculations PDF."])], MISTc))

# ================================================================== PART A
story += [PageBreak(), part_bar("Part A · Questions and answers"), Spacer(1, 4)]
QA = []   # (star, topic, question, answer, if_pushed)
def qa(star, topic, q, a, push=None): QA.append((star, topic, q, a, push))

qa(True, "Big picture", "How does a vapour chamber move heat without a pump?",
   "Heat evaporates water in the wick at the chip. The vapour flows through the open core to a cooler area and condenses, releasing the latent heat. The condensed liquid returns through the porous wick by capillary suction. "
   "The wick is the only pump, so the capillary pressure must beat the liquid loss, the vapour loss and gravity. That sets a maximum heat load, the capillary limit.",
   "In equations: ΔP_cap ≥ ΔP_l + ΔP_v + ΔP_g, and since both flow losses are linear in Q, Q_max = (ΔP_cap − ρ_l g Δz)/(a_l + a_v). My two topics are the liquid term and the vapour term.")
qa(True, "Topic 1", "Why is a finer wick not always better?",
   f"Because one length sets both the pump and the resistance. Capillary pressure goes as 1/r, so it rises as pores shrink. But permeability goes as d², so the liquid resistance rises faster. "
   f"Going from 50 µm to 10 µm powder gives {rp:.0f}× the pump pressure but {rr:.0f}× the liquid resistance. For the liquid alone, Q ∝ ΔP_cap·K ∝ d, so finer actually delivers less.",
   f"In the full model with a 100 µm core, the 50 µm powder reaches about {q_max(p_cap(WICKS[S50]['r']), WICKS[S50]['K'], 100e-6):.0f} W and the 10 µm powder only about {q_max(p_cap(WICKS[S10]['r']), WICKS[S10]['K'], 100e-6):.0f} W, held back by its own wick.")
qa(True, "Topic 1", "What is a biporous wick, and where does 161 W come from?",
   f"It has two pore scales: fine pores inside particle clusters set the pump pressure, and coarse channels between the clusters carry the liquid. In my model I take the pressure from r = 5 µm and the permeability from a 100 µm powder. "
   f"That gives {bhv[2]:.0f} W against {bhv[0]:.0f} W for the fine wick and {bhv[1]:.0f} W for the coarse one. It is an upper bound: it assumes the two regions do not interfere.",
   "Why upper bound: the channels take up volume and break the conduction path, and K from 100 µm particles would not fit in a 50 µm layer. The bar shows the principle, not a buildable wick.")
qa(True, "Topic 1", "What is the 37% on your biporous slide? Is it your result?",
   "No, it is not mine. It is from Patankar, Weibel and Garimella (2016): a 3-D numerical simulation in which a biporous condenser-side wick allowed a thicker vapour core, "
   "and the peak-to-mean surface temperature difference on the condenser fell by 37% compared with a monolithic wick.",
   "Be exact about it: simulation, not experiment; condenser surface temperature difference, not chip temperature; relative to a monolithic wick. Semenic and Catton (2009) is the experimental work on biporous wicks for evaporators.")
qa(True, "Topic 2", "Why does the vapour pressure drop go as 1/h³?",
   "Plane Poiseuille flow in a slit gives a pressure gradient 12μu/h². The flow area is 2πrh, so the velocity itself goes as 1/h. One power of h comes from the velocity, two from the wall shear: 1/h × 1/h² = 1/h³. "
   "So halving the gap multiplies the pressure drop by 2 × 4 = 8.",
   f"Integrating from R1 to R2 gives ΔP_v = 6 μ_v ṁ ln(R2/R1)/(π ρ_v h³). At 5 W and h = 100 µm that is {vc[100]['dP_5W_Pa']:.0f} Pa; at 50 µm it is {vc[50]['dP_5W_Pa']:.0f} Pa, which is 8 times larger.")
qa(True, "Topic 2", "How does a pressure drop become a temperature drop?",
   f"In saturated vapour, pressure and temperature are tied by Clausius–Clapeyron: ΔT ≈ T ΔP/(ρ_v h_fg). For water at 60 °C that is about {out['K_per_kPa']:.1f} K for every kilopascal of vapour pressure drop.",
   f"Example: {vc[100]['dP_5W_Pa']:.0f} Pa at 100 µm and 5 W is {vc[100]['dT_5W_K']:.2f} K. The relation is linearised, so it is only valid while the drop is a small fraction of P_sat; I use 20% (about {N['h_invalid_um']['5W']:.0f} µm at 5 W) as the limit.")
qa(True, "Topic 2", "What does your copper comparison show, and how is it set up?",
   f"A solid copper sheet of the same total thickness carries the same 5 W from the same source to the same rim. At 5 W the chamber has a temperature drop {cu[400]['factor']:.0f} times smaller at h = 400 µm, {cu[200]['factor']:.0f} times at 200 µm, "
   f"{cu[100]['factor']:.0f} times at 100 µm and only about {cu[50]['factor']:.0f} times at 50 µm. Thinning the core erases the advantage, because copper degrades slowly with thickness while the vapour drop grows as 1/h³.",
   f"The chamber's drop is vapour + wick conduction + evaporating interface. The interface term assumes an accommodation coefficient of 0.1. The 50 µm value is marked * because the vapour drop there is above 20% of P_sat, so read it as a trend.")
qa(True, "Method", "Are your numbers from a real device? Is the model validated?",
   "No. They come from a deliberately simple model: saturated water at 60 °C, a disc-shaped chamber with a 10 × 10 mm source and a 48 mm rim, 5 W. They are illustrative, not measured, and I have not validated the model against experiments. "
   "The model is there to show trends and scalings, and to say which effect dominates.",
   "Published experiments are cited only as context. For example, Yan et al. (2023) report a 0.5 mm composite-wick chamber with critical powers up to 60 W; that device differs from my model, so it is not a validation.")
qa(True, "Applications", "Why heat pipes in satellites, and what is special about gravity there?",
   "In orbit there is no gravity, so the liquid cannot drain back; the wick alone must return it. A heat pipe does that with no moving parts and moves heat with very little temperature drop. "
   "In my pressure budget the gravity term ΔP_g is then zero, so the capillary pressure only has to beat the liquid and vapour losses.",
   f"On Earth the term is ρ_l g Δz, which is {N['head_100mm_kPa']:.2f} kPa for a 100 mm rise. At the sub-millimetre scale of a phone chamber surface tension dominates: the Bond number at 200 µm is only {N['Bo']['200um']:.3f}.")

# remaining questions
qa(False, "Big picture", "What is the capillary limit, and what happens if you exceed it?",
   "It is the largest heat load for which the capillary pressure can still return enough liquid. Beyond it the wick cannot resupply the evaporator, the wick dries out near the heat source, and the temperature there rises sharply.",
   "There are other limits (sonic, entrainment, boiling). They are outside my scope. As a check, the sonic limit in my geometry is far above the 5 W load: "
   f"about {vc[100]['Q_sonic_W']:.0f} W at h = 100 µm.")
qa(False, "Big picture", "What is the difference between a micro heat pipe, a heat pipe and a vapour chamber?",
   "They are the same physics in different shapes. A heat pipe moves heat along a line, from an evaporator end to a condenser end. A vapour chamber is the flat, two-dimensional version that spreads heat over a plane. "
   "A micro heat pipe is a very small one, where the corners of the channel carry the liquid. My numbers use the flat chamber geometry.",
   None)
qa(False, "Big picture", "Why water, and why 60 °C?",
   "Water has a high latent heat (2.358 MJ/kg), a high surface tension (0.0662 N/m) and is compatible with copper, so it gives a strong pump and carries a lot of heat per kilogram. "
   "60 °C is an illustrative working temperature for electronics cooling; the properties change only modestly with temperature, so the trends do not depend on it.",
   "I did not run a temperature sweep, so do not claim a precise dependence. The numbers would shift; the 1/d, d² and 1/h³ scalings would not.")
qa(False, "Topic 1", "How did you get the permeability K?",
   f"From the Kozeny–Carman relation for a bed of spheres: K = d²ε³/[150(1−ε)²]. With porosity ε = 0.5 it is K = d²/300. For d = 50 µm that is {WICKS[S50]['K']:.2e} m². "
   f"The mesh value, K = 2.8×10⁻¹¹ m², is a typical figure I chose, not computed.",
   "Kozeny–Carman treats the pores as tubes with the hydraulic diameter of a packed bed. It is an estimate, and real wicks differ from it.")
qa(False, "Topic 1", "Where does r_eff = 0.21 d come from?",
   "It is a common rule of thumb for sintered spheres: the effective pore radius is about a fifth of the particle diameter. I state it as an assumption; it is not derived in my work.",
   "Mesh and groove wicks have their own correlations (Peterson 1994, Faghri 1995).")
qa(False, "Topic 1", "Is Darcy's law valid for a 50 µm wick?",
   "Only roughly. Darcy's law and Kozeny–Carman are continuum descriptions that need a layer many particles thick. A 50 µm layer of 50 µm powder is about one particle deep, so that case is an order-of-magnitude estimate.",
   "It does not change the trend, because the 5× and 25× come from scalings (1/d and d²). It does affect the absolute watts.")
qa(False, "Topic 1", "What if the wick does not wet perfectly?",
   "The capillary pressure carries cos θ. A contact angle drifting from 0° to 60° through oxidation or contamination halves the pump pressure, with no change in the geometry.", None)
qa(False, "Topic 1", "Does orientation matter, for example a phone held upright?",
   f"In the model, only through the gravity head ρ_l g Δz. For a 100 mm rise that is {N['head_100mm_kPa']:.2f} kPa. It would cut my idealised biporous limit from {bhv[2]:.0f} W to {bvv[2]:.0f} W if the source is at the top of a vertical sheet, "
   "while the fine wick, with its high pump pressure, is hardly affected.",
   f"At the sub-millimetre scale the Bond number is {N['Bo']['200um']:.3f} at 200 µm, so inside the sheet surface tension wins over gravity.")
qa(False, "Topic 2", "Why is your 50 µm chamber value marked with an asterisk?",
   f"At 50 µm the vapour pressure drop at 5 W is {vc[50]['dP_5W_Pa']/1000:.1f} kPa, which is above 20% of the saturation pressure ({P_sat/1000:.2f} kPa). "
   "The linearised Clausius–Clapeyron relation is then no longer valid, so that value is a trend, not a prediction.", None)
qa(False, "Topic 2", "Is the vapour flow incompressible and continuum?",
   f"Yes in the range used. At h = 100 µm and 5 W the Mach number is {vc[100]['Ma_5W']:.3f} and the Knudsen number is {vc[100]['Kn']:.4f} (mean free path {N['lambda_um']:.2f} µm), "
   "so the flow is incompressible and the continuum, no-slip description holds.", None)
qa(False, "Topic 2", "What are the main assumptions behind the vapour-core result?",
   "Steady, laminar, incompressible flow; smooth walls; and all the vapour travelling to the rim R2. In reality vapour condenses along the way, so the true pressure drop is lower by a factor of order one. "
   "Support pillars would add drag and raise it.",
   "So my number is conservative on the first point and optimistic on the second. I use the model for the 1/h³ trend, not for the exact watts.")
qa(False, "Topic 2", "The written paper has a thickness-optimisation section that is not in the talk. What is it?",
   f"With a fixed inner thickness of 250 µm, every micron of wick comes out of the vapour core. Liquid resistance falls as 1/t and vapour resistance rises as 1/h³, so the total has a minimum. "
   f"Setting the derivative to zero gives h²/t = 12√(Kν_v/ν_l). For the 50 µm powder: t ≈ {o50['t_um']:.0f} µm, h ≈ {o50['h_um']:.0f} µm, about {o50['Q_opt']:.0f} W.",
   "It is in the written paper. The result is my own derivation from the model, checked against a numerical sweep, and not compared with a published optimum. It maximises the capillary limit only, not thermal resistance.")
qa(False, "Applications", "Why heat pipes in laptops but a vapour chamber in a phone?",
   "A laptop has room to run a heat pipe from the CPU to a fan and fins, so the job is moving heat along a line. A phone has no fan and under a millimetre of free thickness, so the job is spreading the heat across the whole body, which a flat chamber does.", None)
qa(True, "Contribution", "You just collected data from papers. What is the innovation, and what is your contribution?",
   f"I did not collect the data. Apart from one number, the 37% from Patankar, every number on my slides is calculated by a model I assembled from standard equations. What is mine is the combination and its results: one equation that joins the wick and the vapour core; "
   f"the 5× and 25× wick trade-off; an idealised biporous bound ({bhv[2]:.0f} W against {bhv[0]:.0f} and {bhv[1]:.0f} W); the 1/h³ vapour limit with its validity checks; and the finding that the chamber's advantage over copper falls from {cu[200]['factor']:.0f}× to about {cu[50]['factor']:.0f}× as the core thins. "
   "It is a modest, analytical contribution: no new experiments and no new theory.",
   f"The design insight is that the vapour core, not the wick, ends the advantage in a thin chamber. That conclusion does not hinge on my assumed interface coefficient: at 50 µm, {cu[50]['vapour']:.1f} K of the {cu[50]['vc']:.1f} K total is the vapour drop. "
   "The limits: it is unvalidated, and I have not checked whether the same comparison has been published.")
qa(False, "Contribution", "What would you do next?",
   "Validate the trends against a published experiment or a CFD model; add support pillars and several heat sources; replace the Darcy estimate for the thin wick with a pore-scale model; and run the temperature sweep.", None)
qa(False, "Contribution", "What is the weakest part of your analysis?",
   "That it is unvalidated and that some inputs are assumptions: the 5 W load, the geometry, the 0.21 d rule, the mesh permeability and the accommodation coefficient of 0.1. "
   "The trends are robust, because they come from scalings; the absolute watts and kelvins are not.", None)

assert len(QA) == 25, len(QA)
k = 0
for topic in ("Big picture", "Topic 1", "Topic 2", "Applications", "Method", "Contribution"):
    items = [x for x in QA if x[1] == topic]
    if not items: continue
    story.append(Paragraph(fmt({"Big picture": "The big picture", "Topic 1": "Topic 1: the wick (liquid return, biporous)", "Topic 2": "Topic 2: the vapour core",
                                "Applications": "Applications", "Method": "Method and honesty", "Contribution": "Contribution and limits"}[topic]), S["h2"]))
    for star, _, q, a, push in items:
        k += 1
        blk = [Paragraph(fmt(f"Q{k}. " + ("★ " if star else "") + q), S["q"]), Spacer(1, 2),
               Paragraph(fmt(a), S["ans"])]
        if push: blk += [Spacer(1, 2), Paragraph(fmt("If pushed: " + push), ParagraphStyle("p", parent=S["ans"], fontName="Serif-I", fontSize=9.3, leading=13, textColor=FERNc))]
        t = Table([[blk]], colWidths=[16.6 * cm])
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TINTc if star else colors.white), ("BOX", (0, 0), (-1, -1), 0.5, SAGEc),
                               ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 9), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
        story += [KeepTogether([t]), Spacer(1, 5)]

# ================================================================== CALCULATIONS (separate PDF)
storyA = story; story = []
story += [Paragraph("How the numbers are calculated", S["title"]),
          P("Micro heat pipes and vapour chambers · calculations behind the slides · Debanshu Ghosh, 23CH3FP56. "
            "Each section gives the formula, one worked calculation you can repeat on a calculator, and the table the slide uses.", "sub")]
story.append(table([["Slide", "Numbers on the slide", "Calculated in"],
    ["3 (wick)", f"{rp:.0f}× pump pressure, {rr:.0f}× liquid resistance", "sections 2 and 3"],
    ["4 (biporous)", f"{bhv[0]:.0f}, {bhv[1]:.0f}, {bhv[2]:.0f} W", "section 5"],
    ["5 (vapour core)", f"8× per halving; 1.08 K per kPa; {cu[400]['factor']:.0f}×, {cu[200]['factor']:.0f}×, {cu[100]['factor']:.0f}×, ≈{cu[50]['factor']:.0f}×", "sections 4 and 6"]], [3.0, 9.6, 4.0]))
story.append(Spacer(1, 4))
story.append(P("Everything on the slides comes from one script (calc.py, with its companion script for the extra steps), using standard steam-table properties of saturated water at 60 °C and the geometry in section 1. "
               "The chain is always the same: **inputs → formula → number → check**. Below, each step shows the formula, one worked calculation you can repeat on a calculator, and the table the slide uses."))
story.append(Paragraph("1. Inputs", S["h2"]))
story.append(table([["Quantity", "Value", "Kind of input"],
    ["Surface tension σ", "0.0662 N/m", "standard steam-table value"],
    ["Latent heat h_fg", "2.358 MJ/kg", "standard steam-table value"],
    ["Liquid density, viscosity", "983.2 kg/m³, 4.66×10⁻⁴ Pa s", "standard steam-table values"],
    ["Vapour density, viscosity", "0.1304 kg/m³, 1.08×10⁻⁵ Pa s", "standard steam-table values"],
    ["Saturation pressure P_sat, T", "19.95 kPa, 333.15 K (60 °C)", "standard steam-table values"],
    ["Heat load Q, source", "5 W on 10 × 10 mm, so R1 = √(A/π) = 5.64 mm", "assumed (phone-like, illustrative)"],
    ["Chamber", "disc with R2 = 48 mm, the same area as a 60 × 120 mm sheet", "assumed"],
    ["Wick layers, copper walls", "2 × 50 µm wick, 2 × 80 µm wall", "assumed"],
    ["Porosity ε, r_eff", "ε = 0.5; r_eff ≈ 0.21 d for sintered powder", "assumed; rule of thumb"],
    ["Cu mesh #200", "r_eff = 64 µm, K = 2.8×10⁻¹¹ m²", "assumed typical values"],
    ["Contact angle", "θ = 0° (full wetting)", "assumed"],
    ["Gravity head", "Δz = 100 mm", "assumed (vertical case)"]], [4.6, 7.2, 4.8]))
story.append(P(f"Derived once and reused: ln(R2/R1) = ln(48/5.642) = {lnR:.3f}, and the mass flow at 5 W, ṁ = Q/h_fg = 5/2.358×10⁶ = {mdot5:.3e} kg/s.", "body"))

story.append(Paragraph("2. The pump: capillary pressure (slide 3)", S["h2"]))
story += [eqimg(r"\Delta P_{cap}=\dfrac{2\sigma\cos\theta}{r_{eff}}"),
          P(f"Worked: 50 µm powder, r_eff = 0.21 × 50 = 10.5 µm, so ΔP_cap = 2 × 0.0662 / 10.5×10⁻⁶ = {wk[S50]['p_cap_kPa']:.2f} kPa. 10 µm powder: r_eff = 2.1 µm gives {wk[S10]['p_cap_kPa']:.1f} kPa. Ratio = {rp:.0f} (it is 50/10 = 5, because ΔP_cap ∝ 1/d).")]

story.append(Paragraph("3. The loss: permeability and liquid resistance (slide 3)", S["h2"]))
story += [eqimg(r"K=\dfrac{d^{2}\varepsilon^{3}}{150(1-\varepsilon)^{2}}", 7), Spacer(1, 3),
          eqimg(r"\Delta P_l=a_l\,Q,\qquad a_l=\dfrac{\mu_l\,\ln(R_2/R_1)}{2\pi\,\rho_l\,K\,t_l\,h_{fg}},\qquad t_l=2t", 12),
          P(f"Worked: 50 µm powder, K = (50×10⁻⁶)² × 0.125 / (150 × 0.25) = {WICKS[S50]['K']:.3e} m² (that is d²/300). With t_l = 100 µm: "
            f"a_l = 4.66×10⁻⁴ × {lnR:.3f} / (2π × 983.2 × {WICKS[S50]['K']:.3e} × 1×10⁻⁴ × 2.358×10⁶) = {wk[S50]['a_l_Pa_per_W']:.1f} Pa/W. The same steps for 10 µm powder give {wk[S10]['a_l_Pa_per_W']:.0f} Pa/W, a ratio of {rr:.0f} (K ∝ d², so 25)."),
          table([["Wick", "r_eff (µm)", "K (m²)", "ΔP_cap (kPa)", "a_l (Pa/W)"]] +
                [[n, f"{wk[n]['r_um']:.1f}", f"{wk[n]['K']:.2e}", f"{wk[n]['p_cap_kPa']:.1f}", f"{wk[n]['a_l_Pa_per_W']:.1f}"] for n in (MESH, S50, S10)], [5.4, 2.4, 3.0, 2.9, 2.9])]

story.append(Paragraph("4. The vapour resistance and its temperature cost (slide 5)", S["h2"]))
story += [eqimg(r"\Delta P_v=a_v\,Q,\qquad a_v=\dfrac{6\,\mu_v\,\ln(R_2/R_1)}{\pi\,\rho_v\,h^{3}\,h_{fg}},\qquad \Delta T_{sat}\approx\dfrac{T\,\Delta P}{\rho_v\,h_{fg}}", 14.5),
          P(f"Worked: h = 100 µm, a_v = 6 × 1.08×10⁻⁵ × {lnR:.3f} / (π × 0.1304 × (10⁻⁴)³ × 2.358×10⁶) = {av100:.0f} Pa/W. At 5 W: ΔP_v = {av100*5:.0f} Pa. "
            f"The conversion factor is T/(ρ_v h_fg) = 333.15 / (0.1304 × 2.358×10⁶) = 1.08×10⁻³ K/Pa, so ΔT = {vc[100]['dT_5W_K']:.2f} K. Halving h to 50 µm multiplies a_v by 2³ = 8."),
          table([["h (µm)", "ΔP_v at 5 W (Pa)", "ΔT at 5 W (K)", "Mach", "Knudsen", "Valid? (ΔP < 20% P_sat)"]] +
                [[str(h), f"{vc[h]['dP_5W_Pa']:.0f}", f"{vc[h]['dT_5W_K']:.2f}", f"{vc[h]['Ma_5W']:.3f}", f"{vc[h]['Kn']:.4f}", "yes" if vc[h]['dP_5W_Pa'] <= 0.2 * P_sat else "no: trend only"] for h in (400, 200, 100, 50)],
                [1.8, 3.0, 2.8, 1.8, 2.2, 5.0]),
          P(f"The 20% limit is ΔP_v = 0.2 × 19.95 kPa = 3.99 kPa; solving a_v Q = 3.99 kPa for h at 5 W gives h ≈ {N['h_invalid_um']['5W']:.0f} µm. Below that the linearised relation is not trusted. "
            f"Validity checks at h = 100 µm: Mach = u/√(γ R_v T) = {vc[100]['Ma_5W']:.3f} (u = {vc[100]['u_5W_m_s']:.1f} m/s, incompressible); Knudsen = λ/h = {N['lambda_um']:.2f}/100 = {vc[100]['Kn']:.4f} (continuum, no slip).", "cap")]

story.append(Paragraph("5. The capillary limit and the biporous bars (slide 4)", S["h2"]))
story += [eqimg(r"Q_{max}=\dfrac{\Delta P_{cap}-\rho_l g\,\Delta z}{a_l+a_v}", 8),
          P(f"Worked, 50 µm powder with h = 100 µm (horizontal, Δz = 0): Q_max = {wk[S50]['p_cap_kPa']*1000:.0f} / ({wk[S50]['a_l_Pa_per_W']:.1f} + {av100:.0f}) = {Q_50_100:.0f} W. "
            "The three biporous bars use the same equation with a different (r_eff, K) pair, all at h = 100 µm and 2 × 50 µm wick:"),
          table([["Case", "r for ΔP_cap", "K for a_l", "ΔP_cap", "a_l", "a_v", "Q_max"],
                 ["Fine only", "5 µm", f"{Kfine:.2e} (d = 23 µm)", f"{p_cap(5e-6)/1e3:.1f} kPa", f"{a_l(Kfine):.0f} Pa/W", f"{av100:.0f}", f"{bhv[0]:.0f} W"],
                 ["Coarse only", "21 µm", f"{Kcoarse:.2e} (d = 100 µm)", f"{p_cap(21e-6)/1e3:.1f} kPa", f"{a_l(Kcoarse):.1f} Pa/W", f"{av100:.0f}", f"{bhv[1]:.0f} W"],
                 ["Biporous", "5 µm", f"{Kcoarse:.2e}", f"{p_cap(5e-6)/1e3:.1f} kPa", f"{a_l(Kcoarse):.1f} Pa/W", f"{av100:.0f}", f"{bhv[2]:.0f} W"]],
                [2.3, 2.2, 3.7, 2.2, 2.4, 1.6, 2.2]),
          P(f"Check the biporous bar: {p_cap(5e-6):.0f} / ({a_l(Kcoarse):.1f} + {av100:.0f}) = {bhv[2]:.0f} W. The fine wick takes its permeability from a 23 µm powder because its pore radius is 0.21 × 23 ≈ 5 µm, so r and K are consistent with each other. "
            "The biporous bar combines the fine r with the coarse K, which is why it is an idealised upper bound.", "cap")]

story.append(Paragraph("6. Chamber against a solid copper sheet (slide 5)", S["h2"]))
story += [eqimg(r"\Delta T_{Cu}=\dfrac{Q\,\ln(R_2/R_1)}{2\pi\,k\,H},\qquad \Delta T_{chamber}=\Delta T_{vapour}+\Delta T_{wick}+\Delta T_{interface}", 14.5),
          P(f"The copper sheet has the chamber's total thickness H = h + 2 × 50 + 2 × 80 µm and k = 400 W/m K. The chamber terms: vapour from section 4; wick conduction ΔT_w = q″ t_w/k_wick with q″ = Q/A = {q_flux:.0f} W/m² and "
            f"k_wick = {kw:.0f} W/m K from the Maxwell estimate for ε = 0.5; interface ΔT_i = q″/h_i with h_i = {hi01/1e5:.2f}×10⁵ W/m² K from kinetic theory (Hertz–Knudsen–Schrage) with an assumed accommodation coefficient of 0.1."),
          P(f"Worked, h = 200 µm: H = 0.46 mm, ΔT_Cu = 5 × {lnR:.3f} / (2π × 400 × 0.00046) = {cu[200]['cu']:.1f} K. Chamber: {cu[200]['vapour']:.3f} + {cu[200]['wick']:.3f} + {cu[200]['interface']:.3f} = {cu[200]['vc']:.2f} K. Ratio = {cu[200]['factor']:.0f}."),
          table([["h (µm)", "H (mm)", "Copper (K)", "Vapour (K)", "Wick (K)", "Interface (K)", "Chamber (K)", "Copper ÷ chamber"]] +
                [[str(v["h_um"]), f"{v['H_mm']:.2f}", f"{v['cu']:.1f}", f"{v['vapour']:.3f}", f"{v['wick']:.3f}", f"{v['interface']:.3f}", f"{v['vc']:.2f}" + ("*" if v["h_um"] < 60 else ""), (f"{v['factor']:.0f}×" if v["h_um"] >= 100 else f"≈{v['factor']:.0f}×*")] for v in out["vs_copper"]],
                [1.5, 1.5, 2.0, 2.0, 1.8, 2.3, 2.2, 3.3]),
          P("* ΔP_v above 20% of P_sat, so a trend only. Why copper catches up: copper's ΔT rises only from 6.5 to 13.7 K as H falls from 0.66 to 0.31 mm, while the chamber's vapour term rises from 0.01 to 6.2 K because it goes as 1/h³.", "cap")]

storyB = story; story = storyA

# ================================================================== PART C
story += [PageBreak(), part_bar("Part B · What came from where"), Spacer(1, 4)]
story.append(P("Three kinds of input go into the work, and an examiner is entitled to ask which is which. The honest split is below."))
story.append(Paragraph("B1. Numbers taken from research papers", S["h2"]))
story.append(table([["Number or claim", "Where it appears", "Source", "Note"],
    ["37% lower peak-to-mean condenser surface ΔT with a biporous condenser wick", "slide 4 tile", "Patankar, Weibel & Garimella (2016), Int. J. Heat Mass Transfer 101, 927–936", "a 3-D simulation, not an experiment; relative to a monolithic wick"],
    ["Up to 34% performance reduction by thermal throttling on a Nexus 6P", "paper introduction (not on the slides)", "Bhat, Gumussoy & Ogras (2019), DATE 2019", "motivation only"],
    ["0.5 mm composite-wick chamber, critical power up to 60 W", "paper, context", "Yan et al. (2023), Applied Thermal Engineering 226, 120340", "context, not a validation of the model"],
    ["Biporous wicks help high-flux evaporators (experiments)", "slide 4 and paper; qualitative", "Semenic & Catton (2009), IJHMT 52, 5113–5121", "no number from this paper is used"],
    ["Effective conductivity falls as support-column diameter grows", "paper, one sentence", "Zhang et al. (2024), Micromachines 15, 627", "not on the slides"],
    ["Vapour chambers move heat as latent heat, with no moving parts", "paper introduction", "Faghri (2012); Weibel & Garimella (2013); Zhou et al. (2023)", "review papers"]],
    [4.6, 3.0, 5.0, 4.0]))
story.append(P("Only the 37% is a quantitative result borrowed from a paper that appears on the slides. Every other number on the slides comes from the model, shown step by step in the calculations PDF.", "cap"))
story.append(Paragraph("B2. Theory taken from textbooks and the course (not new, not mine)", S["h2"]))
story.append(table([["Result", "Used for"],
    ["Young–Laplace: pressure jump 2σ/R across a curved interface", "capillary pressure"],
    ["Darcy's law, radial form", "liquid pressure loss in the wick"],
    ["Kozeny–Carman permeability for a bed of spheres", "K of the sintered wicks"],
    ["Plane Poiseuille flow between plates", "vapour pressure loss in the core"],
    ["Clausius–Clapeyron relation", "converting vapour pressure drop to temperature drop"],
    ["Maxwell effective conductivity of a porous medium", "wick conduction term in the copper comparison"],
    ["Hertz–Knudsen–Schrage kinetic theory of evaporation", "interface term in the copper comparison"],
    ["Mach and Knudsen number criteria; Bond number", "validity checks"],
    ["Course material (DasGupta & Ganguly, Lectures 1–4)", "scaling, continuum and slip arguments as background"],
    ["Peterson (1994), Faghri (1995)", "standard textbooks cited for classical wick correlations"]], [10.0, 6.6]))
story.append(Paragraph("B3. Values that are assumptions, not data", S["h2"]))
story += bullets([
    "**Properties of water at 60 °C**: standard saturated-water steam-table values, rounded. The paper does not name one specific table, so if asked say “standard steam tables”.",
    "**The operating point**: 5 W, a 10 × 10 mm source, a 48 mm rim, 2 × 50 µm wicks, 2 × 80 µm walls, 100 mm gravity head. All are illustrative and were chosen to be phone-like.",
    "**r_eff ≈ 0.21 d and ε = 0.5** for sintered powder: a rule of thumb and a typical porosity. Not derived here, and not cited to one specific paper.",
    "**Cu mesh #200 (r = 64 µm, K = 2.8×10⁻¹¹ m²)**: typical values chosen for the example, not computed here.",
    "**Accommodation coefficient 0.1** in the interface term: assumed. The literature gives a very wide range of values for water (the full paper lists Marek & Straub, 2001, on this).",
    "**The biporous pair** (r_fine = 5 µm, K from a 100 µm powder): chosen to make the principle visible, which is why the result is an upper bound.",
    "**The 20% of P_sat limit** for the linearised Clausius–Clapeyron relation: a judgement, chosen as a conservative cut-off.",
    "**Copper conductivity 400 W/m K**: a typical handbook value."])

# ================================================================== PART C (contribution)
story += [PageBreak(), part_bar("Part C · Your contribution, according to the slides"), Spacer(1, 4)]
story.append(P("The question to expect: “you only collected data, so what is the innovation?” The first thing to say is that it is not true that you collected data. "
               "Only one number on your slides, the 37%, comes from a paper. Everything else is calculated by a model. Here is what each slide takes from where, and what you added."))
story.append(Paragraph("C1. Slide by slide", S["h2"]))
story.append(table([["Slide", "From the literature or textbooks", "What you added"],
    ["2 · Overview", "The capillary-limit idea for heat pipes",
     "Joined the wick and the vapour core in one equation, with both losses as flow resistances in Pa/W (a_l, a_v), so that each topic is one term of it; numbers for a phone-sized disc."],
    ["3 · Wick", "Young–Laplace, radial Darcy flow, Kozeny–Carman",
     f"Integrated the flow laws over the disc, from R1 to R2. Quantified the trade-off: {rp:.0f}× pump pressure against {rr:.0f}× liquid resistance from 50 µm to 10 µm powder, and showed that for liquid alone Q ∝ d."],
    ["4 · Biporous", "The biporous idea (Semenic & Catton); the 37% (Patankar et al.)",
     f"Built an idealised capillary limit with the pressure from the fine pores and the permeability from the coarse channels: {bhv[2]:.0f} W against {bhv[0]:.0f} and {bhv[1]:.0f} W, stated as an upper bound."],
    ["5 · Vapour core", "Plane Poiseuille flow; Clausius–Clapeyron",
     f"Derived ΔP_v ∝ 1/h³ for radial flow and converted it to temperature ({out['K_per_kPa']:.1f} K per kPa). Set its validity limits (Mach, Knudsen, 20% of P_sat, so h above about {N['h_invalid_um']['5W']:.0f} µm at 5 W). "
     f"Compared the chamber with an equal-thickness copper sheet: {cu[400]['factor']:.0f}×, {cu[200]['factor']:.0f}×, {cu[100]['factor']:.0f}× and about {cu[50]['factor']:.0f}×."],
    ["6 · Applications", "General knowledge of where heat pipes and chambers are used",
     "Linked each application to the limit that matters most in it (phone: vapour core; laptop and LED: liquid return; satellite: no gravity term). The diagrams are schematic."]],
    [2.4, 5.0, 9.2]))
story.append(Paragraph("C2. The innovation, stated honestly", S["h2"]))
story += bullets([
    "**It is a synthesis and a quantification, not new science.** You took standard laws and built them into one transparent model, then used it to get numbers a reader can check.",
    f"**The strongest result is the copper comparison.** It turns the abstract 1/h³ law into a design statement: a chamber beats solid copper by {cu[200]['factor']:.0f}× at a 200 µm core but by only about {cu[50]['factor']:.0f}× at 50 µm, so the vapour core, not the wick, sets how thin a chamber can usefully be. "
    f"This does not hinge on the assumed interface coefficient, because at 50 µm the vapour drop is {cu[50]['vapour']:.1f} K of the {cu[50]['vc']:.1f} K total.",
    "**The second is the wick trade-off made quantitative**, with the biporous bound showing what separating pump and flow could be worth.",
    "**It is consistent with the literature.** Patankar et al. found that making room for a thicker vapour core is the lever that matters at ultra-thin form factors, which is what your model gives as well."])
story.append(Paragraph("C3. What is not new, so do not claim it", S["h2"]))
story += bullets([
    "The governing equations (Young–Laplace, Darcy, Poiseuille, Kozeny–Carman, Clausius–Clapeyron) are standard.",
    "The idea of a biporous wick and the 37% condenser result are from the literature (Semenic & Catton; Patankar et al.).",
    "There are no experiments. The model is not validated, and its inputs are illustrative. It shows scalings and trends, not device performance.",
    "I have not checked whether the same copper comparison has been published, so present it as the conclusion of your model, not as a first.",
    "The written paper also has a thickness-optimisation result, h²/t = 12√(Kν_v/ν_l). It is not on the slides, so you do not need to claim it; if asked, say it is derived within the model and checked against a numerical sweep."])
story.append(Paragraph("C4. One sentence to say it in", S["h2"]))
story.append(box([Paragraph(fmt("“I did not collect data: apart from one number from Patankar, everything on my slides is calculated. My contribution is a simple, transparent model that puts the wick and the vapour core into one capillary-limit equation, "
                               "and uses it to show for a phone-sized chamber that finer pores cost more flow than they gain in pumping, that a biporous wick could separate the two, "
                               "and that the vapour core, through its 1/h³ resistance, decides how thin a chamber can be before it loses its advantage over copper.”"), ParagraphStyle("big", parent=S["ans"], fontName="Serif-B", fontSize=11, leading=16))], MISTc))
story.append(Spacer(1, 8))
story.append(box([P("**Be ready to explain every formula yourself.** The model and scripts were built with Claude's help in this project, so before the talk work through the calculations PDF with a calculator until you can reproduce the worked examples. "
                    "The slides' speaker notes also hold each formula's derivation. If your course asks for a declaration on the use of AI tools, that is for you to check and make.")]))

def build(path, flow, title, foot):
    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont("Sans", 7.5); canvas.setFillColor(INKc)
        canvas.drawString(2.2 * cm, 1.3 * cm, foot)
        canvas.drawRightString(A4[0] - 2.2 * cm, 1.3 * cm, str(doc.page)); canvas.restoreState()
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=1.8 * cm, bottomMargin=2.0 * cm, title=title, author="Debanshu Ghosh")
    doc.addPageTemplates([PageTemplate(id="m", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f", leftPadding=0, rightPadding=0)], onPage=footer)])
    doc.build(flow)
    print("written", path, os.path.getsize(path) // 1024, "KB")


build(OUT, story, "Viva preparation: Q&A, sources and contribution", "Debanshu Ghosh · 23CH3FP56 · Viva preparation: Q&A, sources, contribution")
build(OUT_CALC, storyB, "How the numbers are calculated", "Debanshu Ghosh · 23CH3FP56 · How the numbers are calculated")
