"""Builds Presentation_Micro_Heat_Pipes_and_Vapour_Chambers.pptx (python-pptx). Numbers come from numbers.json."""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image as PILImage
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, ".."); FIG = os.path.join(ROOT, "figures")
N = json.load(open(os.path.join(HERE, "numbers.json")))
OUT = os.path.join(ROOT, "Presentation_Micro_Heat_Pipes_and_Vapour_Chambers.pptx")
EQD = os.path.join(HERE, "eq_slides"); os.makedirs(EQD, exist_ok=True)

NAVY = RGBColor(0x1F, 0x3A, 0x5F); GREY = RGBColor(0x55, 0x55, 0x55); INK = RGBColor(0x22, 0x22, 0x22)
BLUE = RGBColor(0x00, 0x72, 0xB2); ORANGE = RGBColor(0xD5, 0x5E, 0x00); GREEN = RGBColor(0x00, 0x9E, 0x73)
LIGHT = RGBColor(0xEE, 0xF3, 0xF8); AMBER = RGBColor(0xFF, 0xF6, 0xE0); WHITE = RGBColor(255, 255, 255)

prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
vc = {int(r["h_um"]): r for r in N["vapour_core"]}; cl = N["cap_limit"]; wk = N["wicks"]; cp = N["coupling"]; bp = N["biporous"]
mesh, s50, s10 = "Cu mesh (#200)", "Sintered, d = 50 um", "Sintered, d = 10 um"
_n = [0]

def tb(slide, x, y, w, h, text="", size=18, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font="Calibri"):
    s = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = s.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = Inches(0.03)
    p = tf.paragraphs[0]; r = p.add_run(); r.text = text; r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
    p.alignment = align
    return s

def bullets(slide, x, y, w, h, items, size=18, gap=8):
    s = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h)); tf = s.text_frame; tf.word_wrap = True
    first = True
    for it in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        if isinstance(it, tuple): head, body = it
        else: head, body = None, it
        p.space_after = Pt(gap)
        r0 = p.add_run(); r0.text = "• "; r0.font.size = Pt(size); r0.font.color.rgb = BLUE; r0.font.bold = True; r0.font.name = "Calibri"
        if head:
            r1 = p.add_run(); r1.text = head + " "; r1.font.bold = True; r1.font.size = Pt(size); r1.font.color.rgb = NAVY; r1.font.name = "Calibri"
        r2 = p.add_run(); r2.text = body; r2.font.size = Pt(size); r2.font.color.rgb = INK; r2.font.name = "Calibri"
    return s

def new_slide(title, notes, subtitle=None):
    s = prs.slides.add_slide(BLANK); _n[0] += 1
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.12)); bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    tb(s, 0.55, 0.3, 12.2, 0.95, title, size=28, bold=True, color=NAVY, anchor=MSO_ANCHOR.MIDDLE)
    if subtitle: tb(s, 0.55, 1.2, 12.2, 0.4, subtitle, size=16, color=GREY)
    tb(s, 0.55, 7.05, 9.5, 0.3, "Debanshu Ghosh · 23CH3FP56 · Chemical Engineering, IIT Kharagpur", size=10, color=GREY)
    tb(s, 12.2, 7.05, 0.6, 0.3, str(_n[0]), size=10, color=GREY, align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = notes
    return s

def pic(slide, name, x, y, w=None, h=None):
    path = os.path.join(FIG, name); iw, ih = PILImage.open(path).size
    if w and not h: h = w * ih / iw
    if h and not w: w = h * iw / ih
    if w and h and (w / h) > (iw / ih): w = h * iw / ih
    elif w and h: h = w * ih / iw
    return slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))

def eqpng(tex, name, fs=26):
    path = os.path.join(EQD, name + ".png")
    fig = plt.figure(figsize=(0.01, 0.01)); fig.text(0, 0, f"${tex}$", fontsize=fs, family="DejaVu Serif")
    fig.savefig(path, dpi=250, bbox_inches="tight", pad_inches=0.05, transparent=True); plt.close(fig)
    return path

