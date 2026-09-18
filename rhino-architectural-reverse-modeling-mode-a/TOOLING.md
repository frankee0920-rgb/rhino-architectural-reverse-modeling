# Tooling

**Rhino execution reference — revised 2026-09-10**

SKILL.md defines outcomes and scope. Read relevant sections when a Rhino
operation needs them; this reference does not add a mandatory review process. Photo-specific camera
recipes apply only when a photo is being matched. For oral modelling choose a
usable design view rather than inventing a reference station point.

Consult the relevant symptom or operation only. Recorded behavior depends on the
Rhino version and environment; discover current tools and display identifiers
rather than treating historical examples as installed configuration.

# 1. Helper tools

| Tool | Purpose |
|---|---|
| `tools/reference_prep.py` | source metadata, FAR image, MID grid crops, custom NEAR crops |
| `tools/compare_views.py` | normalized pair, side-by-side, 50% overlay, abs difference, edge maps, metrics JSON |
| `tools/register_capture.py` | register a capture on visible features **and detect scale drift** |
| `tools/review_packet.py` | optional evidence packet by `--purpose`; legacy gate/level arguments remain accepted |

Distinguish user-given dimensions, native geometry queries, image measurements
and estimates. If a claim depends on a computed image measurement, retain its
reproducible calculation; ordinary modelling does not need a new script to
re-prove a supplied dimension or a direct application query.

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

Original creation parameters may not be recoverable from final geometry alone.
Preserve useful controls, for example in object user strings, native control
geometry or a parameter file, and identify them for the next session.

# 3. Capture

## Verify the live document and render path early

In a new or changed execution environment, use existing or small representative
geometry to verify the MCP-connected document, material assignment, saved view
and actual image output. Reuse an unchanged, verified setup. With multiple Rhino instances, compare the connected document path
and process with the intended visible document; do not assume they are the same.
After reconnecting or opening a different file, check again before mutating it.

In the observed Rhino 8 environment, hidden-window captures sometimes returned
stale display content. Inspect the actual image and use the intended visible
window when the render pipeline is not updating. A successful capture call is
not evidence that the requested mode rendered. Native `_SetDisplayMode` can be
needed to switch the active pipeline; assigning a viewport display property alone
may not suffice. Save a checkpoint and leave Raytraced mode before substantial
geometry or material edits; live raytraced updates have stalled this workflow.

When material names acquire automatic numeric suffixes, name-only matching can
miss assignments. Prefer stable material references or semantic identifiers;
inspect representative objects after assignment. Native PBR content created with
`PhysicallyBasedMaterialType` retained PBR fields in the observed environment;
conversion through legacy/basic material paths did not. Verify actual content
and render appearance rather than relying on the material's label.

## Use this

```text
-_ViewCaptureToFile _Width=<w> _Height=<h> _Scale=1
  _DrawGrid=_No _DrawWorldAxes=_No _DrawCPlaneAxes=_No
  _TransparentBackground=_No "<absolute path>" _Enter
```

## Blank captures

`CreatePreviewImage` returned all-white or all-black images in observed sessions
despite reporting success. Prefer the capture command above and inspect its
actual image before using it as evidence.

## Camera and capture symptoms

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

**T3 — capture width, not lens alone, sets pixel scale.** When solving for a
framing, fix the capture size first, then calibrate the lens against it.

## Guard

When a photo comparison depends on accurate capture scale, `tools/register_capture.py`
can measure the building's pixel extent against an expected value and refuse
cropping on drift. Use it or an equivalent check when scale is uncertain; it is
not required on every capture. Reuse crop offsets only while framing remains
verified. A reported lens correction is diagnostic, not permission to alter the
camera automatically.

# 4. Camera — store two separate things

Confusing these wastes more time than anything else in this document. A camera can
be perfectly stable while every capture from it is unusable.

## 4.1 The camera — defined by architectural quantities

```text
projection:      infer from perspective/parallelism and available camera evidence
camera_height:   infer or fit; use eye level only when the reference supports it
position:        infer from visible faces and spatial relationships
distance/lens:   fit jointly to supported perspective and framing
shift/crop:      account for corrected verticals and source framing as needed
```

Store as a Named View. Camera and geometry can be ambiguous from one photograph.
Use source cues and other supported views to separate them. Do not refit the camera
automatically to make each geometry change look correct; hold it comparable when
evaluating shape, and revise projection separately when evidence warrants it.

A named view is storage, not state. The camera for the **primary** reference has
one extra requirement at handover: restore it into the Perspective viewport as
the last action before saving, so the delivered file opens on it. See
`SKILL.md` §交付. Orbiting after the restore and saving again silently
undoes it — verify by reopening, not by remembering.

