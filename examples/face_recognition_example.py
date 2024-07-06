from pyiof.face_recognition.face_recognizer import FaceRecognizer
from pyiof.face_recognition.cascade_classifiers_loader import CascadeClassifiersLoader
from pyiof.img_processing.image_processor import ImageProcessor
from pyiof.img_processing.image_files_manager import ImageFilesManager

# Initialize the necessary components
cascade_classifiers_loader = CascadeClassifiersLoader()
image_processor = ImageProcessor()
face_recognizer = FaceRecognizer(cascade_classifiers_loader, image_processor)
image_files_manager = ImageFilesManager()

# Load image
image_source = '../tests/resources/test_images/monthy-python.webp'
image = image_files_manager.load_image(image_source)

# Extract faces regions
face_recognition_result = face_recognizer.get_faces_regions(image)
regions = face_recognition_result.faces_regions
print(regions)

# Highlight faces
face_recognizer.highlight_faces_on_image(image, regions).show()