def eq(slide, tex, name, x, y, h=0.9, fs=26, center_w=None):
    path = eqpng(tex, name, fs); iw, ih = PILImage.open(path).size; w = h * iw / ih
    if center_w: x = x + (center_w - w) / 2
    slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))

def card(slide, x, y, w, h, title, body, fill=LIGHT, tsize=16, bsize=14):
    r = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    r.fill.solid(); r.fill.fore_color.rgb = fill; r.line.color.rgb = RGBColor(0xB8, 0xC4, 0xD2); r.adjustments[0] = 0.06
    tb(slide, x + 0.1, y + 0.05, w - 0.2, 0.45, title, size=tsize, bold=True, color=NAVY)
    tb(slide, x + 0.1, y + 0.5, w - 0.2, h - 0.55, body, size=bsize, color=INK)

# ---------------------------------------------------------------- 1 title
s = prs.slides.add_slide(BLANK); _n[0] += 1
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height); bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
tb(s, 0.9, 0.9, 11.5, 0.4, "MICROSCALE TRANSPORT PROCESSES · TERM PAPER", size=14, bold=True, color=RGBColor(0xBF, 0xD4, 0xEA))
tb(s, 0.9, 1.7, 11.6, 2.2, "Micro Heat Pipes and Vapour Chambers for Smartphone and Chip Cooling", size=44, bold=True, color=WHITE)
tb(s, 0.9, 4.0, 11.5, 0.9, "A critical look at capillary-driven two-phase heat transport: the science, the simplifications, where they fail", size=20, color=RGBColor(0xDD, 0xE6, 0xF0))
tb(s, 0.9, 5.4, 11.5, 0.45, "Debanshu Ghosh · Roll No. 23CH3FP56", size=20, bold=True, color=WHITE)
tb(s, 0.9, 5.9, 11.5, 0.45, "Department of Chemical Engineering, IIT Kharagpur", size=18, color=RGBColor(0xDD, 0xE6, 0xF0))
s.notes_slide.notes_text_frame.text = ("Introduce yourself and the topic in one sentence: this talk is about how a sheet of water and copper thinner than a coin spreads heat in a phone, "
                                       "and what the physics of that tells us about transport at the microscale. Say that the focus is the science, not products. About 30 seconds.")

# ---------------------------------------------------------------- 2 problem
s = new_slide("A phone is limited by skin temperature, not by the chip",
              "Bhat et al. measured a Nexus 6P. The thermal governor cut performance by up to 34% in popular apps, about 12 frames per second in one game; without throttling the package reached about 50 C. "
              "The point: the heat is made in a few square millimetres but must leave through the whole back of a sealed, fanless phone. So the task is spreading heat sideways, fast, in a body under a millimetre thick. "
              "Pumped microchannel cooling (Tuckerman and Pease) works but needs a pump; plain copper cannot spread enough when it is this thin. That is the gap vapour chambers fill. (Source: Bhat et al. 2019, DATE; Garimella et al. 2008.)")
for i, (big, small, col) in enumerate((("up to 34%", "performance lost to thermal throttling in popular apps", ORANGE), ("≈ 12 fps", "frame-rate penalty in one game on the same phone", ORANGE), ("≈ 50 °C", "package temperature reached when throttling was switched off", BLUE))):
    x = 0.7 + i * 4.1
    r = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.7), Inches(3.8), Inches(2.5)); r.fill.solid(); r.fill.fore_color.rgb = LIGHT; r.line.fill.background(); r.adjustments[0] = 0.08
    tb(s, x + 0.1, 1.85, 3.6, 1.0, big, size=44, bold=True, color=col, align=PP_ALIGN.CENTER)
    tb(s, x + 0.2, 3.0, 3.4, 1.1, small, size=16, color=INK, align=PP_ALIGN.CENTER)
