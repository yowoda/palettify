import json
import pathlib
import typing as t

PaletteT = t.List[t.Iterable[int]]

__all__: t.List[str] = ["PaletteT", "load_palette"]


def load_palette(path: str) -> PaletteT:
    path = pathlib.Path(path)
    if path.exists() is False:
        raise FileNotFoundError(f"{path} does not exist.")

    if path.is_dir() is True:
        raise IsADirectoryError(f"{path} is a directory.")

    with open(str(path)) as fp:
        palette = json.load(fp)

    if not isinstance(palette, list) and not all(
        isinstance(channel, int) for rgb in palette for channel in rgb
    ):
        raise ValueError("JSON file must contain list of RGB channels.")

    return [tuple(rgb) for rgb in palette]
