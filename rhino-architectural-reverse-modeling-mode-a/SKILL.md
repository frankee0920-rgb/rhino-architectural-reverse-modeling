---
name: rhino-architectural-reverse-modeling-mode-a
description: >
  Build an editable Rhino architectural model from reference photographs of a building.
  Use when the user supplies one or more images of a real building and wants it modelled,
  measured, or reverse-engineered in Rhino. The goal is a model that is both EDITABLE
  (named components, one architectural decision = one editable object) and DIMENSIONALLY
  DEFENSIBLE (every load-bearing dimension measured two ways, or explicitly asked about).
  Not photogrammetry, not a pixel-perfect copy, not a single carved solid.
---

# Rhino Architectural Reverse Modeling — Mode A

**Version 0.9**

## What this is

A **constraint set**, not a procedure.

v0.3 and v0.4 prescribed staged workflows (`LEVEL_1/2/3`, then `Phase A/B/C`).
Both were scaffolding for a weaker model and became drag on a stronger one: they
consumed attention on process that should have gone into looking at the building.
The staging is gone.

What remains is what does not lose value as the model gets better: domain facts,
executable checks, output constraints, and tool traps.

Work in whatever order the building suggests. Satisfy the seven hard rules, know
the five things listed under *Before geometry*, and meet the editability
contract. Nothing else is prescribed.

**Exhortations have been deleted.** "Understand the architecture first" was in
v0.3 and did not prevent a building being modelled as a slab when it was one end
of a courtyard block. If a lesson is not a check that can fail, it is not in this
file.

v0.6 adds what deleting the staging took with it. The staging prescribed an
order, which was drag; it also happened to define *when a level was finished*,
which nothing replaced. The result was a skill that could tell you a model was
wrong and never that it was unfinished. v0.6 restores the definition of finished
without restoring the order: a depth contract agreed before geometry, checked
against the model before delivery. It also closes the gap the checks did not
cover — reading *inside* one source was tested, transferring scale *between*
sources was not.

v0.7 closes three holes through which a *complete-looking* delivery escaped.
Each one was a place where this file said "optional" about something that is not.

The depth contract could delete the building's structure — nothing set a floor
under it, so a contract offered with floor slabs bundled into the top tier
deleted them with the user's apparent consent. R7 puts the floor in. The scene
axis could delete what the photograph plainly shows, because it conflated *what
exists* with *at what fidelity*; those are now separate questions and only the
second one is the contract's. And the two review gates carried an escape hatch —
"if the environment will not let you spawn a reviewer, say so" — which turned out
to be all a session needed to skip both and self-check instead. The gates are now
unconditional, and the disclosure, if it is ever needed, moves to before geometry
where it is still worth something.

v0.8 fixes the delivered view. v0.7 required the file to open parked on the
primary reference camera, required a named view as well, and required both to be
verified by reading the saved file from disk. All three were done, and the user
opened the file and saw the bottom half of the building. Nothing in the file
could fail on *usable*, because framing a tall building from eye level is a
frustum problem and no rule here mentioned the frustum. v0.8 adds the usability
check and the arithmetic that predicts it, and it retracts a `TOOLING.md` entry
that had written up the correct mechanism as a hazard.

v0.9 closes the material axis. Every rule in this file about material was about
*identity* and *boundaries* — which material, and where it changes. Nothing said
what a material has to consist of. Texture appeared only in
`material-review-display.md`, and only as two checks that presuppose a texture
already exists. So a model whose materials carry a diffuse colour and nothing
else walked the whole material review without a single check firing: the texture
checks had nothing to measure, and silence read as pass. v0.9 makes the absence
of a texture a statable, failable condition, and puts texture resolution on the
depth contract where the user can see it being decided.

It also gives a texture an evidence state. Every dimension in this file has had
one since v0.5, and a texture had none — so an image picked because it looked
about right was indistinguishable from the building's own surface, and one of
the ways to obtain a texture reaches outside the machine and carries a licence.
Both are now decisions the file makes visible rather than assumptions it leaves
to whoever is applying the material.

The last thing v0.6 changes is where the architecture is enforced. Until now the
modeler's own verification was entirely camera-and-silhouette based, and every
architectural-assembly rule lived either in `REVIEWER.md` or in a reference file
with no hook into the workflow. A modeler who did not spawn a reviewer had no
mechanism that could fail on 3D assembly logic at all. R6 gives it one.

