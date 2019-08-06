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
# along with Pycallisto. If not, see <https://www.gnu.org/licenses/>.

from multipledispatch import dispatch
from urllib.error import HTTPError, URLError
import urllib.request
from os.path import join, isdir, abspath
from os import makedirs
from shutil import move
from socket import timeout


def url_retrieve(url: str, save_dir: str = ""):
    """
    Uses urllib to retrieve a given URL.

    :param url: URL to be retrieved.
    :param: save_dir: directory to place what has been retrieved.
    :returns: absolute path of the retrieved file.
    """
    try:
        downloaded_file = urllib.request.urlretrieve(url, url.split('/')[-1])
        filename = downloaded_file[0]

        if save_dir != '':
            file_path = join(save_dir, filename)
            if not isdir(save_dir):
                makedirs(save_dir)
            move(filename, file_path)
            urllib.request.urlcleanup()
            return abspath(file_path)

        urllib.request.urlcleanup()
        return abspath(filename)

    except (HTTPError, URLError) as error:
        urllib.request.urlcleanup()
        print("Data from {} not retrieved because {}".format(url, error))
    except ValueError:
        urllib.request.urlcleanup()
        print("unknown url type: '{}'".format(url))
        print(url, "is not a valid url")
    except timeout:
        urllib.request.urlcleanup()
        print("socket timed out - URL {}".format(url))


@dispatch(str)
def download(url):
    """
    Downloads the file found at the given URL.

    :param url: URL string of a file to be downloaded.
    :returns: absolute path of file downloaded from the given URL.
    """
    assert isinstance(url, str), "{} is not a string".format(url)

    return url_retrieve(url)


@dispatch(str, str)
def download(url, save_dir):
    """
    Downloads the file found at the given URL and saves it in the
    given directory.

    :param url: URL string of a file to be downloaded.
    :param save_dir: directory to save downloaded file.
    :returns: absolute path of file downloaded from the given URL.
    """
    assert isinstance(url, str), "{} is not a string".format(url)
    assert isinstance(save_dir, str), "{} is not a string".format(save_dir)

    return url_retrieve(url, save_dir)


@dispatch(list)
def download(url_list):
    """
    Downloads the files from the given list of URLs.

    :param url_list: list of files' URLs to be downloaded.
    :returns: list of downloaded files' absolute paths.
    """
    assert isinstance(url_list, list), "{} is not a list".format(url_list)

    paths_list = []
    for url in url_list:
        paths_list.append(url_retrieve(url))

    return paths_list


@dispatch(list, str)
def download(url_list, save_dir):
    """
    Downloads the files from the given list of URLs and save them
    in the given directory.

    :param url_list: list of files' URLs to be downloaded.
    :param save_dir: directory to save downloaded files.
    :returns: list of downloaded files' absolute paths.
    """
    assert isinstance(url_list, list), "{} is not a list".format(url_list)
    assert isinstance(save_dir, str), "{} is not a string".format(save_dir)

    paths_list = []
    for url in url_list:
        paths_list.append(url_retrieve(url, save_dir))

    return paths_list
