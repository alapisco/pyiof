import os.path

import pytest

from ocr.dictionary_manager import DictionaryManager, DictionaryManagerError
from utils.common_utils import get_test_resources_dir


def test_find_word_in_dictionary(dictionary_manager):
    word = 'computer'
    assert dictionary_manager.is_word_in_dictionary(word), f'Word {word} to found in dictionary'


def test_not_found_word_in_dictionary(dictionary_manager):
    word = 'computadora'
    assert not dictionary_manager.is_word_in_dictionary(word), f'Word {word} found in dictionary'


def test_not_found_dictionary_exception():
    with pytest.raises(DictionaryManagerError) as e:
        non_existing_dictionary_file = 'invalid_dict.aaa'
        DictionaryManager(dictionary_file=non_existing_dictionary_file).is_word_in_dictionary("word")
    dme = e.value
    assert dme.dictionary_file == non_existing_dictionary_file, \
        f"Not found dictionary expected to be {non_existing_dictionary_file} \n In exception {e}"


def test_invalid_dictionary_exception():
    with pytest.raises(DictionaryManagerError) as e:
        test_resources_dir = get_test_resources_dir()
        scientist_image = os.path.join(test_resources_dir, 'test_images', 'scientists.jpeg')
        DictionaryManager(dictionary_file=scientist_image).is_word_in_dictionary("word")
    dme = e.value
    assert dme.dictionary_file == scientist_image, \
        f"Not found dictionary expected to be {scientist_image} \n In exception {e}"
