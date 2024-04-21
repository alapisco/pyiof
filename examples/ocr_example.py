from ocr.ocr_processor import OCRProcessor
from ocr.dictionary_manager import DictionaryManager
from img_processing.image_processor import ImageProcessor
from img_processing.image_files_manager import ImageFilesManager

# Initialize the necessary components
dictionary_manager = DictionaryManager()
image_processor = ImageProcessor()
ocr_processor = OCRProcessor(dictionary_manager, image_processor)
image_files_manager = ImageFilesManager()

# Load image
image_source = 'tests/resources/test_images/canary_islands.png'
image = image_files_manager.load_image(image_source)

# Extract text
ocr_result = ocr_processor.extract_text(image)
print(ocr_result.text)
print(ocr_result.accuracy)
print(ocr_result.threshold)