## Supplemental files

| File | Read when |
|---|---|
| `references/checks.md` | before measuring anything |
| `references/typological-constraints.md` | before assuming any dimension |
| `references/architectural-construction-logic.md` | **R6 — before modelling any system, and again on the assembly** |
| `TOOLING.md` | before driving Rhino or capturing an image |
| `references/material-review-display.md` | before material review |

# THE SEVEN HARD RULES

Each one can fail. Each one caught, or would have caught, a real production
error.

## R1 — Never invent a principal dimension. Ask.

A principal dimension is one that changes the model globally: overall extent in
any axis, plan figure, storey count, floor-to-floor, structural grid, or the
absolute scale anchor.

If a principal dimension has **no image evidence**, you may not choose a number
on your own. You must:

1. say plainly that there is no evidence;
2. give the plausible range and where it comes from
   (`references/typological-constraints.md`);
3. name the one image that would settle it — corner view, side elevation,
   aerial, plan;
4. ask.

Tagging an invented number `ASSUMED` or `LOW_CONFIDENCE` is **not** compliance.
A confidence label records; it does not control. In production a fabricated
building depth propagated through three rebuilds and a 94/100 review because it
carried a label instead of a question.

Batch all such questions into **one** message. Do not drip-feed them.

## R2 — The model must be editable.

**One architectural decision = one editable object, or one parameter.**

- Semantic name and layer are set **in the same operation that creates the
  object**. Naming later does not work; by then the geometry has no element
  boundaries to name.
- Boolean operations shape **one** component. A boolean that merges distinct
  architectural elements into one solid is forbidden.
- A single carved solid standing for several architectural systems is a defect
  even when its silhouette is perfect.
- Store driving parameters as object user strings, so a later session can recover
  intent from the file rather than from a script it does not have.

Test, and state the result: pick three parameters at random and confirm each can
be changed by editing named objects. If any requires deleting the model and
re-running a build script, the model fails.

## R3 — Two signals and closure, or say so.

A load-bearing dimension needs **two signals that fail differently**. Two
measurements of the same edge with the same detector are one signal.

Every grid must close: `sum(parts) == measured overall`, residual reported.

Single-signal values are legal but must be labelled as such. Never present one
signal as measured fact.

## R4 — Run the impossibility checks before building on a reading.

`references/checks.md` §1. They are cheap and each has caught a real error. The
convex-visibility check alone would have prevented the largest misreading in
production.

## R5 — Verify a capture before comparing anything to it.

A stable camera does not imply a reproducible capture. Rhino's capture scale
depends on the viewport's own pixel size, which can change silently mid-session.
Measure the building's pixel extent in every capture and compare it to the
expected value **before** cropping. `TOOLING.md` §3.

## R6 — Say what each system connects to, before you build it. Then check the junctions.

Reverse modelling from images rewards producing the right *appearance*. Every
self-check in this file that compares model to reference is a frontal-image
check: silhouette, proportion, rhythm, solid/void. An assembly can be
architecturally impossible and pass all of them, because the impossibility is
invisible from the camera you are comparing against.

**Before modelling any architectural system**, answer
`references/architectural-construction-logic.md` §1 for it, in writing, in the
parameter file:

```text
what is it
what space or assembly does it belong to
what does it connect to
what is in front of it and behind it
does it have thickness
what does it do — opening, enclosure, support, screen, railing, finish
```

If you cannot answer "what does it connect to", you are not ready to build it.
Six short lines per system; the systems are few.

**After the assembly is built**, run the `JUNCTION_CHECK` (§9 of the same file)
on the representative conditions listed there. It is not detailing. It asks
whether the assembly is spatially possible.

*Production failure:* a first-floor roof terrace was modelled by cutting the same
opening out of the roof slab **and out of the floor the terrace stands on**, so
the terrace had no floor and the building was open to the ground. Roof screen
walls were built as four traced fragments with both ends in mid air. A window
frame 80 mm deep was set 30 mm into a 200 mm opening, leaving a 90 mm raw slot
behind it. Every one is obvious in one glance from any oblique view. Every one
passed a silhouette comparison that matched the reference photograph to 0.2%,
because none of them is visible from the front.

## R7 — Model the building, not its photograph.

