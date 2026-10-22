"""
Seam carving: make an image narrower without squeezing the objects.

Needs:  pip install numpy pillow
"""
import numpy as np
from PIL import Image


INPUT_FILE = "photo.jpg"    # your photo name
OUTPUT_FILE = "out.jpg"     # the new image will be saved with this name
NEW_WIDTH = 600             # must be smaller than the photo's width
NEW_HEIGHT = None           # optional, e.g. 400. Leave None to keep height



def energy(img):
    """How 'important' each pixel is. Edges = high, flat areas = low."""
    gray = img.astype(np.float64).mean(axis=2)
    gy, gx = np.gradient(gray)
    return np.abs(gx) + np.abs(gy)


def find_vertical_seam(e):
    """Find the cheapest line from top to bottom (one pixel per row)."""
    h, w = e.shape
    cost = e.copy()
    back = np.zeros((h, w), dtype=np.int64)
    cols = np.arange(w)
    for i in range(1, h):
        prev = cost[i - 1]
        left = np.r_[np.inf, prev[:-1]]
        right = np.r_[prev[1:], np.inf]
        options = np.stack([left, prev, right])
        choice = options.argmin(axis=0)  # 0=left, 1=up, 2=right
        back[i] = cols + choice - 1
        cost[i] += options[choice, cols]

    seam = np.zeros(h, dtype=np.int64)
    seam[-1] = cost[-1].argmin()
    for i in range(h - 1, 0, -1):
        seam[i - 1] = back[i, seam[i]]
    return seam


def remove_vertical_seam(img, seam):
    """Delete one pixel from every row along the seam."""
    h, w, c = img.shape
    keep = np.ones((h, w), dtype=bool)
    keep[np.arange(h), seam] = False
    return img[keep].reshape(h, w - 1, c)


def reduce_width(img, n):
    """Remove n seams."""
    for i in range(n):
        img = remove_vertical_seam(img, find_vertical_seam(energy(img)))
        if (i + 1) % 50 == 0:
            print(f"  removed {i + 1}/{n} seams")
    return img


def carve(img, new_w=None, new_h=None):
    h, w, _ = img.shape
    if new_w is not None:
        if not 0 < new_w <= w:
            raise ValueError(f"NEW_WIDTH must be between 1 and {w}")
        img = reduce_width(img, w - new_w)
    if new_h is not None:
        if not 0 < new_h <= h:
            raise ValueError(f"NEW_HEIGHT must be between 1 and {h}")
        # height: do the same on a rotated image
        t = np.ascontiguousarray(img.transpose(1, 0, 2))
        t = reduce_width(t, h - new_h)
        img = np.ascontiguousarray(t.transpose(1, 0, 2))
    return img



arr = np.array(Image.open(INPUT_FILE).convert("RGB"))
print(f"Original size: {arr.shape[1]} x {arr.shape[0]}")
out = carve(arr, NEW_WIDTH, NEW_HEIGHT)
Image.fromarray(out).save(OUTPUT_FILE)
print(f"New size: {out.shape[1]} x {out.shape[0]}")
print("done")