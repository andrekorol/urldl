# urldl: The easiest way to download files from URLs using Python
# Copyright (C) 2019 Andre Rossi Korol

# This file is part of urldl.

# urldl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# urldl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with urldl. If not, see <https://www.gnu.org/licenses/>.

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="urldl",
    version="0.0.1",
    author="Andre Rossi Korol",
    author_email="anrobits@yahoo.com.br",
    description="The easiest way to download files from URLs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrekorol/urldl",
    install_requires=["multipledispatch"],
    keywords=["url", "download"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
