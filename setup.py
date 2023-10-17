import os

import setuptools


def local_file(name):
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


LONG_DESCRIPTION = (
    open("README.md")
    .read()
    .split("## Development\n")[0]
    .replace("# flickr-url-parser\n", "")
    .strip()
)

SOURCE = local_file("src")

setuptools.setup(
    name="flickr-url-parser",
    version="0.9.0",
    author="Flickr Foundation",
    author_email="hello@flickr.org",
    readme="README.md",
    description="Enter a Flickr URL, and find out what sort of URL it is (single photo, album, gallery, etc.)",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(SOURCE),
    package_dir={"": SOURCE},
    url="https://github.com/Flickr-Foundation/flickr-url-parser",
    install_requires=[
        "flask",
        "httpx",
        "humanize",
        "hyperlink",
    ],
    python_requires=">=3.7",
    project_urls={
        "Homepage": "https://github.com/Flickr-Foundation/flickr-url-parser",
        "Changes": "https://github.com/Flickr-Foundation/flickr-url-parser/blob/main/CHANGELOG.md",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
