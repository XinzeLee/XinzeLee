"""Check asset integrity and prove that removing labels preserves the galaxy."""
from collections import Counter
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from build_profile import galaxy_source, THEMES

ROOT = Path(__file__).resolve().parents[1]
NS = "{http://www.w3.org/2000/svg}"
glyph = re.compile(r"^#[limr][0-9a-f]+$")

for theme in THEMES:
    filename = "galaxy-header-light.svg" if theme == "light" else "galaxy-header.svg"
    before = ET.parse(ROOT / "assets" / "upstream" / filename).getroot()
    after = galaxy_source(theme)
    def particles(root):
        return Counter(tuple(sorted(node.attrib.items())) for node in root.iter(NS + "use")
                       if not glyph.fullmatch(node.get("href", "")))
    assert particles(before) == particles(after), f"Particle references changed: {theme}"
    assert [node.text for node in before.iter(NS + "style")] == [node.text for node in after.iter(NS + "style")], "Original animation CSS changed"
    assert not any(glyph.fullmatch(node.get("href", "")) for node in after.iter(NS + "use")), "Outlined labels remain"

files = list((ROOT / "assets" / "generated").glob("*.svg"))
assert len(files) == 28
for path in files:
    root = ET.parse(path).getroot()
    nodes = list(root.iter())
    ids = [node.get("id") for node in nodes if node.get("id")]
    assert len(ids) == len(set(ids)), f"Duplicate SVG IDs: {path.name}"
    for node in nodes:
        assert node.tag not in (NS + "script", NS + "foreignObject"), path.name
        href = node.get("href", "")
        assert not href or href.startswith("#"), f"External SVG dependency: {path.name}"
        refs = re.findall(r"url\(#([^)]*)\)", " ".join(node.attrib.values()))
        if href.startswith("#"):
            refs.append(href[1:])
        assert all(ref in ids for ref in refs), f"Missing SVG reference: {path.name}: {refs}"

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for asset in re.findall(r'(?:src|srcset)="([^"]+)"', readme):
    assert (ROOT / asset).is_file(), f"README missing asset: {asset}"
assert "Reveal it" not in readme
print("PASS: 28 self-contained SVGs; all README assets exist; no outlined galaxy labels remain.")
print("PASS: original particle references and all galaxy animation CSS are unchanged in both themes.")
