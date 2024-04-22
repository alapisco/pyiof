import pytest
from unittest.mock import patch, MagicMock
from pyiof.face_recognition.cascade_classifiers_loader import CascadeClassifiersLoader


def test_load_default_cascade_classifiers_success():
    # Mock the os.path.exists to always return True
    with patch('os.path.exists', return_value=True):
        # Mock cv2.CascadeClassifier to prevent actual file loading
        with patch('cv2.CascadeClassifier', return_value=MagicMock()):
            loader = CascadeClassifiersLoader()
            classifiers = loader.load_cascade_classifiers()

            # Assert we got a list of classifiers
            assert isinstance(classifiers, list)
            assert len(classifiers) == 2


def test_load_cascade_classifiers_file_not_found():
    # Test with a non-existing file
    with patch('os.path.exists', return_value=False):
        loader = CascadeClassifiersLoader(['nonexistent_file.xml'])

        with pytest.raises(FileNotFoundError):
            loader.load_cascade_classifiers()
