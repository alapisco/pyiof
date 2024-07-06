import pytest

from pyiof.face_recognition.face_recognizer import FaceRecognizer
from pyiof.models.face_recognition_result import FaceRecognitionResult
from pyiof.face_recognition.cascade_classifiers_loader import CascadeClassifiersLoader


@pytest.fixture
def cascade_classifiers_loader():
    return CascadeClassifiersLoader()


@pytest.fixture
def face_recognizer(cascade_classifiers_loader, image_processor):
    return FaceRecognizer(face_classifiers_loader=cascade_classifiers_loader, image_processor=image_processor)


@pytest.fixture
def image_with_faces(image_files_manager, scientists_image_path):
    return image_files_manager.load_image(scientists_image_path)


def test_get_face_recognition_result(face_recognizer, image_with_faces):
    scale_factor = 1.05
    min_neighbors = 25
    fr_result = face_recognizer.get_faces_regions(image_with_faces, scale_factor, min_neighbors)
    assert isinstance(fr_result, FaceRecognitionResult)
    # Expected faces recognized is 29
    assert len(fr_result.faces_regions) == 29
    assert fr_result.scale_factor == scale_factor
    assert fr_result.min_neighbors == min_neighbors
