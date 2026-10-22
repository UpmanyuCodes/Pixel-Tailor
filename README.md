# Seam Carving Image Resizer

Make an image **narrower without squeezing** the things in it.

Normal resizing squashes everything, so people and objects look thin. This tool uses **seam carving**: it removes thin lines of pixels (one pixel from every row) from the boring parts of the image, like sky or empty ground. Important things stay the same shape.

## Example

<img width="507" height="173" alt="Sample input and output" src="https://github.com/user-attachments/assets/ae3c66cf-0ed7-43c2-82fb-f1067508720d" />

Left: original image. Right: resized to a narrower width.

## How it works

1. **Find importance:** edges and details get a high score. Flat areas get a low score.
2. **Find the cheapest seam:** a path from top to bottom, one pixel per row, with the lowest total score (found with dynamic programming).
3. **Remove the seam:** the image becomes 1 pixel narrower.
4. **Repeat** until the image reaches the width you want.

## Requirements

- Python 3.8 or newer
- numpy
- Pillow

```
pip install numpy pillow
```

## How to use

1. Put your image in the same folder as the script.
2. Open `MystyleCompressor.py` and change the settings at the top:

   ```python
   INPUT_FILE = "photo.jpg"   # your image name
   OUTPUT_FILE = "out.jpg"    # name of the new image
   NEW_WIDTH = 600            # new width in pixels (smaller than the original)
   NEW_HEIGHT = None          # optional: new height in pixels
   ```

3. Run:

   ```
   python MystyleCompressor.py
   ```

4. Open `out.jpg` to see the result.

## Tips for good results

- **Resize big photos first.** Use an image about 800-1000 px wide. Large images are very slow.
- **Do not cut too much.** Removing up to about 30% of the width usually looks natural. Removing more can bend or distort objects.
- **Best images:** landscapes, skies, and subjects on a plain background.
- **Harder images:** busy scenes, flat-color drawings, and dark silhouettes, because the tool may cut through the subject.

## Known limits

- Pure Python, so it is slow on big images.
- Straight lines (like a horizon or a building edge) can look bent after big cuts.
- Flat dark or single-color objects can be treated as "boring" and get thinner.

## Ideas for the future

- Protect mask: mark areas that must never be cut (faces, people).
- Forward energy: a smarter way to choose seams, with less distortion.
- Faster version using Numba.
- Simple app with a slider to preview the result.

## How it was built

- `numpy` for fast array math
- `Pillow` for opening and saving images