tb(s, 0.7, 4.35, 12, 0.35, "Measured on a Nexus 6P (Bhat et al., DATE 2019)", size=13, color=GREY)
bullets(s, 0.7, 4.85, 12, 2.1, [("Heat made here:", "a few mm² of silicon. Heat leaves through: the whole back of a sealed, fanless phone."),
                                 ("So the real job is:", "spread heat sideways, quickly, in a sheet under ~1 mm thick, with no moving parts.")], size=20)

# ---------------------------------------------------------------- 3 idea
s = new_slide("Idea: carry heat as latent heat in a sealed loop of water and vapour",
              "Walk through the four numbered steps. Evaporation at the hot spot, vapour flows outward through the thin core, condensation at the cool region, liquid returns through the wick by capillary suction. "
              "Because each kilogram of water carries 2.36 MJ, a mass flow of only about 2 milligrams per second moves 5 W. No pump: the wick itself is the pump. A micro heat pipe is the one-dimensional version; the vapour chamber is the flat two-dimensional one.")
pic(s, "f1_cycle.png", 0.6, 1.6, w=8.3)
bullets(s, 9.1, 1.75, 3.9, 4.8, [("1", "water evaporates at the hot spot"), ("2", "vapour flows through the thin core"), ("3", "it condenses where it is cooler"), ("4", "liquid returns through the wick, driven by capillary suction"),
                                  ("Numbers:", f"2.36 MJ per kg, so 5 W needs only {N['mdot_5W_kg_s']*1e6:.1f} mg/s")], size=17, gap=10)

# ---------------------------------------------------------------- 4 capillary
s = new_slide("Smaller pores pump harder, and gravity stops mattering",
              "Young-Laplace: a meniscus in a pore of radius r supports a pressure difference of 2 sigma cos theta over r. Pressure grows as 1/r. For water at 60 C, a 64 micron mesh pore gives about 2 kPa, a 10 micron pore about 13 kPa, a 1 micron pore about 130 kPa. "
              "The Bond number rho g h squared over sigma is 0.15 at 1 mm and 0.006 at 200 microns, so gravity cannot rearrange liquid inside the sheet. Gravity still acts over the length: lifting water 100 mm costs 0.96 kPa, which fine wicks cover easily and coarse mesh only with about a factor of two to spare. "
              "Assumptions: spherical meniscus, constant contact angle, uniform pores, pure liquid.")
eq(s, r"\Delta P_{cap}=\dfrac{2\,\sigma\cos\theta}{r_{eff}}", "e_cap", 0.8, 1.6, h=1.0, fs=28, center_w=5.4)
bullets(s, 0.7, 3.0, 5.8, 3.8, [("Pressure ∝ 1/r:", f"64 µm pore → {wk[mesh]['p_cap_kPa']:.1f} kPa; 10 µm → 13 kPa; 1 µm → 130 kPa"),
                                 ("Bond number:", f"{N['Bo']['200um']:.4f} at 200 µm, so gravity is negligible inside the sheet"),
                                 ("But over the length:", f"lifting 100 mm costs {N['head_100mm_kPa']:.2f} kPa; coarse mesh keeps only ~2× margin")], size=20, gap=14)
pic(s, "f2_capillary_pressure.png", 6.7, 1.6, w=6.2)

# ---------------------------------------------------------------- 5 budget
s = new_slide("One idea organises everything: the pressure budget",
              "The capillary pump must beat every loss: liquid flow in the wick (Darcy), vapour flow in the core (Poiseuille) and gravity. Both flow losses scale with the heat load Q, so the budget gives a maximum heat load, the capillary limit. "
              "To raise it you can raise the pump pressure with finer pores, lower the liquid resistance with bigger more permeable pores, or lower the vapour resistance with a thicker core. These demands conflict. The next slides take each term in turn.")
