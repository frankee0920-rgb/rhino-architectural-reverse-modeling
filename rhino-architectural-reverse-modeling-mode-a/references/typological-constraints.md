# Typological Constraints

Numbers, not labels. A building type is useful in reverse modeling because it
carries falsifiable dimensional expectations — so state them as ranges and use
them to **rule things out**.

All values in metres. Ranges are ordinary practice, not absolute limits; a value
outside a range is a question, not a verdict.

## 1. Universal scale references

Use these to establish absolute scale when no dimension is given. Prefer the ones
that are code-bound, because their lower limits are hard.

| Element | Range | Note |
|---|---|---|
| Person, standing | 1.60–1.85 | |
| Door leaf height | 2.00–2.10 | head at 2.05–2.15 |
| Guard / balustrade / parapet | **≥1.05** | China, building ≤24 m; **≥1.10** above 24 m. Code-bound — a strong anchor |
| Handrail | 0.85–0.95 | |
| Window sill, habitable | 0.85–1.00 | low sill 0.45–0.60 needs a guard |
| Stair riser / going | 0.15–0.18 / 0.26–0.30 | |
| Floor-to-ceiling, residential | ≥2.40 | code minimum |
| Floor-to-ceiling, office | 2.60–2.90 | |
| Car | 4.4–4.9 L × 1.8 W × 1.45 H | |
| Parking stall | 2.4–2.5 × 5.3 | aisle 5.5–6.0 |
| Traffic lane | 3.0–3.75 | |
| Street tree, newly planted | 5–8 | mature 10–18 |
| Street lamp | 8–12 | |
| Chinese standard brick | 240 × 115 × 53 | **course = 63** with joint |
| Brick pier, loadbearing | 0.37–0.80 | |
| Concrete slab edge / floor band | 0.30–0.60 | |

**Brick coursing caution.** At 63 mm a course is often below the resolution of a
web-sized photograph. If the apparent course pitch implies an implausible floor
height, you are measuring a banding pattern of several courses, not one course.

## 2. By building type

### Hotel / guest-room building
| Quantity | Range |
|---|---|
| Floor-to-floor, guest floors | 3.20–3.60 |
| Guest room width (bay) | 3.60–4.80 |
| Guest room depth incl. bathroom | 7.0–8.5 |
| Corridor width | 1.80–2.40 |
| **Wing depth, single-loaded** | **10.0–13.0** |
| **Wing depth, double-loaded** | **15.0–19.0** |
| Lobby / public ground floor, floor-to-floor | 4.5–7.5 |
| Balcony depth | 1.2–2.0 |
| Loggia depth (outdoor room) | 1.8–3.0 |

### Office
| Quantity | Range |
|---|---|
| Floor-to-floor | 3.60–4.20 |
| Planning grid | 1.35–1.50 |
| Structural bay | 7.2–9.0 |
| Lease depth, single-sided core | 12–18 |
| Ground floor / lobby | 4.5–6.5 |

### Apartment / residential
| Quantity | Range |
|---|---|
| Floor-to-floor | 2.80–3.20 |
| Unit bay | 3.30–4.20 |
| Unit depth | 9–13 |
| Corridor width | 1.50–2.00 |
| Balcony depth | 1.2–2.0 |

### School
| Quantity | Range |
|---|---|
| Floor-to-floor | 3.60–3.90 |
| Classroom | 9.0 × 6.6–7.2 |
| Corridor width | 2.40–3.00 |

### Hospital / ward block
| Quantity | Range |
|---|---|
| Floor-to-floor | 4.20–4.80 |
| Ward bay | 3.60 |
| Corridor width | 2.40–3.00 |

### Retail / mall
| Quantity | Range |
|---|---|
| Floor-to-floor | 5.0–6.0 |
| Structural bay | 8.4–9.0 |

### Museum / gallery
| Quantity | Range |
|---|---|
| Floor-to-floor | 4.5–7.0 |
| Clear span | often 12–24 |

### Industrial / warehouse
| Quantity | Range |
|---|---|
| Clear height | 6–12 |
| Span | 18–30 |

### Parking structure
| Quantity | Range |
|---|---|
| Floor-to-floor | 3.0–3.6 |
| Double-loaded bay depth | 16.1–17.0 |

## 3. Plan-logic rules — these are what rule things out

### P1. Daylight depth
A habitable room lit from one side reaches roughly **2.0–2.5 × floor-to-ceiling
height** from the window: about 6.0–7.5 m for ordinary storeys.

Consequence: a habitable plan deeper than about `2 × room depth + corridor`
cannot be solid. Above roughly 20 m of plan depth, a habitable building requires
a **court, atrium, or light well** — or its programme is not habitable (parking,
storage, retail big-box, industrial).

Apply this before accepting any depth assumption. It is arithmetic.

### P2. Corridor implication
Cellular rooms along a facade imply a corridor. A corridor implies either rooms
on the other side of it (double-loaded) or a court/exterior on the other side
(single-loaded). Both readings give a bounded wing depth — use §2.

There is no third option in which the space behind the rooms is simply solid.

### P3. Vertical circulation
Any building over three storeys needs a stair, and over four to five storeys
practically needs a lift. Both need a shaft that appears in plan and, usually, on
some elevation. If nothing in the reading can be a core, part of the plan is
missing from the reading.

This is a check on the **reading** and a requirement on the **model**. Fitting a
core into the read plan tests the plan: a footprint that cannot hold one is
evidence the footprint is wrong, and that is cheap to learn early. Then build it
— `SKILL.md` R7. A core with no image evidence is `INFERRED` and is placed by
type (centre for a square tower, offset or end for a slab, sized at roughly
15–25% of the gross floor plate for an office tower). Its being invisible in the
reference sets its evidence state; it does not make it optional.

### P4. Span plausibility
An opening in masonry wider than about 4–6 m needs visible transfer — a lintel,
a beam, an arch, or a frame. A long unsupported recess at ground level is not a
structural system; it is a misreading.

Reinforced-concrete flat slab spans 6–9 m; with beams, 8–12 m. A read grid far
outside that needs an explanation.

### P5. Symmetry default
Repetitive building types are usually set out symmetrically about the facade.
A reading that produces an unexplained asymmetry in end conditions is more likely
a wrong element decomposition than a real asymmetry — re-examine what the
outermost elements actually are.

### P6. Ground-floor difference
Public ground floors are usually taller than the floors above (see §2) and
usually have a different structural rhythm — often piers at every bay, or every
second bay. Do not assume the upper rhythm continues to the ground; look.

## 4. How to use this file

1. Name the type from the reading.
2. Write out the ranges that apply.
3. Write out **what they rule out** — the contradiction, in numbers.
4. If the reading survives, the type supports it. If not, either the reading is
   wrong or the type is wrong. Say which you think it is, and why.

Step 3 is the whole point. A type recorded as a label constrains nothing; in
production a building was correctly identified as a hotel and still modelled with
a plan depth that the type forbids, because the label was never turned into
arithmetic.
