import os
from utils.common_utils import get_resources_dir, get_test_resources_dir, calculate_md5
from pathlib import Path


def test_get_test_resources_dir():
    test_resources_dir = get_test_resources_dir()
    tests_dir = Path(__file__).parent.parent
    expected_resources_dir = os.path.join(tests_dir, 'resources')
    assert test_resources_dir == expected_resources_dir, f'Got "{test_resources_dir}" \n' \
                                                         f'Expected {expected_resources_dir} '


def test_get_resources_dir():
    resources_dir = get_resources_dir()
    tests_dir = Path(__file__).parent.parent.parent
    expected_resources_dir = os.path.join(tests_dir, 'resources')
    assert resources_dir == expected_resources_dir, f'Got "{resources_dir}" \n' \
                                                    f'Expected {expected_resources_dir}'


def test_calculate_md5(scientists_image_path):
    md5 = calculate_md5(scientists_image_path)
    # Expected md5 for scientists.jpeg in tests/resources/test_images
    expected_md5 = '18059918cc26f67b78f6f2378b1a8e5b'
    assert md5 == expected_md5, f'Calculated MD5 for scientists.jpeg is {md5} \n' \
                                f'Expected {expected_md5}'