eq(s, r"\Delta P_{cap}\;\geq\;\Delta P_{l}+\Delta P_{v}+\Delta P_{g}", "e_budget", 0.7, 1.55, h=0.85, fs=28, center_w=12)
eq(s, r"Q_{max}=\dfrac{\Delta P_{cap}-\rho_l\,g\,\Delta z}{a_l+a_v}", "e_qmax", 0.7, 2.55, h=1.15, fs=28, center_w=12)
for i, (t, b, col) in enumerate((("ΔP_cap: the pump", "set by pore size and wetting (slide 4)", GREEN), ("a_l: liquid resistance", "set by wick permeability and thickness (slides 6–7)", BLUE), ("a_v: vapour resistance", "set by core thickness, grows as 1/h³ (slide 8)", ORANGE))):
    card(s, 0.7 + i * 4.1, 4.2, 3.9, 2.0, t, b, tsize=20, bsize=19)
tb(s, 0.7, 6.3, 12, 0.5, "Interface losses appear as a temperature jump, not a pressure drop (slide 9).", size=16, color=GREY)

# ---------------------------------------------------------------- 6 wick trade-off
s = new_slide("The wick is a trade-off: finer pores pump harder but resist flow more",
              f"Pressure goes as 1 over d, permeability as d squared (Kozeny-Carman). Going from 50 micron powder to 10 micron powder gives 5 times the pump pressure but 25 times the liquid resistance. "
              f"So the fine wick is liquid-limited: about {cl[s10]['100um']['horizontal_W']:.0f} W whatever the core thickness, while the 50 micron powder reaches {cl[s50]['100um']['horizontal_W']:.0f} W at a 100 micron core. "
              "Excess pump pressure is wasted: the best wick is the coarsest one that leaves enough margin. Assumptions: rigid uniform isotropic wick, constant contact angle, no vapour-liquid shear. Real wicks have pore-size distributions and partial dry-out.")
pic(s, "f3_wick_tradeoff.png", 0.5, 1.5, w=6.9)
rows = [("Wick", "r (µm)", "ΔP_cap (kPa)", "a_l (Pa/W)"), ("Cu mesh #200", f"{wk[mesh]['r_um']:.0f}", f"{wk[mesh]['p_cap_kPa']:.1f}", f"{wk[mesh]['a_l_Pa_per_W']:.0f}"),
        ("Sintered 50 µm", f"{wk[s50]['r_um']:.1f}", f"{wk[s50]['p_cap_kPa']:.1f}", f"{wk[s50]['a_l_Pa_per_W']:.0f}"), ("Sintered 10 µm", f"{wk[s10]['r_um']:.1f}", f"{wk[s10]['p_cap_kPa']:.1f}", f"{wk[s10]['a_l_Pa_per_W']:.0f}")]
t = s.shapes.add_table(4, 4, Inches(7.6), Inches(1.7), Inches(5.3), Inches(2.0)).table
for r_, row in enumerate(rows):
    for c_, v in enumerate(row):
        cell = t.cell(r_, c_); cell.text = v; p = cell.text_frame.paragraphs[0]; p.runs[0].font.size = Pt(15); p.runs[0].font.name = "Calibri"; p.runs[0].font.bold = (r_ == 0)
        cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT if r_ == 0 else WHITE; p.runs[0].font.color.rgb = INK
bullets(s, 7.6, 4.0, 5.3, 2.9, [("5×", "pump pressure for 10 µm vs 50 µm"), ("25×", "liquid resistance for the same change"), ("So:", "excess pump pressure is wasted; choose the coarsest wick with enough margin")], size=19, gap=8)

# ---------------------------------------------------------------- 7 biporous + optimum
s = new_slide("Escaping the trade-off: biporous wicks and an optimal wick thickness",
              f"A biporous wick has fine pores for pumping pressure and coarse channels for flow; Semenic and Catton studied them experimentally. In my idealised calculation the capillary limit rises from about {list(bp['horizontal'].values())[0]:.0f} W (fine) or {list(bp['horizontal'].values())[1]:.0f} W (coarse) to about {list(bp['horizontal'].values())[2]:.0f} W. "
              "This is an upper bound: it assumes the two regions do not interfere, which they do in real structures. The lesson is the idea: separate the length scale that sets pressure from the one that sets flow. "
              f"Right: if the inner thickness is fixed at {N['coupling_H_in_um']:.0f} microns, every micron of wick is taken from the vapour core, so there is an optimum wick thickness, {cp[s50]['tw_opt_um']:.0f} microns per layer for the 50 micron powder in this model, and it depends on the wick.")
