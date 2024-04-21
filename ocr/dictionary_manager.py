import os
from typing import Optional, Set
from utils.common_utils import get_resources_dir
from ocr.interfaces.idictionary_manager import IDictionaryManager


class DictionaryManagerError(Exception):
    """
    Exception raised by DictionaryManager in case of errors, especially when
    dealing with dictionary file operations.

    Attributes:
        dictionary_file (str): The file path of the dictionary file causing the exception.
        message (str): An explanation of the error.
    """
    def __init__(self, dictionary_file, message):
        self.dictionary_file = dictionary_file
        super().__init__(message)


class DictionaryManager(IDictionaryManager):
    """
    Manages dictionary operations for OCR processing, such as checking if a word exists in the dictionary.

    Attributes:
        _dictionary_file (str): The file path of the dictionary.
        _dictionary (Set[str]): The set of words loaded from the dictionary file.
    """
    def __init__(self, dictionary_file: Optional[str] = None):
        """
        Initializes the DictionaryManager with a specified dictionary file.

        Parameters:
            dictionary_file (Optional[str]): The file path of the dictionary. If None,
                                             a default dictionary file is used.
        """
        self._dictionary_file = dictionary_file or self._default_dictionary_file()
        self._dictionary = None

    @classmethod
    def _default_dictionary_file(cls) -> str:
        """
        Returns the default dictionary file path.

        Returns:
            str: The file path to the default dictionary file.
        """
        resources_dir = get_resources_dir()
        return os.path.join(resources_dir, 'words_alpha.txt')

    def _load_dictionary(self) -> Set[str]:
        """
        Loads the dictionary from the file and returns it as a set of words.

        Returns:
            Set[str]: A set of words read from the dictionary file.

        Raises:
            DictionaryManagerError: If there is an error reading the dictionary file.
        """
        try:
            with open(self._dictionary_file, "r") as f:
                data = f.read()
                return set(data.split("\n"))
        except Exception as e:
            raise DictionaryManagerError(dictionary_file=self._dictionary_file,
                                         message=f"Error reading dictionary file {self._dictionary_file} {e}")

    def is_word_in_dictionary(self, word: str) -> bool:
        """
        Checks if the specified word exists in the dictionary.

        Parameters:
            word (str): The word to be checked.

        Returns:
            bool: True if the word exists in the dictionary, False otherwise.
        """
        if self._dictionary is None:
            self._dictionary = self._load_dictionary()
        return word in self._dictionary
