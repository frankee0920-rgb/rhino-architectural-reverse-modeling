# Checks

**Version 0.6**

Executable tests. Each one can fail. Each caught, or would have caught, a real
production error.

Precision is not accuracy. A reading can be measured to sub-pixel precision and
still be wrong, and every later step inherits it.

# 1. Impossibility checks — run before building on a reading

## 1.1 Convex visibility
A convex volume cannot show two opposite side faces from one camera.

If a feature appears beyond **both** the left and right silhouette edges of a
facade, at least one of them is not a receding side face — it must project
outward, or belong to a separate volume.

*Production failure:* strips appeared beyond both ends of a facade. The
contradiction was noticed, written down, and then ignored; the facade was
modelled with symmetric end walls that forced an unexplainable 320 mm asymmetry.
The user identified them as projecting balcony side plates. This check, taken
seriously, resolves it alone.

## 1.2 Silhouette taper
For a plane parallel to the image plane, width is constant with height, and equal
real heights project to equal image heights.

Measure width at two or more heights. Taper means the surface is battered, or the
plane is not parallel to the image plane. No taper puts a **bound** on the
batter — state the bound.

Caution: if the outermost silhouette belongs to a projecting element, this
constrains that element and says nothing about the facade behind it.

## 1.3 Projective equal spacing
Equally spaced collinear points satisfy `1/(x − x_v)` linear in index `n`, for
vanishing point `x_v`.

Fit it. Residual well under 1 px proves the points are a genuinely equally spaced
structural rhythm — and the fit then extrapolates reliably to members hidden
behind trees and to the face edges.

*This is the highest-value measurement in the whole toolkit.* It converted a
receding facade into an exact bay count (11 piers, rms 0.23 px), which turned a
fabricated building depth into a measured one. Use it before counting bays by eye.

## 1.4 Horizon consistency
For a horizontal plane at image row `y_f` receding to `y_b`:

```
(y_f − y_b) / (y_f − y_h) = D / (Z + D)
```

Solving `y_h` from two rows and then reporting the depth is circular. Measure
three or more rows and test whether one `(y_h, D)` fits them all.

If the implied horizon falls below the ground line, or implies a camera below
ground level, **the reading is wrong, not the horizon.**

## 1.5 Closure
`sum(parts) == measured overall`. Report the residual in mm and px.

A closure that only works by making a symmetric building asymmetric is evidence
of a wrong element decomposition, not evidence of asymmetry. See
`typological-constraints.md` P5.

## 1.6 Typological impossibility
Check the reading against the numeric ranges and plan-logic rules in
`typological-constraints.md`. A plan that cannot daylight its rooms, a span no
structure carries, a corridor that cannot exist — these falsify a reading as
decisively as a geometric contradiction, and they are the checks most likely to
catch an error in the *invisible* parts of the building.

## 1.7 Cross-source scale transfer

Every number in a photo-to-model workflow passes through a transfer: pixels to
millimetres, one drawing's scale against another's, one plane's px/m applied to a
point on a different plane. §1.1–§1.6 test readings **inside** one source.
Nothing tests the transfer **between** sources — and §2 actively pushes you to
combine sources without testing the combination.

**Compare ratios, not only values.**

```text
r_A = dimension_1 / dimension_2      as read from source A
r_B = dimension_1 / dimension_2      as read from source B
residual = |r_A / r_B - 1|
```

A ratio carries no scale. It survives an unknown camera distance and an unknown
reproduction scale, so it tests the one thing a shared scale factor cannot hide:
whether the two sources agree about the building's *proportions*.

Above 3%, one source is anisotropic (§5.1) or one datum is contaminated (§3). Do
not derive a level, a storey height or a setting-out dimension from either until
it is resolved, and do not average (§2).

*Production failure:* box height had three agreeing signals, the grid three, the
window head four inside 28 mm, and the dimension chain closed to 15 mm. The
ground-floor storey height was still 200 mm too tall. Section and photographs
disagreed by 9% about the ratio ground-floor : box, and nothing required that
ratio to be computed. Every gate was green.

### When there is only one source

Often there is one image and nothing else. Then this check cannot run — which is
a state to declare, not a step to skip:

- the scale transfer is **unverified**, and every dimension derived through it
  inherits that;
- the absolute anchor has no second opinion. R1 applies: ask;
- §4.1 matters more, not less. With one camera, every quantity depends on
  correctly classifying which plane each measured point lies in.

Say it in one line. A single-source chain left unlabelled reads as measured.

# 2. Two-signal rule

No load-bearing quantity rests on one signal. Two signals must **fail
differently** — two measurements of the same edge with the same detector are one
signal.

Independent pairs, by example:

- floor-to-floor from fascia spacing × guard height meeting a code minimum;
- bay pitch from peak detection × autocorrelation of the same band;
- recess depth from soffit convergence × reveal width — the latter is a pure
  ratio, independent of camera distance, so it survives an unknown `Z`.

When two signals disagree, **do not average**. Find which is contaminated, and
record the disagreement.

# 3. Detector contamination

What your detector reports is a property of the detector as much as of the
building. Two levels of this, and the second is worse because it does not look
like a measurement error at all.

## 3.1 Material contamination — the measurement

A brightness-keyed detector measures the **material boundary**, not the
**geometric boundary**.

Before comparing a measurement across floors, bays or faces, confirm the
materials on both sides of the edge are the same in every instance.