pic(s, "f8_biporous.png", 0.4, 1.7, w=6.5)
pic(s, "f9_coupling.png", 7.0, 1.6, w=6.0)
tb(s, 0.5, 4.8, 6.4, 1.0, "Biporous (ideal upper bound): fine pores set the pressure, coarse channels set the flow.", size=17, color=INK)
tb(s, 7.1, 5.2, 5.9, 1.0, "Wick and vapour core share a fixed thickness, so each wick has an optimum split.", size=17, color=INK)
tb(s, 0.5, 6.2, 12.3, 0.7, "Caveat: the biporous bar assumes fine and coarse regions do not interfere; real structures lose some of the gain.", size=16, color=GREY)

# ---------------------------------------------------------------- 8 vapour core
s = new_slide("Thin vapour cores: the pressure drop grows as 1/h³",
              f"Radial Poiseuille flow in a slit gives delta P v equals 6 mu m-dot ln(R2/R1) over pi rho v h cubed. Halving the thickness makes the core exactly {N['ratio_halving']:.0f} times more resistive. "
              "A vapour pressure drop matters because in saturated vapour pressure and temperature are tied: Clausius-Clapeyron gives about 1.1 K per kilopascal for water at 60 C. "
              f"At a 200 micron core, 5 W costs about {vc[200]['dT_5W_K']:.2f} K; at 100 microns {vc[100]['dT_5W_K']:.2f} K; at 50 microns the model gives about {vc[50]['dT_5W_K']:.0f} K but that is beyond its validity range. "
              "Patankar et al. found that at ultra-thin sizes the vapour core limits performance, and a biporous condenser wick that allows a thicker core cut the peak-to-mean skin temperature difference by 37% in their simulation. "
              f"Checks: Mach number only {vc[100]['Ma_5W']:.2f} so incompressible; Knudsen number {vc[100]['Kn']:.3f} in the core so continuum; but about {N['Kn_pore_1um']:.1f} inside 1 micron pores.")
eq(s, r"\Delta P_{v}=\dfrac{6\,\mu_v\,\dot m\,\ln(R_2/R_1)}{\pi\,\rho_v\,h^{3}}", "e_vap", 0.5, 1.55, h=1.1, fs=26, center_w=6.3)
pic(s, "f4_vapour_core.png", 6.9, 1.5, w=6.0)
bullets(s, 0.6, 3.0, 6.1, 3.9, [("Halve h:", f"core becomes exactly {N['ratio_halving']:.0f}× more resistive"),
                                 ("Pressure → temperature:", "about 1.1 K per kPa (Clausius–Clapeyron)"),
                                 ("At 5 W:", f"{vc[200]['dT_5W_K']:.2f} K at 200 µm, {vc[100]['dT_5W_K']:.2f} K at 100 µm"),
                                 ("Literature:", "a biporous condenser wick allowing a thicker core cut skin ΔT by 37% (Patankar 2016)")], size=19, gap=10)

# ---------------------------------------------------------------- 9 interface
s = new_slide("At the interface the physics is uncertain by orders of magnitude",
              "Kinetic theory gives the evaporation flux in terms of molecules striking and leaving the surface, scaled by an accommodation coefficient between 0 and 1. For a coefficient of 1 the interface is almost free, 4.4 MW per square metre kelvin. "
              "But measured values for water scatter widely (Marek and Straub), roughly 0.01 to 1. For 5 W on 1 square centimetre the temperature jump is about 11 millikelvin at 1 and 2 kelvin at 0.01, 23 kelvin in the extreme case 0.001. "
              "So whether the interface matters in a phone-thin chamber depends on a number the community has not pinned down. Going deeper: heat enters mostly in thin film regions near the contact line (Wayner), where k over delta is large: 650 kW per square metre kelvin at 1 micron, 6.5 at 100 microns. "
              "Note that I took the flux over the whole source area, which overstates the jump.")
