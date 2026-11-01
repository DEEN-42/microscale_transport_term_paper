"""Builds Presentation_3min_Micro_Heat_Pipes_and_Vapour_Chambers.pptx (python-pptx): 3 minutes, 3 topics, 7 slides.
Run after focused_model.py and figs_focused.py. Numbers come from numbers.json and focused_model.py.
Charts are native PowerPoint charts; illustrations and equations are images from figs_focused.py / mathtext."""
import copy, os, re, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData, XyChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION, XL_MARKER_STYLE, XL_TICK_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from focused_model import *
from talk_script import head, running, clock, EQ_SPLIT, EQ_OPT

ROOT = os.path.join(HERE, ".."); FIGD = os.path.join(ROOT, "figures")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "Presentation_3min_Micro_Heat_Pipes_and_Vapour_Chambers.pptx")
EQD = os.path.join(HERE, "eq_slides_focused"); os.makedirs(EQD, exist_ok=True)
HEAD_FONT, BODY_FONT = "Cambria", "Calibri"

def rgb(h): return RGBColor.from_string(h.lstrip("#"))
cSAGE, cFERN, cPINE, cINK, cTINT, cMIST, cWHITE = map(rgb, (SAGE, FERN, PINE, INK, TINT, MIST, "#FFFFFF"))

vc = {int(r["h_um"]): r for r in N["vapour_core"]}; wk = N["wicks"]; bh = N["biporous"]["horizontal"]; opt = out["wick"]

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

# ---------------------------------------------------------------- theme and layouts
theme_part = next(r.target_part for r in prs.slide_master.part.rels.values() if r.reltype.endswith("/theme"))
th = etree.fromstring(theme_part.blob)
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
th.set("name", "Vapour chamber palette")
colors = dict(dk1=INK, lt1="#FFFFFF", dk2=PINE, lt2=TINT, accent1=PINE, accent2=FERN, accent3=SAGE, accent4=INK, accent5=MIST, accent6=TINT, hlink=PINE, folHlink=FERN)
scheme = th.find(f".//{A}clrScheme"); scheme.set("name", "Vapour chamber palette")
for k, v in colors.items():
    el = scheme.find(A + k)
    for c in list(el): el.remove(c)
    etree.SubElement(el, A + "srgbClr").set("val", v.lstrip("#"))
fonts = th.find(f".//{A}fontScheme")
fonts.find(f"{A}majorFont/{A}latin").set("typeface", HEAD_FONT)
fonts.find(f"{A}minorFont/{A}latin").set("typeface", BODY_FONT)
theme_part._blob = etree.tostring(th, xml_declaration=True, encoding="UTF-8", standalone=True)

TITLE_ONLY, BLANK, DARK = prs.slide_layouts[5], prs.slide_layouts[6], prs.slide_layouts[2]
def fix_layout(layout):
    """Default template is 4:3: drop its date/footer placeholders and move the title to the deck's position."""
    for ph in list(layout.placeholders):
        if ph.placeholder_format.idx in (10, 11, 12): ph._element.getparent().remove(ph._element)
    for ph in layout.placeholders:
        if ph.placeholder_format.idx == 0:
            ph.left, ph.top, ph.width, ph.height = Inches(0.6), Inches(0.62), Inches(12.13), Inches(0.72)
            tf = ph.text_frame; tf.vertical_anchor = MSO_ANCHOR.TOP; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            bp = tf._txBody.find(qn("a:bodyPr"))
            for c in list(bp): bp.remove(c)
            lst = tf._txBody.find(qn("a:lstStyle"))
            for c in list(lst): lst.remove(c)
            lvl = etree.SubElement(lst, qn("a:lvl1pPr")); lvl.set("algn", "l")
            d = etree.SubElement(lvl, qn("a:defRPr")); d.set("sz", "3000"); d.set("b", "1")
            f = etree.SubElement(d, qn("a:solidFill")); etree.SubElement(f, qn("a:schemeClr")).set("val", "tx2")
for ph in list(DARK.placeholders):
    if ph.placeholder_format.idx == 1: ph._element.getparent().remove(ph._element)
DARK.name = "Closing (dark)"
for l in (TITLE_ONLY, BLANK, DARK): fix_layout(l)
_t = next(p for p in DARK.placeholders if p.placeholder_format.idx == 0)
_t._element.find(".//" + qn("a:defRPr")).find(qn("a:solidFill"))[0].set("val", "bg1")
DARK.background.fill.solid(); DARK.background.fill.fore_color.rgb = cINK
for ph in list(prs.slide_master.placeholders):      # master placeholders follow the wide canvas
    k = prs.slide_width / Inches(10)
    ph.left, ph.width = int(ph.left * k), int(ph.width * k)

# slide number field lives on the layouts
def slide_number(layout, scheme_color):
    layout.shapes._spTree.append(parse_xml(f'''<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
<p:nvSpPr><p:cNvPr id="90" name="Slide number"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{Inches(12.13)}" y="{Inches(7.0)}"/><a:ext cx="{Inches(0.6)}" cy="{Inches(0.3)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0"/><a:lstStyle/><a:p><a:pPr algn="r"/><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum"><a:rPr lang="en-GB" sz="1100"><a:solidFill><a:schemeClr val="{scheme_color}"/></a:solidFill></a:rPr><a:t>‹#›</a:t></a:fld></a:p></p:txBody></p:sp>'''))
slide_number(TITLE_ONLY, "accent2"); slide_number(DARK, "accent3")