A reverse model is a building. Its floor structure and its vertical circulation
exist whether or not a camera can see them.

**Mandatory in every architectural model, under every depth contract:**

| Element | Why it cannot be optional |
|---|---|
| a floor plate at every storey level | storey levels are usually the *best-measured* quantity in the whole model; a model without them throws away the one thing the reading actually established |
| vertical circulation core — stair and lift shafts | `typological-constraints.md` P3. Without it the model is N plates with no way between them, and the plan has never been tested for whether a core fits it |
| ground meeting | the building stands on something |
| roof and its closure | the building is closed |

**Visibility is not the test.** "Not visible in the reference" is the reason a
dimension is `INFERRED`. It is never a reason for an element to be *absent*. An
inferred core in a plausible position is a modelling statement a later session
can correct. No core is a building that cannot work, with nothing in the file
saying so.

Half of `architectural-construction-logic.md` §2 is unanswerable without these:
wall ↔ slab, curtain wall ↔ slab edge, stair ↔ landing, slab ↔ column. A model
with no slabs cannot really pass R6 either — the questions have no referents.

The depth contract sets the **resolution** of these elements: a slab may be a
plate or a full floor assembly, a core may be a shaft or a modelled stair and
lift group. It never sets whether they exist.

*Production failure:* a 35-storey office tower was delivered as five solid boxes
carrying a curtain-wall system. No floor plates, no core, nothing inside. Every
gate was green, the silhouette matched the reference at 0.94 IoU, and the storey
rhythm had been measured two independent ways and closed to 30 mm — a number the
delivered model did not contain anywhere. The depth contract had been offered
with "floor slabs" bundled into the highest detail tier, which the user did not
pick, so the omission looked authorized. It was not. The contract is not allowed
to reach this far down.

# BEFORE GEOMETRY

Five things must be known. There is no prescribed order and no gate ceremony —
but building without them produces work that gets thrown away.

## 1. Depth contract — what is being delivered?

Agree this with the user **before** building, in the same message as the R1
dimension questions. It costs one exchange, and it is the only thing that makes
*unfinished* a statable condition.

Three axes. Each needs an explicit line; none has a safe default.

| Axis | The question |
|---|---|
| Geometry resolution | above the R7 baseline: massing, envelope with real openings and frames, or full element detail |
| Material | which surfaces carry a real material, **at what texture resolution**, and how each one is evidenced |
| Scene and surroundings | at what fidelity the setting is built, and how far out — *what exists* is not on this axis |

**The material axis is not answered by a list of material names.** A list of
names is what the surfaces *are*; the axis also has to say what they are *made
of* in the model — textured and mapped, or colour only — **and where any texture
comes from**, since one of the sources requires the user's permission before you
can use it. Offer that as the choice it is, because the options cost very
different amounts and only some of them deliver a material whose name is about
its surface. An axis answered as "these four materials" and nothing else
resolves to colour by default, and the default is invisible to every check in
this file — see `# MATERIAL, SCENE AND SURROUNDINGS`.

### The contract has a floor, and you may not offer options below it

The contract varies **resolution**. It never varies:

- whether the building is a complete architectural system — R7;
- whether something the reference plainly shows exists at all — see
  `# MATERIAL, SCENE AND SURROUNDINGS`.

**You write the options, so a bad option is your defect, not the user's choice.**
A user selecting wording that removes a mandatory element has not authorized the
omission; they have accepted a menu that should never have contained it. Before
putting the contract to the user, read your own options back and ask: *does any
of these describe a building with no floors, no core, or a scene missing
something plainly in the photograph?* If yes, rewrite it.

Every axis is offered **above** the baseline. "Massing only" means the massing of
a complete building — volumes, slabs, core — not a hollow shell.

A related trap in how the contract gets framed: it is natural to sort the options
by *what the reference can resolve*, because that is what you have been staring
at. Reference resolution governs how precisely an element is modelled and whether
its dimensions come out `MEASURED` or `INFERRED`. It has no bearing on whether the
element is in the building. Sorting by legibility is exactly how floor slabs —
typically the best-measured thing available — end up in the same tier as
curtain-wall joint patterns that sit below the image's resolution floor.

Write the answers down. Before delivery, walk the model against them item by
item — see `# DELIVERABLE`.

