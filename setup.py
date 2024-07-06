from setuptools import setup, find_packages

setup(
    name='pyiof',
    version='0.1.0',
    author='Eduardo Alapisco',
    author_email='alapisco@gmail.com',
    description='A versatile Python library for image processing, OCR, and face recognition.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/alapisco/pyiof',
    packages=find_packages(),
    package_data={
        'pyiof': ['resources/*.*', 'resources/haarcascades/*.*'],
    },
    include_package_data=True,
    install_requires=[
        'pillow==10..0',
        'pytesseract==0.3.10',
        'opencv-python==4.10.0.82',
        'numpy==1.26.4'
    ],
    extras_require={
        'dev': [
            'pytest==8.1.1',
            'setuptools 70.2.0'
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