pic(s, "f5_interface.png", 0.5, 1.6, w=7.3)
bullets(s, 8.0, 1.8, 5.0, 4.8, [("Accommodation coeff. = 1:", f"interface almost free ({N['h_interface']['1.0']/1e6:.1f} MW/m²K)"),
                                 ("Measured values scatter:", "roughly 0.01 to 1 for water (Marek & Straub)"),
                                 ("Effect at 5 W/cm²:", f"{N['dT_interface_5W']['1.0']*1000:.0f} mK at 1, {N['dT_interface_5W']['0.01']:.1f} K at 0.01"),
                                 ("Where heat enters:", "thin liquid films near the contact line, k/δ is large")], size=20, gap=12)

# ---------------------------------------------------------------- 10 limits
s = new_slide("Operating limits: which quantity runs out first?",
              f"Five classical limits: capillary, sonic, entrainment, boiling, viscous. The figure shows the first two from the model. Thick cores: the wick sets the limit, coarse powder near 150 W, mesh near 80 W, fine powder near 30 W. "
              f"Thin cores: the vapour sets it; the powder gives {cl[s50]['100um']['horizontal_W']:.0f} W at 100 microns and only {cl[s50]['50um']['horizontal_W']:.0f} W at 50 microns, just above a 5 W load. "
              f"Gravity mostly hurts the coarse mesh: {cl[mesh]['100um']['horizontal_W']:.0f} W falls to {cl[mesh]['100um']['vertical_W']:.1f} W with the source on top. The sonic limit is well above for a phone. "
              "What the model cannot see: local dry-out under the hot spot, entrainment, boiling. Yan et al. measured up to 60 W for a 0.5 mm chamber; Weibel et al. found 600 to 1200 micron sintered wicks handled over 500 W per square centimetre locally without dry-out, but those are much thicker. "
              "The closeness of my 56 W to 60 W is a coincidence of order of magnitude, not validation.")
pic(s, "f6_limits.png", 0.4, 1.6, w=7.6)
bullets(s, 8.2, 1.7, 4.8, 5.0, [("Thick core:", "the wick sets the limit (~150 W, 80 W, 30 W)"), ("Thin core:", "the vapour sets it, so Q_max falls fast below ~100 µm"),
                                 ("Gravity:", "hurts coarse mesh most"), ("Not in the model:", "local dry-out, entrainment, boiling"), ("Experiment:", "up to 60 W for a 0.5 mm chamber (Yan 2023)")], size=18, gap=9)

# ---------------------------------------------------------------- 11 keff
s = new_slide("‘Effective thermal conductivity’ is not a property",
              "Chambers are rated by an effective conductivity, defined by comparing the temperature drop to a solid conductor. But the geometry used in the definition changes the number: from the same temperature drop, the radial definition gives 11 thousand W per metre kelvin at 200 microns and the strip definition 125 thousand, a factor of 11. "
              "It also falls as the core thins, and in experiments it depends on load and orientation. Zhang et al. report 3473 to 3837 W/mK for a 0.39 mm chamber; Yan et al. 11,817 W/mK at 50 W against gravity for a 0.5 mm chamber. These devices differ, so the numbers are not interchangeable without checking definitions. "
              "Zhang also found k_eff fell as support column diameter increased: pillars stiffen the shell but block vapour.")
