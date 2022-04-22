from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from PIL.Image import Image

__all__: t.Final[t.List[str]] = ["calculate_size"]


def calculate_size(
    img: Image, autoscale: bool, width: t.Optional[int], height: t.Optional[int]
) -> t.Tuple[int, int]:
    if autoscale is True:
        from PIL import ImageGrab

        height = ImageGrab.grab().height
        width = int(img.width / img.height * height)

    if width is not None:
        height = int(width * img.height / img.width)

    if height is not None:
        if width is None:
            width = int(img.width / img.height * height)

    return width or img.width, height or img.height
