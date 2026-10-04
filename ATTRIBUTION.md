# Sources and modifications

The spiral galaxy animation is adapted from **Vinícius Melo**:

- Profile: https://github.com/vinimlo
- Project: https://github.com/vinimlo/galaxy-profile
- Source snapshot: https://github.com/vinimlo/vinimlo/tree/main/assets/generated
- Renderer: https://github.com/vinimlo/vinimlo/blob/main/generator/plates/galaxy.py
- License: GNU General Public License v3.0, preserved in `LICENSE`.
- Original SVGs and renderer were retrieved on 2026-10-04 and are preserved in `assets/upstream`.

The adaptation removes eight groups of outlined text (identity, focus areas,
and repository labels), along with their unused font outlines. The particle
paths, masks, animation rules, star geometry, phases, and timing are retained.
The decorative galaxy is framed next to new ASTRA Lab text; it does not claim
to visualize Xinze Li's repository data.

The new header, links, icons, slogan animation, responsive layout, generator,
and preview are project-local additions, distributed under the same GPL-3.0
license. No raster artwork or external typing/badge service is required.

The slogan's Chinese brush lettering and italic English serif are stored as
vector artwork in `assets/lettering.json`; no font files are distributed.
The optional Windows authoring script records the selected font families and
converts the two exact slogan phrases into paths for consistent SVG rendering.

The header's structure is inspired by Jonah Lawrence's profile:
https://github.com/DenverCoder1. Its pink graphics and source code are not copied.
