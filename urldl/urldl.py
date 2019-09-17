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

from urllib.error import HTTPError, URLError
import urllib.request
import os
import os.path as path
from socket import timeout
from typing import List


def url_retrieve(url: str, save_dir: str = "") -> str:
    """
    Uses urllib to retrieve a given URL.

    :param url: URL to be retrieved.
    :param save_dir: directory to place what has been retrieved.
    :returns: absolute path of the retrieved file.
    """
    try:
        filename = url.split("/")[-1]
        with urllib.request.urlopen(url) as fin:
            url_content = fin.read()
        if save_dir:
            filepath = path.join(save_dir, filename)
            if not path.isdir(save_dir):
                try:
                    os.makedirs(save_dir)
                except PermissionError as e:
                    urllib.request.urlcleanup()
                    error_msg = "The current user does not have permission " \
                                "to create the '{}' directory".format(save_dir)
                    raise PermissionError(error_msg).\
                        with_traceback(e.__traceback__)
        else:
            filepath = filename
        with open(filepath, 'wb') as fout:
            fout.write(url_content)

        urllib.request.urlcleanup()
        return path.abspath(filepath)

    except (URLError, HTTPError) as e:
        urllib.request.urlcleanup()
        error_msg = "Data from {} not retrieved because {}".format(url, e)
        if isinstance(e, URLError):
            raise URLError(error_msg).with_traceback(e.__traceback__)
        else:
            raise HTTPError(e.url, e.code, error_msg, e.hdrs, e.fp)

    except ValueError as e:
        urllib.request.urlcleanup()
        error_msg = "unknown url type: '{}'\n{} is not a valid url".format(url,
                                                                           url)
        raise ValueError(error_msg).with_traceback(e.__traceback__)


def download(url: str, save_dir: str = "") -> str:
    """
    Downloads the file found at the given URL.

    :param url: URL string of a file to be downloaded.
    :param save_dir: directory to save downloaded file.
    If omitted, the file is saved in the current working directory.
    :returns: absolute path of file downloaded from the given URL.
    """
    return url_retrieve(url, save_dir)


def download_list(url_list: List[str], save_dir: str = "") -> List[str]:
    """
    Downloads the files from the given list of URLs.

    :param url_list: list of files' URLs to be downloaded.
    :param save_dir: directory to save downloaded files.
    If omitted, the files are saved in the current working directory.
    :returns: list of downloaded files' absolute paths.
    """
    paths_list = []
    for url in url_list:
        paths_list.append(url_retrieve(url, save_dir))

    return paths_list