A model can satisfy every hard rule, close its dimension chain and match the
reference silhouette, and still be at the wrong resolution. **Every check in this
file will call that model green.**

*Production failure:* depth was agreed as "complete exterior". The model was
built, every gate passed, and it was delivered with no window frames, no
glass/solid distinction at ground level, and roof rooms modelled as wall strips.
The contract existed. Nothing ever compared the model to it.

## 2. Extent — what am I actually looking at?

```text
Complete building, or one face of something larger?
Is each silhouette edge a real corner, or a crop, an occlusion, or a junction
  with an adjoining volume?
Plan figure: slab, courtyard/perimeter, L, U, tower, unknown?
Is the visible facade the long side or the short side?
```

A real corner shows: the facade terminating in an end wall with the grid closing,
a visible return face, the roofline stopping. Not a corner: the grid running off
frame, an abutting volume, the frame cutting the silhouette.

This is the most expensive thing to get wrong, because no amount of measurement
precision detects it and every later step inherits it.

## 3. Typological constraints — as numbers

Naming the type is worthless. A type is useful because it carries falsifiable
numeric expectations. Produce them, and produce **what they rule out**.

`references/typological-constraints.md` has the ranges and the plan-logic rules.

Worked example of the mechanism: hotel → habitable wing depth 10–19 m → a 32 m
wide plan cannot be a solid slab; it is a courtyard, a double bar, or the type is
wrong. That contradiction is *arithmetic*, not intuition, which is why it belongs
here.

## 4. Generator — what, once fixed, determines the rest?

Ask it openly. Repetition is the most common answer, not the only one.

| Organizational logic | Generator | Build order it implies |
|---|---|---|
| Repetitive cellular / framed | typical bay or unit | unit → instance → exceptions |
| Freeform / continuous surface | control curves and rules | control geometry → surface → panelization |
| Composed volumes | volume set and transforms | volumes → relationships → junctions |
| Extruded / profile | section + path | section → sweep → ends |
| Centralized / symmetric | generatrix + transform | generatrix → revolve/mirror → openings |
| Rule-driven envelope | rule + driving field | rule → apply to carrier → exceptions |

Two consequences that always hold:

- **Build and verify the generator before multiplying it.** An unverified unit
  arrayed 190 times is 190 errors. This is the cheapest check available.
- **Exceptions come last** — corners, ends, ground meeting, roof termination,
  entrances, junctions between systems. Their definition depends on the generator
  being resolved. Most of the real architectural thinking lives here; budget for
  it.

If no organizing logic can be found, say so and treat it as composed volumes.

## 5. Dimension chain

Dimensions derive from each other, not independently. Record the derivation and
the evidence state:

| State | Meaning |
|---|---|
| `USER_GIVEN` | supplied by the user |
| `MEASURED` | two independent signals agree and the grid closes |
| `INFERRED` | one signal, or derived from measured values |
| `TYPOLOGICAL` | no image evidence; range stated, user informed |
| `FABRICATED` | invented. Forbidden — see R1 |

The absolute scale anchor is **provisional**. If later measurement falsifies the
reasoning that justified it, say so, quote old and new, keep the user's number
unless they change it, and record the equally-good alternative.

One parameter file is the single source of truth, and it never disagrees with the
Rhino model. If geometry changes, it changes in the same step.

# VERIFICATION

## After every geometry operation

`analyze_objects`: validity, closed-solid state, naked-edge count, bbox against
intent. Near-zero cost; run it always.

## Against the reference

Clay/white display, camera comparable per `TOOLING.md` §4, registered capture per
R5, then overlay and difference. Judge silhouette, proportion, rhythm, and
solid/void relationships.

**Camera tolerance: same view class, verticals treated as in the reference,
building occupying the frame within ±5%, same aspect ratio. Once inside, stop.**
Sub-pixel camera matching is optional refinement, never a prerequisite, and never
a reason to alter geometry.

## Measurement effort

Measure to the precision the current decision needs. Do not pursue residuals
below the reference image's own distortion floor (`references/checks.md` §5).

## Independent review — two gates, and only two

**Gate 1 — early screen.** Once, as soon as the mass and the dimension chain are
fixed and before any detail is built. It checks three things only: extent,
generator, dimension-chain closure. It does **not** check completeness — nothing
is finished yet, and a reviewer reporting missing detail here is reporting noise.

