from PIL import Image, UnidentifiedImageError
import os


class ImageFilesManager:
    def __init__(self):
        self.supported_save_formats = self._load_supported_save_formats()
        self.supported_load_formats = self._load_supported_load_formats()

    @staticmethod
    def load_image(image_source: str) -> Image:
        """
        Loads an image from the specified source path.

        Parameters:
            image_source (str): The file path of the image to be loaded.

        Returns:
            Image: An Image object loaded from the specified file path.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            UnidentifiedImageError: If the file is not a valid image or cannot be recognized.
            OSError: For other types of OS-related errors.
        """
        try:
            return Image.open(image_source)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File does not exist: {image_source}") from e
        except UnidentifiedImageError as e:
            raise UnidentifiedImageError(f"File is not a valid image: {image_source}") from e
        except OSError as e:
            raise OSError(f"An error occurred while trying to open the image: {image_source}") from e

    @staticmethod
    def save_image(image: Image, path: str):
        """
        Saves an image to the specified path.

        Parameters:
            image (Image): The PIL Image object to be saved.
            path (str): The file path where the image will be saved.

        Raises:
            ValueError: If the image path is invalid.
            FileNotFoundError: If the directory does not exist.
            OSError: For other OS errors that prevent saving.
        """
        try:
            image.save(path)
        except ValueError as e:
            error_msg = f"Invalid image path: {path}. Check that a supported image file extension " \
                        f"was used to save the image. Supported formats: {self.supported_save_formats}"
            raise ValueError(error_msg) from e
        except FileNotFoundError as e:
            error_msg = f"Directory '{os.path.dirname(path)}' does not exist."
            raise FileNotFoundError(error_msg) from e
        except OSError as e:
            error_msg = f"Failed to save image due to an OS error at '{path}': {e}"
            raise OSError(error_msg) from e

    @staticmethod
    def _load_supported_save_formats() -> set:
        """
        Private method to load supported image file formats for saving.

        Returns:
            set: A set of file extensions supported for saving images.
        """
        extensions = Image.registered_extensions()
        return {ext for ext, fmt in extensions.items() if fmt in Image.SAVE}

    @staticmethod
    def _load_supported_load_formats() -> set:
        """
        Private method to load supported image file formats for loading.

        Returns:
            set: A set of file extensions supported for loading images.
        """
        extensions = Image.registered_extensions()
        return {ext for ext, fmt in extensions.items() if fmt in Image.OPEN}
