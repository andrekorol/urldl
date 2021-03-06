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

from urllib.error import URLError
import urllib.request
import urllib.parse
import cgi
import os
import os.path as path


def download(url, save_dir=""):
    """
    Downloads the file found at the given URL.

    :param url: URL string of a file to be downloaded.
    :param save_dir: directory to save downloaded file.
    If omitted, the file is saved in the current working directory.
    :returns: absolute path of file downloaded from the given URL.
    """
    try:
        with urllib.request.urlopen(url) as response:
            content_disposition = response.headers.get("Content-Disposition",
                                                       "")
            _, params = cgi.parse_header(content_disposition)
            if "filename" in params.keys():
                filename = params["filename"]
            else:
                response_filepath = urllib.parse.urlparse(response.url).path
                filename = path.basename(response_filepath)

            if filename == "":
                filename = url.split("/")[-1]

            url_content = response.read()

        if save_dir:
            filepath = path.join(save_dir, filename)
        else:
            filepath = filename

        try:
            with open(filepath, 'wb') as fout:
                fout.write(url_content)
        except FileNotFoundError:
            try:
                os.makedirs(save_dir)
                with open(filepath, 'wb') as fout:
                    fout.write(url_content)
            except PermissionError as e:
                urllib.request.urlcleanup()
                error_msg = "The current user does not have permission " \
                            "to create the '{}' directory".format(save_dir)
                raise PermissionError(error_msg).\
                    with_traceback(e.__traceback__)

        urllib.request.urlcleanup()

        return path.abspath(filepath)

    except URLError as e:
        urllib.request.urlcleanup()
        error_msg = "Data from {} not retrieved because {}".format(url, e)
        raise URLError(error_msg).with_traceback(e.__traceback__)

    except ValueError as e:
        urllib.request.urlcleanup()
        error_msg = "unknown url type: '{}'\n{} is not a valid url".format(url,
                                                                           url)
        raise ValueError(error_msg).with_traceback(e.__traceback__)


def download_list(url_list, save_dir=""):
    """
    Downloads the files from the given list of URLs.

    :param url_list: list of files' URLs to be downloaded.
    :param save_dir: directory to save downloaded files.
    If omitted, the files are saved in the current working directory.
    :returns: list of downloaded files' absolute paths.
    """
    paths_list = []
    for url in url_list:
        paths_list.append(download(url, save_dir))

    return paths_list