# ---------------------------------------------------------------- helpers
def tb(slide, x, y, w, h, text="", size=16, bold=False, color=cINK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font=None, italic=False, name=None):
    s = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = s.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    runs = text if isinstance(text, list) else [(text, {})]
    p = tf.paragraphs[0]; p.alignment = align
    for t, o in [(part, o_) for t_, o_ in runs for part in re.split("(\n)", t_)]:
        if t == "\n": p.add_line_break(); continue
        r = p.add_run(); r.text = t; r.font.size = Pt(o.get("size", size)); r.font.bold = o.get("bold", bold); r.font.italic = italic
        r.font.color.rgb = o.get("color", color)
        if font: r.font.name = font
    if name: s.name = name
    return s

def tag(slide, text): tb(slide, 0.6, 0.3, 11, 0.3, text, size=14, bold=True, color=cFERN, name="Section label")

def new_slide(tag_text, title, notes):
    s = prs.slides.add_slide(TITLE_ONLY); s.shapes.title.text = title
    tag(s, tag_text); s.notes_slide.notes_text_frame.text = notes
    return s

def pic(slide, name, x, y, w=None, h=None, alt=""):
    path = os.path.join(FIGD, name); iw, ih = PILImage.open(path).size
    if w and not h: h = w * ih / iw
    elif h and not w: w = h * iw / ih
    p = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    p._element.nvPicPr.cNvPr.set("descr", alt); p.name = name
    return p

def box(slide, x, y, w, h, fill=cTINT, name="Card", shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.07):
    r = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    r.fill.solid(); r.fill.fore_color.rgb = fill; r.line.fill.background(); r.shadow.inherit = False; r.name = name
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE: r.adjustments[0] = adj
    return r

def eq(slide, tex, key, x, y, h, w_box=None, color=INK, alt=None):
    """Equation image at a set height; centred in w_box if given."""
    path = os.path.join(EQD, key + ".png")
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, f"${tex}$", fontsize=30, color=color, math_fontfamily="cm")
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.03, transparent=True); plt.close(fig)
    iw, ih = PILImage.open(path).size; w = h * iw / ih
    if w_box and w > w_box: w, h = w_box, w_box * ih / iw
    x_ = x + (w_box - w) / 2 if w_box else x
    p = slide.shapes.add_picture(path, Inches(x_), Inches(y), Inches(w), Inches(h))
    p._element.nvPicPr.cNvPr.set("descr", alt or tex); p.name = "Equation " + key
    return p

def eq_card(slide, x, y, w, h, label, tex, key, eh=0.72, alt=None):
    box(slide, x, y, w, h, name="Equation card " + key)
    tb(slide, x + 0.2, y + 0.1, w - 0.4, 0.3, label, size=14, bold=True, color=cPINE)
    eq(slide, tex, key, x + 0.2, y + 0.42 + max(0, (h - 0.5 - eh) / 2), eh, w_box=w - 0.4, alt=alt)

def stat(slide, x, y, w, big, small, fill=cPINE, h=1.2, bigsize=36):
    box(slide, x, y, w, h, fill=fill, name="Stat " + big)
    y += max(0, h - 1.42) / 2
    tb(slide, x + 0.1, y + 0.08, w - 0.2, 0.62, big, size=bigsize, bold=True, color=cWHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, font=HEAD_FONT)
    tb(slide, x + 0.12, y + 0.7, w - 0.24, h - 0.74, small, size=14, color=cWHITE, align=PP_ALIGN.CENTER)

def style_chart(ch, ytitle=None, xtitle=None, legend=False, size=13):
    ch.font.size = Pt(size); ch.font.color.rgb = cINK; ch.font.name = BODY_FONT
    ch.has_title = False; ch.has_legend = legend
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False; ch.legend.font.size = Pt(size)
    va, ca = ch.value_axis, ch.category_axis
    va.has_major_gridlines = True; va.major_gridlines.format.line.color.rgb = cMIST; va.major_gridlines.format.line.width = Pt(0.75)
    va.format.line.fill.background(); ca.has_major_gridlines = False; ca.format.line.color.rgb = cFERN
    va.tick_labels.font.size = Pt(size); ca.tick_labels.font.size = Pt(size)
    for axis, t in ((va, ytitle), (ca, xtitle)):
        axis.has_title = bool(t)
        if t:
            tf = axis.axis_title.text_frame; tf.text = t
            r = tf.paragraphs[0].runs[0]; r.font.size = Pt(size); r.font.bold = False; r.font.color.rgb = cINK; r.font.name = BODY_FONT

