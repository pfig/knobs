"""Executable and public bits."""

from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from knobs import knobs

__version__ = "0.0.1"
__all__ = [
    "__version__",
]


def main() -> None:
    parser = ArgumentParser(
        description="Create knob animations for audio plugins.",
        prog="knob",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--knob", "-k", type=str, required=True, help="Path to the knob image file."
    )
    parser.add_argument(
        "--strip", "-s", type=str, required=True, help="Path to save the knob animation strip."
    )
    parser.add_argument(
        "--nframes", "-n", type=int, default=10, help="Number of frames in the animation."
    )
    parser.add_argument(
        "--angle", "-a", type=int, default=225, help="Starting angle for the knob rotation."
    )

    args = parser.parse_args()

    knob_image = knobs.load_knob_image(args.knob)
    animation_strip = knobs.create_animation(
        knob_image, nframes=args.nframes, start_angle=args.angle
    )
    knobs.save_knob_animation(animation_strip, args.strip)

    print(f"Knob animation saved to {args.strip}")
