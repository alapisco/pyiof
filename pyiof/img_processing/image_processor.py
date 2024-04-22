from PIL import Image, ImageDraw
from pyiof.img_processing.interfaces.iimage_processor import IImageProcessor
import numpy as np

from cv2.typing import Rect


class ImageProcessor(IImageProcessor):
    """
    Provides image processing functionalities such as converting images to
    grayscale, binarizing images, converting images to numpy arrays, cropping
    images from specified regions, and drawing rectangles on images.

    Inherits from IImageProcessor interface.
    """

    def grayscale_image(self, image: Image) -> Image:
        """
        Converts the given image to grayscale.

        Parameters:
            image (Image): The image to be converted to grayscale.

        Returns:
            Image: The grayscale version of the image.
        """
        return image.convert("L")

    def binarize_image(self, image: Image, threshold: int) -> Image:
        """
        Converts the given image to a binary image based on the specified threshold.

        Parameters:
            image (Image): The image to be converted.
            threshold (int): The threshold value used for binarization.

        Returns:
            Image: The binarized image.
        """
        grayscale = self.grayscale_image(image) if image.mode != "L" else image
        result = grayscale.point(lambda x: 255 if x >= threshold else 0)
        return result

    def convert_pil_image_to_np_array(self, pil_image: Image):
        """
        Converts a PIL image to a numpy array.

        Parameters:
            pil_image (Image): The PIL Image object to be converted.

        Returns:
            ndarray: The image as a numpy array.
        """
        return np.array(pil_image)

    def get_images_from_regions(self, regions: list[Rect], image: Image) -> list[Image]:
        """
        Crops the image based on the specified regions and returns the cropped images.

        Parameters:
            regions (list[Rect]): A list of rectangles defining the regions to be cropped.
            image (Image): The image from which regions are to be cropped.

        Returns:
            list[Image]: A list of cropped images.
        """
        cropped_images = []

        for (x, y, width, height) in regions:
            left = x
            upper = y
            right = x + width
            lower = y + height

            cropped_image = image.crop((left, upper, right, lower))
            cropped_images.append(cropped_image)
        return cropped_images

    def draw_rectangles_on_image(self, image: Image, regions: list[Rect]) -> Image:
        """
        Draws rectangles on the image as specified by the regions.

        Parameters:
            image (Image): The image on which to draw rectangles.
            regions (list[Rect]): A list of rectangles defining the regions where rectangles are to be drawn.

        Returns:
            Image: The image with rectangles drawn on it.
        """
        draw = ImageDraw.Draw(image)
        for (x, y, width, height) in regions:
            right, lower = x + width, y + height
            draw.rectangle((x, y, right, lower), outline="red", width=2)
        return image

    def get_image_dimensions(self, image: Image):
        """
        Retrieves the dimensions of the given image.

        Parameters:
            image (Image): The image whose dimensions are to be retrieved.

        Returns:
            tuple[int, int]: A tuple containing the width and height of the image.
        """
        return image.size
