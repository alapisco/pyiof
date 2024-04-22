from PIL import Image
import pytesseract
from typing import Tuple

from pyiof.img_processing.interfaces.iimage_processor import IImageProcessor
from pyiof.models.ocr_result import OCRResult
from pyiof.ocr.interfaces.idictionary_manager import IDictionaryManager


class OCRProcessorError(Exception):
    """
    Custom exception class for OCRProcessor errors.

    Attributes:
        message (str): Description of the error.
    """
    def __init__(self, message: str):
        """
        Initialize the exception with a message.

        Args:
            message (str): The message describing the error.
        """
        super().__init__(message)
        self.message = message


class OCRProcessor:
    """
    OCRProcessor is a class that manages the Optical Character Recognition (OCR) process.

    Attributes:
        dictionary_manager (IDictionaryManager): An instance of a dictionary manager to validate words.
        image_processor (IImageProcessor): An instance of an image processor to preprocess images for OCR.
    """

    def __init__(self, dictionary_manager: IDictionaryManager, image_processor: IImageProcessor):
        """
        Initializes the OCRProcessor with necessary components.

        Args:
            dictionary_manager (IDictionaryManager): The dictionary manager component.
            image_processor (IImageProcessor): The image processing component.
        """
        self.dictionary_manager = dictionary_manager
        self.image_processor = image_processor

    def _calculate_ocr_accuracy(self, text: str) -> Tuple[int, int]:
        """
        Calculates the accuracy of OCR by counting the number of recognized words present in the dictionary.

        Args:
            text (str): The text obtained from OCR to evaluate.

        Returns:
            Tuple[int, int]: A tuple where the first element is the number of words in the dictionary
                             and the second element is the total length of those words.
        """
        if not text or type(text) != str:
            return 0, 0

        words_in_dict = 0
        words_length = 0
        text = text.lower()
        words = text.split()

        for word in words:
            if self.dictionary_manager.is_word_in_dictionary(word):
                words_in_dict += 1
                words_length += len(word)

        return words_in_dict, words_length

    def extract_text(self, image: Image) -> OCRResult:
        """
        Extracts text from an image using OCR, optimizing for the best accuracy by adjusting the threshold.

        Args:
            image (Image): The image from which text needs to be extracted.

        Returns:
            OCRResult: An instance of OCRResult containing the extracted text, its accuracy, and the best threshold.
        """
        best_accuracy = (0, 0)
        best_threshold = 64
        text = ''

        grayscale_img = self.image_processor.grayscale_image(image)

        for threshold in range(32, 256, 32):
            binarized_img = self.image_processor.binarize_image(grayscale_img, threshold)
            ocr_text = pytesseract.image_to_string(binarized_img)
            ocr_accuracy = self._calculate_ocr_accuracy(ocr_text)

            if ocr_accuracy > best_accuracy:
                best_accuracy = ocr_accuracy
                best_threshold = threshold
                text = ocr_text

        return OCRResult(text, best_accuracy, best_threshold)
