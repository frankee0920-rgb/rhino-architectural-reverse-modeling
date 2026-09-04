# Tooling

**Version 0.8**

What the execution layer can and cannot do, the traps it hides, and the recipes
that survive them. Nothing here is procedure.

# 1. Helper tools

| Tool | Purpose |
|---|---|
| `tools/reference_prep.py` | source metadata, FAR image, MID grid crops, custom NEAR crops |
| `tools/compare_views.py` | normalized pair, side-by-side, 50% overlay, abs difference, edge maps, metrics JSON |
| `tools/register_capture.py` | register a capture on visible features **and detect scale drift** |
| `tools/review_packet.py` | machine-readable packet for the reviewer |

Prose is not measurement. Anything claimed as measured must come from a script
whose output can be re-run.

# 2. Rhino MCP capability boundary

| Need | Tool | Boundary |
|---|---|---|
| Document overview | `get_document_summary` | object counts, per-layer counts, units, model bbox |
| Exact dimensions | `analyze_objects` | axis-aligned bbox, validity, closed-solid, naked edges, volume, area |
| One object in detail | `get_object_info`, `get_object_attributes` | id, name, type, layer, bbox, user strings |
| By layer | `get_objects(layer_filter=...)` then `analyze_objects` | |
| Create primitives | `create_object` | |
| Move / rotate / scale | `modify_object`, `modify_objects` | no generic `set_geometry_parameter(width=…)` exists |
| Name / layer / user strings | `update_object_attributes` | |
| Booleans, extrude, loft, sweep, pipe, offset | typed tools | prefer these over script |
| Camera and view | `execute_rhinoscript_python_code` | no typed camera tool exists |
| Materials, textures, texture mapping | `execute_rhinoscript_python_code` | no typed material tool exists. Creating a material and setting a colour is one call; giving it a **bitmap** and giving the object a **mapping** are two more, and they are easy to skip without any error |
| Named views | `NamedViews`, `AddNamedView`, `RestoreNamedView`, `DeleteNamedView` | |
| Image to disk | `run_command` with `-_ViewCaptureToFile` | see §3 |
| Image returned inline | `capture_viewport` | 100–4096 px; can itself alter the viewport |

**Never infer a dimension from a screenshot when Rhino can be asked.**

Look up RhinoScript documentation (`get_rhinoscript_docs`) before writing Python.
Do not guess signatures.

Original creation parameters are **not** recoverable from geometry. If you want a
later session to know them, write them as object user strings.

# 3. Capture

## Use this

```text
-_ViewCaptureToFile _Width=<w> _Height=<h> _Scale=1
  _DrawGrid=_No _DrawWorldAxes=_No _DrawCPlaneAxes=_No
  _TransparentBackground=_No "<absolute path>" _Enter
```

## Do not use `CreatePreviewImage`

v0.3 specified it as the durable-file adapter and recorded it as verified. In
later sessions it produced **an all-white image at one size and an all-black image
at another** — silently, with `success=True` and a plausible file size.

## Three traps, all hit in production

**T1 — `ViewCameraLens` moves the camera.** Setting the lens dollies the camera to
preserve framing, sometimes drastically. Set **lens first, then camera/target,
then up vector, then display mode** — and read all of it back and assert it
matches. Never set the lens after the camera and assume the camera survived.

A target placed very close to the geometry can also make Rhino reset the camera
entirely. Keep the target a sensible distance along the view axis.

**T2 — viewport resize silently changes capture scale.** `-_ViewCaptureToFile`
output scale depends on the Rhino **viewport's own pixel size**. If the Rhino
window is resized mid-session, the same lens and the same requested capture size
produce a different number of pixels per metre, silently invalidating every
earlier registration.

In production the viewport went 901×551 → 1814×1088 and a correct camera produced
a mis-registered capture. Time was then wasted "fixing the camera", which was
never broken.

**T3 — capture width, not lens alone, sets pixel scale.** When solving for a
framing, fix the capture size first, then calibrate the lens against it.

## Guard

Run `tools/register_capture.py` on every capture. It measures the building's pixel
extent, compares it to the expected value, prints a lens correction factor, and
**refuses to crop on drift**. Never hard-code a crop offset from a previous
capture.

# 4. Camera — store two separate things

Confusing these wastes more time than anything else in this document. A camera can
be perfectly stable while every capture from it is unusable.

## 4.1 The camera — defined by architectural quantities

```text
view_axis:       horizontal   (unless the reference itself shows convergence)
camera_height:   eye level, 1500-1700 mm
position:        on the facade's centre-line
distance:        so the building occupies a similar fraction of frame
lens:            one measurement, one proportional correction, done
```

Store as a Named View. Because it is defined by the building, a change in building
dimensions means the camera is **recomputed** — cheap, normal, not a symptom of
anything wrong.

A named view is storage, not state. The camera for the **primary** reference has
one extra requirement at handover: restore it into the Perspective viewport as
the last action before saving, so the delivered file opens on it. See
`SKILL.md` `# DELIVERABLE`. Orbiting after the restore and saving again silently
undoes it — verify by reopening, not by remembering.

