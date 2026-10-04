"""Assemble browser-captured frames into a motion preview. Requires Pillow."""
import json
from pathlib import Path
from PIL import Image

root = Path(__file__).resolve().parents[1]
folder = root / 'preview' / '_moonframes'
times = json.loads((folder / 'timing.json').read_text())
frames = []
for index in range(len(times)):
    with Image.open(folder / f'{index:03}.png') as image:
        frames.append(image.convert('RGB').quantize(colors=256, dither=Image.Dither.NONE))
durations = [max(40, (int(end - start) // 10) * 10)
             for start, end in zip(times, times[1:] + [18000])]
destination = root / 'preview' / 'moonlight-transition.gif'
frames[0].save(destination, save_all=True, append_images=frames[1:], duration=durations,
               loop=0, optimize=False, disposal=2)
print(f'Saved {destination.name}: {len(frames)} captured frames; {sum(durations)/1000:.2f} seconds')
# Only remove this task's temporary captured frames, after the GIF was saved.
assert folder.resolve() == (root / 'preview' / '_moonframes').resolve()
for file in folder.iterdir():
    if file.suffix in ('.png', '.json'):
        file.unlink()
folder.rmdir()
