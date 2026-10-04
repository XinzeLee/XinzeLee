"""Build GitHub-safe, self-contained animated SVGs. Python standard library only."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "generated"
UPSTREAM = ROOT / "assets" / "upstream"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

THEMES = {
    "dark": {"bg": "#0d1117", "ink": "#e6edf3", "mute": "#9ba8b8", "accent": "#9bcfff", "rule": "#263344"},
    "light": {"bg": "#ffffff", "ink": "#172435", "mute": "#5e6f82", "accent": "#3075ad", "rule": "#dce7f1"},
}
MONO = "Consolas, 'Liberation Mono', Menlo, monospace"
SANS = "'Segoe UI', Helvetica, Arial, sans-serif"
SERIF = "Georgia, 'Times New Roman', serif"


def text(x, y, value, size, fill, *, family=SANS, anchor="start", extra=""):
    escaped = value.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{escaped}</text>')


def svg(width, height, body, title, defs="", desc=""):
    return (f'<svg xmlns="{NS}" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" aria-labelledby="title description">\n'
            f'<title id="title">{title}</title><desc id="description">{desc or title}</desc>\n'
            f'<defs>{defs}</defs>\n{body}\n</svg>\n')


def write(name, content):
    (OUTPUT / name).write_text(content, encoding="utf-8")


def lettering(kind, size, baseline, center=None, x=None):
    """Fixed vector lettering, so GitHub visitors need no installed calligraphy font."""
    outlines = json.loads((ROOT / "assets" / "lettering.json").read_text(encoding="utf-8-sig"))
    glyphs = outlines[kind]
    scale = size / 1000
    width = glyphs["width"] * scale
    left = x if x is not None else center - width / 2
    top = baseline - glyphs["ascent"] * size
    return (f'<g transform="translate({left:.3f} {top:.3f}) scale({scale})" fill="#182e45">'
            f'<path fill-rule="evenodd" d="{glyphs["path"]}"/></g>')


def header(theme, mobile):
    t = THEMES[theme]
    width, height = (390, 142) if mobile else (850, 126)
    center = width / 2
    roles = ("Researcher", "Educator", "Engineer")
    # Native SVG visibility avoids CSS clip geometry failures in mobile renderers.
    # One synchronized timeline, with exactly one visible role and a safe fallback.
    style = []
    animated = []
    font_size = 20 if mobile else 23
    for index, role in enumerate(roles):
        values = ['visible' if phase == index else 'hidden' for phase in (0, 1, 2, 0)]
        fallback = 'visible' if index == 0 else 'hidden'
        letters = []
        for letter_index, letter in enumerate(role):
            # Discrete character visibility types and erases without animated clipping.
            appear = index / 3 + .06 * (letter_index + 1) / len(role)
            disappear = index / 3 + .30 - .045 * letter_index / len(role)
            letters.append(f'<tspan visibility="{fallback}">{letter}'
                           '<animate attributeName="visibility" values="hidden;visible;hidden;hidden" '
                           f'keyTimes="0;{appear:.12f};{disappear:.12f};1" '
                           'dur="6s" begin="0s" calcMode="discrete" repeatCount="indefinite"/></tspan>')
        animated.append(text(center, 78, '', font_size, t["accent"], family=MONO, anchor="middle",
                             extra=f'visibility="{fallback}"').replace('</text>',
                             ''.join(letters) +
                             '<animate attributeName="visibility" '
                             f'values="{";".join(values)}" keyTimes="0;0.333333333333;0.666666666667;1" '
                             'dur="6s" begin="0s" calcMode="discrete" repeatCount="indefinite"/></text>'))
    style.append('.static-role{display:none}@media(prefers-reduced-motion:reduce){.moving-role{display:none}.static-role{display:block}}')
    body = text(center, 37, "Xinze Li", 31 if mobile else 36, t["ink"], family=MONO, anchor="middle")
    body += '<g class="moving-role">' + "".join(animated) + '</g>'
    body += text(center, 78, "Researcher · Educator · Engineer", 14 if mobile else 20, t["accent"], family=MONO,
                 anchor="middle", extra='class="static-role"')
    if mobile:
        body += text(center, 108, "AI for Power Electronics", 15, t["mute"], anchor="middle")
        body += text(center, 130, "and Semiconductor Fabrication", 15, t["mute"], anchor="middle")
    else:
        body += text(center, 112, "AI for Power Electronics and Semiconductor Fabrication", 17, t["mute"], anchor="middle")
    return svg(width, height, body, "Xinze Li — Researcher, Educator, Engineer",
               '<style>' + "".join(style) + '</style>',
               "Researcher, Educator, Engineer in AI for Power Electronics and Semiconductor Fabrication")


ICONS = {
    "website": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-5 5-5 13 0 18 5-5 5-13 0-18ZM5 7h14M5 17h14"/>',
    "scholar": '<path d="m2 9 10-5 10 5-10 5-10-5ZM6 11v6c4 3 8 3 12 0v-6M22 9v8"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M7.5 10v7M11.5 17v-7M11.5 13c0-4 5-4 5 0v4"/><circle cx="7.5" cy="7" r=".5"/>',
    "stars": '<path d="m12 2.5 2.9 5.9 6.5.9-4.7 4.6 1.1 6.5-5.8-3-5.8 3 1.1-6.5-4.7-4.6 6.5-.9Z"/>',
}


def link_icon(kind, theme, stars, mobile=False):
    t = THEMES[theme]
    labels = {"website": "Website", "scholar": "Scholar", "linkedin": "LinkedIn", "stars": f"{stars:,} stars"}
    label = labels[kind]
    width = 74 if mobile else 82
    center = width / 2
    body = (f'<g transform="translate({center - 9} 3) scale(.75)" fill="none" stroke="{t["accent"]}" '
            f'stroke-width="1.55" stroke-linejoin="round" stroke-linecap="round">{ICONS[kind]}</g>')
    body += text(center, 39, label, 11.5, t["mute"], anchor="middle")
    return svg(width, 48, body, label)


def galaxy_source(theme):
    """Remove complete outlined-text layers without touching any animated star group."""
    name = "galaxy-header-light.svg" if theme == "light" else "galaxy-header.svg"
    root = ET.parse(UPSTREAM / name).getroot()
    glyph = re.compile(r"^#[limr][0-9a-f]+$")
    removed = 0
    for child in list(root):
        if child.tag == f"{{{NS}}}g" and any(
            node.tag == f"{{{NS}}}use" and glyph.fullmatch(node.get("href", ""))
            for node in child.iter()
        ):
            root.remove(child)
            removed += 1
    if removed != 8:
        raise ValueError(f"Expected 8 isolated text layers, found {removed}; review upstream before building")
    # Glyph definitions are now unused. Particle geometry uses d*, t*, b*, etc.
    defs = root.find(f"{{{NS}}}defs")
    for child in list(defs):
        if child.tag == f"{{{NS}}}path" and glyph.fullmatch("#" + child.get("id", "")):
            defs.remove(child)
    for child in list(root):
        if child.tag in (f"{{{NS}}}title", f"{{{NS}}}desc", f"{{{NS}}}rect"):
            root.remove(child)
    # The existing source stars already have a cool blue / neutral palette.
    # Background comes from the surrounding GitHub theme; keep the image transparent.
    root.attrib = {"viewBox": "420 0 420 430", "overflow": "hidden"}
    return root


def lab(theme, mobile):
    t = THEMES[theme]
    width, height = (390, 542) if mobile else (850, 310)
    x = 36 if mobile else 72
    y = 43 if mobile else 100
    body = text(x, y, "ASTRA Lab", 33 if mobile else 39, t["ink"], family=SERIF)
    body += f'<path d="M{x} {y + 16}h38" stroke="{t["accent"]}" stroke-width="1.5"/>'
    # Mark exactly the five acronym letters, keeping the user's capitalization.
    mark = lambda letter: f'<tspan fill="{t["accent"]}" text-decoration="underline">{letter}</tspan>'
    lines = [f'Next-generation {mark("A")}I for', f'{mark("S")}emiconductors and',
             f'power elec{mark("T")}ronics -', f'{mark("R")}esearch and {mark("A")}dvancements']
    for index, line in enumerate(lines):
        body += (f'<text x="{x}" y="{y + 45 + 24 * index}" font-size="{17 if mobile else 18}" '
                 f'fill="{t["mute"]}" font-family="{SERIF}">{line}</text>')
    galaxy = galaxy_source(theme)
    galaxy.set("x", "20" if mobile else "472")
    galaxy.set("y", "180" if mobile else "0")
    galaxy.set("width", "350" if mobile else "300")
    galaxy.set("height", "358" if mobile else "307")
    body += ET.tostring(galaxy, encoding="unicode")
    return svg(width, height, body, "ASTRA Lab — animated spiral galaxy",
               desc="ASTRA Lab: Next-generation AI for Semiconductors and power elecTronics - Research and Advancements. Decorative, label-free animated spiral galaxy adapted from Vinícius Melo.")


def slogan(mobile):
    width, height = (390, 148) if mobile else (850, 128)
    center = width / 2
    # 18-second loop: 0-4 moonlight reveal, 4-12 reading, 12-16 dusk, 16-18 night.
    style = f'''
      .sweep{{animation:moonlight 18s cubic-bezier(.4,0,.2,1) infinite}}
      .paper-world{{animation:twilight 18s ease-in-out infinite}}
      .chinese-reveal{{animation:chinese 18s ease-in-out infinite}}
      .english-reveal{{animation:english 18s ease-in-out infinite}}
      .beam{{opacity:0;animation:beam 18s ease-in-out infinite}}
      .night-stars{{animation:night 18s ease-in-out infinite}}
      @keyframes moonlight{{0%,89%,100%{{transform:translateX(-{width * .4}px)}}
        22.222%,88.889%{{transform:translateX({width * 1.2}px)}}}}
      @keyframes twilight{{0%,66.667%{{opacity:1}}88.889%,100%{{opacity:0}}}}
      @keyframes chinese{{0%,6%{{opacity:0}}13%,100%{{opacity:1}}}}
      @keyframes english{{0%,10%{{opacity:0}}18%,100%{{opacity:1}}}}
      @keyframes beam{{0%,2%,22.222%,100%{{opacity:0}}7%,17%{{opacity:.8}}}}
      @keyframes night{{0%,88.889%,100%{{opacity:.45}}22.222%,66.667%{{opacity:0}}}}
      @media(prefers-reduced-motion:reduce){{.sweep{{animation:none;transform:translateX({width * 1.2}px)}}
        .paper-world,.chinese-reveal,.english-reveal{{animation:none;opacity:1}}
        .night-stars,.beam{{animation:none;opacity:0}}}}
    '''
    defs = ('<linearGradient id="night" x2="0" y2="1"><stop stop-color="#0b1524"/>'
            '<stop offset="1" stop-color="#19344e"/></linearGradient>'
            '<linearGradient id="morning" x2="0" y2="1"><stop stop-color="#e5f0fc"/>'
            '<stop offset=".55" stop-color="#f6faff"/>'
            '<stop offset="1" stop-color="#ffffff"/></linearGradient>'
            '<linearGradient id="reveal"><stop stop-color="white"/>'
            '<stop offset=".5" stop-color="white"/><stop offset=".54" stop-color="black"/>'
            '<stop offset="1" stop-color="black"/></linearGradient>'
            '<linearGradient id="moonbeam"><stop stop-color="#f6fcff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#f6fcff" stop-opacity=".28"/>'
            '<stop offset="1" stop-color="#f6fcff" stop-opacity="0"/></linearGradient>'
            '<filter id="paper-grain" x="0" y="0" width="100%" height="100%">'
            '<feTurbulence type="fractalNoise" baseFrequency=".65 .12" numOctaves="3" seed="17"/>'
            '<feColorMatrix type="matrix" values="0 0 0 0 .42 0 0 0 0 .52 0 0 0 0 .63 .025 .025 .025 0 0"/>'
            '</filter>'
            f'<clipPath id="panel"><rect width="{width}" height="{height}" rx="12"/></clipPath>'
            f'<mask id="moon-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="{width}" height="{height}">'
            f'<g transform="rotate(-24 {center} {height / 2})"><g class="sweep">'
            f'<rect x="-{width * 3}" y="-{height * 4}" width="{width * 6}" height="{height * 9}" fill="url(#reveal)"/>'
            '</g></g></mask>'
            f'<style>{style}</style>')
    body = f'<g clip-path="url(#panel)"><rect width="{width}" height="{height}" fill="url(#night)"/>'
    body += '<g class="night-stars" fill="#b9d8f5">'
    for px, py, radius in ((.08, .22, .7), (.16, .75, .8), (.28, .32, .5), (.65, .18, .6), (.85, .69, .7), (.93, .29, .8)):
        body += f'<circle cx="{width * px:.1f}" cy="{height * py:.1f}" r="{radius}"/>'
    body += '</g><g class="paper-world"><g mask="url(#moon-mask)">'
    body += f'<rect width="{width}" height="{height}" fill="url(#morning)"/>'
    if mobile:
        # Small fixed specks keep the paper feel without per-frame turbulence work.
        body += '<g fill="#6885a1" opacity=".045">'
        for index in range(80):
            px = (index * 137 + 17) % width
            py = (index * 61 + 23) % height
            body += f'<circle cx="{px}" cy="{py}" r=".55"/>'
        body += '</g>'
    else:
        body += f'<rect width="{width}" height="{height}" filter="url(#paper-grain)"/>'
    body += '<g class="motto">'
    if mobile:
        body += '<g class="chinese-reveal">' + lettering("chinese", 46, 65, center=center) + '</g>'
        body += '<g class="english-reveal">' + lettering("english", 21, 105, center=center) + '</g>'
    else:
        outlines = json.loads((ROOT / "assets" / "lettering.json").read_text(encoding="utf-8-sig"))
        chinese_width = outlines["chinese"]["width"] * .044
        english_width = outlines["english"]["width"] * .032
        left = center - (chinese_width + english_width + 28) / 2
        body += '<g class="chinese-reveal">' + lettering("chinese", 44, 80, x=left) + '</g><g class="english-reveal">'
        body += text(left + chinese_width + 14, 75, "-", 26, "#395978", family=SERIF, anchor="middle")
        body += lettering("english", 32, 78, x=left + chinese_width + 28)
        body += '</g>'
    body += '</g></g></g>'
    body += f'<g class="beam" transform="rotate(-24 {center} {height / 2})"><g class="sweep">'
    body += f'<rect x="-{width * .08}" y="-{height * 4}" width="{width * .4}" height="{height * 9}" fill="url(#moonbeam)"/>'
    body += '</g></g></g>'
    return svg(width, height, body, "知行合一 - Unity of Knowledge and Action", defs,
               "Diagonal moonlight reveals calligraphy on fine silver-blue paper. Four seconds to reveal, eight seconds to read, four seconds fading to darkness, two seconds of night. Reduced motion displays the slogan immediately.")


def repositories(refresh):
    cache = UPSTREAM / "repositories.json"
    if refresh:
        repos = []
        page = 1
        while True:
            headers = {"Accept": "application/vnd.github+json", "User-Agent": "XinzeLee-profile"}
            token = os.environ.get("GITHUB_TOKEN")
            if token:
                headers["Authorization"] = f"Bearer {token}"
            request = urllib.request.Request(
                f"https://api.github.com/users/XinzeLee/repos?type=owner&per_page=100&page={page}", headers=headers)
            with urllib.request.urlopen(request, timeout=30) as response:
                batch = json.load(response)
            repos.extend(batch)
            if len(batch) < 100:
                break
            page += 1
        # Store only public fields that this profile generator actually needs.
        cache.write_text(json.dumps([{k: r[k] for k in ("name", "stargazers_count", "fork", "private")}
                                     for r in repos], indent=2) + "\n", encoding="utf-8")
    return json.loads(cache.read_text(encoding="utf-8-sig"))


def picture(name, alt, width=850):
    return f'''  <picture>
    <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="assets/generated/{name}-mobile-light.svg" />
    <source media="(max-width: 600px)" srcset="assets/generated/{name}-mobile-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="assets/generated/{name}-light.svg" />
    <img src="assets/generated/{name}-dark.svg" width="{width}" alt="{alt}" />
  </picture>'''


def readme():
    urls = {"website": "https://xinzelee.github.io/", "scholar": "https://scholar.google.com/citations?user=YilrlZMAAAAJ",
            "linkedin": "https://www.linkedin.com/in/xinze-li-8199561b0/",
            "stars": "https://github.com/XinzeLee?tab=repositories&amp;sort=stargazers"}
    links = []
    for kind, url in urls.items():
        links.append(f'''  <a href="{url}" title="{'Total stars received by public repositories' if kind == 'stars' else kind.title()}">
    <picture>
      <source media="(max-width: 600px) and (prefers-color-scheme: light)" srcset="assets/generated/{kind}-mobile-light.svg" />
      <source media="(max-width: 600px)" srcset="assets/generated/{kind}-mobile-dark.svg" />
      <source media="(prefers-color-scheme: light)" srcset="assets/generated/{kind}-light.svg" />
      <img src="assets/generated/{kind}-dark.svg" alt="{'LinkedIn' if kind == 'linkedin' else kind.title()}" />
    </picture>
  </a>''')
    return ('<!-- Xinze Li profile. Local SVGs; no third-party badge or typing service. -->\n'
            '<p align="center">\n' + picture("header", "Xinze Li — Researcher, Educator, Engineer in AI for Power Electronics and Semiconductor Fabrication") + '\n</p>\n\n'
            '<p align="center">\n' + '\n'.join(links) + '\n</p>\n\n'
            '<p align="center">\n' + picture("lab", "ASTRA Lab: Next-generation AI for Semiconductors and power elecTronics - Research and Advancements; animated galaxy without text") + '\n</p>\n\n'
            '<p align="center">\n' + picture("slogan", "知行合一 - Unity of Knowledge and Action; darkness-to-dawn animation") + '\n</p>\n\n'
            '<!-- Galaxy animation adapted from https://github.com/vinimlo/galaxy-profile, GPL-3.0. See ATTRIBUTION.md. -->\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-stars", action="store_true")
    args = parser.parse_args()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    repos = repositories(args.refresh_stars)
    stars = sum(r["stargazers_count"] for r in repos if not r.get("private", False))
    for theme in THEMES:
        for mobile in (False, True):
            suffix = f"{'mobile-' if mobile else ''}{theme}"
            write(f"header-{suffix}.svg", header(theme, mobile))
            write(f"lab-{suffix}.svg", lab(theme, mobile))
            write(f"slogan-{suffix}.svg", slogan(mobile))
        for kind in ICONS:
            write(f"{kind}-{theme}.svg", link_icon(kind, theme, stars))
            write(f"{kind}-mobile-{theme}.svg", link_icon(kind, theme, stars, mobile=True))
    (ROOT / "README.md").write_text(readme(), encoding="utf-8")
    (OUTPUT / "metadata.json").write_text(json.dumps({"username": "XinzeLee", "total_stars": stars,
        "definition": "Sum of stars received by all owned public repositories, including forks.",
        "public_repositories": len(repos)}, indent=2) + "\n", encoding="utf-8")
    print(f"Built 28 SVGs and README. Total public repository stars: {stars}.")


if __name__ == "__main__":
    main()
