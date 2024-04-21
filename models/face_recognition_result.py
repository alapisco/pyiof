from cv2.typing import Rect


class FaceRecognitionResult:
    def __init__(self, faces_regions: list[Rect], scale_factor: float, min_neighbors: int):
        self.faces_regions = faces_regions
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors

    def __repr__(self):
        return f'FaceRecognitionResult(faces_regions={self.faces_regions}, ' \
               f'scale_factor={self.scale_factor}, min_neighbors={self.min_neighbors})'