# ---------------------------------------------------------------- 1 title
s = prs.slides.add_slide(BLANK)
bg = s.background.fill; bg.solid(); bg.fore_color.rgb = cINK
tb(s, 0.75, 0.62, 11.8, 0.35, "MICROSCALE TRANSPORT PROCESSES · TERM PAPER", size=14, bold=True, color=cSAGE, name="Course")
tb(s, 0.75, 1.1, 11.8, 1.6, "Micro Heat Pipes and Vapour Chambers", size=46, bold=True, color=cWHITE, font=HEAD_FONT, name="Title")
tb(s, 0.75, 2.1, 11.8, 0.6, "Liquid return in the wick, wick-thickness optimisation and vapour flow in a thin core", size=22, color=cMIST, name="Subtitle")
pic(s, "g0_title_band.png", 0, 3.0, w=13.333, alt="Stylised vapour chamber cross-section with vapour flowing right through the core and liquid returning left through the wicks.")
tb(s, 0.75, 6.0, 11.8, 0.4, "Debanshu Ghosh · Roll No. 23CH3FP56", size=20, bold=True, color=cWHITE, name="Author")
tb(s, 0.75, 6.45, 11.8, 0.4, "Department of Chemical Engineering, IIT Kharagpur", size=16, color=cMIST, name="Department")
s.notes_slide.notes_text_frame.text = head(1).rstrip()

# ---------------------------------------------------------------- 2 overview
s = new_slide("OVERVIEW", "A capillary pump must beat every loss in the loop",
    head(2) +
    "ABOUT THE PICTURE\n"
    "It is a half section through the centre of a disc-shaped chamber, the geometry of the model. The dashed left edge is the centre line, the chip sits under the centre (radius R1) and the rim is at R2. "
    "Heat enters through the bottom wall at the chip and evaporates liquid from the bottom wick. Vapour flows outward and condenses over the whole cooler top surface, mostly near the chip, so the arrow narrows; that is where the heat leaves. "
    "The condensate returns through the top wick, runs down the wick columns and joins the bottom wick, which carries it back to the evaporator.\n\n"
    "HOW THE FORMULA COMES\n"
    "1. Pressure around the closed loop must balance. Only the meniscus raises pressure; everything else loses it: ΔP_cap ≥ ΔP_l + ΔP_v + ΔP_g.\n"
    "2. Mass flow from an energy balance: ṁ = Q/h_fg. At 5 W and h_fg = 2.358 MJ/kg, ṁ = 2.1 mg/s.\n"
    "3. Both flow losses are laminar, so linear in ṁ and hence in Q. Write ΔP_l = a_l Q and ΔP_v = a_v Q, where a is a flow resistance in Pa/W.\n"
    "4. Gravity: ΔP_g = ρ_l g Δz. Substitute with equality and solve for Q: Q_max = (ΔP_cap − ρ_l g Δz)/(a_l + a_v).\n\n"
    "IF ASKED\n"
    "Numbers use saturated water at 60 °C and an illustrative disc: R1 = 5.64 mm (10 × 10 mm source), R2 = 48 mm (same area as a 60 × 120 mm sheet). They are not measured device data.")
pic(s, "g1_cycle.png", 0.97, 1.35, w=11.2, alt="Half section of a vapour chamber. The chip sits under the centre line. Vapour flows outward through the core (topic 3) and condenses over the whole cooler top surface, where heat leaves. Liquid returns through the top wick, down the wick columns and along the bottom wick to the chip (topic 1). Wick thickness t and core height h share a fixed total (topic 2).")
box(s, 0.6, 5.05, 12.13, 1.72, name="Pressure budget card")
tb(s, 0.85, 5.15, 5.7, 0.3, "The pressure budget", size=14, bold=True, color=cPINE)
eq(s, r"\Delta P_{cap}\;\geq\;\Delta P_{l}+\Delta P_{v}+\Delta P_{g}", "budget", 0.85, 5.72, 0.56, w_box=5.6, alt="Delta P cap is at least Delta P l plus Delta P v plus Delta P g")
tb(s, 6.85, 5.15, 5.7, 0.3, "So the heat load has a ceiling (capillary limit)", size=14, bold=True, color=cPINE)
eq(s, r"Q_{max}=\dfrac{\Delta P_{cap}-\rho_l\,g\,\Delta z}{a_l+a_v}", "qmax", 6.85, 5.47, 1.16, w_box=5.6, alt="Q max equals Delta P cap minus rho l g Delta z, over a l plus a v")

