# Working with images

This guide shows how to draw pictures on the canvas with the `image()` helper. It uses simple English and many examples so that high school students who are not native English speakers can follow every step.

## Function signature at a glance

```python
from drawzero import image

image(image, pos, width: int = None, alpha=255)
```

The four parameters control what file is loaded, where it appears, how wide it becomes, and how transparent it looks.

| Parameter | What it means | Required? | Typical values |
|-----------|----------------|-----------|----------------|
| `image`   | Path to the picture file (for example `'cat.png'` or `this_file_dir / 'cat.png'`) | Yes | PNG, JPG, or other formats that `pygame` can open |
| `pos`     | Top-left corner of where the picture will be drawn on the canvas | Yes | `(x, y)` tuples like `(100, 200)` |
| `width`   | Desired width on the canvas. Height changes automatically to keep the same shape. | No | Whole numbers such as `200` or `350` |
| `alpha`   | Transparency. `255` is fully solid, `0` is invisible. | No | Numbers between `0` and `255` |

> ℹ️ If you want a deeper explanation of transparency, read [Transparency (`alpha`) and line thickness (`line_width`)](transparency_and_line_width.md#understanding-alpha).

## Parameter by parameter

### `image`: choose the file to draw

* Accepts strings with file names, absolute paths, or `pathlib.Path` objects.
* Relative paths are resolved from the Python file that calls `image()`. A safe pattern is:
  ```python
  from pathlib import Path
  this_file_dir = Path(__file__).resolve().parent
  image(this_file_dir / 'pictures' / 'cat.png', (100, 100))
  ```
* PNG images keep their transparent background. JPG files ignore transparent pixels because the format does not store them.
* Large images are fine, but very big files slow down loading. For games or animations, keep images under 2000×2000 pixels if possible.

**Common mistakes**

* Typing a wrong folder name. Fix it by printing the full path and checking if the file exists.
* Forgetting the file extension (`.png`, `.jpg`, `.gif`).
* Using backslashes (`\`) on Windows inside normal strings. Either use raw strings (`r'images\\cat.png'`) or forward slashes (`'images/cat.png'`).

### `pos`: place the image on the canvas

* The canvas uses the same 1000×1000 virtual coordinate system as the shape primitives.
* `(0, 0)` is the top-left corner. Increasing `x` moves the picture to the right. Increasing `y` moves it down.
* `pos` can be a tuple, list, or a `Pt` object.
* The coordinates represent the **top-left corner** of the image. If you want to center the picture, subtract half of its width and height:
  ```python
  image('badge.png', (500 - 128, 500 - 128))
  ```
* `image()` will round the numbers to the nearest pixel. Decimals are allowed, but they are converted to integers internally.

### `width`: control the size without breaking proportions

* Leave it as `None` to keep the original size of the file.
* Pass a positive integer to scale the image horizontally. The helper automatically calculates the matching height so the picture does not look stretched.
* The value is measured in virtual canvas units. With the default 1000×1000 window, `width=200` shows the image 200 pixels wide.
* Set `width` to the same value for all frames in an animation to avoid flickering.
* You can compute the width dynamically. For example, to scale by 50%:
  ```python
  original_width = 400
  image('robot.png', (300, 400), width=original_width // 2)
  ```
* Passing `0` or a negative value will raise a `BadDrawParmsError`. Always use a positive integer.

### `alpha`: blend images with the background

* Accepts integers from `0` (fully transparent) to `255` (fully opaque).
* The default value `255` draws the picture with no extra transparency.
* Use mid-range values (for example `128`) to create soft shadows, glass effects, or hints of motion.
* The alpha value applies to the entire image. Per-pixel transparency stored in PNG files still works and is multiplied by this value.
* Read the [full guide on transparency](transparency_and_line_width.md#understanding-alpha) to see layered examples and mixing tips.

## Step-by-step examples

### Example 1 – show a mascot in the corner

```python
from drawzero import *

fill('white')
image('mascot.png', (50, 50))
```

The mascot keeps its original size. The white background makes the colors easy to see.

### Example 2 – center an image and scale it to a fixed width

```python
from drawzero import *
from pathlib import Path

this_file_dir = Path(__file__).resolve().parent
logo_path = this_file_dir / 'assets' / 'school_logo.png'

# Draw the logo 300 units wide and keep it centered on the canvas
logo_width = 300
logo_x = 500 - logo_width // 2
logo_y = 300
image(logo_path, (logo_x, logo_y), width=logo_width)
```

This snippet works even if you move the script to another computer, because the path is built relative to the file location.

### Example 3 – ghost trail using alpha

```python
from drawzero import *

fill('black')
for step in range(5):
    image('spaceship.png', (150 + step * 80, 400), width=200, alpha=255 - step * 40)
```

The loop draws five copies of the same image. Each copy is more transparent than the previous one, creating a motion trail.

### Example 4 – responsive width based on the window size

```python
from drawzero import *

fill((10, 10, 40))
window_width = 800  # imagine we measured the real window
picture_width = int(window_width * 0.6)
image('city.png', (100, 200), width=picture_width)
```

Because the width is calculated in code, you can adapt it to different screen sizes.

## Checklist before calling `image()`

1. Place your picture file in the project folder (for example `docs/` or `assets/`).
2. Confirm the Python script can reach the file path (print it if needed).
3. Decide the placement coordinates. Use `grid()` from DrawZero if you need help visualizing positions.
4. Choose a width or leave it as `None`.
5. Decide whether you need extra transparency.
6. Only then call `image()`.

## Troubleshooting guide

| Problem | Likely cause | How to fix |
|---------|--------------|------------|
| `BadDrawParmsError: bad coords` | The `pos` argument is not a two-number tuple or list. | Make sure you pass `(x, y)` with numbers. |
| `No file '...' found in working directory` | The image path is wrong. | Print `Path(image).resolve()` and verify the file exists there. |
| Image looks stretched | You set both `width` and `height`. Only `width` should be supplied. | Remove any manual height scaling. DrawZero calculates it for you. |
| Image is very blurry | You scaled a tiny picture to a huge size. | Start with a higher-resolution file or reduce the target width. |
| Transparent PNG looks too solid | You used `alpha=255`. | Lower the alpha value to let the background show through. |

With these tips you can confidently display images and combine them with the drawing primitives.