**The first line is the only one that really matters.** Architectural photographs
are usually vertically corrected: verticals parallel, not converging. If the model
view converges while the reference does not, the two silhouettes cannot be compared
at all and no framing accuracy repairs it. Everything else is framing, and framing
may be approximate.

## 4.2 The capture recipe — defined by pixels

```text
capture_width_px:
capture_height_px:
lens_at_that_capture_size:
expected_building_width_px:   <- the check value, verified every time
crop_offset:                  <- measured every time, never reused
```

If the check value is off, the viewport or capture size changed (T2/T3), not the
camera. Fix the recipe; leave the camera alone.

## 4.3 Shifted lens — required whenever the reference is shifted

If the reference's horizon is not at mid-frame, its principal point is offset: it
was shot with a rise-shift lens, which is ordinary practice for tall buildings.

**Rhino can reproduce this.** Set an asymmetric frustum — §6.1 has the call and
the registration arithmetic.

Earlier versions of this file said the opposite: that Rhino could not offset the
principal point, and that the only faithful emulation was to capture a larger
frame and crop off-centre. That is wrong, and it was expensive. Capture-and-crop
reproduces the reference *image* while leaving the delivered *viewport* centred
on the horizon, so the saved model opens showing the lower half of a tall
building — every camera check passing, the deliverable unusable. See `SKILL.md`
`# DELIVERABLE`.

Capture-and-crop remains the right way to pull an exact reference framing out of
a viewport whose aspect does not match, once the frustum is already correct. What
it is not is a substitute for the frustum.

For a comparability *check* on its own, accepting the horizon at mid-frame is
still a legitimate documented simplification. For the **delivered** view it is
not, because the delivered view has to be looked at.

## 4.4 Display modes

Geometry review uses one white/clay mode. Query `ViewDisplayModes(True)` and use
the returned name or id **exactly** — installed names may contain typos. In the
audited Rhino 8 session the material mode is spelled `Arctic mode with matertial`
(id `33238429-4ea4-48d1-8443-552fcafe851f`). Do not silently correct it.

Switching geometry → material review changes **Display Mode only**. Compare
camera, target, up, projection and lens before and after; fail the switch if any
changed.

# 5. Geometry construction rules

The execution layer makes it very easy to produce a correct-looking model that
cannot be edited. Guard here, not at handover.

- **Name at creation.** Set name and layer in the same operation that creates the
  object. Naming later does not work — by then the geometry has no element
  boundaries to name.
- **Boolean within one component only.** Subtracting many cutters from one block
  produces a solid in which no architectural element exists as an object. In
  production this forced a full rebuild on every change, which churned the whole
  dimension chain.
- **Verify each component**, not only the assembly: `analyze_objects` for
  validity, closed-solid state, naked edges, bbox against intent.
- **Batch heavy booleans.** 229 cutters against one solid timed out. Batch, and
  verify after each batch so a failure is localized.
- **Instance repeated elements** with semantic master names. Never array an
  unverified master.
- **A block instance does not carry its layer's material.** The geometry inside
  the block definition keeps the layer it was created on. Setting the
  *instance's* layer changes nothing about how it renders. Put the master on its
  target layer **before** defining the block, and check one instance in the
  material view. In production every mullion in the building rendered in the
  default layer's material while every instance sat on the correct layer.
- **A material with a colour and no bitmap fails silently and completely.** The
  call that creates a layer material and sets its colour, transparency and shine
  returns success and renders plausibly, and nothing downstream distinguishes it
  from a finished material. Setting the **bitmap** is a separate call, and it is
  the one that gets left out. Assert it: read each material back and check it
  actually carries a texture, rather than trusting the sequence you wrote.
- **A texture with no mapping is not a texture at a known scale.** Without a
  mapping the surface's own parameterization drives the texture, which on a boxy
  Brep differs face to face and cannot be fixed by editing the material. Set an
  explicit mapping — box, cylindrical or spherical to suit the element — and set
  its size in **model units**, so texture scale is a dimension you can measure
  against the reference rather than a slider you nudge.
- **Store driving parameters as user strings.**

# 6. The delivered camera lives in the file, not the session

The handover requirement in `SKILL.md` `# DELIVERABLE` is about the **saved
file**. Asking the running session what its camera is answers a different
question, and the two come apart silently.

## Verify from disk

Read the saved `.3dm` directly and print the viewports the file opens with, plus
the named views the user can click:

```python
import rhino3dm
f = rhino3dm.File3dm.Read(path)
for v in f.Views:                     # what the file opens on
    vp = v.Viewport
    print(v.Name, vp.IsPerspectiveProjection, vp.CameraLocation,
          vp.CameraUp, vp.GetFrustum())     # frustum: dict with left/right/bottom/top
for v in f.NamedViews:                # what the user can click
    print(v.Name, v.Viewport.CameraLocation, v.Viewport.GetFrustum())
```

Print the **frustum**, not only the lens length. A shifted frustum is the part of
the delivered view most likely to be lost, and a lens length cannot show you
whether it is still there.

