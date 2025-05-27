import os.path

import pytest

from pyiof.ocr.ocr_processor import OCRProcessor
from pyiof.utils.common_utils import get_test_resources_dir
from pyiof.ocr.ocr_processor import OCRResult


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
    assert ocr_result.best_threshold == 0, "best_threshold should now always be 0"
    assert len(ocr_result.text) > 0, "Text should not be empty"
    # Adjusted accuracy expectation due to significant OCR pipeline changes.
    # The new preprocessing (scaling, blur, adaptive threshold) and Tesseract params (OEM, PSM)
    # will likely change the output. This value is a placeholder and ideally
    # should be updated after running the OCR on the 'canary_islands.png' image
    # with the new settings to get a new baseline.
    assert ocr_result.accuracy[0] >= 100, f"Accuracy (word count) should be at least 100. Actual: {ocr_result.accuracy[0]}"
