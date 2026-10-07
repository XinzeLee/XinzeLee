# Xinze Li's GitHub profile

Open `http://127.0.0.1:8765/preview/` after running:

```powershell
python scripts/serve_preview.py
```

The preview uses the same `<picture>` and `<img>` elements as `README.md`.
Animations run inside SVG images, without JavaScript in the profile itself.
The preview controls are local review tools; they are not part of the README.

## Publish

Copy `README.md`, `assets/`, `scripts/build_profile.py`,
`.github/workflows/profile.yml`, `LICENSE`, and `ATTRIBUTION.md` into the public
**XinzeLee/XinzeLee** profile repository. The profile repository must have
the same name as your GitHub username. Nothing has been published by this build.

## Refresh

```powershell
python scripts/build_profile.py
python scripts/build_profile.py --refresh-stars
```

The first command builds offline using cached data. The second reads public
repository counts from the GitHub API, with pagination. Once installed, the
workflow refreshes weekly on Mondays at 08:17 UTC and supports manual dispatch.

Total stars means stars **received** by all owned public repositories, including
forks; it does not mean the number of repositories you have starred.

## Design

- Ice-blue accents, theme-specific text, transparent header and galaxy panels.
- Monospace name and cycling role; fixed research fields underneath.
- Four clickable links with consistent 18 px outline icons and labels.
- Serif ASTRA text beside the label-free, original animated spiral.
- Mobile stacks the lab text over the galaxy; the research fields wrap cleanly.
- Slogan loops for 18 seconds: 4 s diagonal moonlight reveal, 8 s hold, 4 s dusk, 2 s night.
- Roles cycle in 9 seconds. Acronym letters A/S/T/R/A are underlined in the lab expansion.
- Slogan lettering is vector artwork; no visitor font installation is needed.
- `scripts/export_lettering.ps1` is an optional Windows authoring step to change
  the slogan lettering. Normal generation uses the checked-in outlines in
  `assets/lettering.json` and requires only Python's standard library.
- Reduced motion shows a static role list and the fully visible light slogan.

GitHub README sanitization rules prevent custom hover/tap interactions, so
the slogan animation plays automatically, as agreed. The browser's preferred
color scheme selects the theme through `<picture>`. If the browser's preference
and a manually selected GitHub theme disagree, the SVG theme may differ from
GitHub's page theme, which is also a limitation of the reference profile.
