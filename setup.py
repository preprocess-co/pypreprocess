from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.4.0'
DESCRIPTION = 'Preprocess SDK'

# Setting up
setup(
    name="pypreprocess",
    version=VERSION,
    author="Preprocess",
    author_email="<support@preprocess.co>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    license_files=('LICENSE',),
    install_requires=['requests'],
    keywords=['python', 'python3', 'preprocess', 'chunks', 'paragraphs', 'chunk', 'paragraph', 'llama', 'llamaondex', "langchain", "chunking", "llm", "rag"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License"
    ]
)