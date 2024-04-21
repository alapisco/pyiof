import pytest
from utils.common_utils import get_test_resources_dir
import os
from img_processing.image_files_manager import UnidentifiedImageError
from PIL import Image


@pytest.fixture
def text_file_path():
    resources_dir = get_test_resources_dir()
    return os.path.join(resources_dir, 'not_an_image.txt')


@pytest.fixture
def save_image_path():
    test_resources_dir = get_test_resources_dir()
    return os.path.join(test_resources_dir, 'temp_img.png')


@pytest.fixture
def pil_image():
    return Image.new('RGB', (100, 100))


def test_load_valid_image(image_files_manager, scientists_image_path):
    image = image_files_manager.load_image(scientists_image_path)
    assert image is not None
    assert isinstance(image, Image.Image)


def test_not_existing_image(image_files_manager):
    with pytest.raises(FileNotFoundError):
        image_files_manager.load_image('not_existing_image.img')


def test_invalid_image(image_files_manager, text_file_path):
    with pytest.raises(UnidentifiedImageError):
        image_files_manager.load_image(text_file_path)


def test_save_image_success(image_files_manager, pil_image, save_image_path):
    # Ensure the file does not exist before the test
    if os.path.exists(save_image_path):
        os.remove(save_image_path)

    # Test saving the image
    image_files_manager.save_image(pil_image, save_image_path)

    # Check that the file now exists
    assert os.path.exists(save_image_path), "The image file was not saved correctly."

    # Clean up: remove the file after assertion to ensure it does not affect other tests
    os.remove(save_image_path)


def test_save_image_non_existent_directory(image_files_manager, pil_image):
    # Attempt to save to a non-existent directory to check how it handles directory creation errors
    non_existent_path = os.path.join(get_test_resources_dir(), 'non_existent_directory', 'temp_img.png')
    with pytest.raises(FileNotFoundError):
        image_files_manager.save_image(pil_image, non_existent_path)
    # Ensure no directory or file was created
    assert not os.path.exists(non_existent_path), "Non-existent directory was incorrectly handled."