pic(s, "f7_keff.png", 0.4, 1.6, w=7.2)
bullets(s, 7.8, 1.8, 5.2, 4.9, [("Same data, two definitions:", f"× {N['keff'][3]['keff_strip']/N['keff'][3]['keff_radial']:.0f} difference"), ("Not a material property:", "falls as the core thins; varies with load and orientation"),
                                 ("Reported:", "3473–3837 W/m K (0.39 mm, Zhang 2024) vs 11,817 W/m K (0.5 mm, 50 W, anti-gravity, Yan 2023)"), ("Rule:", "compare only with the same definition, load and orientation")], size=19, gap=12)

# ---------------------------------------------------------------- 12 models
s = new_slide("Models: each one hides something",
              "Four model families. A resistance network is cheap and good for sizing but treats the vapour as isothermal and cannot see dry-out. Analytical 1-D or 2-D flow models, like the one in this paper, explain trends but ignore pillars, non-uniform condensation and transients. "
              "3-D continuum porous-medium models like Vadakkan et al. predict hot-spot maps but depend on effective K, k_eff and the accommodation coefficient, rarely known independently. Microstructure-aware models like Ranjan et al. put particle size and packing into the model, but are costly and idealised. "
              "Message: the cheaper models are not worse, only more limited. Also note my own model's limits: single temperature, disc geometry, full wetting, linear Clausius-Clapeyron valid only for pressure drops under about 20% of saturation pressure, steady state, no gas, no pillars.")
rows = [("Model", "Assumes", "Hides / fails when"),
        ("Resistance network (Prasher)", "lumped stages; vapour ~ isothermal", "pressure loss, dry-out; thin cores, high loads"),
        ("Analytical 1-D / 2-D (this paper)", "laminar, uniform wick, all vapour to rim", "pillars, transients, fine wicks (Kn)"),
        ("3-D porous continuum (Vadakkan)", "effective K, k_eff, one interface coefficient", "depends on poorly known inputs"),
        ("Microstructure-aware (Ranjan)", "particle size / packing explicit", "cost; idealised packings, contact angle")]
t = s.shapes.add_table(5, 3, Inches(0.7), Inches(1.7), Inches(11.9), Inches(3.3)).table
t.columns[0].width = Inches(3.7); t.columns[1].width = Inches(4.1); t.columns[2].width = Inches(4.1)
for r_, row in enumerate(rows):
    for c_, v in enumerate(row):
        cell = t.cell(r_, c_); cell.text = v; p = cell.text_frame.paragraphs[0]; p.runs[0].font.size = Pt(16); p.runs[0].font.name = "Calibri"; p.runs[0].font.bold = (r_ == 0)
        cell.fill.solid(); cell.fill.fore_color.rgb = LIGHT if r_ == 0 else WHITE; p.runs[0].font.color.rgb = INK
card(s, 0.7, 5.3, 11.9, 1.5, "This paper's own model: assumptions to keep in mind", "single temperature (60 °C) · disc geometry, all vapour to the rim · full wetting (θ = 0) · linear Clausius–Clapeyron (valid only while ΔP < 20% of P_sat) · steady state · no gas, no pillars", fill=AMBER, tsize=17, bsize=15)

# ---------------------------------------------------------------- 13 fabrication + reliability
s = new_slide("Fabrication sets the physics; reliability limits the life",
              "Lectures 2 and 3 covered the fabrication routes themselves; here only what each route fixes for transport. Powder fixes particle size so pore radius and permeability; mesh fixes wire diameter; etched grooves give well-defined directional permeability; nanostructures raise pressure and wetting but age; bonding fixes hermeticity and gas level; pillars stiffen the shell but obstruct the vapour. "
              "Reliability: copper and water are compatible; aluminium and water make hydrogen. Non-condensable gas collects at the condenser and shuts off area. A contact angle drift from 0 to 60 degrees halves the pump pressure. Fouling is the Lecture 4 mechanism, here hitting the pump pressure. "
              "Water at 60 C is about 20 kPa, below atmospheric, so the shell relies on pillars; freezing expands water by about 9%. In the sources I used, lifetime data are scarcer than steady-state performance data.")
