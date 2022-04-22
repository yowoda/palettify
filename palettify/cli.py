import argparse
import sys

from palettify import palettify_image


def excepthook(_, error: BaseException, __) -> None:
    print(f"\33[31m{error}\33[0m")


def main():
    sys.excepthook = excepthook
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "paths", nargs="+", help="The paths to the images to apply the palette to."
    )
    parser.add_argument(
        "-p",
        "--palette",
        required=True,
        help="The JSON file to load the palette from or the amount of the most dominant colors in the original image to use for the palette.",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="Path to the file or directory to write the image(s) to.",
    )
    parser.add_argument(
        "-O",
        "--overwrite",
        required=False,
        action="store_true",
        help="Whether to overwrite the original images.",
    )
    parser.add_argument(
        "-a",
        "--autoscale",
        required=False,
        action="store_true",
        help="Whether to resize the image to the screen resolution.",
    )
    parser.add_argument(
        "-w", "--width", required=False, type=int, help="The width of the image."
    )
    parser.add_argument(
        "-H", "--height", required=False, type=int, help="The height of the image."
    )
    parser.add_argument(
        "-t",
        "--threads",
        required=False,
        type=int,
        default=10,
        help="The number of threads to start.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        action="store_true",
        help="Explain what is being done.",
    )
    args = parser.parse_args()

    palettify_image(**args.__dict__)
