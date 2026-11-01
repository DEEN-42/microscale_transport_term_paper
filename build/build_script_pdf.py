"""Builds Speaking_Script_3min_Micro_Heat_Pipes_and_Vapour_Chambers.pdf: the words to say for each slide, what to point at,
the formulas in plain words, and likely questions. The spoken text comes from talk_script.py, the same source as the deck's speaker notes.
Run after focused_model.py:  python -X utf8 build_script_pdf.py"""
import os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image, Table, TableStyle,
                                KeepTogether, CondPageBreak, PageBreak)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from talk_script import *
from talk_script import _bar, _cu, _o50

ROOT = os.path.join(HERE, ".."); OUT = os.path.join(ROOT, "Speaking_Script_3min_Micro_Heat_Pipes_and_Vapour_Chambers.pdf")
EQD = os.path.join(HERE, "eq_script"); os.makedirs(EQD, exist_ok=True)

fd = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
for nm, fn in (("Serif", "DejaVuSerif.ttf"), ("Serif-B", "DejaVuSerif-Bold.ttf"), ("Serif-I", "DejaVuSerif-Italic.ttf"),
               ("Serif-BI", "DejaVuSerif-BoldItalic.ttf"), ("Sans", "DejaVuSans.ttf"), ("Sans-B", "DejaVuSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(nm, os.path.join(fd, fn)))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-BI")
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")

PINEc, FERNc, SAGEc, INKc, TINTc, MISTc = (colors.HexColor(x) for x in (PINE, FERN, SAGE, INK, TINT, MIST))
S = dict(
    title=ParagraphStyle("title", fontName="Sans-B", fontSize=21, leading=26, textColor=PINEc, spaceAfter=4),
    sub=ParagraphStyle("sub", fontName="Serif-I", fontSize=11, leading=15, textColor=INKc, spaceAfter=8),
    h=ParagraphStyle("h", fontName="Sans-B", fontSize=12.5, leading=16, textColor=colors.white),
    lab=ParagraphStyle("lab", fontName="Sans-B", fontSize=8.5, leading=11, textColor=FERNc, spaceBefore=8, spaceAfter=3),
    say=ParagraphStyle("say", fontName="Serif", fontSize=13.5, leading=21, textColor=INKc),
    body=ParagraphStyle("body", fontName="Serif", fontSize=10, leading=14.2, textColor=INKc, spaceAfter=3),
    bul=ParagraphStyle("bul", fontName="Serif", fontSize=10, leading=14, leftIndent=14, bulletIndent=2, spaceAfter=3, textColor=INKc),
    cell=ParagraphStyle("cell", fontName="Serif", fontSize=9.5, leading=12.5, textColor=INKc),
    cellb=ParagraphStyle("cellb", fontName="Serif-B", fontSize=9.5, leading=12.5, textColor=INKc),
)
def fmt(t):
    """Escape for reportlab, then turn X_y into subscripts."""
    return re.sub(r"([A-Za-zΔνμρσθε]+)_([A-Za-z0-9]+)", r"\1<sub>\2</sub>", escape(t))
def P(t, st="body"): return Paragraph(fmt(t), S[st])

_n = [0]
def eqimg(tex, width_max=11.5):
    _n[0] += 1; path = os.path.join(EQD, f"e{_n[0]}.png")
    fig = plt.figure(figsize=(0.01, 0.01)); fig.text(0, 0, f"${tex}$", fontsize=15, math_fontfamily="cm", color=INK)
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.03, transparent=True); plt.close(fig)
    w, h = PILImage.open(path).size; wc, hc = w * 72 / 300 / 28.35, h * 72 / 300 / 28.35
    if wc > width_max: hc *= width_max / wc; wc = width_max
    return Image(path, width=wc * cm, height=hc * cm)

story = []
tot_words = sum(len(s["say"].split()) for s in SLIDES)
story += [Paragraph("Speaking script", S["title"]),
          P(f"Micro heat pipes and vapour chambers: liquid return in the wick, wick-thickness optimisation, vapour flow in a thin core. "
            f"Debanshu Ghosh, 23CH3FP56. About {tot_words} spoken words, {clock(running()[-1])} at 150 words a minute."
            , "sub")]

rows = [[P("Slide", "cellb"), P("What it covers", "cellb"), P("Time", "cellb"), P("Running", "cellb")]]
for i, s in enumerate(SLIDES):
    rows.append([P(str(i + 1)), P(s["title"]), P(f"{s['secs']} s"), P(clock(running()[i]))])