# ---------------------------------------------------------------- 3 liquid return
ratio_p = wk[S10]["p_cap_kPa"] / wk[S50]["p_cap_kPa"]; ratio_r = wk[S10]["a_l_Pa_per_W"] / wk[S50]["a_l_Pa_per_W"]
s = new_slide("TOPIC 1 · LIQUID RETURN IN THE WICK", "Finer pores pump harder but resist flow far more",
    head(3) +
    "HOW THE FORMULAS COME\n"
    "Young-Laplace: a spherical interface of radius R has a pressure jump 2σ/R. In a pore of radius r_eff the meniscus meets the wall at contact angle θ, so geometry gives R = r_eff/cos θ. Hence ΔP_cap = 2σ cos θ / r_eff.\n"
    "Water at 60 °C: σ = 0.0662 N/m. For θ = 0 and r_eff = 10.5 µm: 2(0.0662)/10.5e-6 = 12.6 kPa.\n\n"
    "Darcy in radial flow: Darcy's law is dP/dr = μ_l u / K. Mass conservation across a cylinder of radius r through total wick thickness t_l gives ṁ = ρ_l u (2π r t_l), so u = ṁ/(2π ρ_l r t_l).\n"
    "Substitute: dP/dr = μ_l ṁ / (2π ρ_l K t_l r). Integrate from R1 to R2, where ∫dr/r = ln(R2/R1). Hence ΔP_l = μ_l ṁ ln(R2/R1) / (2π ρ_l K t_l).\n"
    "Here t_l = 2t because there is a wick on each wall.\n\n"
    "Kozeny-Carman: treat the pores as bundled tubes with Hagen-Poiseuille flow, using the hydraulic diameter of a packed bed, ∝ ε d/(1−ε). This gives K = d²ε³/[150(1−ε)²]. With ε = 0.5, K = d²/300. Rule of thumb for sintered spheres: r_eff ≈ 0.21 d.\n\n"
    "THE 5× AND 25×\n"
    "ΔP_cap ∝ 1/d, so 50 → 10 µm gives ×5 (12.6 → 63.0 kPa). K ∝ d², so a_l goes ×25 (82 → 2055 Pa/W). The liquid-only limit goes as ΔP_cap·K ∝ d, so finer alone loses.\n\n"
    "IF ASKED\n"
    "Darcy and Kozeny-Carman are continuum models and need a wick many particles thick. A 50 µm layer of 50 µm powder is about one particle thick, so treat this case as an order-of-magnitude estimate. Contact-angle drift matters too: θ = 60° halves ΔP_cap.")
pic(s, "g2_wick.png", 0.5, 1.45, h=5.45, alt="Left: a meniscus in one pore of radius r_eff, contact angle theta, vapour above and liquid below. Right: a coarse wick is a weak pump with easy flow; a fine wick is a strong pump with hard flow.")
cx, cw = 7.95, 4.78
eq_card(s, cx, 1.45, cw, 1.22, "Pump: Young–Laplace", r"\Delta P_{cap}=\dfrac{2\sigma\cos\theta}{r_{eff}}", "cap", eh=0.72, alt="Delta P cap equals 2 sigma cos theta over r eff")
eq_card(s, cx, 2.77, cw, 1.22, "Loss: radial Darcy flow", r"\Delta P_{l}=\dfrac{\mu_l\,\dot m\,\ln(R_2/R_1)}{2\pi\rho_l K\,t_l}", "darcy", eh=0.72, alt="Delta P l equals mu l m dot ln R2 over R1, over 2 pi rho l K t l")
eq_card(s, cx, 4.09, cw, 1.22, "Permeability: Kozeny–Carman", r"K=\dfrac{d^{2}\varepsilon^{3}}{150(1-\varepsilon)^{2}},\quad r_{eff}\approx 0.21\,d", "kc", eh=0.72, alt="K equals d squared epsilon cubed over 150 times 1 minus epsilon squared; r eff is about 0.21 d")
stat(s, cx, 5.45, 2.3, f"{ratio_p:.0f}×", "pump pressure\n10 µm vs 50 µm powder", fill=cFERN, h=1.42)
stat(s, cx + 2.48, 5.45, 2.3, f"{ratio_r:.0f}×", "liquid resistance\n10 µm vs 50 µm powder", fill=cPINE, h=1.42)

# ---------------------------------------------------------------- 4 biporous
vals = list(bh.values())
s = new_slide("TOPIC 1 · BIPOROUS WICK", "Biporous wicks separate the pump from the flow path",
    head(4) +
    "HOW THE FORMULA COMES\n"
    "Start from Q_max = ΔP_cap/(a_l + a_v). In a single-pore-size wick, r_eff and K both come from the same d. A biporous wick lets each come from its own length scale:\n"
    "• ΔP_cap = 2σ/r_fine, because the smallest menisci at the evaporator set the pump.\n"
    "• a_l uses K_coarse, because the liquid takes the easiest path through the channels.\n\n"
    "THE THREE BARS (h = 100 µm, 2 × 50 µm wick, a_v = 144 Pa/W)\n"
    f"Fine: r = 5 µm, ΔP_cap = 26.5 kPa, K = 1.76e-12 m² (d = 23 µm), a_l = 389 Pa/W. Q = 26480/(389+144) = {vals[0]:.0f} W.\n"
    f"Coarse: r = 21 µm, ΔP_cap = 6.3 kPa, K = 3.33e-11 m² (d = 100 µm), a_l = 20.5 Pa/W. Q = 6305/(20.5+144) = {vals[1]:.0f} W.\n"
    f"Biporous: fine ΔP_cap with coarse K. Q = 26480/(20.5+144) = {vals[2]:.0f} W.\n\n"
    "IF ASKED\n"
    "Why an upper bound? It assumes the regions do not interfere and it borrows K from 100 µm particles, which would not fit in a 50 µm layer. Channels also take up volume and break the conduction path. The lesson is the principle, not the number.\n"
    "Be exact about the 37%: it is a simulation, it is the condenser surface peak-to-mean temperature difference, and it is relative to a monolithic wick (Patankar, Weibel and Garimella 2016). Experiments on biporous evaporator wicks: Semenic and Catton 2009.")
