"""The spoken script, in one place: it feeds the speaker notes of the deck and the printable script PDF.
Numbers come from numbers.json and focused_model.py. Spoken text is kept near 150 words a minute."""
from focused_model import *

_bar = list(N["biporous"]["horizontal"].values())
_o50, _o10 = out["wick"][S50], out["wick"][S10]
_cu = {int(v["h_um"]): v for v in out["vs_copper"]}
_rp = N["wicks"][S10]["p_cap_kPa"] / N["wicks"][S50]["p_cap_kPa"]
_rr = N["wicks"][S10]["a_l_Pa_per_W"] / N["wicks"][S50]["a_l_Pa_per_W"]

EQ_BUDGET = r"\Delta P_{cap}\;\geq\;\Delta P_{l}+\Delta P_{v}+\Delta P_{g}"
EQ_QMAX = r"Q_{max}=\dfrac{\Delta P_{cap}-\rho_l\,g\,\Delta z}{a_l+a_v}"
EQ_CAP = r"\Delta P_{cap}=\dfrac{2\,\sigma\cos\theta}{r_{eff}}"
EQ_DARCY = r"\Delta P_{l}=\dfrac{\mu_l\,\dot m\,\ln(R_2/R_1)}{2\pi\rho_l K\,t_l}"
EQ_KC = r"K=\dfrac{d^{2}\varepsilon^{3}}{150(1-\varepsilon)^{2}},\quad r_{eff}\approx 0.21\,d"
EQ_BIP = r"Q_{max}=\dfrac{2\sigma/r_{fine}}{a_l(K_{coarse})+a_v}"
EQ_SPLIT = r"a_l+a_v=\dfrac{\ln(R_2/R_1)}{\pi h_{fg}}\left(\dfrac{\mu_l}{4\rho_l K\,t}+\dfrac{6\mu_v}{\rho_v\,h^{3}}\right)"
EQ_OPT = r"\dfrac{h^{2}}{t}=12\sqrt{K\,\dfrac{\nu_v}{\nu_l}}"
EQ_VAP = r"\Delta P_{v}=\dfrac{6\mu_v\dot m\ln(R_2/R_1)}{\pi\rho_v h^{3}}"
EQ_CC = r"\Delta T_{sat}\approx\dfrac{T\,\Delta P}{\rho_v h_{fg}}"
EQ_CU = r"\Delta T_{Cu}=\dfrac{Q\,\ln(R_2/R_1)}{2\pi\,k\,H}"

