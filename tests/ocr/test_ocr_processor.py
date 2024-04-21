import os.path

import pytest

from ocr.ocr_processor import OCRProcessor
from utils.common_utils import get_test_resources_dir
from ocr.ocr_processor import OCRResult


@pytest.fixture
def ocr_processor(dictionary_manager, image_processor):
    return OCRProcessor(dictionary_manager=dictionary_manager, image_processor=image_processor)


@pytest.fixture
def image_with_text(image_files_manager):
    test_resources_dir = get_test_resources_dir()
    image_path = os.path.join(test_resources_dir, 'test_images', 'canary_islands.png')
    return image_files_manager.load_image(image_path)


def test_get_ocr_result(ocr_processor, image_with_text):
    ocr_result = ocr_processor.extract_text(image_with_text)
    assert isinstance(ocr_result, OCRResult)
    assert len(ocr_result.text) > 0, "Text should not be empty"
    assert ocr_result.accuracy[0] >= 154, f"Accuracy should be at least 191. Actual accuracy {ocr_result.accuracy[0]}"
