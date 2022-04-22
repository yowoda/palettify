from __future__ import annotations

import logging
import multiprocessing
import pathlib
import threading
import typing as t

from PIL import Image

from palettify.internal import apply_palette, calculate_size, load_palette

if t.TYPE_CHECKING:
    from palettify.internal import PaletteT

_LOGGER: t.Final[logging.Logger] = logging.getLogger(__name__)

__all__: t.List[str] = ["palettify_image"]


def _process_image(
    input_path: str,
    output_path: str,
    palette: t.Optional[PaletteT],
    auto_palette: t.Optional[int],
    autoscale: bool,
    width: t.Optional[int],
    height: t.Optional[int],
    threads: int,
) -> None:
    img = Image.open(input_path)
    width, height = calculate_size(
        img=img, autoscale=autoscale, width=width, height=height
    )

    size = (width, height)
    if size != img.size:
        img = img.resize(size)
        _LOGGER.info("Resized image to %sx%s", width, height)

    if auto_palette is not None:
        _LOGGER.info(
            "Creating color palette using %s most dominant colors.", auto_palette
        )
        palette = [
            rgb
            for _, rgb in sorted(
                img.getcolors(16777216), key=lambda t: t[0], reverse=True
            )[:auto_palette]
        ]

    pixels = img.load()
    pixel_step = width // threads

    threads_started: t.List[threading.Thread] = []

    _LOGGER.info("Starting %s threads for %s.", threads, input_path)
    for x in range(pixel_step, width + pixel_step, pixel_step):
        t = threading.Thread(
            target=apply_palette, args=(pixels, palette, x - pixel_step, x, height)
        )
        t.daemon = True
        t.start()
        threads_started.append(t)

    for t in threads_started:
        t.join()

    _LOGGER.info("Saving image to %s.", output_path)
    img.save(output_path)


def _path_duplicate(path: pathlib.Path) -> str:
    return path.stem + "-palettified" + path.suffix


def palettify_image(
    paths: t.Iterable[str],
    palette: str,
    *,
    autoscale: bool = False,
    output: t.Optional[str] = None,
    overwrite: bool = False,
    width: t.Optional[int] = None,
    height: t.Optional[int] = None,
    threads: int = 10,
    verbose: bool = False,
) -> None:
    if verbose is True:
        logging.basicConfig(format="%(message)s", level="INFO")

    auto_palette: t.Optional[int] = None
    _LOGGER.info("Loading color palette.")
    if not palette.isdigit():
        palette = load_palette(palette)

    else:
        auto_palette = int(palette)
        _LOGGER.info(
            "Palette detection is enabled. Color palette will be created using the %s most dominant colors.",
            auto_palette,
        )

    processes_started: t.List[multiprocessing.Process] = []

    for input_path in paths:
        _LOGGER.info("Processing %s.", input_path)
        input_path = pathlib.Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"{input_path} does not exist.")

        if overwrite is True:
            _LOGGER.info("Overwrite is enabled, using input path as output path.")
            output_path = input_path

        elif output is not None:
            output_path = pathlib.Path(output)
            _LOGGER.info("Processing %s.", output_path)
            if output_path.exists() and output_path.is_dir():
                output_path /= _path_duplicate(input_path)

            elif len(paths) > 1:
                raise NotADirectoryError(
                    "A directory needs to be passed for multiple input paths."
                )

        else:
            output_path = input_path.parent / _path_duplicate(input_path)
            _LOGGER.info("No output path is given, defaulting to %s.", output_path)

        _LOGGER.info("Starting process for %s.", input_path)
        p = multiprocessing.Process(
            target=_process_image,
            args=(
                str(input_path),
                str(output_path),
                palette,
                auto_palette,
                autoscale,
                width,
                height,
                threads,
            ),
        )
        p.daemon = True
        p.start()
        processes_started.append(p)

    for p in processes_started:
        p.join()