Its whole justification is cost. A reading error caught here costs a re-reading.
The same error caught at Gate 2 costs the model.

**Gate 2 — delivery gate.** When you believe the model is finished. It checks
everything, including conformance to the depth contract. **Nothing is delivered
until it passes.** After it passes the model is final: the user receives a
finished model, not a review to perform.

No other rounds. Not for a parameter change — in production four full rounds ran
on what were mostly numeric adjustments, and the reviewer's genuine catches were
architectural, not numeric.

**Both gates are mandatory. Neither is conditional on being asked for.**

Invoking this skill **is** the request to spawn reviewer agents. A host rule of
the form "do not spawn agents unless the user asks" is already satisfied: the
user asked, by invoking a skill whose deliverable is *defined* as review-passed.
Do not put the question to the user, and do not read the absence of a separate,
explicit request as a prohibition.

If a gate genuinely cannot run — the capability is **absent**, not merely
unrequested — that is a blocking condition, and it surfaces **before geometry**,
batched with the R1 questions, while it still costs a re-reading instead of the
model. Raising it for the first time in the delivery is too late by construction:
Gate 1 exists precisely because an error caught there is cheap, so a Gate 1
disclosed at handover has already forfeited everything it was for. A delivery
silent about review reads as reviewed.

**Self-checking is not a reduced form of review; it is a different thing that
cannot do this job.** Every check you can run sits downstream of your own reading
and your own measurement chain. It will catch internal contradictions — and it
should, they are cheap — but a chain that is wrong end to end is invisible to it.

*Production failure:* a session read a host rule as forbidding subagents, skipped
both gates, self-checked instead, and disclosed it in one line at the top of the
delivery. The self-checks were genuine and caught a real error — a px/m factor
applied to a point lying on a different plane. Every one of them ran on the
modeler's own chain. The absolute scale anchor, the plan closure, an entirely
missing floor structure and a missing core all passed straight through, and the
delivery presented the result as verified.

Give the reviewer `REVIEWER.md`, the references, the registered capture,
comparison outputs, an axonometric, the parameter file, the depth contract,
**and the object list** — editability and completeness are judged from names and
counts, not from pictures.

The reviewer must re-derive load-bearing quantities with a **different extraction
method**. Independent judgment over a shared method launders systematic error
rather than catching it: in production the reviewer and the modeler anchored on
the same contaminated datum and produced two different wrong values.

# WHAT NEVER SUBSTITUTES FOR GEOMETRY

Colour, material, shadow, transparency, a floating plane, surface overlap, camera
angle, entourage.

If the reference shows a real recess, opening, slab, railing, wall or window
relationship, model it as real geometry.

Nor does a lower-dimensional stand-in: a room modelled as its wall, a volume as a
plane, a solid as a strip.

If a contour trace is how you obtained a footprint, check what the contour was a
contour *of*. Tracing wall pixels and extruding them gives you a wall. If the
reference shows a room there, you have built the wrong element — and it will read
as correct in plan and wrong in every oblique view.

*Production failure:* roof-level enclosures were produced by tracing wall pixels
from a roof plan and extruding them. The elevation photograph shows an enclosed
room with a window at that position. The axonometric showed open-ended strips
standing on the roof.

# MATERIAL, SCENE AND SURROUNDINGS

Part of the deliverable, not a finishing touch. Governed by the same rules as
geometry.

**R1 applies to material identity.** A material you cannot see in any reference
is a principal decision about how the building looks. Do not choose one silently.
Ask, or state the range and what would settle it — exactly as for a dimension.

**Material identity includes surface, and a diffuse colour does not carry it.**
Architectural materials are named by their surface, not their hue:
bush-hammered concrete, board-marked concrete, split-face stone, coursed brick,
brushed metal, sawn oak, woven mesh. Every one of those names is a claim about
aggregate, grain, joint or weave, and none of it survives being reduced to an
RGB value. A contract line reading "concrete" that renders as flat grey has not
been delivered at a lower fidelity; it has been **renamed**. The same applies to
any material whose reference shows a pattern at all.

Decide it per material, in one line, and write the decision down:

```text
does the reference show a surface pattern on this material?
  yes -> it needs a texture and a mapping. Texture scale is a real-world
         dimension and is measured, not eyeballed.
  no  -> colour is the correct answer. Say which it is: a flush painted
         surface, clear glass, a schematic scene stand-in, or an unseen
         surface carrying no evidence at all.
```

