# Architectural Construction Logic

Domain knowledge for Mode A, current as of v0.5. These are **general architectural rules**. They
apply objectively across building types and test cases. They must never be
rewritten as case-specific exceptions for a single image or benchmark.

This reference has priority over any conflicting element-modeling instruction in
`SKILL.md`. It does not replace the Large Form → Medium Form → Fine Form
hierarchy, the review loop, or the independent Reviewer.

## 1. Core Principle: Model Architectural Systems, Not Stacked Surfaces

Mode A must reconstruct architecture as a three-dimensional assembly of real
architectural systems.

The model must not merely reproduce the appearance of the reference image by
stacking or attaching surfaces.

For every visible architectural element, the Modeler must identify:

1. what the element is;
2. what space or assembly it belongs to;
3. what it connects to;
4. what is in front of it and behind it;
5. whether it has thickness;
6. whether it creates an opening, enclosure, support, screen, railing, finish,
   or other architectural function.

A visually similar but architecturally impossible assembly must fail review.

**The six questions presuppose that the building's primary systems exist.** Most
of §2 below is about how an element meets a floor slab, a slab edge, a landing or
a column. If the model has no slabs and no core, those questions have no
referents and the reasoning cannot be done at all — it can only be simulated.
Floor structure and vertical circulation are therefore not detail to be reached
later; they are the frame the rest of this file hangs on. See `SKILL.md` R7,
which makes them mandatory under every depth contract, visible or not.

## 2. Mandatory Architectural Relationship Reasoning

Before modeling any medium- or fine-scale architectural system, explicitly
establish its relationship to adjacent systems.

Understand and model correctly where applicable:

- wall ↔ floor/slab;
- wall ↔ ceiling/roof;
- wall ↔ window;
- wall ↔ door;
- slab ↔ column;
- beam ↔ column;
- balcony ↔ slab;
- railing/parapet ↔ balcony/slab edge;
- curtain wall ↔ slab edge;
- façade screen ↔ structural/enclosure wall;
- ceiling ↔ structural slab;
- stair ↔ floor/landing;
- roof ↔ wall/parapet;
- cladding ↔ backing wall/subframe.

These are not optional detailing knowledge. They are basic architectural
modeling knowledge and must be correct before a model can pass.

## 3. Window / Wall Relationship — Hard Rule

A window is **not a surface pasted onto a wall**.

For a normal wall-based window condition, the model must represent, at the
required level of detail:

1. a real wall or enclosure element with thickness;
2. a real opening in that wall;
3. the window/frame positioned within the opening;
4. a believable setback or alignment relative to the wall faces;
5. sill, head, and jamb relationships consistent with the reference and
   architectural logic.

Forbidden:

- placing glass directly on the exterior face of an opaque wall without an
  opening;
- allowing glass to visually overlap solid wall geometry as a substitute for a
  window;
- using a single floating plane to represent a real window system when depth is
  visible;
- leaving the wall continuous behind a visible window opening unless the
  reference clearly shows a surface-applied glass assembly.

Reviewer rule: if a visible window/glazing element does not have a valid
relationship with its wall/opening, classify as
`CRITICAL_ARCHITECTURAL_RELATIONSHIP_ERROR` and the current Level cannot pass.

## 4. Curtain Wall / Glazing Relationship

Distinguish curtain wall and large glazing systems from ordinary wall windows.

Where the reference indicates a curtain-wall system, identify:

- glazing plane;
- mullion/transom rhythm;
- slab-edge relationship;
- opaque spandrel zone if present;
- frame depth;
- corner condition;
- connection or setback relative to structural frame.

Do not model a curtain wall as a gray or transparent sheet attached arbitrarily
to the front of another façade.

## 5. Balcony / Loggia / Parapet Relationship

A balcony, recessed loggia, or external corridor is a spatial assembly, not
several unrelated planes.

Where applicable, identify:

1. front structural/façade frame;
2. balcony or corridor slab;
3. side boundaries;
4. parapet / railing / screen;
5. rear wall or glazing plane;
6. actual depth between front and rear elements.

Parapets, brick screens, and railings must terminate logically at side walls,
columns, or frame boundaries unless the reference clearly shows a gap.

Do not leave arbitrary gaps at both ends merely because the element was modeled
as a shorter rectangular surface.

## 6. Typical Floor Consistency

If the reference clearly indicates repeated typical floors, establish a
`TYPICAL_FLOOR_SYSTEM` before modeling each floor independently.

The typical-floor system should define, as applicable:

- floor-to-floor height;
- slab thickness;
- structural bay/module;
- column/vertical-frame positions;
- balcony/loggia depth;
- parapet/railing height;
- rear façade setback;
- opening positions;
- major façade module.

Repeated floors must inherit the same base system unless visible evidence shows
a deliberate variation.

Reviewer must compare repeated floors for:

