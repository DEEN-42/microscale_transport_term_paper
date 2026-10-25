# Study Guide: Micro Heat Pipes and Vapour Chambers

**For:** Debanshu Ghosh (23CH3FP56), Chemical Engineering, IIT Kharagpur
**Course:** Microscale Transport Processes (DasGupta & Ganguly)
**Goes with:** `Term_Paper_Micro_Heat_Pipes_and_Vapour_Chambers.pdf` and `Presentation_Micro_Heat_Pipes_and_Vapour_Chambers.pptx`

This guide is written so that you can *understand* the term paper well enough to present it and answer questions. The paper is the formal version. This guide explains the same ideas in plain words, with analogies, step-by-step derivations, the numbers worked out by hand, the likely questions, and a talk script.

**Suggested reading order (about 2 hours):**
1. Part 1 (5 min) and Part 2 (10 min): the big picture and the vocabulary.
2. Part 3 (60 min): the physics, one section at a time. Do the derivations on paper yourself once.
3. Part 4 (10 min): the worked example, with a calculator.
4. Parts 5–6 (15 min): assumptions and how to defend each claim.
5. Part 7 (15 min): practise the questions out loud.
6. Part 8: rehearse the talk with the slides.

---

## Part 1. The whole paper in 5 minutes

**The problem.** A phone chip makes heat in a few square millimetres. The phone has no fan and is held in the hand, so what limits performance is the *skin temperature* of the case. When the case gets too hot, the software slows the chip ("throttling"). On a Nexus 6P, Bhat et al. measured performance loss of up to 34% in popular apps, about 12 frames per second in one game, and about 50 °C at the package when throttling was off [2]. So the job is to spread the heat sideways quickly inside a sheet less than ~1 mm thick.

**The idea.** A *vapour chamber* is a flat sealed sheet containing a little water. Water evaporates at the hot spot, the vapour flows outward, condenses where it is cooler, and the liquid comes back through a porous layer (the *wick*) by *capillary suction*, like a sponge pulling up water. Heat is carried as *latent heat*, so very little water has to move: for 5 W only about 2.1 milligrams per second.

**The one big idea of the paper: the pressure budget.** The capillary pump has to beat three losses: the liquid flowing through the wick, the vapour flowing through the core, and gravity.

> pump pressure ≥ (liquid loss) + (vapour loss) + (gravity)

Everything else in the paper is about those three terms.

**The five findings:**
1. **The wick is a compromise.** Finer pores pump harder (pressure ∝ 1/d) but let the liquid through much less easily (permeability ∝ d²). The best wick is the coarsest one that still has enough pumping pressure.
2. **Wick and vapour core fight for thickness.** In a sheet of fixed thickness, every micrometre of wick is taken from the vapour core. So there is an *optimal* wick thickness (50 µm per layer for the 50 µm powder in my model).
3. **The vapour core follows an inverse-cube law.** Pressure drop ∝ 1/h³. Halve the core, and it becomes 8× more resistive. Below ~100 µm the vapour core, not the wick, controls how uniform the temperature is.
4. **The interface is uncertain.** How easily molecules leave the liquid depends on a number (accommodation coefficient) that is known only to within orders of magnitude.
5. **"Effective thermal conductivity" is not a property.** Its value depends on how it is defined, on the load and on the orientation, so numbers from different papers cannot simply be compared.

**What makes it a critical review rather than a summary:** each section states the assumptions behind the equation, shows a number, says where it fails, and compares with published experiments.

---

## Part 2. Glossary (plain words)

| Term | Plain meaning |
|---|---|
| **Heat pipe** | A sealed tube with a little fluid that moves heat by evaporating at one end and condensing at the other. |
| **Micro heat pipe** | A heat pipe so small that the capillary action of the fluid alone is enough to bring the liquid back. |
| **Vapour chamber (VC)** | A flat, two-dimensional heat pipe; it spreads heat over an area. |
| **Wick** | The porous layer (powder, mesh, grooves) on the walls that sucks liquid back to the hot spot. |
| **Vapour core** | The open space between the wicks where the vapour flows. |
| **Latent heat (h_fg)** | The heat absorbed when a liquid evaporates (2.358 MJ/kg for water at 60 °C). The reason a tiny mass flow carries a lot of heat. |
| **Capillary pressure (ΔP_cap)** | The suction created by a curved liquid surface in a small pore: 2σcosθ / r. |
| **Surface tension (σ)** | The "skin" force of a liquid surface (0.0662 N/m for water at 60 °C). |
| **Contact angle (θ)** | The angle the liquid makes with the wall. θ = 0 means it wets completely. |
| **Permeability (K)** | How easily liquid flows through the porous wick (m²). Larger K, easier flow. |
| **Darcy's law** | Flow through a porous medium is proportional to the pressure gradient (and to K). |
| **Poiseuille flow** | The smooth (laminar) flow between plates or in a tube; pressure drop ∝ viscosity × flow / (gap³ for a slit). |
| **Bond number (Bo)** | ρ g h² / σ. Compares gravity with surface tension. Bo ≪ 1 means surface tension wins. |
| **Knudsen number (Kn)** | Mean free path λ / length. Kn small means the fluid behaves as a continuum. |
| **Mach number (Ma)** | Flow speed / speed of sound. Small Ma means the flow can be treated as incompressible. |
| **Clausius–Clapeyron relation** | Links the saturation pressure and temperature of a vapour; lets us turn a pressure drop into a temperature drop. |
| **Accommodation coefficient (σ_a)** | The fraction of molecules hitting the liquid surface that are actually taken up. Sets the interface resistance. |
| **Capillary limit (Q_max)** | The largest heat load for which the capillary pump can still return liquid. |
| **Dry-out** | The wick runs out of liquid at the hot spot and the temperature shoots up. |
| **Biporous wick** | A wick with two pore sizes: fine for pumping pressure, coarse for easy flow. |
| **Non-condensable gas** | Air or hydrogen trapped in the chamber; it collects at the condenser and blocks it. |
| **k_eff (effective conductivity)** | The conductivity a solid block would need to give the same temperature drop. Not a material property. |
| **Skin temperature** | The temperature of the phone's outer case, which is what the user feels. |

