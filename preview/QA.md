# Render verification

The delivered implementation was checked against `DESIGN.md`, the user's
approved five-row layout, and `references/space-vinimlo.png`.

Actual browser screenshots: `desktop-dark.png`, `desktop-light.png`, and
`mobile-dark.png`. All were rendered with the Codex in-app browser and inspected
as images. The stills use the preview's **Dawn** setting, which exposes a stable
review frame and the full role list. **Live animation** uses the production assets.

| Comparison | Evidence and result |
| --- | --- |
| Copy and order | Name, roles, fields, four links, lab expansion, galaxy, and bilingual slogan match the approved order. No added profile copy. |
| Typography | Monospace name/roles, restrained fixed field text, serif lab heading and description. Mobile fields and slogan wrap into explicit lines. |
| Palette | Dark/light text and ice-blue icons checked in both themes. Slogan reveals into a cool light background. No pink. |
| Spacing and alignment | Centered header and links; consistent lab left gutter; balanced two-column desktop panel; explicit mobile stack. |
| Icons and links | Matching 18 px outline icons, live Website/Scholar/LinkedIn/repositories destinations. Stars display 658 from the public API snapshot. |
| Galaxy fidelity | Visual comparison with Melo reference; label groups removed. Automated checks prove all original particle references and animation CSS are unchanged. |
| Responsive behavior | A 375 px preview frame was checked at native size. All four icons share the same row; all images load and fit the frame. A browser-wide viewport override did not resize the existing tab, so the exact-width iframe supplied the mobile viewport. |
| Animation | Production slogan computed opacity changes over time; duration is 14 seconds. Header's clip animation visibly types a partial word. Original spiral particles retain their animation. |

Material fixes made: reduced mobile link widths, removed excess link whitespace
that caused a three-plus-one wrap, and corrected preview frame height reporting
to eliminate extra bottom space.

Integrity command: `python scripts/verify_profile.py` — passed for all 28
self-contained SVGs and every README image source. Public star refresh command
was also run successfully. The project has no package dependencies.

Intentional differences from the references: no galaxy labels, custom ASTRA
copy, blue icons, transparent galaxy background, and automatic dawn slogan.
The frozen review frame shows all three roles; live mode cycles them individually.
No material mismatch with the approved layout remains. Live GitHub rendering
has not been tested because this deliverable has not been published.

## Typography and dawn revision

Reviewed `desktop-dark-v2.png` and `mobile-dark-v2.png` in the browser.
The A/S/T/R/A letters are underlined in the expansion. The role cycle is now
9 seconds. The enlarged slogan uses portable vector outlines, rather than
depending on a visitor's installed fonts.

The revised dawn uses a soft vertical reveal mask and subtle horizon glow.
In the production SVG, browser inspection recorded the reveal transform at
`translateY(148px)`, an intermediate `translateY(-57.85px)`, and
`translateY(-148px)`. Lettering opacity progresses from 0 to 1 as dawn completes.
`dawn-transition-v2.png` captures the gradient sweep during that transition.
The 28-asset integrity and unchanged-galaxy checks passed after regeneration.

## Diagonal moonlight revision

The selected direction replaces the vertical reveal with a broad diagonal
moonlight beam across fine silver-blue paper. Chinese and English lettering
share the paper's spatial reveal mask; the English has a slightly later entrance.
The animation runs for 18 seconds: 4 s reveal, 8 s hold, 4 s fade, 2 s darkness.
Reduced-motion mode shows the completed paper and lettering immediately.

`moonlight-profile.png` was inspected as the mid-reveal frame. The preview's
Moonlight, Dawn, and Night controls supply stable review frames; Live animation
uses the actual production SVG. `moonlight-transition.gif` contains 61 real
in-app-browser screenshots of the SVG animation, captured over one full cycle.
Temporary recording frames were removed after GIF assembly. The GIF is a motion
preview, while the production profile retains scalable SVG rendering.

All 28 self-contained SVG integrity checks still pass. The diagonal reveal,
unchanged lettering sizes, cool palette, paper texture, and light/dark endpoints
match the user's selected direction. No additional profile content was added.
