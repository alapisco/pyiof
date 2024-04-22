import pytest
from PIL import Image
import numpy as np


@pytest.fixture()
def red_pil_image():
    return Image.new(mode='RGB', size=(100, 100), color=(255, 0, 0))


def test_grayscale_image(image_processor, red_pil_image):
    # Convert the image to grayscale
    grayscale_image = image_processor.grayscale_image(red_pil_image)

    # Check that the converted image is in grayscale mode
    assert grayscale_image.mode == 'L'


def test_binarize_image(image_processor, red_pil_image):
    gray_image = image_processor.grayscale_image(red_pil_image)

    # Binarize the image with a threshold of 100
    threshold = 100
    binary_image = image_processor.binarize_image(gray_image, threshold)

    # Check that all pixels are either 0 or 255
    for pixel in binary_image.getdata():
        assert pixel in (0, 255)

    # Check that the image is still in 'L' mode
    assert binary_image.mode == 'L'


def test_convert_pil_image_to_np_array(image_processor, red_pil_image):
    result_array = image_processor.convert_pil_image_to_np_array(red_pil_image)
    assert isinstance(result_array, np.ndarray)
    assert result_array.shape == (100, 100, 3)


def test_get_regions_images(image_processor, red_pil_image):
    regions = [(10, 10, 50, 50), (60, 60, 30, 30)]
    images = image_processor.get_images_from_regions(regions, red_pil_image)

    assert len(regions) == len(images)

    for image in images:
        assert isinstance(image, Image.Image)

    for i, image in enumerate(images):
        x, y, w, h = regions[i]
        assert image.size == (w, h)


def test_get_image_size(image_processor, red_pil_image):
    width, height = image_processor.get_image_dimensions(red_pil_image)
    expected_width = 100
    expected_height = 100
    assert width == expected_width, f"Expected width {expected_width}. Actual width {width}"
    assert height == expected_height, f"Expected height {expected_height}. Actual height {height}"