---

## Part 3. The physics, one section at a time

### 3.1 The cycle (paper Section 2.1)

**Analogy.** Think of a kitchen kettle with a tray of ice above it. Water evaporates at the bottom, the steam rises, the steam condenses on the cold tray and drips back. A vapour chamber is that loop, shrunk down to a sheet less than a millimetre thick, with a sponge (the wick) instead of gravity to bring the water back.

**Why heat moves so well.** Evaporating 1 kg of water absorbs 2.358 MJ. So 5 W only needs ṁ = Q / h_fg = 5 / 2.358×10⁶ = 2.12e-06 kg/s. This is *latent heat* transport, not conduction, which is why a vapour chamber can be "much more conductive than copper".

### 3.2 Capillary pressure: the pump (paper Section 2.2)

**The idea.** In a narrow pore the liquid surface curves. A curved surface has a pressure jump across it. The narrower the pore, the stronger the curvature and the stronger the suction.

**The equation:** ΔP_cap = 2σ cosθ / r_eff

**Where it comes from, in 3 steps:**
1. In a pore of radius r, with contact angle θ, the liquid surface is part of a sphere of radius R = r / cosθ.
2. The pressure jump across a spherical surface is 2σ/R (Young–Laplace).
3. Substituting gives 2σ cosθ / r.

**Numbers (water at 60 °C, θ = 0):**
- 64 µm pore (mesh): 2 × 0.0662 / 64×10⁻⁶ = 2.1 kPa
- 10 µm pore: 13.2 kPa
- 1 µm pore: 132 kPa

**Gravity check (Bond number).** Bo = ρ g h² / σ. For h = 200 µm: Bo = 983 × 9.81 × (2×10⁻⁴)² / 0.0662 = 0.0058. This is ≪ 1, so inside the sheet gravity cannot rearrange the liquid. **But** over the length of the sheet gravity still acts: lifting water 100 mm takes ρ g Δz = 0.96 kPa. Fine wicks (10–60 kPa) cover that easily; mesh (2.1 kPa) has only about twice the margin.

> **Say it simply:** "Surface tension beats gravity inside the sheet, but over the length of a phone gravity can still matter for coarse wicks."

**Assumptions:** spherical meniscus, constant contact angle, uniform pores, pure liquid.
**Where it breaks:** real wicks have a spread of pore sizes; the contact angle changes with oxidation and dirt; cosθ = 0.5 (θ = 60°) halves the pressure.

### 3.3 The pressure budget (paper Section 2.3)

**Analogy.** A water pump on a pipe network must overcome friction in the pipes and the lift. If friction + lift is bigger than the pump's pressure, no water arrives. Here the pump is the wick, and "friction" is the liquid flow in the wick and the vapour flow in the core.

**Equations:**
- Budget: ΔP_cap ≥ ΔP_l + ΔP_v + ΔP_g
- Both flow losses are proportional to Q, so ΔP_l = a_l Q and ΔP_v = a_v Q.
- Therefore **Q_max = (ΔP_cap − ρ g Δz) / (a_l + a_v)**.

This is the backbone of the whole paper. To raise Q_max you can: raise ΔP_cap (finer pores), lower a_l (more permeable/thicker wick), or lower a_v (thicker core). They conflict, which is the subject of the next parts.

### 3.4 The wick (paper Section 3)

**Analogy.** A paper towel and a coffee filter. A tightly woven filter (fine pores) pulls water up strongly but water barely moves through it. A coarse sponge lets water flow easily but pulls weakly.

**Darcy's law for the radial flow in the wick:**

ΔP_l = μ_l ṁ ln(R₂/R₁) / (2π ρ_l K t_l)

- Bigger K, bigger thickness t_l → smaller loss.
- The ln(R₂/R₁) comes from integrating radial flow from the rim to the heat source.

**Kozeny–Carman permeability for sintered spheres:** K = d² ε³ / [150 (1−ε)²], and r_eff ≈ 0.21 d (a rule of thumb).

**The trade-off in one line:** pressure ∝ 1/d, but permeability ∝ d². Shrinking d by 5 gives 5× the pressure and 25× the resistance.

