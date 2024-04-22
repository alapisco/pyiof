from abc import ABC, abstractmethod


class IDictionaryManager(ABC):
    """
    Interface for managing dictionary operations.

    This interface defines methods for interacting with a dictionary,
    such as checking if a word exists within it.
    """

    @abstractmethod
    def is_word_in_dictionary(self, word: str) -> bool:
        """
        Checks if the specified word is in the dictionary.

        Parameters:
            word (str): The word to check in the dictionary.

        Returns:
            bool: True if the word is in the dictionary, False otherwise.
        """
        pass
