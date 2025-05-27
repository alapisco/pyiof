from PIL import Image
import pytesseract
from typing import Tuple
import cv2
import numpy as np

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
        # Target DPI for Tesseract
        TARGET_DPI = 300
        DEFAULT_DPI = 72

        # Convert PIL image to OpenCV array for scaling and initial processing
        image_cv_rgb = np.array(image.convert('RGB'))

        # Get current DPI
        original_dpi_x, original_dpi_y = image.info.get('dpi', (DEFAULT_DPI, DEFAULT_DPI))
        
        # Ensure original_dpi_x is not zero to prevent division by zero error
        if original_dpi_x <= 0:
            original_dpi_x = DEFAULT_DPI # Fallback to default if DPI is invalid

        # Calculate scaling factor
        scale_factor = TARGET_DPI / original_dpi_x
        
        scaled_image_cv = image_cv_rgb
        if scale_factor != 1.0 and scale_factor > 0: # Proceed if scaling is needed and factor is valid
            new_width = int(image_cv_rgb.shape[1] * scale_factor)
            new_height = int(image_cv_rgb.shape[0] * scale_factor)
            
            # Choose interpolation based on scaling up or down
            if scale_factor > 1.0: # Upscaling
                interpolation = cv2.INTER_CUBIC
            else: # Downscaling (scale_factor < 1.0)
                interpolation = cv2.INTER_AREA
            
            # Check if new dimensions are valid
            if new_width > 0 and new_height > 0:
                scaled_image_cv = cv2.resize(image_cv_rgb, (new_width, new_height), interpolation=interpolation)
            else:
                # Fallback to original image if new dimensions are invalid
                scaled_image_cv = image_cv_rgb
        else:
            # No scaling if factor is 1.0 or invalid
            scaled_image_cv = image_cv_rgb

        # 2. Apply Gaussian Blur to the scaled image
        blurred_image_cv = cv2.GaussianBlur(scaled_image_cv, (5, 5), 0)

        # 3. Convert to Grayscale
        grayscale_image_cv = cv2.cvtColor(blurred_image_cv, cv2.COLOR_RGB2GRAY)

        # 4. Apply Adaptive Thresholding
        binarized_img_cv = cv2.adaptiveThreshold(
            grayscale_image_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )

        # 5. Convert processed OpenCV array back to PIL Image
        binarized_pil_img = Image.fromarray(binarized_img_cv)

        # 6. OCR with Tesseract
        # Configuration for Tesseract: LSTM engine (--oem 1), Assume a single uniform block of text (--psm 6)
        tesseract_config = "--oem 1 --psm 6"
        ocr_text = pytesseract.image_to_string(binarized_pil_img, config=tesseract_config)
        
        # 7. Calculate accuracy
        ocr_accuracy = self._calculate_ocr_accuracy(ocr_text)

        # 8. Return result (best_threshold is now 0 as it's less relevant)
        return OCRResult(ocr_text, ocr_accuracy, 0)
