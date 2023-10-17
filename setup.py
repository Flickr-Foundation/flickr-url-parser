import os

import setuptools


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


SOURCE = local_file("src")

setuptools.setup(
    name="flickr-url-parser",
    version="0.0.1",
    author="Flickr Foundation",
    author_email="hello@flickr.org",
    packages=setuptools.find_packages(SOURCE),
    package_dir={"": SOURCE},
    url="https://github.com/Flickr-Foundation/flickr-url-parser",
    install_requires=[
        'flask',
        'httpx',
        'humanize',
        'hyperlink',
    ],
    python_requires=">=3.7",
)
