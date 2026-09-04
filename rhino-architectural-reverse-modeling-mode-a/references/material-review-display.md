# Material Review Display

Display-mode rules for Mode A v0.9. Overrides any conflicting display guidance.

## Separate geometry and material review

Use one white/clay display mode for all geometry review. Judge proportion,
mass relationships, setbacks, offsets, recess/projection, component placement
and architectural geometry. Do not use materials or rendering to conceal
geometry errors.

## Material review mode

For material review, prefer the installed Rhino display mode
corresponding to `Arctic mode with material` as `MATERIAL_REVIEW_MODE`.
Query the current Rhino Display Mode name and ID first. Use the exact returned
name or ID; never invent or normalize it.

Use a typed Display Mode tool if one exists. Otherwise use the available Rhino
Python or Rhino Command adapter.

## Keep the camera fixed

Continue from the passed Review Camera. When switching to material review,
change only Display Mode. Do not change Camera, Target, Up, Projection, Lens,
crop or frame.

Maintain:

- `BASIC_REVIEW_VIEW`: fixed Review Camera + white/clay mode.
- `MATERIAL_REVIEW_VIEW`: identical Camera + `MATERIAL_REVIEW_MODE`.

## Precondition — checks 4 and 5 need a texture to exist before they can run

Checks 4 and 5 measure texture scale and UV mapping. A material carrying only a
diffuse colour gives them nothing to measure, so they return neither PASS nor
FAIL. Left unreported, that silence is indistinguishable from a pass, and a
model whose materials are all colour walks the entire material review untouched.

**Classify every material into exactly one of these before running any check,
and report the classification.** This is the first thing material review
produces, not an aside.

| State | Meaning | What follows |
|---|---|---|
| `TEXTURED` | bitmap present and mapped | run checks 4 and 5 normally, **and check the recorded texture source** |
| `COLOUR_BY_DECISION` | the reference shows no surface pattern, or the depth contract puts this surface at a fidelity where colour is the answer, or no reference covers the surface at all | record the reason in one line; 4 and 5 do not apply |
| `TEXTURE_ABSENT` | the reference shows a surface pattern and the material has none | **defect, same severity as an unassigned material** |

`TEXTURE_ABSENT` is not a lower fidelity level. A material named for its surface
— coursed brick, sawn timber, split stone, brushed metal, any textured concrete
— cannot be delivered as a colour without becoming a different material. Where
the whole character of a building rests on one such surface, treat it as
`CRITICAL`.

Texture scale is a **real-world dimension**. Measure it against something known
in the reference — course height, board width, panel joint, plank width — and
report the number, not an impression.

For every `TEXTURED` material, the parameter file must name a source state:
`FROM_REFERENCE`, `PROCEDURAL` or `LIBRARY` (see `SKILL.md`
`# MATERIAL, SCENE AND SURROUNDINGS`). A texture with no recorded source is
`TEXTURE_PROVENANCE_UNRECORDED`; a texture that is plainly not the reference's
surface and is presented as if it were is `TEXTURE_INVENTED`, and that is the
material-side violation of R1, not a housekeeping lapse.

A `FROM_REFERENCE` texture is checkable in a way the others are not: its px/m is
recorded, so its mapping size can be recomputed and compared. Do that rather
than judging the scale by eye.

## Material checks

Check:

1. Material assignment to the correct objects.
2. Material identity: wood, stone, metal, glass, concrete, and other categories.
3. Material boundaries against the reference.
4. Real-world texture scale. Reject oversized brick, distorted wood grain, and
   incorrect stone-joint proportions.
5. Mapping/UV direction, stretch, rotation, continuity and repetition.
6. Shared material consistency across repeated Blocks/components.

## Cause classification

Classify every abnormal material display before editing:

- `DISPLAY_MODE`
- `MATERIAL_NOT_ASSIGNED`
- `TEXTURE_ABSENT`
- `TEXTURE_INVENTED`
- `TEXTURE_PROVENANCE_UNRECORDED`
- `WRONG_MATERIAL_IDENTITY`
- `TEXTURE_SCALE`
- `UV_MAPPING`
- `MAPPING_NOT_SET` — texture present, but the object carries no mapping, so the
  surface's natural parameterization sets the scale. On a boxy Brep this differs
  face to face and cannot be corrected by editing the material.
- `MATERIAL_BOUNDARY`
- `GEOMETRY_ERROR`

Fix the Display Mode first when it is the cause. Return to the appropriate
modeling level when geometry is the cause. Do not repeatedly edit a material
without identifying the cause.