pic(s, "g4_biporous.png", 0.5, 1.5, w=6.3, alt="Biporous wick: clusters of fine particles give small pores and a strong pump; liquid flows easily through the coarse channels between clusters.")
cd = CategoryChartData(number_format="0"); cd.categories = ["Fine only", "Coarse only", "Biporous (ideal)"]; cd.add_series("Capillary limit (W)", [round(v) for v in vals])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(7.1), Inches(1.45), Inches(5.63), Inches(3.3), cd); gf.name = "Chart: capillary limit by wick"
ch = gf.chart; style_chart(ch, ytitle="Capillary limit (W), h = 100 µm")
pl = ch.plots[0]; pl.gap_width = 60; pl.has_data_labels = True; dl = pl.data_labels; dl.show_value = True; dl.position = XL_LABEL_POSITION.OUTSIDE_END; dl.font.size = Pt(16); dl.font.bold = True; dl.font.color.rgb = cINK
ser = pl.series[0]
for i, c in enumerate((cSAGE, cSAGE, cPINE)):
    pt = ser.points[i]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = c
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 200; ch.value_axis.major_unit = 50
eq_card(s, 7.1, 4.85, 3.1, 2.02, "Each from its own scale", r"Q_{max}=\dfrac{2\sigma/r_{fine}}{a_l(K_{coarse})+a_v}", "bip", eh=1.0, alt="Q max equals 2 sigma over r fine, over a l of K coarse plus a v")
stat(s, 10.35, 4.85, 2.38, "37%", "lower surface ΔT in a\nsimulation (Patankar 2016)", fill=cPINE, h=2.02, bigsize=40)
box(s, 0.6, 5.75, 6.2, 1.12, name="Caveat card")
tb(s, 0.85, 5.75, 5.7, 1.12, [("Upper bound, not a prediction: ", dict(bold=True, color=cPINE)), ("it assumes the fine and coarse regions do not interfere.", {})], size=16, anchor=MSO_ANCHOR.MIDDLE, name="Caveat")

# ---------------------------------------------------------------- 5 thickness
o50 = opt[S50]; oM = opt[MESH]; o10 = opt[S10]
ex = out["split_examples"]
s = new_slide("TOPIC 2 · THICKNESS OPTIMISATION", "In a fixed thickness, every wick has a best split",
    head(5) +
    "HOW THE FORMULA COMES\n"
    "1. Constraint: H = 2t + h, so h = H − 2t and dh/dt = −2.\n"
    "2. From the earlier slides, with t_l = 2t, the liquid resistance is a_l = C_l/t with C_l = μ_l ln(R2/R1)/(4π ρ_l K h_fg), and the vapour resistance is a_v = C_v/h³ with C_v = 6 μ_v ln(R2/R1)/(π ρ_v h_fg). The slide shows both in one expression, with ln(R2/R1)/(π h_fg) factored out.\n"
    "3. ΔP_cap does not depend on t, so maximum Q means minimum (a_l + a_v). Differentiate: d/dt [C_l/t + C_v/h³] = −C_l/t² + 6C_v/h⁴ = 0. (The 6 is 3 from the cube times 2 from dh/dt = −2.)\n"
    "4. Rearrange: h⁴/t² = 6C_v/C_l = 144 K (μ_v/ρ_v)/(μ_l/ρ_l). Take the root: h²/t = 12 √(K ν_v/ν_l), where ν = μ/ρ is kinematic viscosity.\n\n"
    "NUMBERS\n"
    f"Water at 60 °C: ν_v/ν_l = {nu_ratio:.0f}. For d = 50 µm, K = 8.33e-12 m²: 12√(K·{nu_ratio:.0f}) = {o50['G_um']:.0f} µm.\n"
    f"Then (250 − 2t)² = {o50['G_um']:.0f} t gives t = {o50['t_um']:.1f} µm, h = {o50['h_um']:.0f} µm. The numerical sweep agrees (50 µm).\n"
    f"All three wicks: mesh t = {oM['t_um']:.0f} µm, {oM['Q_opt']:.0f} W; 50 µm powder t = {o50['t_um']:.0f} µm, {o50['Q_opt']:.0f} W; 10 µm powder t = {o10['t_um']:.0f} µm, {o10['Q_opt']:.0f} W.\n\n"
    "WHAT IT TELLS YOU\n"
    "• The optimum does not depend on Q, σ, θ or R2/R1, only on K and the fluid. Lower K pushes the optimum to a thicker wick.\n"
    f"• At the optimum a_l/a_v = 6t/h, so the loss split is not 50:50. It is {o50['al_over_av']:.1f}:1 for the 50 µm powder.\n\n"
    "IF ASKED\n"
    f"This maximises the capillary limit only, not thermal resistance. At these ceiling loads the vapour drop is no longer small: {o50['dP_v_at_Qopt_kPa']:.1f} kPa for the 50 µm powder (about 21% of P_sat), so read the watts as trends. The closed-form derivation is mine, not from a cited paper; it was checked against the sweep.")