card(s, 0.7, 1.6, 5.9, 5.1, "How the process sets the physics", "Powder: particle size → r_eff, K\nMesh: wire diameter → coarse r_eff, thin\nGrooves: width, depth → directional K\nNanostructures: wetting, small r (age!)\nBonding: hermetic seal, gas level\nPillars: stiffness, but block the vapour", tsize=22, bsize=22)
card(s, 6.8, 1.6, 5.9, 5.1, "What limits the life", "Non-condensable gas at the condenser\nContact-angle drift: 0° → 60° halves the pump pressure\nFouling of the finest pores (Lecture 4 mechanism)\nCu–water compatible; Al–water makes H₂\nSealed at ~20 kPa, below atmosphere → pillars\nFreezing: ≈ 9% volume expansion", fill=AMBER, tsize=22, bsize=22)

# ---------------------------------------------------------------- 14 synthesis
s = new_slide("What is solid, what is argued over, what is open",
              "Established: the pressure budget picture, the wick trade-off, the dominance of the vapour core in ultra-thin sheets, and the benefit of biporous and patterned wicks. Argued over: the accommodation coefficient and the interface, comparability of reported performance, how well simple models predict absolute limits, and long-term behaviour. "
              "Limits of this review: one fluid, one geometry, steady state, illustrative numbers, textbook correlations used at face value.")
card(s, 0.7, 1.6, 3.9, 5.0, "Well established", "• capillary pressure vs flow resistance sets every wick\n• vapour core ∝ 1/h³ dominates ultra-thin sheets\n• biporous / patterned wicks help (experiment and simulation)", fill=RGBColor(0xE6, 0xF4, 0xEE), tsize=22, bsize=20)
card(s, 4.7, 1.6, 3.9, 5.0, "Still argued over", "• accommodation coefficient and interface resistance\n• comparability of k_eff and ‘maximum power’\n• how well simple models predict absolute limits\n• lifetime behaviour", fill=AMBER, tsize=22, bsize=20)
card(s, 8.7, 1.6, 3.9, 5.0, "Limits of this review", "• one fluid, one geometry, steady state\n• illustrative numbers, not design values\n• textbook correlations used at face value", fill=LIGHT, tsize=22, bsize=20)

# ---------------------------------------------------------------- 15 conclusions
s = new_slide("Conclusions",
              "Close by repeating the three ideas the listener should keep: the pressure budget, the two trade-offs, and the 1 over h cubed law. Then the honest message: the field has a good first-order picture of why thin vapour chambers work, and weaker tools for predicting exactly how well and for how long. "
              "Key sources: Faghri 2012 and Weibel and Garimella 2013 for the review base, Bhat 2019 for the problem, Patankar 2016 for the vapour-core result, Semenic and Catton 2009 for biporous wicks, Marek and Straub 2001 for the interface. Thank the audience and invite questions.")
bullets(s, 0.7, 1.55, 12.0, 4.2, [("Pressure budget:", "capillary pressure must beat wick + vapour + gravity losses"),
                                   ("Two trade-offs:", "pump pressure vs permeability, and wick thickness vs vapour-core height"),
                                   ("Inverse-cube law:", f"halving the core makes it {N['ratio_halving']:.0f}× more resistive, so ultra-thin chambers are vapour-limited"),
                                   ("Open problems:", "the interface, standard performance metrics, long-term wetting")], size=21, gap=14)
tb(s, 0.7, 5.35, 12, 0.35, "Key sources", size=14, bold=True, color=NAVY)
tb(s, 0.7, 5.7, 12, 1.2, "Bhat et al. 2019 (DATE) · Faghri 2012 (J. Heat Transfer) · Weibel & Garimella 2013 · Patankar et al. 2016 · Semenic & Catton 2009 · Marek & Straub 2001 · Yan et al. 2023 · Zhang et al. 2024. Full list of 26 references in the term paper.", size=14, color=GREY)

prs.save(OUT); print("saved", OUT, len(prs.slides._sldIdLst), "slides")