- inconsistent floor height;
- inconsistent slab level;
- inconsistent parapet height;
- drifting window alignment;
- changing balcony depth;
- changing frame width;
- unexplained module differences.

Any unexplained inconsistency in an obviously repeated typical-floor system is
at least `MAJOR`. A floor-height error that changes the building's vertical
rhythm or identity may be `CRITICAL`.

## 7. Repetition: Build the Type First, Then Instance

When the reference shows repeated architectural units:

1. identify the repeated type;
2. model one correct master unit;
3. verify its geometry and architectural relationships;
4. convert it to a block/instance or controlled repeated system;
5. place instances according to the actual reference.

Do not independently rebuild each repeated unit if they are meant to be the
same. Do not array an incorrect master unit.

The repeated type must pass architectural-relationship checks before
multiplication.

## 8. Depth Must Be Explicit

At every review gate, Modeler and Reviewer must distinguish:

- coplanar;
- recessed;
- projected;
- overlapping in view only;
- physically connected;
- physically separated.

Where visible depth materially defines the architecture, use real 3D offsets.

Do not approximate a recessed façade by placing darker material on the same
plane. Do not approximate a projecting element by changing color only.

## 9. Junction Check

Perform a `JUNCTION_CHECK` on the generator unit before multiplying it, and
again across the finished assembly.

Inspect representative conditions:

- wall-window jamb/head/sill;
- wall-door opening;
- slab-balcony edge;
- parapet/slab edge;
- column/slab;
- curtain wall/slab edge;
- roof/parapet;
- façade screen/primary enclosure;
- stair/landing.

The purpose is not construction-document detailing. The purpose is to confirm
that the architectural assembly is spatially and logically valid.

A model can be visually similar and still fail if the junction logic is
fundamentally wrong.

## 10. Reviewer Gate — Architectural Relationships

`ARCHITECTURAL_RELATIONSHIPS: PASS / FAIL` is a mandatory Reviewer hard gate.

The Reviewer must not only ask:

- Does the element exist?
- Is the size approximately correct?
- Is the position approximately correct?

The Reviewer must also ask:

- Is it the correct architectural element?
- Is it connected to the correct adjacent element?
- Is its depth relationship correct?
- Does it create a real opening where required?
- Does it terminate correctly?
- Is repetition logically consistent?
- Is the element modeled as a real 3D architectural assembly rather than a
  pasted surface?

If any high-salience visible element violates basic architectural construction
logic, set `ARCHITECTURAL_RELATIONSHIPS = FAIL`. The current Level cannot pass.

## 11. Error Categories

- `WRONG_ELEMENT_TYPE`
- `WRONG_FLOOR_HEIGHT`
- `TYPICAL_FLOOR_INCONSISTENCY`
- `INVALID_WINDOW_WALL_RELATIONSHIP`
- `INVALID_CURTAIN_WALL_RELATIONSHIP`
- `INVALID_BALCONY_PARAPET_RELATIONSHIP`
- `INVALID_JUNCTION`
- `MISSING_OPENING`
- `PASTED_SURFACE_GEOMETRY`
- `WRONG_DEPTH_RELATIONSHIP`
- `UNJUSTIFIED_END_GAP`
- `REPETITION_SYSTEM_ERROR`

For every such error, the Reviewer must report:

```text
Severity:
Error class:
Reference evidence:
Model evidence:
Architectural principle violated:
Recommended correction:
```

## 12. Review Priority

### Highest priority
- overall dimensions;
- mass hierarchy;
- floor-count / large vertical rhythm;
- major voids and setbacks;
- roof/base relationship.

### Then
- typical-floor system;
- architectural depth;
- balcony/loggia/recess relationships;
- major openings;
- structural/façade rhythm;
- primary junction logic.

### Last
- windows/doors;
- curtain-wall subdivisions;
- railings/screens;
- detailed component relationships;
- materials and mapping;
- fine junctions.

An architectural relationship error found on the generator unit must be fixed on
the unit, before propagation. It must never be relabelled as later "detail work"
and multiplied.

## 13. No Visual Cheat Rule

The following must never be used as substitutes for correct architectural
geometry:

- color difference;
- material difference;
- shadow;
- transparency;
- floating plane;
- surface overlap;
- camera angle;
- entourage.

If the reference shows a real recess, opening, slab, railing, wall, or window
relationship, model it as real geometry at the appropriate Level.

## 14. Objective Adaptability

These rules remain building-type neutral.

Do not hard-code assumptions such as:

- every façade is curtain wall;
- every repeated bay has the same width;
- every balcony is recessed;
- every building uses a frame structure;
- every window is centered in a wall;
- every floor is a typical floor.

Instead:

1. identify evidence;
2. determine the applicable architectural system;
3. apply the correct system logic;
4. preserve uncertainty where evidence is insufficient.

Behave like an architect applying transferable construction knowledge, not like
a benchmark-specific script.
