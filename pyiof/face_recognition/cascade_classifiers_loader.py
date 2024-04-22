import cv2

from pyiof.face_recognition.interfaces.icascade_classifiers_loader import ICascadeClassifiersLoader
from pyiof.utils.common_utils import get_resources_dir
import os


class CascadeClassifiersLoader(ICascadeClassifiersLoader):
    """
    CascadeClassifiersLoader is responsible for loading Haar cascade classifier files for face detection.

    Attributes:
        _face_cascade_classifier_files (list[str]): A list of file paths for the Haar cascade classifier files.
    """
    def __init__(self, face_cascade_classifier_files: list[str] = None):
        """
        Initializes the CascadeClassifiersLoader with optional specific classifier files.

        Args:
            face_cascade_classifier_files (list[str], optional): A list of paths to Haar cascade classifier files.
                                                                 If not provided, defaults to common face detection classifiers.
        """
        self._face_cascade_classifier_files = face_cascade_classifier_files or \
                                              self._get_cascade_classifiers_files()

    @staticmethod
    def _get_cascade_classifiers_files() -> list[str]:
        """
        Retrieves the default Haar cascade classifier files for face detection from the resources directory.

        Returns:
            list[str]: A list containing the paths to the default Haar cascade classifier files.
        """
        haarcascades_dir = os.path.join(get_resources_dir(), 'haarcascades')
        return [
            os.path.join(haarcascades_dir, 'haarcascade_frontalface_default.xml'),
            os.path.join(haarcascades_dir, 'haarcascade_profileface.xml')
        ]

    def load_cascade_classifiers(self) -> list[cv2.CascadeClassifier]:
        """
        Loads the Haar cascade classifiers for face detection from the specified classifier files.

        Returns:
            list[cv2.CascadeClassifier]: A list of cv2.CascadeClassifier objects loaded from the classifier files.

        Raises:
            FileNotFoundError: If any of the classifier files do not exist.
        """
        face_cascade_classifiers = []
        for face_cascade_classifier_file in self._face_cascade_classifier_files:
            if not os.path.exists(face_cascade_classifier_file):
                raise FileNotFoundError(f"The classifier file {face_cascade_classifier_file} was not found.")
            face_cascade_classifiers.append(cv2.CascadeClassifier(face_cascade_classifier_file))
        return face_cascade_classifiers