Both must be right, and they are separate facts: `Views` is the parked viewport,
`NamedViews` is the control the user reaches for after orbiting. Reopening the
file into the live session is a weaker version of this check and costs you the
session.

## 6.1 Two-point perspective is the mechanism, not a hazard

When the reference photograph has **parallel verticals** — as architectural
photographs of tall buildings usually do — the projection you need is a two-point
perspective with a **shifted (asymmetric) frustum**. That is what a rise-shift
lens is, and Rhino does it.

There are two ways to get parallel verticals and they are the same projection:

- set the camera axis horizontal — camera and target at the same `Z`, up `+Z`.
  Rhino reports `IsTwoPointPerspectiveProjection == True` for such a camera even
  if you never touched the mode;
- call `vp.ChangeToTwoPointPerspectiveProjection(lens)`.

Neither one alone solves framing. A symmetric frustum centres the frame on the
horizon, so a tall building is cut off at the top in any ordinary viewport.
**Shift the frustum.** `RhinoViewport` has no `SetFrustum`, which is the only
reason this looks harder than it is:

Derive the vertical window from the building and the camera. Never carry a
frustum number over from another job — it encodes that building's height and that
camera's distance, and it will be wrong here.

```python
import Rhino, scriptcontext as sc
vp  = sc.doc.Views.ActiveView.ActiveViewport
vpi = Rhino.DocObjects.ViewportInfo(vp)
ok, l, r, b, t, n, f = vpi.GetFrustum()

eye    = vp.CameraLocation.Z
D      = <horizontal distance from camera to the building's near vertical arris>
z_hi   = <highest world Z the frame must show>    # roof, parapet, plant screen
z_lo   = <lowest  world Z the frame must show>    # near ground, or the reference's
                                                  #   own bottom edge if matching it
margin = 0.06                                     # a little air top and bottom

top =  n * ((z_hi - eye) / D) * (1.0 + margin)    # tan(angle) x near
bot = -n * ((eye - z_lo) / D) * (1.0 + margin)

h = top - bot
w = (vp.Size.Width / float(vp.Size.Height)) * h    # must keep the viewport aspect
vpi.SetFrustum(-w/2.0, w/2.0, bot, top, n, f)
vp.SetViewProjection(vpi, True)
sc.doc.Views.Redraw()
```

`top` and `bot` are `near x tan(angle)`, so they are pure geometry: the ratio
`top/n` is the tangent of the angle from the camera up to `z_hi`, and nothing
else. Keep the viewport's aspect ratio or Rhino re-fits the frustum on the next
redraw.

The asymmetry **survives the save** and reads back from disk — the verification
snippet above prints it.

Registering a capture taken through a shifted frustum is arithmetic, not
calibration:

```text
horizon row = top / (top - bot) * H_px
f_px        = H_px * near / (top - bot)
```

In production both matched a measured silhouette apex to within 1 px on the first
try, with no iteration.

## 6.2 The two real traps

**The viewport gets renamed, and then every call that addresses it by name
fails.** Two causes, and the second is not obvious:

- the user toggling two-point perspective from the Rhino UI renames the viewport
  to the localized label;
- **`RestoreNamedView` renames the viewport to the named view's name.** Whatever
  you called your named view, the viewport is called that afterwards — so the very
  next `rs.ViewCameraLens("Perspective", …)` fails with `unable to coerce
  Perspective into a view`.

Address the viewport through `sc.doc.Views.ActiveView.ActiveViewport` instead of
by name, or set `vp.Name` back immediately after any restore. Calling
`ChangeToTwoPointPerspectiveProjection` yourself does **not** rename it.

**A projection change invalidates every earlier capture calibration.** Switching
mode, or shifting the frustum, changes `f_px` and the horizon row. Re-register
(§3) before comparing anything to a capture taken across the change — and do not
go "fix the camera", which was never broken.

Guard, immediately before the final save: assert the viewport carries the name
you address it by, assert the projection is the one you intend, and check
`DocumentModified` *after* the save — a `True` means something changed the
document afterwards, and whatever the user saves next is not what you verified.

*Production failure, and a retraction.* Two-point perspective was toggled on
mid-session from the Rhino UI. One comparison capture came back at a completely
different scale and horizon, and twenty minutes went into "fixing the camera".
The lesson was then written into this file as *"two-point perspective is a trap;
it forces a symmetric frustum; use a horizontal camera axis instead"* — and every
clause of that is wrong. It is the correct projection for this class of
reference, it accepts an asymmetric frustum, and the horizontal-axis camera **is**
a two-point perspective. The building was consequently delivered on a camera that
showed half of it. A write-up that turns a state-management incident into a
verdict on the feature is worse than no write-up: it steers the next session away
from the only mechanism that frames a tall building correctly from a real eye
height.

# 7. Session hygiene

An adapter that worked in a previous session may not work now. At the start of a
session, before relying on it: create a test box of known dimensions, verify with
`analyze_objects`, set a camera, capture, and confirm the file has the requested
dimensions and is not blank.

A capture adapter can fail while reporting success. Verify the pixels, not the
return value.