SLIDES = [
 dict(title="Title", secs=8,
      say="Vapour chambers are the thin sheets that spread heat inside a phone. I will cover three transport questions about them.",
      point=["Stay on the title; the band shows vapour going right and liquid returning left."],
      formulas=[], qa=[]),
 dict(title="Overview: the capillary pump must beat every loss", secs=28,
      say=("Heat evaporates water at the chip. Vapour flows through the core, condenses over the cooler surface, and the liquid returns through a porous wick. "
           "The only pump is the wick itself. So capillary pressure must beat the liquid loss, the vapour loss and gravity, and that sets a maximum heat load. "
           "My three topics are the terms of this one equation: the liquid return, the thickness split, and the vapour core."),
      point=["Trace the loop with your finger: chip, vapour arrow, heat out, liquid back through the wicks.",
             "Point at badges 1, 2, 3 in turn during the last sentence, then at the two formulas."],
      formulas=[(EQ_BUDGET, "Around a closed loop the pressure must balance. Only the meniscus raises it; liquid flow, vapour flow and gravity all lower it."),
                (EQ_QMAX, "Both flow losses are proportional to the heat load Q (a is a flow resistance in Pa/W). Set the two sides equal and solve for Q.")],
      qa=[("Why is there a gravity term?", f"If the chip is at the top of a vertical sheet the liquid must be lifted: ρ g Δz = {N['head_100mm_kPa']:.2f} kPa for 100 mm. Horizontal, it is zero."),
          ("Why does orientation hardly matter inside the sheet?", f"The Bond number ρgh²/σ is only {N['Bo']['200um']:.3f} at 200 µm, so surface tension beats gravity at that scale."),
          ("Are the numbers from a real device?", "No. They are for water at 60 °C and an illustrative phone-like disc: 10 × 10 mm source (R1 = 5.64 mm), rim at R2 = 48 mm, 5 W.")]),
 dict(title="Topic 1: finer pores pump harder but resist flow far more", secs=34,
      say=("The meniscus in each pore is the pump, and Young–Laplace says its pressure goes as one over pore radius. "
           "But the liquid also has to flow through the wick, and Darcy's law gives that loss. Permeability goes as particle size squared, so one length sets both. "
           f"Going from 50 to 10 micron powder gives {_rp:.0f} times the pump pressure but {_rr:.0f} times the liquid resistance. "
           "So the best wick is the coarsest one with enough margin."),
      point=["Left: the meniscus. Middle: coarse strip, then fine strip. Right: the three formulas top to bottom.",
             "Finish on the 5× and 25× tiles."],
      formulas=[(EQ_CAP, "σ surface tension, θ contact angle, r_eff the effective pore radius. A spherical meniscus of radius r_eff/cos θ has a pressure jump 2σ divided by that radius."),
                (EQ_DARCY, "μ_l viscosity, ṁ = Q/h_fg the mass flow, K permeability, t_l the total wick thickness (two layers). It is Darcy's law integrated radially from the rim R2 to the source R1."),
                (EQ_KC, "d particle diameter, ε porosity (0.5 here). With ε = 0.5 this is K = d²/300. Pore radius is about 0.21 of the particle diameter.")],
      qa=[("Why 0.21 d?", "A common rule of thumb for sintered spheres; mesh and groove wicks have their own correlations. It is a stated assumption, not derived here."),
          ("What if the wick does not wet perfectly?", "ΔP_cap carries cos θ, so θ = 60° halves the pump pressure with no change in geometry."),
          ("Is Darcy's law valid for such a thin wick?", "It needs a layer many particles thick. A 50 µm layer of 50 µm powder is about one particle deep, so treat that case as an order-of-magnitude estimate.")]),
 dict(title="Topic 1: biporous wicks separate the pump from the flow path", secs=24,
      say=("A biporous wick escapes that trade-off. Fine pores inside clusters set the pump pressure, and coarse channels between clusters carry the flow. "
           f"In my idealised estimate the limit rises from {_bar[0]:.0f} or {_bar[1]:.0f} watts to about {_bar[2]:.0f}, as an upper bound. "
           "In Patankar's simulation, a biporous condenser wick cut the peak-to-mean surface temperature difference by 37 percent."),
      point=["Illustration first (clusters and channels), then the three bars, then the formula, then the 37% tile."],
      formulas=[(EQ_BIP, "The pump comes from the fine pore radius, while the liquid resistance uses the coarse permeability. Each job gets its own length scale.")],
      qa=[("Why only an upper bound?", "It assumes the fine and coarse regions do not interfere, and it borrows K from 100 µm particles, which would not fit in a 50 µm layer. It shows the principle, not a buildable wick."),
          ("What exactly is the 37%?", "A simulation result (Patankar, Weibel and Garimella 2016): the peak-to-mean temperature difference on the condenser surface, relative to a monolithic wick, because the biporous wick allows a thicker vapour core.")]),
 dict(title="Topic 2: in a fixed thickness every wick has a best split", secs=32,
      say=("The inner thickness is fixed, here 250 microns, so every micron of wick comes out of the vapour core. "
           "Liquid resistance falls as one over t, but vapour resistance climbs as one over h cubed, so the total has a minimum. "
           "Setting the derivative to zero gives a clean result: h squared over t depends only on permeability and the fluid. "
           f"For the 50 micron powder that means a {_o50['t_um']:.0f} micron wick, a {round(_o50['h_um'], -1):.0f} micron core, and about {_o50['Q_opt']:.0f} watts."),
      point=["Left: the three drawings, 57 W then 101 W then 27 W. Right: the curves; each dot is the best split for that wick.",
             "Point at the h²/t card last."],
      formulas=[(EQ_SPLIT, "The first term is the Darcy loss per watt with t_l = 2t (it falls as 1/t). The second is the Poiseuille loss per watt (it rises as 1/h³). Together they are the total flow resistance, with h = H − 2t."),
                (EQ_OPT, "Differentiate with dh/dt = −2: the 3 from the cube and the 2 give 6, so h⁴/t² = 144 K ν_v/ν_l, and the square root gives the 12. ν = μ/ρ is the kinematic viscosity.")],
      qa=[("Does the optimum depend on the heat load?", "No. Q, σ, θ and R2/R1 all cancel. Only the permeability and the fluid remain."),
          ("Is this from a paper?", "No. It is my derivation from the same model, and I checked it against a direct numerical sweep for all three wicks (within the 2 µm grid)."),
          ("Does it also minimise temperature?", f"No, it maximises the capillary limit only. At the optimum the vapour drop is {_o50['dP_v_at_Qopt_kPa']:.1f} kPa, about {_o50['dP_v_at_Qopt_kPa']*1e3/P_sat*100:.0f}% of P_sat, so read the watts as trends.")]),
 dict(title="Topic 3: halve the vapour gap and copper catches up", secs=34,
      say=("Vapour spreads radially in a thin slit, which is Poiseuille flow, so the pressure drop goes as one over h cubed. Halve the gap and it is eight times worse. "
           "In saturated vapour that pressure drop is a temperature drop, about 1.1 kelvin per kilopascal. "
           f"Against a copper sheet of the same thickness, at 5 watts, the chamber is about {_cu[200]['factor']:.0f} times better at 200 microns, but only about {_cu[50]['factor']:.0f} times better at 50. "
           "Thin cores erase the advantage."),
      point=["Left: radial picture, then the Poiseuille profile with the ×8 line. Then the two formulas.",
             "Right: grey bars are copper, dark bars are the chamber; finish on the tiles with the ratios."],
      formulas=[(EQ_VAP, "Plane Poiseuille flow in a slit gives dP/dr = −12 μ_v u/h²; the flow area is 2π r h, so u = ṁ/(ρ_v 2π r h). Integrate from R1 to R2. The h³ is one power from the velocity and two from the wall shear."),
                (EQ_CC, "Clausius–Clapeyron with v_fg ≈ 1/ρ_v. For water at 60 °C it is 1.08 K per kPa."),
                (EQ_CU, "The copper sheet of thickness H carries the same heat radially from the same source to the same rim. k = 400 W/m K. H is the whole chamber thickness (core, two wicks, two walls).")],
      qa=[("What is the copper comparison exactly?", f"A solid copper sheet with the same total thickness H as the chamber, the same 5 W source and the same rim. At h = 200 µm: copper {_cu[200]['cu']:.1f} K, chamber {_cu[200]['vc']:.2f} K."),
          ("What is inside the chamber's ΔT?", f"Vapour drop + wick conduction + evaporating interface (accommodation coefficient assumed 0.1). At 200 µm that is {_cu[200]['vapour']:.2f} + {_cu[200]['wick']:.2f} + {_cu[200]['interface']:.2f} K. The interface term is the biggest for thick cores."),
          ("Why is the 50 µm bar marked with an asterisk?", f"Its vapour pressure drop ({_cu[50]['vapour']:.1f} K equivalent) is above 20% of P_sat, so the linear Clausius–Clapeyron relation is not valid. Read it as a trend."),
          ("Is this a micro heat pipe or a vapour chamber?", "A micro heat pipe is the one-dimensional version of the same physics. The numbers here are for the flat chamber geometry.")]),
 dict(title="Three results and references", secs=8,
      say="So: one length sets the wick, a simple formula sets the split, and h cubed sets the vapour limit. Thank you.",
      point=["Read the three badges quickly; leave the reference list on screen for questions."],
      formulas=[], qa=[]),
]

def running():
    t, out_ = 0, []
    for s in SLIDES:
        t += s["secs"]; out_.append(t)
    return out_

def clock(sec): return f"{sec // 60}:{sec % 60:02d}"

def head(i):
    """Header of the speaker notes for slide i (1-based): timing, then the words to say."""
    s = SLIDES[i - 1]
    return f"TIME: {s['secs']} s  (running total {clock(running()[i - 1])})\n\nSAY: \"{s['say']}\"\n\n"