pic(s, "g5_split.png", 0.6, 1.8, w=5.9, alt=f"Three 250 micron stacks of the 50 micron powder: thin wick gives {ex[0]['Q']:.0f} W, best split gives {ex[1]['Q']:.0f} W, thin core gives {ex[2]['Q']:.0f} W.")
eq_card(s, 0.6, 4.95, 7.55, 1.92, "Minimise liquid + vapour resistance, with h = H − 2t", EQ_SPLIT, "split", eh=0.95, alt="a l plus a v equals ln R2 over R1 over pi h fg, times mu l over 4 rho l K t plus 6 mu v over rho v h cubed")
eq_card(s, 8.3, 4.95, 4.43, 1.92, "Optimum: set the derivative to zero", EQ_OPT, "opt", eh=0.86, alt="h squared over t equals 12 root of K nu v over nu l")
xd = XyChartData(number_format="0")
for n in (S50, S10, MESH):
    se = xd.add_series(SHORT[n])
    for t_, q_ in zip(out["sweep"]["tw_um"], out["sweep"][n]): se.add_data_point(t_, round(q_, 1))
for n in (S50, S10, MESH):
    se = xd.add_series(f"Optimum, {SHORT[n]}"); se.add_data_point(round(opt[n]["t_um"], 1), round(opt[n]["Q_opt"], 1))
gf = s.shapes.add_chart(XL_CHART_TYPE.XY_SCATTER_SMOOTH_NO_MARKERS, Inches(6.6), Inches(1.4), Inches(6.13), Inches(3.4), xd); gf.name = "Chart: capillary limit vs wick thickness"
ch = gf.chart; style_chart(ch, ytitle="Capillary limit (W)", xtitle="Each wick layer, t (µm), with h = 250 − 2t", legend=True)
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 120; ch.value_axis.major_unit = 20
ch.category_axis.minimum_scale = 10; ch.category_axis.maximum_scale = 100; ch.category_axis.major_unit = 10
sers = list(ch.plots[0].series)
for se, c, w_ in zip(sers[:3], (cPINE, cINK, cSAGE), (3.5, 2.25, 2.25)):
    se.format.line.color.rgb = c; se.format.line.width = Pt(w_); se.smooth = True; se.marker.style = XL_MARKER_STYLE.NONE
for se, c, n in zip(sers[3:], (cPINE, cINK, cSAGE), (S50, S10, MESH)):
    se.format.line.fill.background(); se.marker.style = XL_MARKER_STYLE.CIRCLE; se.marker.size = 12
    se.marker.format.fill.solid(); se.marker.format.fill.fore_color.rgb = c; se.marker.format.line.color.rgb = cINK
    dl = se.points[0].data_label; tf = dl.text_frame; tf.text = f"{opt[n]['t_um']:.0f} µm, {opt[n]['Q_opt']:.0f} W"
    tf.paragraphs[0].runs[0].font.size = Pt(13); tf.paragraphs[0].runs[0].font.bold = True; tf.paragraphs[0].runs[0].font.color.rgb = cINK
    dl.position = XL_LABEL_POSITION.ABOVE
    if n == S10:
        lbl = dl._dLbl; lay = parse_xml('<c:layout xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"><c:manualLayout><c:x val="0.075"/><c:y val="-0.05"/></c:manualLayout></c:layout>')
        lbl.insert(1, lay)
# keep the optimum markers out of the legend: they are labelled directly
leg = ch.legend._element
for i in (3, 4, 5):
    le = etree.SubElement(leg, qn("c:legendEntry")); etree.SubElement(le, qn("c:idx")).set("val", str(i)); etree.SubElement(le, qn("c:delete")).set("val", "1")
    leg.remove(le); leg.insert(1 + i - 3, le)

