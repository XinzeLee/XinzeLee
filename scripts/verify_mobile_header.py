"""Check role exclusivity, including boundaries and animation-disabled fallback."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
NS = '{http://www.w3.org/2000/svg}'
for path in (ROOT / 'assets' / 'generated').glob('header-*.svg'):
    root = ET.parse(path).getroot()
    group = next(node for node in root.iter(NS + 'g') if node.get('class') == 'moving-role')
    roles = list(group)
    assert [''.join(letter.text for letter in node.findall(NS + 'tspan')) for node in roles] == ['Researcher', 'Educator', 'Engineer']
    assert sum(node.get('visibility') == 'visible' for node in roles) == 1
    timelines = []
    for role in roles:
        assert 'clip-path' not in role.attrib
        animation = role.find(NS + 'animate')
        assert animation.get('attributeName') == 'visibility'
        assert animation.get('calcMode') == 'discrete'
        assert animation.get('dur') == '6s' and animation.get('begin') == '0s'
        timelines.append((list(map(float, animation.get('keyTimes').split(';'))),
                          animation.get('values').split(';')))
    boundaries = timelines[0][0]
    samples = [i / 6000 for i in range(6000)]
    samples += [t + delta for t in boundaries[1:-1] for delta in (-1e-12, 0, 1e-12)]
    for time in samples:
        visible = 0
        for times, values in timelines:
            phase = max(i for i, start in enumerate(times) if start <= time)
            visible += values[phase] == 'visible'
        assert visible == 1, (path.name, time, visible)
    # Every typed frame is a prefix of one role, including all letter boundaries.
    letter_timelines = []
    for role in roles:
        entries = []
        for letter in role.findall(NS + 'tspan'):
            assert letter.get('visibility') == role.get('visibility')
            animation = letter.find(NS + 'animate')
            assert animation.get('calcMode') == 'discrete' and animation.get('dur') == '6s'
            times = list(map(float, animation.get('keyTimes').split(';')))
            entries.append((times, animation.get('values').split(';')))
            samples += [t + delta for t in times[1:-1] for delta in (-1e-12, 0, 1e-12)]
        letter_timelines.append(entries)
    for time in samples:
        counts = []
        for (times, values), entries in zip(timelines, letter_timelines):
            role_visible = values[max(i for i, start in enumerate(times) if start <= time)] == 'visible'
            flags = [values[max(i for i, start in enumerate(times) if start <= time)] == 'visible'
                     for times, values in entries]
            assert role_visible or not any(flags)
            assert flags == sorted(flags, reverse=True), (path.name, time, flags)
            counts.append(sum(flags))
        assert sum(count > 0 for count in counts) <= 1, (path.name, time, counts)
    assert any(0 < count < len(entries) for entries in letter_timelines
               for time in (.03, .363333333333, .696666666667)
               for count in [sum(values[max(i for i, start in enumerate(times) if start <= time)] == 'visible'
                                 for times, values in entries)])
for path in (ROOT / 'assets' / 'generated').glob('slogan-mobile-*.svg'):
    root = ET.parse(path).getroot()
    assert not any('filter' in node.attrib for node in root.iter()), path.name
print('PASS: typing and erasing show a prefix of at most one role at all letter boundaries and 6,000 samples per header; safe fallback; mobile slogan uses no filters.')
