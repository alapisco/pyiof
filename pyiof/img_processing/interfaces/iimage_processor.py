from abc import ABC, abstractmethod
from PIL import Image
from cv2.typing import Rect


class IImageProcessor(ABC):
    """
    Interface for image processing operations.

    This interface defines the methods for common image processing tasks
    such as converting images to grayscale, binarizing images, converting images
    to numpy arrays, cropping images from specified regions, and drawing rectangles
    on images.
    """

    @abstractmethod
    def grayscale_image(self, image: Image) -> Image:
        """
        Converts the given image to grayscale.

        Parameters:
            image (Image): The image to be converted.

        Returns:
            Image: The grayscale version of the image.
        """
        pass

    @abstractmethod
    def binarize_image(self, image: Image, threshold: int) -> Image:
        """
        Converts the given image to a binary image using the specified threshold.

        Parameters:
           image (Image): The image to be converted.
           threshold (int): The threshold value for binarization.

        Returns:
           Image: The binarized image.
       """
        pass

    @abstractmethod
    def convert_pil_image_to_np_array(self, pil_image: Image):
        """
        Converts a PIL image to a numpy array.

        Parameters:
            pil_image (Image): The PIL Image object to convert.

        Returns:
            numpy.ndarray: The image as a numpy array.
        """
        pass

    @abstractmethod
    def get_images_from_regions(self, regions: list[Rect], image: Image) -> list[Image]:
        """
        Crops the given image into multiple images based on the specified regions.

        Parameters:
            regions (List[Rect]): A list of regions (as x, y, width, height tuples) to crop the image.
            image (Image): The image from which regions will be cropped.

        Returns:
            List[Image]: A list of cropped images.
        """
        pass

    @abstractmethod
    def draw_rectangles_on_image(self, image: Image, regions: list[Rect]) -> Image:
        """
        Draws rectangles on the given image as specified by the regions.

        Parameters:
            image (Image): The image on which to draw rectangles.
            regions (List[Rect]): A list of regions (as x, y, width, height tuples) where rectangles will be drawn.

        Returns:
            Image: The image with rectangles drawn on it.
        """
        pass

    @abstractmethod
    def get_image_dimensions(self, image: Image) -> tuple[int, int]:
        """
        Retrieves the dimensions of the given image.

        Parameters:
            image (Image): The image whose dimensions are to be retrieved.

        Returns:
            tuple[int, int]: A tuple containing the width and height of the image.

        """
        pass