# ---------------------------------------------------------------- 6 vapour core
vs = out["vs_copper"]; cu = {int(v["h_um"]): v for v in vs}
s = new_slide("TOPIC 3 · VAPOUR FLOW IN A THIN CORE", "Halve the gap: 8× the drop, and copper catches up",
    head(6) +
    "HOW THE FORMULAS COME\n"
    "Plane Poiseuille flow between plates a gap h apart: the mean velocity is u = (h²/12μ)(−dP/dr), so dP/dr = −12 μ_v u / h².\n"
    "Mass conservation for radial flow: the flow area at radius r is 2π r h, so u = ṁ/(ρ_v 2π r h). Velocity falls as 1/r.\n"
    "Substitute: dP/dr = −[12 μ_v / h²]·[ṁ/(2π ρ_v r h)] = −6 μ_v ṁ / (π ρ_v h³ r).\n"
    "Integrate from R1 to R2: ΔP_v = 6 μ_v ṁ ln(R2/R1) / (π ρ_v h³).\n"
    "Where the h³ comes from: one power from velocity (u ∝ 1/h) and two from the wall shear (dP/dr ∝ u/h²). So halving h gives 2 × 4 = 8.\n\n"
    "Clausius-Clapeyron: dP/dT = h_fg/(T v_fg). With v_fg ≈ 1/ρ_v this is dP/dT = ρ_v h_fg / T. Rearranged for small drops: ΔT_sat ≈ T ΔP / (ρ_v h_fg).\n"
    "Water at 60 °C: 333.15/(0.1304 × 2.358e6) = 1.08e-3 K/Pa = 1.08 K/kPa.\n\n"
    "WORKED EXAMPLE (5 W, h = 100 µm)\n"
    f"ṁ = 5/2.358e6 = 2.12e-6 kg/s; ln(R2/R1) = ln(48/5.64) = 2.14. ΔP_v = 6(1.08e-5)(2.12e-6)(2.14)/[π(0.1304)(1e-4)³] = {vc[100]['dP_5W_Pa']:.0f} Pa, so ΔT = {vc[100]['dT_5W_K']:.2f} K.\n\n"
    "THE COPPER COMPARISON (bar chart)\n"
    "Copper sheet: a solid copper sheet of the same total thickness H = h + 2 wicks + 2 walls (80 µm each) carries the same 5 W radially from the source (R1) to the rim (R2). Heat balance Q = −k (2π r H) dT/dr gives ΔT_Cu = Q ln(R2/R1) / (2π k H), with k = 400 W/m K.\n"
    f"At h = 200 µm, H = {cu[200]['H_mm']:.2f} mm: ΔT_Cu = 5 × 2.14 / (2π × 400 × {cu[200]['H_mm']*1e-3:.5f}) = {cu[200]['cu']:.1f} K.\n"
    f"Chamber: ΔT = vapour + wick + interface. At 200 µm that is {cu[200]['vapour']:.3f} + {cu[200]['wick']:.3f} + {cu[200]['interface']:.3f} = {cu[200]['vc']:.2f} K (wick conduction from a Maxwell estimate, k about 160 W/m K; interface from kinetic theory with an assumed accommodation coefficient of 0.1).\n"
    f"Ratios, copper ÷ chamber: 400 µm {cu[400]['factor']:.0f}×, 200 µm {cu[200]['factor']:.0f}×, 100 µm {cu[100]['factor']:.0f}×, 50 µm about {cu[50]['factor']:.0f}× (trend only).\n"
    "Why it collapses: the copper sheet gets only mildly worse as it thins (H falls from 0.66 to 0.31 mm), while the chamber's vapour drop grows as 1/h³.\n\n"
    "IF ASKED\n"
    f"Validity checks at 100 µm: Mach = {vc[100]['Ma_5W']:.3f}, so incompressible. Knudsen = {vc[100]['Kn']:.4f} (mean free path {N['lambda_um']:.2f} µm), so continuum and no slip.\n"
    f"The 50 µm chamber value is marked * because its vapour pressure drop ({vc[50]['dP_5W_Pa']/1000:.1f} kPa) is above 20% of P_sat (19.95 kPa), where the linear relation stops being valid (below about {N['h_invalid_um']['5W']:.0f} µm at 5 W). Read it as a trend.\n"
    "The model assumes all vapour reaches R2. Real vapour condenses along the way, so the true drop is lower by an order-one factor. Support pillars would raise it.\n"
    "A micro heat pipe is the one-dimensional version of the same physics; this comparison uses the flat chamber geometry.")
pic(s, "g6_vapour.png", 0.5, 1.5, w=6.3, alt="Left: top view of radial vapour flow from source radius R1 to rim R2. Right: parabolic Poiseuille profile in a slit of height h; halving h doubles velocity and raises 1 over h squared four times, so the pressure gradient rises eight times.")
eq_card(s, 0.6, 4.7, 3.55, 2.17, "Radial Poiseuille flow", r"\Delta P_{v}=\dfrac{6\mu_v\dot m\ln(R_2/R_1)}{\pi\rho_v h^{3}}", "vap", eh=0.9, alt="Delta P v equals 6 mu v m dot ln R2 over R1, over pi rho v h cubed")
eq_card(s, 4.27, 4.7, 2.53, 2.17, "Clausius–Clapeyron", r"\Delta T_{sat}\approx\dfrac{T\,\Delta P}{\rho_v h_{fg}}", "cc", eh=0.9, alt="Delta T sat is about T Delta P over rho v h fg")
cd = CategoryChartData(number_format="0.0"); cd.categories = [f"{v['h_um']:.0f} µm" for v in vs]
cd.add_series("Copper sheet, same thickness", [round(v["cu"], 1) for v in vs]); cd.add_series("Vapour chamber", [round(v["vc"], 2) for v in vs])
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(7.05), Inches(1.4), Inches(5.68), Inches(4.2), cd); gf.name = "Chart: temperature drop, chamber vs copper sheet"
ch = gf.chart; style_chart(ch, ytitle="ΔT at 5 W (K)", xtitle="Vapour core thickness h", legend=True)
pl = ch.plots[0]; pl.gap_width = 55; pl.overlap = -5; pl.has_data_labels = True
dl = pl.data_labels; dl.show_value = True; dl.number_format = "0.0"; dl.number_format_is_linked = False; dl.position = XL_LABEL_POSITION.OUTSIDE_END
dl.font.size = Pt(15); dl.font.bold = True; dl.font.color.rgb = cINK
for ser_, col in zip(pl.series, (cSAGE, cPINE)): ser_.format.fill.solid(); ser_.format.fill.fore_color.rgb = col
sdl = pl.series[1].data_labels; sdl.show_value = True; sdl.number_format = "0.0"; sdl.number_format_is_linked = False; sdl.position = XL_LABEL_POSITION.OUTSIDE_END
sdl.font.size = Pt(15); sdl.font.bold = True; sdl.font.color.rgb = cINK
lab = pl.series[1].points[3].data_label; lab.text_frame.text = f"{vs[3]['vc']:.1f}*"; lab.position = XL_LABEL_POSITION.OUTSIDE_END
r_ = lab.text_frame.paragraphs[0].runs[0]; r_.font.size = Pt(15); r_.font.bold = True; r_.font.color.rgb = cINK
ch.value_axis.minimum_scale = 0; ch.value_axis.maximum_scale = 16; ch.value_axis.major_unit = 4
box(s, 7.05, 5.7, 5.68, 1.17, name="Ratio strip")
tb(s, 7.25, 5.77, 5.3, 0.3, "Copper ÷ chamber: same thickness, source and rim", size=14, bold=True, color=cPINE)
for i, v in enumerate(vs):
    txt = f"{v['factor']:.0f}×" if v["h_um"] >= 100 else f"≈{v['factor']:.0f}×*"
    tb(s, 7.2 + i * 1.36, 6.1, 1.3, 0.42, txt, size=22, bold=True, color=cPINE, align=PP_ALIGN.CENTER, font=HEAD_FONT)
    tb(s, 7.2 + i * 1.36, 6.5, 1.3, 0.28, f"{v['h_um']:.0f} µm" + ("  *trend" if v["h_um"] < 60 else ""), size=12, color=cINK, align=PP_ALIGN.CENTER)

