from abc import ABC, abstractmethod
import cv2


class ICascadeClassifiersLoader(ABC):

    @abstractmethod
    def load_cascade_classifiers(self) -> list[cv2.CascadeClassifier]:
        """
        Loads the cascade classifiers.

        Returns:
            List[cv2.CascadeClassifier]: A list of loaded cascade classifier objects.

        Raises:
            FileNotFoundError: If a specified classifier file does not exist.
        """
        pass
