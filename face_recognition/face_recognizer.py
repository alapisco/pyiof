from face_recognition.cascade_classifiers_loader import ICascadeClassifiersLoader
from models.face_recognition_result import FaceRecognitionResult
from PIL import Image
from img_processing.image_processor import IImageProcessor


class FaceRecognizer:
    """
    FaceRecognizer is a class for detecting faces in images using cascade classifiers.

    Attributes:
        face_classifiers_loader (ICascadeClassifiersLoader): An object responsible for loading face cascade classifiers.
        image_processor (IImageProcessor): An object to process images, such as converting to grayscale and cropping.
        _face_cascade_classifiers (list): A private list of loaded face cascade classifiers for face detection.
    """

    def __init__(self, face_classifiers_loader: ICascadeClassifiersLoader,
                 image_processor: IImageProcessor):
        """
        Initializes the FaceRecognizer with necessary components for face detection.

        Args:
            face_classifiers_loader (ICascadeClassifiersLoader): The loader for face cascade classifiers.
            image_processor (IImageProcessor): The image processor for image manipulations.
        """
        self.face_classifiers_loader = face_classifiers_loader
        self.image_processor = image_processor
        self._face_cascade_classifiers = None

    def get_faces_regions(self, image: Image,
                          scale_factor: float = 1.05, min_neighbors: int = 25) -> FaceRecognitionResult:
        """
        Detects faces in the image and returns their regions.

        Args:
            image (Image): The image to detect faces in.
            scale_factor (float): The scale factor to adjust the image size during detection.
            min_neighbors (int): The minimum number of neighbors each rectangle should have to retain it.

        Returns:
            FaceRecognitionResult: The result containing the regions of detected faces and detection parameters.
        """
        if not self._face_cascade_classifiers:
            self._face_cascade_classifiers = self.face_classifiers_loader.load_cascade_classifiers()

        gray_scaled_image = self.image_processor.grayscale_image(image)
        gray_scaled_image_np = self.image_processor.convert_pil_image_to_np_array(gray_scaled_image)

        # Find regions containing faces
        face_regions = []
        for face_cascade_classifier in self._face_cascade_classifiers:
            faces = face_cascade_classifier.detectMultiScale(
                gray_scaled_image_np,
                scaleFactor=scale_factor,
                minNeighbors=min_neighbors,
            )
            face_regions += list(faces)

        return FaceRecognitionResult(face_regions, scale_factor, min_neighbors)

    def get_faces_images(self, image, regions_with_faces):
        """
        Extracts the images of detected faces from the original image.

        Args:
            image: The original image.
            regions_with_faces: The regions where faces were detected.

        Returns:
            A list of images of the detected faces.
        """
        return self.image_processor.get_images_from_regions(regions_with_faces, image)

    def highlight_faces_on_image(self, image, regions_with_faces):
        """
        Draws rectangles around detected faces in the image.

        Args:
            image: The original image.
            regions_with_faces: The regions where faces were detected.

        Returns:
            The image with rectangles drawn around the detected faces.
        """
        return self.image_processor.draw_rectangles_on_image(image, regions_with_faces)
