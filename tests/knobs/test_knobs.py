import pytest

from knobs import knobs


def test_load_knob_image():
    """Test loading a knob image."""
    knob_image = knobs.load_knob_image("tests/resources/sample.png")
    assert knob_image is not None
    assert knob_image.size == (40, 40)


def test_load_knob_image_invalid_path():
    """Test loading a knob image with an invalid path."""
    with pytest.raises(ValueError) as exc_info:
        knobs.load_knob_image("invalid/path/to/knob.png")

    assert str(exc_info.value).startswith(
        "Error loading knob image from invalid/path/to/knob.png:"
    )


def test_create_knob_strip():
    """Test creating a knob strip."""
    strip = knobs.create_knob_strip(knob_width=40, knob_height=40, nframes=10)
    assert strip.size == (40, 400)


def test_create_animation():
    """Test creating an animation from a knob image."""
    knob_image = knobs.load_knob_image("tests/resources/sample.png")
    animation_strip = knobs.create_animation(knob_image, nframes=10, start_angle=225)
    assert animation_strip.size == (40, 400)

    # Check if the first frame is rotated correctly
    first_frame = animation_strip.crop((0, 0, 40, 40))
    assert first_frame.size == (40, 40)  # First frame should be the same size as the knob image


def test_save_knob_animation(tmp_path):
    """Test saving a knob animation."""
    knob_image = knobs.load_knob_image("tests/resources/sample.png")
    animation_strip = knobs.create_animation(knob_image, nframes=10, start_angle=225)

    output_path = tmp_path / "knob_animation.png"
    knobs.save_knob_animation(animation_strip, str(output_path))

    # Check if the file was created
    assert output_path.exists()
    assert output_path.stat().st_size > 0  # Ensure the file is not empty


def test_save_knob_animation_invalid_path():
    """Test saving a knob animation with an invalid path."""
    knob_image = knobs.load_knob_image("tests/resources/sample.png")
    animation_strip = knobs.create_animation(knob_image, nframes=10, start_angle=225)

    with pytest.raises(ValueError) as exc_info:
        knobs.save_knob_animation(animation_strip, "invalid/path/to/knob_animation.png")

    assert str(exc_info.value).startswith(
        "Error saving knob animation to invalid/path/to/knob_animation.png:"
    )
