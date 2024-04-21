from typing import Tuple


class OCRResult:
    def __init__(self, text: str, accuracy: Tuple[int, int], threshold: int):
        self.text = text
        self.accuracy = accuracy
        self.threshold = threshold

    def __repr__(self):
        return f'OCRResult(text={self.text}, accuracy={self.accuracy}, threshold={self.threshold})'