*Production failure:* loggia depth was measured from the dark run of the ceiling
shadow. The top floor closed on a bright perforated screen; the floors below
closed on a dark window head and timber. The detector overshot on the lower
floors and manufactured a monotonic trend — which was then reported as
"decisive", and pointed the **wrong way**. The clean signal was bay pitch, which
is material-invariant, and it disagreed. The user supplied the truth.

**A trend measured across instances with differing materials is inadmissible.**
Re-measure on a material-invariant signal — spacing, centre-to-centre pitch,
silhouette — or restrict the comparison to instances with identical materials.

## 3.2 Decomposition contamination — the element breakdown

The same failure one level up, and the expensive one: **a detector setting
decides how many elements the building has.**

Morphological cleanup, thresholds, minimum run lengths, contour tolerance — any
of these can sever one continuous element into several, or merge several into
one. The result does not read as a measurement error. It reads as architecture,
and it gets named, built and delivered as architecture.

Test: **re-run the extraction with a different detector setting and count the
elements again.**

```text
N(setting_1) == N(setting_2)   -> the count is the building's
N(setting_1) != N(setting_2)   -> the count is the detector's
```

When the count moves, no measurement resolves it. Go back to the drawing, at
enough zoom to see the element, and decide by looking.

*Production failure:* a roof plan was cleaned with a 7x7 erosion before
connected-component labelling. One continuous curved screen wall came apart into
four components. Four disconnected fragments were built, each given a semantic
name derived from its own bounding box, each terminating in mid air. At a 5x5
erosion the same wall is one component. Nothing in the model, and no measurement
taken from it, could have revealed this: the number of walls had been set by a
kernel size.

# 4. Datum ranking

Anchor on the highest-ranked datum available, and record which one you used:

1. silhouette against sky;
2. a long straight arris with uniform material on both sides;
3. an interior edge with uniform material;
4. anything adjacent to glazing, screens, timber, foliage or deep shadow — last
   resort.

When a value turns out wrong, check the datum before the arithmetic.

*Production failure:* a ground-floor head elevation was derived three times and
wrong twice, by both the modeler and the reviewer, because both anchored on the
bottom-row ceiling — rank 4, adjacent to glazing and screens. Re-anchoring on the
top-row ceiling (rank 2) gave agreement to 0.6 px on the first try.

Never anchor on the instance nearest the occluding vegetation just because it is
nearest the feature of interest.

## 4.1 Rank is not enough — check the point lies in the plane you scaled

`px/m` derived from a facade applies only to points lying in that facade's plane.

Classify the point before accepting **or rejecting** a measurement:

| where the point is | what applies |
|---|---|
| in the facade plane | that facade's px/m, directly |
| offset behind it by `d`, camera at distance `Z` | px/m × `(Z+d)/Z` — a known correction |
| on a plane receding from the camera | that px/m does **not** apply at all |

The point where a column meets the ground is a point *on the column*. It belongs
to the first or second row even though the ground is a receding plane. A
perspective argument about the receding plane says nothing about it.

Misclassifying costs more than a contaminated datum. A bad value gets
re-measured; a good value wrongly discarded does not come back.

*Production failure:* ground-floor height measured 2960 mm from column bases on
two independent facades. It was rejected with a receding-ground-plane argument
that did not apply to a point on a column, and a contaminated drawing value was
used instead. A principal dimension went 200 mm wrong.

# 5. Reference distortion floor

Establish once per reference image: on a facade parallel to the image plane,
bay-to-bay spacing must be constant. Any systematic drift is the photograph's
residual lens distortion or a small facade-to-sensor angle — **not building
geometry**.

Record it in px per bay. It is the accuracy floor for every horizontal
registration afterwards. Do not chase residuals below it: a rigid uniform model
cannot fit both the ends and the middle of a distorted photograph, and trying
will bend a correct grid.

## 5.1 Drawings are not exempt, and they fail differently

A photograph distorts radially, worst at the frame edge. A scanned, re-drawn or
re-published plan or section can instead be **anisotropic**: uniform within each
axis, different between them.

Nothing inside the drawing reveals this. Every dimension you read stays
self-consistent with every other dimension in the same drawing.

Test once per drawing, before reading any dimension from it: take one X-direction
and one Y-direction dimension that are both known from another source, and
compare the two implied scales.

If they differ, do not pick one and do not average. Record both, state which
evidence chain each axis is tied to, and treat any quantity read across the two
axes as single-signal.

Pick the two known dimensions from **different** evidence chains, and never from
the comparison you are trying to test. Calibrating one axis against a contaminated
comparison manufactures anisotropy that is not there.

*Production near-miss:* a section was believed anisotropic by 4.7% and a
correction was about to be applied to every storey height. Running this test
properly — horizontal scale from a plan-derived column diameter, vertical scale
from overall height — returned 209.0 px/m on both axes. The section was uniform.
The apparent anisotropy was an artefact of having calibrated the vertical axis on
the very comparison that was in dispute. The test is cheap, and here it prevented
a wrong correction rather than catching a wrong reading.

# 6. Multi-image identity

Before treating two photographs as the same building, verify it.

Evidence: matching bay count, matching storey count, matching structural rhythm,
matching floor-to-floor ratio. Similar material and style are **not** evidence —
a complex usually contains several buildings of one family.

The check that settles it is §1.3 on each face: a short face whose bay count
matches the other photograph exactly is strong identification.
