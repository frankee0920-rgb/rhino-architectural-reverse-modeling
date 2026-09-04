# Rhino Architectural Reverse Modeling — Mode A

A [Claude Code](https://claude.ai/code) skill for turning reference photographs of a
real building into a Rhino model that is **editable** and **dimensionally defensible**.

Not photogrammetry. Not a pixel-perfect copy. Not a single carved solid.

## What it optimises for

Most image-to-model workflows optimise for *looks like the photo*. That is easy to
reach and hard to build on: the result is usually one boolean-carved blob whose
dimensions are eyeballed, and which nobody — including the model that made it — can
tell you is wrong.

This skill optimises for two different things:

- **Editable** — one architectural decision equals one named, editable object.
  Changing the loggia depth must not require deleting the model and re-running a
  script.
- **Dimensionally defensible** — every load-bearing dimension is either measured two
  independent ways, given by the user, or explicitly flagged as unevidenced and
  *asked about*. Inventing a principal dimension and labelling it low-confidence is
  forbidden.

## Design

It is a **constraint set, not a procedure.**

Earlier versions prescribed staged workflows (`LEVEL_1/2/3`, then `Phase A/B/C`).
Staging turned out to be scaffolding for a weaker model that becomes drag on a
stronger one — it spends attention on process that should go into looking at the
building. It was also ordered by geometric scale, which does not correlate with
where the risk is: the largest dimension in a building can be the one with no
evidence at all.

So the staging was deleted. What remains is what does not lose value as the
underlying model improves:

| Kept | Why |
|---|---|
| Domain facts | typological dimension ranges, construction logic — things a model will not reliably recall |
| Executable checks | each one can fail; each caught a real error |
| Output constraints | editability, naming, no fabricated dimensions |
| Tool traps | silent failure modes in the Rhino MCP layer |

Every exhortation was removed. *"Understand the architecture first"* was in an
early version and did not prevent a building being modelled as a slab when it was
one end of a courtyard block. **If a lesson is not a check that can fail, it is not
in the file.**

## Contents

```
rhino-architectural-reverse-modeling-mode-a/
├── SKILL.md                                  the constraint set — hard rules, what to
│                                             establish before geometry, verification
├── REVIEWER.md                               brief for an independent reviewer sub-agent
├── TOOLING.md                                Rhino MCP capability boundary, capture
│                                             recipes, and the traps that fail silently
├── references/
│   ├── architectural-construction-logic.md   wall/window, curtain wall, balcony/parapet,
│   │                                         slab/support, repetition — modelled as real
│   │                                         assemblies, never as stacked surfaces
│   ├── checks.md                             impossibility checks, two-signal rule,
│   │                                         detector contamination, datum ranking
│   ├── typological-constraints.md            numeric dimension ranges by building type,
│   │                                         plus plan-logic rules that rule things out
│   └── material-review-display.md            display-mode and material review rules
└── tools/
    ├── reference_prep.py                     crops and metadata from a reference image
    ├── compare_views.py                      overlay, difference, edge comparison
    ├── register_capture.py                   registers a capture and refuses to crop on
    │                                         silent scale drift
    └── review_packet.py                      machine-readable packet for the reviewer
```

## Requirements

- Claude Code
- A Rhino MCP server connected to Rhino 8
- Python 3 with `pillow` and `numpy` for the helper tools

## Install

```bash
git clone https://github.com/frankee0920-rgb/rhino-architectural-reverse-modeling.git
cp -r rhino-architectural-reverse-modeling/rhino-architectural-reverse-modeling-mode-a \
      ~/.claude/skills/
```

Or drop the folder into a project's `.claude/skills/` to scope it to that project.

## Use

Give Claude Code one or more photographs of a building and ask for a Rhino model.
The skill activates on its description.

Expect it to **ask you questions early** — batched, once — about anything the images
cannot settle: overall depth, plan figure, ground-floor height. That is the design.
A single sentence from someone who knows the building is the highest-accuracy,
lowest-cost evidence available, and the skill is written to use it first rather than
last.

## Status

Version 0.9. Developed against real buildings; every check in `checks.md` and every
trap in `TOOLING.md` records an actual production failure rather than a hypothetical
one.

Least tested: the *generator* taxonomy on freeform and curved buildings. The
repetitive-unit branch is well exercised; the surface branch is reasoned, not proven.

## License

MIT — see [LICENSE](LICENSE).