Match the projection shown by the source. Parallel verticals may indicate
perspective correction or a shifted view; converging verticals require a matching
perspective. Camera position and focal length also affect visible depth and
openings, so matching verticals alone does not establish a valid comparison.

## 4.2 The capture recipe — defined by pixels

```text
capture_width_px:
capture_height_px:
lens_at_that_capture_size:
expected_building_width_px:   <- check when framing/scale changes or is uncertain
crop_offset:                  <- reuse only while its framing remains verified
```

If the check value changes unexpectedly, inspect viewport/capture size (T2/T3),
projection and document state before changing the camera or geometry. A mismatch
alone does not identify its cause.

## 4.3 Off-centre framing

An off-centre horizon can result from lens shift, cropping, camera tilt or
perspective correction. Diagnose the projection rather than assuming a shifted
lens. When appropriate, Rhino can use an asymmetric frustum; §6.1 provides an
example. Retain framing settings so the saved view and delivered image agree.
Cropping may refine framing but does not correct a wrong camera projection.

## 4.4 Display modes

Use a neutral mode to inspect geometry and an appropriate material/render mode
to inspect appearance. Query installed display modes and use their returned
names or IDs; historical custom modes are not portable. If a mode switch changes
framing unexpectedly, inspect camera and viewport state before altering geometry.
Keep comparable framing while judging material changes.

# 5. Geometry construction rules

The execution layer makes it very easy to produce a correct-looking model that
cannot be edited. Guard here, not at handover.

- **Maintain semantic identity.** Naming and assigning layers during creation is
  a useful default; a reliable batch organization is also valid. Preserve useful
  component boundaries and editable controls through booleans and joins. A single
  opaque final solid may force a full rebuild on each user change.
- **Check meaningful geometry**, not only an assembly bounding box. Use actual
  queries or batch validation for validity, intended solid/open state, naked edges
  and dimensions. Inspect representative junctions and suspect operations; no
  separate report or API call is required for every repeated component.
- **Batch heavy booleans.** 229 cutters against one solid timed out. Batch, and
  verify after each batch so a failure is localized.
- **Instance repeated elements** with semantic master names. Never array an
  unverified master.
- **Block material inheritance needs inspection.** Definition geometry can retain
  its own material/layer source, so changing the instance layer may not change its
  appearance. Inspect the material source and one actual instance; configure the
  master or inheritance deliberately. In a recorded failure, mullions retained
  the default layer material despite correctly organized instance layers.
- **Material creation does not prove the required pattern exists.** Where a bitmap
  is needed, verify actual assignment, accessible image and mapping; a successful
  colour/transparency call does not set the bitmap. Uniform surfaces and native
  procedural materials are valid when appropriate. Inspect the required surface
  appearance, not bitmap presence for every material.
- **A texture with no mapping is not a texture at a known scale.** Without a
  mapping the surface's own parameterization drives the texture, which on a boxy
  Brep differs face to face and cannot be fixed by editing the material. Set an
  explicit mapping — box, cylindrical or spherical to suit the element — and set
  its size in **model units**, so texture scale is a dimension you can measure
  against the reference rather than a slider you nudge.
- **Keep driving parameters recoverable.** User strings, named control geometry,
  native controls or a concise parameter file are possible mechanisms; choose what
  supports practical editing and identify the entry point at handover.

# 6. The delivered camera lives in the file, not the session

The handover requirement in `SKILL.md` §交付 is about the **saved
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

Use this recipe when source cues establish a two-point perspective and the
desired framing requires an asymmetric frustum. Parallel verticals alone do not
prove a shifted view: distinguish perspective, orthographic views, cropping and
correction under §4 before selecting the mechanism.

There are two ways to get parallel verticals and they are the same projection:

- set the camera axis horizontal — camera and target at the same `Z`, up `+Z`.
  Rhino reports `IsTwoPointPerspectiveProjection == True` for such a camera even
  if you never touched the mode;
- call `vp.ChangeToTwoPointPerspectiveProjection(lens)`.

Projection alone may not solve framing. For a tall building viewed from low
eye height, the desired frame may extend far above the horizon. When that is
the diagnosed condition, shift the frustum. The following recipe uses a
`ViewportInfo` copy to set the required frustum:

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

An adapter that worked in a previous session may not work now. When its current
behavior is unknown or suspect, verify the uncertain operation with a small
reversible example: known geometry for dimensions, or a capture for framing and
pixel content. Reuse established session evidence instead of repeating a full
startup ritual. Final rendering and saved-view requirements are in SKILL.md.

A capture adapter can fail while reporting success. Verify the pixels, not the
return value.
