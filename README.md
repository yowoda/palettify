# palettify - Apply color palettes to images within seconds

## Installation
```
pip install palettify
```
<details>
<summary>
    Didn't work?
</summary>

- `pip` is not in `PATH`
    ```sh
    python -m pip install palettify
    ```

- Check if the path of your python executable matches the path of the interpreter you run your code with<br>
    In UNIX-like systems:
    ```sh
    which python
    ```

</details>

## Usage
You can use either the command-line or the python API to palettify an image.

Through the command-line:
Invoke palettify using `palettify` or `python -m palettify`.

### paths [paths ...] (required)
You can input multiple images, each one pointing to an existing file. A list of supported image formats can be found [here](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html).

### -p/--palette (required)
The color palette to use. If an integer `n`, palettify will try to find the `n` most dominant colors in the original image and build the palette using those colors.

### -o/--output (optional)
If more than one input path is given, the output path **has** to be an existing directory. If only one input path is given, the output path can be either a directory or the path to a file. If no output path is given, palettify will create path duplicates of the input paths and add a `-palettified` suffix.

### -a/--autoscale (optional)
If autoscale is enabled, palettify tries to find the desktop resolution and resizes the image accordingly, while keeping the original ratio. A display server is required Defaults to `False`.

### -w/--width (optional)
The width of the palettified image. If `-h/--height` is not given, palettify will calculate the height to keep the original ratio.

### -H/--height (optional)
The height of the palettified image. If `-w/--width` is not given, palettify will calculate the width to keep the original ratio. If neither `width` or `height` are given, palettify will use the resolution of the original image.

### -t/--threads (optional)
The number of threads to start for a single image. Defaults to `10`.

### -v/--verbose (optional)
Whether to explain what is being done. Defaults to `False`.

## Invoking palettify through python
```py
from palettify import palettify_image

palettify_image(...)
```

You can pass in the same arguments as in the command-line. However, optional arguments are keyword-only.