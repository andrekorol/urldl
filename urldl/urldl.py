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

from multipledispatch import dispatch
from urllib.error import HTTPError, URLError
import urllib.request
import os
import os.path as path
from socket import timeout


def raise_with_msg(exception_obj, msg, preserve_traceback=True):
    """
    Raises an exception with a custom message.

    :param exception_obj: exception object to be raised.
    :param msg: custom message to be attached to the exception.
    :param preserve_traceback: Boolean to indicate whether to
    raise the exception with the traceback from where the original
    error occurred or not.
    """
    if preserve_traceback:
        raise Exception(msg).with_traceback(exception_obj.__traceback__)
    else:
        raise Exception(msg) from exception_obj


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
                except PermissionError as error:
                    urllib.request.urlcleanup()
                    error_msg = "The current user does not have permission " \
                                "to create the '{}' directory".format(save_dir)
                    raise_with_msg(error, error_msg)
        else:
            filepath = filename
        with open(filepath, 'wb') as fout:
            fout.write(url_content)

        urllib.request.urlcleanup()
        return path.abspath(filepath)

    except (HTTPError, URLError) as error:
        urllib.request.urlcleanup()
        error_msg = "Data from {} not retrieved because {}".format(url, error)
        raise_with_msg(error, error_msg)
    except ValueError as error:
        urllib.request.urlcleanup()
        error_msg = "unknown url type: '{}'\n{} is not a valid url".format(url,
                                                                           url)
        raise_with_msg(error, error_msg)
    except timeout as error:
        urllib.request.urlcleanup()
        error_msg = "socket timed out - URL {}".format(url)
        raise_with_msg(error, error_msg)


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
