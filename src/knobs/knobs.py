"""Functions to create knob animations for audio plugins."""

from PIL import Image


def load_knob_image(knob_path: str) -> Image.Image:
    """Load a knob image from the specified path."""
    try:
        knob_image = Image.open(knob_path)
        return knob_image
    except Exception as e:
        raise ValueError(f"Error loading knob image from {knob_path}: {e}") from e


def create_knob_strip(knob_width: int, knob_height: int, nframes: int) -> Image.Image:
    """Create a strip of knobs from the given image."""

    strip_height = knob_height * nframes
    strip = Image.new("RGBA", (knob_width, strip_height), (0, 0, 0, 0))

    return strip


def create_animation(knob_image: Image.Image, nframes: int, start_angle: int) -> Image.Image:
    """Create an animation from the knob image."""

    knob_width, knob_height = knob_image.size
    strip = create_knob_strip(knob_width, knob_height, nframes)

    knob_travel = 360 - (270 - start_angle) * 2
    knob_step = knob_travel / (nframes - 1)
    for f in range(nframes):
        angle = -f * knob_step
        rotated_knob = knob_image.rotate(angle, expand=False)
        strip.paste(rotated_knob, (0, f * knob_height))

    return strip


def save_knob_animation(strip: Image.Image, output_path: str) -> None:
    """Save the knob animation strip to the specified path."""
    try:
        strip.save(output_path, format="PNG")
    except Exception as e:
        raise ValueError(f"Error saving knob animation to {output_path}: {e}") from e
