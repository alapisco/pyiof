import pytest
from utils.common_utils import get_test_resources_dir
from ocr.dictionary_manager import DictionaryManager
from img_processing.image_processor import ImageProcessor
from img_processing.image_files_manager import ImageFilesManager
import os


@pytest.fixture
def image_files_manager():
    return ImageFilesManager()


@pytest.fixture
def dictionary_manager():
    return DictionaryManager()


@pytest.fixture
def image_processor():
    return ImageProcessor()


@pytest.fixture
def scientists_image_path():
    resources_dir = get_test_resources_dir()
    return os.path.join(resources_dir, 'test_images', 'scientists.jpeg')