**A texture carries an evidence state, exactly as a dimension does.** Where it
came from is part of the deliverable, and an unrecorded source is the material
equivalent of an unlabelled number. Record it per material in the parameter file:

| State | Meaning |
|---|---|
| `FROM_REFERENCE` | a patch of the reference itself — rectified, de-lit, made tileable. Record which image, and the px/m used to set its real-world size |
| `PROCEDURAL` | synthesized locally. Record the parameters, so a later session can regenerate it |
| `LIBRARY` | an external source. Record the source and its licence |
| `INVENTED` | an image chosen because it looked about right, with no stated relation to the reference. **Forbidden — this is R1 on the material side** |

`FROM_REFERENCE` is usually both the strongest and the cheapest. The reference
is already the material evidence, and by the time materials are applied its
scale is already known from the measurement work — which turns texture scale
into a *measured* quantity rather than a slider. Prefer it for any surface the
reference samples cleanly and close to frontally.

`PROCEDURAL` is the right answer where the reference cannot sample a surface
cleanly — ground cover, gravel, distant scene material, anything only ever seen
obliquely or at low resolution. An isotropic synthetic tiles better than a
salvaged crop and carries no licence.

`LIBRARY` is legitimate, and sometimes the only route to a full PBR set. It is
never *this* building's surface, so say so rather than letting it read as
evidenced. **Downloading is an outward-facing action and a licensing decision:
ask before doing it.**

**Absence of a texture is a finding, not a silence.** `material-review-display.md`
§4 and §5 measure texture scale and UV mapping. On a material that has no
texture there is nothing for them to measure, so they return neither PASS nor
FAIL — which means a model of colour-only materials passes material review by
default, untouched. Report the state explicitly per material; the reference file
names the three states and their severities.

*Production failure:* a depth contract named four materials, one of them a
surface treatment that was the building's dominant characteristic. Every one was
created as a layer material with a diffuse colour, a transparency and a shine
value, and nothing else — no bitmap, no mapping. Material assignment was
correct, boundaries were correct, every object rendered in the right layer's
material, and the two checks that would have caught it could not run. The
surface the building was known for was delivered as a flat tone, and no gate
could say so.

**Material boundaries are geometry boundaries.** Where the reference shows the
material changing, something changes there: a plane, a recess, a joint, a
different element. Painting a boundary across a continuous surface is the
material-side version of a floating plane, and `WHAT NEVER SUBSTITUTES` applies.

**Surfaces no reference shows carry no material evidence.** Name them, in one
line. Do not let a plausible guess enter as fact because it renders well.

**Scene extent is contract, not taste — but existence is the reference's call,
not the contract's.** Ground plane at minimum: the building meets it and every
reference photograph shows it.

Beyond that, split the question in two, and do not let the contract answer the
first one.

- **What exists** is set by the reference. Anything the photograph plainly shows
  as part of the setting — street trees, the terrain the building stands
  against, lamp columns, road markings, vehicles, adjoining buildings — is part
  of the scene and must be represented. A reference showing a wooded ridge behind
  the building and a row of street trees along its frontage does not describe a
  building on a bare plane.
- **At what fidelity** is the depth contract's third axis. A street tree may be a
  sphere on a stick. A hill may be one coarse mesh. A neighbouring block may be
  an untextured box. Those are legitimate contract choices, and a schematic
  stand-in is a real answer — it records that the thing is there.

**Absent is not a fidelity level.** If the contract puts something at the lowest
fidelity, model the stand-in. If the contract genuinely excludes it, name it in
the delivery as excluded — so "not there" is never confusable with "not noticed".

*Production failure:* a dusk photograph of an office tower showed a forested
ridge filling the right third of the frame, a row of street trees along the
frontage, and lamp columns down the near footpath. The scene axis was offered as
"ground / ground + road / ground + road + surrounding volumes", the middle option
was chosen, and the model was delivered on a bare grey plane with a road on it.
Nothing in the file recorded that a hill had ever been in the picture.

`references/material-review-display.md` governs how to review this. By then
camera and geometry are fixed; only Display Mode changes.

# STOP AND ASK