| Wick | r_eff (µm) | K (m²) | ΔP_cap (kPa) | a_l (Pa per W) |
|---|---|---|---|---|
| Cu mesh #200 | 64 | 2.8e-11 | 2.1 | 24 |
| Sintered 50 µm | 10.5 | 8.3e-12 | 12.6 | 82 |
| Sintered 10 µm | 2.1 | 3.3e-13 | 63.0 | 2055 |

**Reading it.** The 10 µm wick has 5× the pressure of the 50 µm wick but 25× the resistance (2055 vs 82 Pa/W). It is *liquid-limited*: it delivers about 29 W no matter how thick the vapour core is. The extra pump pressure is wasted.

**Biporous wicks.** Use two length scales: fine pores for pressure, coarse channels for flow. In my idealised calculation the limit rises from 50 W (fine) or 38 W (coarse) to 161 W. **This is an upper bound** (it assumes the two regions don't interfere). Say so if asked. Semenic and Catton [18] studied biporous wicks experimentally.

**Optimal wick thickness.** If the inner thickness is fixed (250 µm), then a thicker wick leaves a thinner core. Result: an optimum, at 50 µm per layer for the 50 µm powder (giving 101 W), 36 µm for mesh (35 W), 82 µm for the fine powder (43 W).

### 3.5 The vapour core (paper Section 4)

**Analogy.** A highway whose number of lanes you halve. Because the lane width enters as a *cube*, traffic jams get catastrophically worse, not just twice as bad.

**Derivation of the inverse-cube law (4 steps):**
1. Vapour leaves the source and spreads radially. At radius r the mean velocity is u = ṁ / (ρ_v · 2π r h).
2. For laminar flow between two plates a distance h apart, dP/dr = −12 μ_v u / h².
3. Substitute u: dP/dr = −6 μ_v ṁ / (π ρ_v r h³).
4. Integrate from R₁ to R₂: **ΔP_v = 6 μ_v ṁ ln(R₂/R₁) / (π ρ_v h³)**.

The h³ in the denominator is the whole story. Halve h and ΔP goes up by exactly 2³ = 8.

**From pressure to temperature (Clausius–Clapeyron).** Vapour pressure and temperature are tied: ΔT_sat ≈ T ΔP / (ρ_v h_fg) ≈ 1.1 K per kPa. So the vapour pressure drop shows up as a temperature non-uniformity, which is what the user feels as a hot patch.

| Core h (µm) | ΔP at 5 W (Pa) | ΔT at 5 W (K) | ΔT at 20 W (K) | Ma at 5 W | Kn |
|---|---|---|---|---|---|
| 400 | 11 | 0.012 | 0.049 | 0.003 | 0.0019 |
| 200 | 90 | 0.10 | 0.39 | 0.005 | 0.0038 |
| 100 | 718 | 0.78 | 3.1 | 0.010 | 0.0077 |
| 50 | 5745 | 6.2 (invalid) | (invalid) | 0.020 | 0.0154 |

"Invalid" means the pressure drop exceeds 20% of the saturation pressure (19.95 kPa), where the linear Clausius–Clapeyron relation is no longer reliable. Only the trend should be read from those rows.

**Short checks (why you can use simple flow equations):**
- *Mach number* 0.010 at 100 µm, so the flow is effectively incompressible.
- *Knudsen number* λ/h = 0.77 µm / 100 µm = 0.008, so continuum, no slip. But in a 1 µm wick pore Kn = 0.77, which is **not** continuum. Most models ignore this.
- *Sonic limit* ~228 W at 100 µm, far above a phone load.

**Literature link.** Patankar et al. [15] found that ultra-thin chambers are limited by the vapour core, and that a biporous condenser-side wick, which allows a thicker core, cut the peak-to-mean skin temperature difference by **37%** (3-D simulation).

**Why the vapour chamber beats copper only if the core is thick enough.** In the model, at 5 W with 200 µm core, the chamber's total temperature drop is 0.33 K against 9.3 K for a copper plate of the same thickness (factor ~28); at 50 µm it is 6.5 K against 13.7 K (factor ~2). The advantage shrinks.

### 3.6 The interface (paper Section 5)

**Analogy.** Evaporating water is like people leaving a crowded room through a door: even with a big open space outside, how many get out per second depends on how many actually manage to get through the door. The "accommodation coefficient" is the fraction that make it through.

**Equation:** h_i = [2σ_a/(2−σ_a)] · (ρ_v h_fg² / T) · sqrt(1 / (2π R_v T)). You do not need to derive this; know what it means: heat-transfer coefficient of the interface from kinetic theory.

| σ_a | 1 | 0.1 | 0.03 | 0.01 | 0.001 |
|---|---|---|---|---|---|
| h_i (kW/m²K) | 4,429 | 233 | 67 | 22.3 | 2.2 |
| ΔT at 50 kW/m² (K) | 0.011 | 0.21 | 0.74 | 2.25 | 22.6 |

**The message:** measured values of σ_a for water scatter widely (about 0.01 to 1; Marek and Straub [21]), so the temperature jump at the interface is uncertain by orders of magnitude. Note: the table uses the whole source area (1 cm²), which *overstates* the jump because the real interface area is larger.

**Thin-film region ("going deeper" box).** Heat enters mostly through thin liquid films near the contact line (Wayner et al. [20]). Conduction through a film of thickness δ gives k_l/δ: 653 kW/m²K at δ = 1 µm, 65 at 10 µm, 6.5 at 100 µm. So a thick layer of liquid over the heater is a resistance, and the wick should keep the heater wetted by a *thin* film.

### 3.7 Operating limits (paper Section 6)

Think of each limit as "which quantity runs out first":

| Limit | What runs out |
|---|---|
| Capillary | pump pressure |
| Sonic | the vapour reaches the speed of sound at the exit |
| Entrainment | vapour drags droplets off the liquid and starves the wick |
| Boiling | bubbles form inside the wick and block liquid access |
| Viscous | at start-up the vapour pressure is too low to drive flow |

**Model results (Fig. 8 of the paper):**
- *Thick core:* wick sets the limit (coarse 50 µm powder ~150 W, mesh ~80 W, fine 10 µm powder ~30 W).
- *Thin core:* vapour sets the limit. The 50 µm powder gives 56 W at 100 µm but only 10 W at 50 µm.
- *Gravity* mostly hurts the coarse mesh: 12 W falls to 6.6 W (source on top, 100 µm core).

**What the model cannot see:** local dry-out, entrainment, boiling. Experiments: Yan et al. [16] measured up to 60 W for a 0.5 mm chamber; Weibel et al. [14] found 600–1200 µm sintered wicks handled >500 W/cm² locally without dry-out, but those are much thicker. **Do not say the model agrees with experiment**: the 56 W vs 60 W closeness is a coincidence of order of magnitude.

### 3.8 Modelling and effective conductivity (paper Section 7)

**Four model families:** resistance network (cheap, for sizing) → analytical 1-D/2-D (explains trends; this paper) → 3-D porous continuum (hot-spot maps) → microstructure-aware (most detail, most cost). *The cheaper models are not worse, only more limited.*

**k_eff = Q ln(R₂/R₁) / (2π H ΔT)** (radial definition). Same temperature drop, but if you treat the sheet as a strip of width equal to the source, you get a number 11× bigger (11×10³ vs 125×10³ W/m K at 200 µm). It also falls as the core thins (4.7×10³ at 100 µm, 851 at 50 µm).

**Reported values:** 3473–3837 W/m K for a 0.39 mm chamber (Zhang et al. [17]) and 11,817 W/m K at 50 W against gravity for a 0.5 mm chamber (Yan et al. [16]). These devices differ in size, thickness, load and orientation, so you cannot say one is better without checking the definition.

### 3.9 Fabrication and reliability (paper Sections 8–9)

- **Do not describe the fabrication steps** (that is Lectures 2–3). Say only what each route *fixes*: powder → particle size → r_eff and K; mesh → wire diameter; etched grooves → directional K; nanostructures → small pores and wetting (but ageing); bonding → hermeticity and gas level; pillars → stiffness but they block vapour.
- **Reliability:** non-condensable gas collects at the condenser; θ drift 0° → 60° halves the pump pressure; fouling of fine pores (the Lecture 4 mechanism, here hitting pump pressure); Cu–water compatible, Al–water makes H₂; sealed at ~20 kPa so the shell relies on pillars; freezing expands water ~9%.

---

## Part 4. Worked example (do this once with a calculator)

**Setup:** water at 60 °C, 5 W, source 10×10 mm (R₁ = 5.64 mm), disc R₂ = 48 mm, ln(R₂/R₁) = 2.141, sintered 50 µm powder, two wick layers of 50 µm, core h = 100 µm.

1. **Mass flow.** ṁ = 5 / 2.358×10⁶ = 2.12e-06 kg/s.
2. **Pump pressure.** r_eff = 0.21 × 50 = 10.5 µm; ΔP_cap = 2 × 0.0662 / 10.5×10⁻⁶ = 12.6 kPa.
3. **Permeability.** K = d²ε³ / [150(1−ε)²] = (50×10⁻⁶)² × 0.125 / (150 × 0.25) = 8.3e-12 m².
4. **Liquid loss.** ΔP_l = μ_l ṁ ln(R₂/R₁) / (2π ρ_l K t_l), with t_l = 2 × 50 µm = 100 µm. This gives a_l = 82 Pa/W, so at 5 W ΔP_l = 411 Pa.
5. **Vapour loss.** ΔP_v = 6 μ_v ṁ ln(R₂/R₁) / (π ρ_v h³) = 718 Pa at 5 W (h = 100 µm), so a_v = 144 Pa/W.
6. **Capillary limit (horizontal).** Q_max = ΔP_cap / (a_l + a_v) = 12610 / (82 + 144) ≈ 56 W. That is 11× the 5 W load.
7. **Temperature spread from the vapour.** ΔT = T ΔP / (ρ_v h_fg) = 333.15 × 718 / (0.1304 × 2.358×10⁶) = 0.78 K.

**Check your understanding:** What happens to step 5 and 7 if h drops to 50 µm? (ΔP_v rises 8× to 5745 Pa and ΔT to ~6.2 K, which is outside the model's validity.)

---

## Part 5. Assumptions checklist (know these cold)

| Assumption | Why | Effect | When it fails |
|---|---|---|---|
| Single temperature, 60 °C | simplicity | small | large temperature spread |
| Disc geometry, centre source, all vapour to rim | closed-form maths | overestimates vapour ΔP by an order-1 factor | multiple sources, corners |
| Uniform wick, Kozeny–Carman, r_eff = 0.21 d | standard correlations | K, r_eff uncertain ×2 or more | real pore distributions |
| θ = 0 | best case | overestimates ΔP_cap | oxidised/dirty surfaces |
| Laminar, incompressible vapour | checked via Ma, Kn | negligible at phone loads | very high loads, very thin cores |
| Linear Clausius–Clapeyron | closed-form ΔP → ΔT | valid while ΔP < 20% P_sat | cores thinner than ~60 µm at 5 W |
| Steady state | limits are defined at steady state | misses dry-out and start-up | fast mobile power transients |
| No gas, no pillars | clean idealisation | optimistic | real chambers have both |

---

## Part 6. How to defend each claim

| Claim | Evidence | Source | Caveat to volunteer |
|---|---|---|---|
| Throttling costs up to 34% | Nexus 6P experiments, ~12 fps in one game | Bhat et al. [2] | one phone, one study |
| Capillary pressure ∝ 1/r | Young–Laplace | textbooks [25, 26] | θ constant, uniform pores |
| Wick trade-off | K ∝ d², ΔP_cap ∝ 1/d; Table 2 of paper | Kozeny–Carman [25, 26] | correlations are approximate |
| Biporous helps | experiments on biporous wicks | Semenic & Catton [18] | my 161 W is an idealised upper bound |
| Vapour ΔP ∝ 1/h³ | Poiseuille slit derivation | standard fluid mechanics | laminar, all vapour to rim |
| Thicker vapour core helped skin ΔT by 37% | 3-D simulation | Patankar et al. [15] | simulation, not experiment |
| Interface resistance is uncertain | scatter in measured σ_a | Marek & Straub [21] | exact range depends on conditions |
| k_eff isn't comparable across papers | radial vs strip: 11× in my model; 3473–3837 vs 11,817 | Zhang [17], Yan [16] | I compared definitions in my own model, not by re-deriving theirs |
| Models agree with experiment | **Not claimed** | – | The 56 W vs 60 W closeness is coincidental |

---

## Part 7. Likely questions with short answers

**General**
1. *Why this topic?* It is a clean example of microscale transport: surface tension, capillary pumping and thin-film flow dominate at small scales, and it solves a real problem (skin temperature).
2. *What is new compared with the lectures?* The lectures cover scaling, fabrication and microstructured heat exchangers. This paper adds capillary two-phase transport: wick physics, the pressure budget, the inverse-cube vapour law, the interface, limits and model assumptions. The lectures are used only as background.
3. *Why not just use a thicker copper sheet?* In a sheet under ~1 mm, copper conducts heat sideways poorly; in the model the copper plate has a temperature drop of 9.3 K versus 0.33 K for the chamber at 5 W (200 µm core).
4. *Why not liquid cooling?* It needs a pump and plumbing that a sealed phone can't hold (Tuckerman and Pease, Garimella et al.).

**Physics**
5. *What drives the liquid?* Capillary suction from the curved meniscus, ΔP = 2σcosθ/r.
6. *Why does it work in any orientation?* Bo ≪ 1 inside the sheet; gravity head over 100 mm is 0.96 kPa, much smaller than the pump pressure of fine wicks.
7. *Why is a finer wick not always better?* Pressure ∝ 1/d but permeability ∝ d², so liquid resistance rises faster than the pump pressure; beyond what you need, extra pressure is wasted.
8. *What is the capillary limit?* Q_max = (ΔP_cap − ρgΔz)/(a_l + a_v), the heat load at which the pump pressure just equals the losses.
9. *Why 1/h³ for the vapour?* Poiseuille flow between plates: ΔP ∝ μ Q_v / h³ per unit width; integrating radially keeps the h³.
10. *How does a pressure drop become a temperature drop?* In saturated vapour pressure and temperature are linked; ΔT ≈ TΔP/(ρ_v h_fg) ≈ 1.1 K/kPa.
11. *When does the vapour matter more than the wick?* For core thickness below roughly 100 µm in this model (for the powder wick).
12. *Is the vapour compressible?* Not at phone loads: Ma = 0.010.
13. *Is the continuum assumption fine?* In the core, Kn = 0.008, yes. In 1 µm pores Kn = 0.77, no.
14. *What is the accommodation coefficient?* The fraction of molecules striking the liquid that are taken up; it sets h_i.
15. *Why does the interface matter if h_i is 4.4 MW/m²K for σ_a = 1?* Because σ_a for water is uncertain by orders of magnitude; at 0.01 the jump at 5 W/cm² is 2.2 K.
16. *What is a biporous wick?* Fine pores for pressure plus coarse channels for flow.
17. *What is the optimum wick thickness?* It depends on the wick: 50 µm per layer for the 50 µm powder when the inner thickness is 250 µm.
18. *What are the operating limits?* Capillary, sonic, entrainment, boiling, viscous.

**Critical review**
19. *What are the weakest assumptions of your model?* Disc geometry with all vapour to the rim, θ = 0, uniform wick, steady state, no gas or pillars (Part 5).
20. *Does your model agree with experiments?* I do not claim that. It explains trends; the absolute limits are set by local effects it cannot see.
21. *Why can't I compare k_eff between papers?* The geometry and reference length used in its definition, the load and the orientation differ. In my model two definitions differ by 11× for the same data.
22. *What is controversial?* The accommodation coefficient, comparability of performance metrics, how well simple models predict absolute limits, lifetime behaviour.
23. *What did Patankar et al. show?* A biporous condenser-side wick allowing a thicker vapour core reduced the peak-to-mean skin temperature difference by 37% (simulation).
24. *Which source is the weakest in your list?* The two textbooks [25, 26] are used for classical correlations and limits; I did not re-derive them. Also [1] is course material.
25. *Why do you use a 5 W load?* Illustrative, phone-like; not a measured value from any device.

**Reliability and fabrication**
26. *Why does non-condensable gas matter?* It collects at the condenser and shuts off part of the condensing area, so the chamber runs hotter.
27. *What does contact angle do?* ΔP_cap ∝ cosθ; from 0° to 60° the pump pressure halves.
28. *What happens when water freezes?* It expands by about 9%, which can deform a thin shell.
29. *Which fabrication route is best?* There isn't one: each fixes different properties (Table 7 of the paper). Depends on the load, thickness and orientation.
30. *What do pillars do?* They stop the thin shell from collapsing but obstruct the vapour and add conduction paths; Zhang et al. [17] saw k_eff fall as column diameter grew.

---

## Part 8. Talk script (about 12–13 minutes, 15 slides)

Speak slowly; one idea per slide; if you run short of time skip slides 12–13 and say "see the paper".

| # | Slide | Time | What to say |
|---|---|---|---|
| 1 | Title | 0:30 | "This talk is about how a sheet of water and copper thinner than a coin spreads heat in a phone, and what that teaches us about transport at the microscale. I focus on the science, not products." |
| 2 | The problem | 1:00 | Three numbers: up to 34%, about 12 fps, about 50 °C (Bhat et al.). "Heat is made in a few mm² and must leave through the whole back of the phone." |
| 3 | The idea | 1:00 | Walk through the four steps. "A few milligrams of water per second carry 5 W, because latent heat is 2.36 MJ/kg." |
| 4 | Capillary pressure | 1:15 | Show the equation. 64 µm → 2 kPa, 1 µm → 130 kPa. Bond number says gravity doesn't matter inside the sheet; over 100 mm it costs 0.96 kPa. |
| 5 | Pressure budget | 1:00 | "One idea organises everything." Read the inequality; then Q_max. Name the three terms. |
| 6 | Wick trade-off | 1:15 | Pressure ∝ 1/d, permeability ∝ d². Table: 5× pressure for 25× resistance. "Excess pressure is wasted." |
| 7 | Biporous and optimum | 1:00 | Two length scales. "The biporous bar is an upper bound." Wick vs core thickness gives an optimum. |
| 8 | Vapour core | 1:15 | 1/h³: halve the core, 8× resistance. 1.1 K per kPa. 0.10 K at 200 µm, 0.78 K at 100 µm. Patankar's 37%. |
| 9 | Interface | 0:45 | The accommodation coefficient is uncertain by orders of magnitude; "I do not claim to know which is right." |
| 10 | Limits | 1:00 | Thick core: wick limits; thin core: vapour limits. Gravity hurts the coarse mesh. "I do not claim the model agrees with experiments." |
| 11 | k_eff | 0:45 | Same data, two definitions, factor 11. "Don't compare k_eff across papers without checking definitions." |
| 12 | Models | 0:45 | "Each model hides something." Point at the table and the amber assumptions box. |
| 13 | Fabrication/reliability | 0:45 | "Fabrication sets pore size, porosity, contact angle, hermeticity; life is limited by gas, wetting drift, fouling and freezing." |
| 14 | Synthesis | 0:45 | Well established / argued over / limits of this review. |
| 15 | Conclusions | 0:45 | Four bullets. End: "The field understands why thin vapour chambers work; predicting exactly how well, and for how long, is still open." |

Speaker notes are already in each slide (open *Notes* in PowerPoint). They contain the same material in more detail.

---

## Part 9. Source map: what each source is used for

| # | Source | Used for |
|---|---|---|
| 1 | Course notes, Lectures 1–4 | Background only (scaling, fabrication, fouling) |
| 2 | Bhat et al. 2019 | The throttling problem: 34%, 12 fps, 50 °C |
| 3 | Garimella et al. 2008 | Thermal challenges in electronics, why liquid cooling is hard in a phone |
| 4 | Tuckerman & Pease 1981 | The microchannel liquid-cooling alternative |
| 5 | Faghri 2012 | Heat-pipe review: operating principle, limits |
| 6 | Peterson & Ma 1996 | Maximum heat transport in triangular grooves (idealised micro heat pipes) |
| 7 | Vasiliev 2008 | Micro and miniature heat pipes for electronics |
| 8 | Weibel & Garimella 2013 | Vapour-chamber transport review |
| 9 | Bulut et al. 2019 | Vapour-chamber review |
| 10 | Zhou et al. 2023 | Ultra-thin vapour-chamber review |
| 11 | Duan et al. 2022 | Ultra-thin heat-pipe manufacturing review |
| 12 | Filippou et al. 2024 | Microfabrication review for thin heat pipes/VCs |
| 13 | Hanlon & Ma 2003 | Evaporation from sintered porous media |
| 14 | Weibel et al. 2010 | Evaporation/boiling from sintered wicks; thick wicks handled >500 W/cm² |
| 15 | Patankar et al. 2016 | Biporous condenser wick; 37% skin ΔT reduction; vapour core limits |
| 16 | Yan et al. 2023 | 0.5 mm UTVC, composite wick, up to 60 W, 11,817 W/m K at 50 W |
| 17 | Zhang et al. 2024 | 0.39 mm UTVC, 3473–3837 W/m K, columns lower k_eff |
| 18 | Semenic & Catton 2009 | Biporous wicks |
| 19 | Khrustalev & Faghri 1995 | Evaporation on grooved structures |
| 20 | Wayner et al. 1976 | Interline region of an evaporating film |
| 21 | Marek & Straub 2001 | Scatter of the evaporation coefficient of water |
| 22 | Vadakkan et al. 2004 | 3-D model of flat heat pipes |
| 23 | Ranjan et al. 2011 | Flat heat-pipe model with wick microstructure |
| 24 | Prasher 2003 | Simplified conduction-based modelling |
| 25 | Peterson 1994 (book) | Wick correlations, standard limits |
| 26 | Faghri 1995 (book) | Standard limits and theory |

---

## Part 10. How the paper satisfies the course rules

| Rule | How it is met |
|---|---|
| Related to TRANSPORT and MICROSCALE | Capillary pumping, Darcy/Poiseuille flow, interfacial phase change and heat spreading at sub-millimetre scales |
| Content covered in class not repeated | Lectures cited in one line for background only; no re-derivation of scaling, Navier–Stokes, or fabrication steps; the wick, pressure budget, 1/h³ law, interface, limits and model audit are new |
| Focus on science, not market | No market, cost or product comparison anywhere |
| Review of multiple sources with assumptions, simplifications and demerits | 26 references (14 reviews/experimental/model papers, 2 textbooks); Sections 3–5 end with assumptions; Section 7 compares models; the assumption audit table; Section 10 separates settled from disputed |

**One honest warning for the viva:** if a later lecture (not in your folder) covers heat pipes, mention that the paper only cites the lectures as background and ask which part overlaps.

---

## Part 11. Reproducing the numbers

All numbers come from `build/calc.py`. From the project folder:

```
python -X utf8 build/calc.py        # writes build/numbers.json and the figures
python -X utf8 build/build_paper.py   # rebuilds the PDF
python -X utf8 build/build_pptx.py    # rebuilds the slides
python -X utf8 build/build_guide.py   # rebuilds this guide
```

References were checked against Crossref with `build/verify_refs.py`.

### Full reference list

1. DasGupta, S., & Ganguly, S. Microscale Transport Processes, Lectures 1-4 (course notes: Lecture 1; Lecture 2 - Top-Down Approach; Lecture 3 - Bottom-Up Approach; Lecture 4 - Main Issues of Successful Microstructures). IIT Kharagpur.
2. Bhat, G., Gumussoy, S., & Ogras, U. Y. (2019). Power and thermal analysis of commercial mobile platforms: Experiments and case studies. Proc. Design, Automation & Test in Europe (DATE) 2019, 144-149. <https://doi.org/10.23919/DATE.2019.8714831>
3. Garimella, S. V., Fleischer, A. S., Murthy, J. Y., Keshavarzi, A., Prasher, R., Patel, C., ... Raad, P. (2008). Thermal challenges in next-generation electronic systems. IEEE Trans. Components and Packaging Technologies, 31(4), 801-815. <https://doi.org/10.1109/TCAPT.2008.2001197>
4. Tuckerman, D. B., & Pease, R. F. W. (1981). High-performance heat sinking for VLSI. IEEE Electron Device Letters, 2(5), 126-129. <https://doi.org/10.1109/EDL.1981.25367>
5. Faghri, A. (2012). Review and advances in heat pipe science and technology. Journal of Heat Transfer, 134(12), 123001. <https://doi.org/10.1115/1.4007407>
6. Peterson, G. P., & Ma, H. B. (1996). Theoretical analysis of the maximum heat transport in triangular grooves: A study of idealized micro heat pipes. Journal of Heat Transfer, 118(3), 731-739. <https://doi.org/10.1115/1.2822693>
7. Vasiliev, L. L. (2008). Micro and miniature heat pipes - Electronic component coolers. Applied Thermal Engineering, 28(4), 266-273. <https://doi.org/10.1016/j.applthermaleng.2006.02.023>
8. Weibel, J. A., & Garimella, S. V. (2013). Recent advances in vapor chamber transport characterization for high-heat-flux applications. Advances in Heat Transfer, 45, 209-301. <https://doi.org/10.1016/B978-0-12-407819-2.00004-9>
9. Bulut, M., Kandlikar, S. G., & Sozbir, N. (2019). A review of vapor chambers. Heat Transfer Engineering, 40(19), 1551-1573. <https://doi.org/10.1080/01457632.2018.1480868>
10. Zhou, F., Zhou, J., & Huai, X. (2023). Advancements and challenges in ultra-thin vapor chambers for high-efficiency electronic thermal management: A comprehensive review. Int. J. Heat and Mass Transfer, 214, 124453. <https://doi.org/10.1016/j.ijheatmasstransfer.2023.124453>
11. Duan, L., Li, H., Du, J., Liu, K., & He, W. (2022). Research on the manufacturing process and heat transfer performance of ultra-thin heat pipes: A review. Materials, 15(15), 5459. <https://doi.org/10.3390/ma15155459>
12. Filippou, I., Tselepi, V., & Ellinas, K. (2024). A review of microfabrication approaches for the development of thin, flattened heat pipes and vapor chambers for passive electronic cooling applications. Micro and Nano Engineering, 22, 100235. <https://doi.org/10.1016/j.mne.2023.100235>
13. Hanlon, M. A., & Ma, H. B. (2003). Evaporation heat transfer in sintered porous media. Journal of Heat Transfer, 125(4), 644-652. <https://doi.org/10.1115/1.1560145>
14. Weibel, J. A., Garimella, S. V., & North, M. T. (2010). Characterization of evaporation and boiling from sintered powder wicks fed by capillary action. Int. J. Heat and Mass Transfer, 53(19-20), 4204-4215. <https://doi.org/10.1016/j.ijheatmasstransfer.2010.05.043>
15. Patankar, G., Weibel, J. A., & Garimella, S. V. (2016). Patterning the condenser-side wick in ultra-thin vapor chamber heat spreaders to improve skin temperature uniformity of mobile devices. Int. J. Heat and Mass Transfer, 101, 927-936. <https://doi.org/10.1016/j.ijheatmasstransfer.2016.05.093>
16. Yan, C., Li, H., Tang, Y., Ding, X., Yuan, X., Liang, Y., & Zhang, S. (2023). A novel ultra-thin vapor chamber with composite wick for portable electronics cooling. Applied Thermal Engineering, 226, 120340. <https://doi.org/10.1016/j.applthermaleng.2023.120340>
17. Zhang, S., Huang, H., Bai, J., Yan, C., Qiu, H., Tang, Y., & Luo, F. (2024). Experimental investigation on ultra-thin vapor chamber with composite wick for electronics thermal management. Micromachines, 15(5), 627. <https://doi.org/10.3390/mi15050627>
18. Semenic, T., & Catton, I. (2009). Experimental study of biporous wicks for high heat flux applications. Int. J. Heat and Mass Transfer, 52(21-22), 5113-5121. <https://doi.org/10.1016/j.ijheatmasstransfer.2009.05.005>
19. Khrustalev, D., & Faghri, A. (1995). Heat transfer during evaporation on capillary-grooved structures of heat pipes. Journal of Heat Transfer, 117(3), 740-747. <https://doi.org/10.1115/1.2822638>
20. Wayner, P. C., Kao, Y. K., & LaCroix, L. V. (1976). The interline heat-transfer coefficient of an evaporating wetting film. Int. J. Heat and Mass Transfer, 19(5), 487-492. <https://doi.org/10.1016/0017-9310(76)90161-7>
21. Marek, R., & Straub, J. (2001). Analysis of the evaporation coefficient and the condensation coefficient of water. Int. J. Heat and Mass Transfer, 44(1), 39-53. <https://doi.org/10.1016/S0017-9310(00)00086-7>
22. Vadakkan, U., Garimella, S. V., & Murthy, J. Y. (2004). Transport in flat heat pipes at high heat fluxes from multiple discrete sources. Journal of Heat Transfer, 126(3), 347-354. <https://doi.org/10.1115/1.1737773>
23. Ranjan, R., Murthy, J. Y., Garimella, S. V., & Vadakkan, U. (2011). A numerical model for transport in flat heat pipes considering wick microstructure effects. Int. J. Heat and Mass Transfer, 54(1-3), 153-168. <https://doi.org/10.1016/j.ijheatmasstransfer.2010.09.057>
24. Prasher, R. S. (2003). A simplified conduction based modeling scheme for design sensitivity study of thermal solution utilizing heat pipe and vapor chamber technology. Journal of Electronic Packaging, 125(3), 378-385. <https://doi.org/10.1115/1.1602479>
25. Peterson, G. P. (1994). An Introduction to Heat Pipes: Modeling, Testing, and Applications. Wiley, New York.
26. Faghri, A. (1995). Heat Pipe Science and Technology. Taylor & Francis, Washington, DC.