t = Table(rows, colWidths=[1.4 * cm, 10.2 * cm, 1.8 * cm, 2.2 * cm], repeatRows=1)
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, SAGEc), ("BACKGROUND", (0, 0), (-1, 0), TINTc), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                       ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
story += [t, Spacer(1, 8), Paragraph("HOW TO USE THIS", S["lab"])]
for b in ("Say it, do not read the slide. The slide carries the picture and the formula; the script carries the sentence that connects them. The deck's speaker notes hold the same words, plus how each formula is derived.",
          f"Each slide gets 24 to 34 seconds. If you are behind at the halfway mark (slide 4 should end at {clock(running()[3])}), drop the 37% sentence first, then the saturated-vapour sentence on slide 6.",
          "Rehearse once aloud with a timer. Silent reading is always faster than speaking."):
    story.append(Paragraph(fmt(b), S["bul"], bulletText="•"))
story.append(Paragraph("NUMBERS TO HAVE IN YOUR HEAD", S["lab"]))
o50 = out["wick"][S50]
nums = [("5× and 25×", "pump pressure and liquid resistance, 10 µm against 50 µm powder"),
        (f"{_bar[0]:.0f}, {_bar[1]:.0f}, {_bar[2]:.0f} W", "fine, coarse and biporous capillary limits at a 100 µm core (biporous is an upper bound)"),
        ("37%", "lower peak-to-mean condenser surface ΔT in Patankar's simulation, biporous condenser wick"),
        (f"{_o50['t_um']:.0f} µm, {round(_o50['h_um'], -1):.0f} µm, {_o50['Q_opt']:.0f} W", "best split of 250 µm for the 50 µm powder: wick layer, core, capillary limit"),
        ("8×", "vapour resistance when the core is halved (1/h³)"),
        ("1.1 K per kPa", "saturation temperature change per vapour pressure drop, water at 60 °C"),
        (f"{_cu[200]['factor']:.0f}× and {_cu[50]['factor']:.0f}×", "chamber against copper sheet at 5 W, for h = 200 µm and h = 50 µm (the 50 µm value is a trend)")]
t = Table([[P(a, "cellb"), P(b)] for a, b in nums], colWidths=[4.4 * cm, 11.2 * cm])
t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, SAGEc), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (0, -1), TINTc),
                       ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
story.append(t)
story.append(Paragraph("The calculated values are illustrative: water at 60 °C, a disc-shaped chamber with a 10 × 10 mm source and a 48 mm rim, 5 W. They are not measured device data. Say so if asked.", S["sub"]))

for i, s in enumerate(SLIDES):
    block = []
    hdr = Table([[Paragraph(fmt(f"Slide {i + 1}  ·  {s['title']}"), S["h"]), Paragraph(f"{s['secs']} s  ·  ends {clock(running()[i])}", ParagraphStyle("r", parent=S["h"], alignment=2))]],
                colWidths=[12.2 * cm, 3.4 * cm])
    hdr.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), PINEc), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                             ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8)]))
    say = Table([[Paragraph(fmt(s["say"]), S["say"])]], colWidths=[15.6 * cm])
    say.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), TINTc), ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                             ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    block += [hdr, Paragraph("SAY", S["lab"]), say, Paragraph("POINT AT", S["lab"])]
    block += [Paragraph(fmt(x), S["bul"], bulletText="•") for x in s["point"]]
    story += [PageBreak() if 2 <= i <= 5 else CondPageBreak(11 * cm), KeepTogether(block)]
    if s["formulas"]:
        story.append(Paragraph("THE FORMULAS, IN ONE BREATH EACH", S["lab"]))
        for tex, meaning in s["formulas"]:
            story.append(KeepTogether([eqimg(tex), Spacer(1, 2), P(meaning), Spacer(1, 4)]))
    if s["qa"]:
        story.append(Paragraph("IF ASKED", S["lab"]))
        for q, a in s["qa"]:
            story.append(KeepTogether([Paragraph(fmt(q), ParagraphStyle("q", parent=S["body"], fontName="Serif-B", spaceAfter=1)), Paragraph(fmt(a), S["bul"])]))
    story.append(Spacer(1, 10))

def footer(canvas, doc):
    canvas.saveState(); canvas.setFont("Sans", 7.5); canvas.setFillColor(INKc)
    canvas.drawString(2.5 * cm, 1.3 * cm, "Debanshu Ghosh · 23CH3FP56 · Speaking script, 3-minute talk")
    canvas.drawRightString(A4[0] - 2.5 * cm, 1.3 * cm, str(doc.page)); canvas.restoreState()
doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=1.8 * cm, bottomMargin=2.0 * cm,
                      title="Speaking script: micro heat pipes and vapour chambers", author="Debanshu Ghosh")
doc.addPageTemplates([PageTemplate(id="m", frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")], onPage=footer)])
doc.build(story)
print("written", OUT, os.path.getsize(OUT) // 1024, "KB")