- a principal dimension has no evidence (R1);
- a principal dimension has two sources whose cross-source ratio check fails
  (`references/checks.md` §1.7) — evidence existing is not evidence agreeing;
- two readings are equally plausible and change the model materially;
- two references conflict and the conflict changes geometry;
- a discovery invalidates something the user already approved;
- three correction attempts on the same defect have failed.

Asking early is cheap. In production, four one-sentence answers from the user
resolved what unaided derivation had spent most of a session failing at, and got
two of them wrong. **The user is the highest-accuracy, lowest-cost evidence
source available. Use them first, not last.**

# DELIVERABLE

**One finished model.** Complete to the depth contract, walked against it item by
item, passed at Gate 2, and final. Named components, semantic layers,
blocks/instances — that is what makes it editable, not a separate artefact.

**Saved with the Perspective viewport parked on the primary reference camera.**
The file must *open* on that view. A named view the viewport is not sitting on
does not satisfy this — the person opening the model would see whatever camera
was last used, which is never the one that matters.

The primary reference is the image the user designated as the main view. The
delivered image is a capture from this same view, and it is the view every later
comparison starts from.

Check, and it can fail: **read the camera out of the saved file on disk**, not
out of the live session. The session is not the deliverable and it drifts — an
orbit, a display-mode change or a projection toggle after the save leaves the
session looking right and the file wrong, or the file right and the session
wrong, with nothing to tell the two apart. `TOOLING.md` §6 has the recipe, and
the toggle that causes it.

The camera read from the file must match the primary-reference camera inside the
comparability tolerance — same view class, verticals treated as in the reference,
building within ±5% of the reference framing, same aspect ratio.

**And it must be usable.** Open the file and look: is the whole building in the
viewport? A parked camera that shows half the building satisfies every sentence
above and defeats all of them. This one is not a matter of taste — it is
arithmetic, and you can see it coming before you ever set the camera:

```text
a building of height H seen from eye level at distance D rises
    atan((H - eye) / D)   above the horizon
a symmetric frustum must be at least that half-angle in the vertical, and in a
landscape viewport the horizontal half-angle grows with it by the aspect ratio
```

For a 146 m tower at 116 m that is 51° above the horizon. A symmetric frustum
puts the horizon at mid-frame, so an ordinary landscape viewport shows the lower
half of the building and sky-less air below it. **Architectural photographs of
tall buildings are shifted, not symmetric** — that is exactly why the reference
is a portrait frame with the horizon near the bottom.

So when the reference has parallel verticals, deliver a **shifted (asymmetric)
frustum**. `TOOLING.md` §6.1 has the mechanism, and it keeps the camera at the
real eye height and the real station point — which is the entire point of a
reference camera.

**Do not fix the framing by moving the camera.** Raising it to mid-height, or
tilting it up, will show the whole building, and it is no longer the reference
camera: every comparison made from it is measuring a different photograph.
Framing is a frustum problem. Solve it in the frustum.

*Production failure:* a 146 m tower was delivered with the viewport parked on a
verified reference camera — right station point, horizontal axis, parallel
verticals, confirmed by reading the camera out of the saved file on disk. The
user opened it and saw the bottom half of the building. The camera had been
designed around a tall crop of a tall capture, and nothing had ever asked whether
it worked in a viewport. The first repair attempted was to raise the camera 56 m,
which framed the building nicely and silently threw away the station point the
whole reconstruction was built on.

**A named view is required, and it exists for a person, not for you.** Store the
camera as a named view as well, so it survives someone orbiting, and **tell the
user its name in the delivery**: it is a control they click, and a control they
do not know about does not exist. The parked viewport and the named view are two
separate requirements and both must hold — the viewport so the file opens right,
the named view so the view can be got back after it does not.

Two things travel with it. Both exist so the model can be edited later. Neither
is work handed to the user to audit:

- the parameter file — every driving dimension, where it came from and how it was
  derived, stored also as object user strings so a later session recovers intent
  from the file, plus the R6 six-line answer for each architectural system;
- one page — the decisions you made on the user's behalf, anything this
  reference set genuinely cannot determine, and **the name of the named view**
  that restores the primary camera.

Do **not** deliver: review views for the user to review, evidence-state
inventories, per-revision narrative files. Evidence states are the discipline
that stops you fabricating numbers while you work. They are not the product.

The user asked for a model. Hand over a model.