# ---------------------------------------------------------------- 7 references
s = prs.slides.add_slide(DARK); s.shapes.title.text = "Three results, and where they come from"
tb(s, 0.6, 0.3, 11, 0.3, "REFERENCES", size=14, bold=True, color=cSAGE, name="Section label")
for i, (t, b) in enumerate((("Wick", "One length sets pump and resistance; biporous wicks separate them"),
                            ("Thickness", "h²/t = 12√(K νᵥ/νₗ) gives the best split"),
                            ("Vapour", "ΔPᵥ ∝ 1/h³, so thin cores become the bottleneck"))):
    y = 1.65 + i * 1.65
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.6), Inches(y), Inches(0.62), Inches(0.62)); c.fill.solid(); c.fill.fore_color.rgb = cSAGE; c.line.fill.background(); c.shadow.inherit = False; c.name = f"Badge {i+1}"
    c.text_frame.text = str(i + 1); pp = c.text_frame.paragraphs[0]; pp.alignment = PP_ALIGN.CENTER; pp.runs[0].font.size = Pt(20); pp.runs[0].font.bold = True; pp.runs[0].font.color.rgb = cINK
    c.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE; c.text_frame.margin_left = c.text_frame.margin_right = c.text_frame.margin_top = c.text_frame.margin_bottom = 0
    tb(s, 1.42, y - 0.03, 3.9, 0.4, t, size=20, bold=True, color=cSAGE, font=HEAD_FONT)
    tb(s, 1.42, y + 0.37, 3.9, 0.9, b, size=16, color=cWHITE)
refs = ("DasGupta & Ganguly. Microscale Transport Processes, course notes, IIT Kharagpur.",
        "Faghri (2012). Review and advances in heat pipe science and technology. J. Heat Transfer 134(12), 123001.",
        "Weibel & Garimella (2013). Recent advances in vapor chamber transport characterization. Adv. Heat Transfer 45, 209–301.",
        "Semenic & Catton (2009). Experimental study of biporous wicks for high heat flux applications. IJHMT 52, 5113–5121.",
        "Patankar, Weibel & Garimella (2016). Patterning the condenser-side wick in ultra-thin vapor chamber heat spreaders. IJHMT 101, 927–936.",
        "Peterson (1994). An Introduction to Heat Pipes: Modeling, Testing, and Applications. Wiley.",
        "Faghri (1995). Heat Pipe Science and Technology. Taylor & Francis.")
sb = s.shapes.add_textbox(Inches(5.75), Inches(1.6), Inches(6.98), Inches(4.5)); sb.name = "Reference list"; tf = sb.text_frame; tf.word_wrap = True
tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
for i, r_ in enumerate(refs):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); p.space_after = Pt(9)
    ru = p.add_run(); ru.text = r_; ru.font.size = Pt(14); ru.font.color.rgb = cMIST
tb(s, 5.75, 6.3, 6.98, 0.5, "Calculated values are illustrative (water at 60 °C, disc geometry). Full list in the term paper.", size=12, italic=True, color=cSAGE, name="Note")
s.notes_slide.notes_text_frame.text = (head(7) + f"The whole script runs about {clock(running()[-1])} at 150 words a minute, which leaves a margin inside 3:00. "
    "If you run over, drop the 37% sentence on the biporous slide first, then the saturated-vapour sentence on the vapour slide.")

prs.save(OUT); print("saved", OUT, len(prs.slides._sldIdLst), "slides")
