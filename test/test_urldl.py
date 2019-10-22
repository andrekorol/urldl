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

import socket
import unittest
import hashlib
import os
import os.path as path
import shutil
from unittest import mock
from urllib.error import URLError

from urldl import urldl


def internet(host="8.8.8.8", port=53, timeout=3):
    """
    Tests for internet connection.

    :param host: IP addres of host to be tested.
    Defaults to 8.8.8.8 (google-public-dns-a.google.com).
    :param port: port to use for connection. Defaults to 53/tcp.
    :param timeout: time, in seconds, for socket timeout. Defaults to 3
    seconds.
    :returns: True if connection is successful, otherwise, False.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host,
                                                                   port))
        return True
    except socket.error as err:
        print(err)
        return False


def md5(fname):
    """
    Get the MD5 checksum of a given file.

    :param fname: name of the file to be checked.
    :returns: hex string representation for the MD5 hash digest.
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class UrldlTestCase(unittest.TestCase):
    def setUp(self):
        self.valid_url = "https://example.com"
        self.unknown_url_name = "httpxsl://example.com"
        self.unknown_url_type = "example.com"

    @unittest.skipIf(not internet(), "requires an internet connection")
    def test_download(self):
        makedirs_patcher = mock.patch("os.makedirs")
        mock_makedirs = makedirs_patcher.start()
        mock_makedirs.side_effect = PermissionError

        self.assertRaises(PermissionError, urldl.download, self.valid_url,
                          "mock_dir")
        makedirs_patcher.stop()

        self.assertRaises(URLError, urldl.download, self.unknown_url_name)

        self.assertRaises(ValueError, urldl.download,
                          self.unknown_url_type)

        valid_url_path = urldl.download(self.valid_url)
        self.assertIsInstance(valid_url_path, str)
        self.assertEqual("example.com", path.basename(valid_url_path))

        valid_url_dir_path = urldl.download(self.valid_url, "valid_dir")
        self.assertIsInstance(valid_url_dir_path, str)

        self.assertEqual(path.join("valid_dir", "example.com"),
                         path.join(valid_url_dir_path.split(path.sep)[-2],
                                   valid_url_dir_path.split(path.sep)[-1])
                         )

        code_icon_url = "https://fonts.gstatic.com/s/i/materialiconssharp/"\
                        "code/v1/black-18dp.zip"
        code_icon_path = urldl.download(code_icon_url)
        self.assertEqual("code-black-18dp.zip", path.basename(code_icon_path))
        self.assertEqual(md5(code_icon_path),
                         md5(path.join("test", "code-black-18dp.zip")))

        https_icon_url = "https://fonts.gstatic.com/s/i/materialiconssharp/"\
                         "https/v1/24px.svg?download=true"
        https_icon_path = urldl.download(https_icon_url)
        self.assertEqual("https-24px.svg", path.basename(https_icon_path))
        self.assertEqual(md5(https_icon_path),
                         md5(path.join("test", "https-24px.svg")))

    @unittest.skipIf(not internet(), "requires an internet connection")
    def test_download_list(self):
        alarm_icon_url = "https://fonts.gstatic.com/s/i/materialiconssharp/"\
                         "alarm/v1/24px.svg?download=true"
        backup_icon_url = "https://fonts.gstatic.com/s/i/materialiconssharp/"\
                          "backup/v1/24px.svg?download=true"
        copyright_icon_url = "https://fonts.gstatic.com/s/i/materialiconsshar"\
                             "p/copyright/v2/24px.svg?download=true"
        delete_icon_url = "https://fonts.gstatic.com/s/i/materialiconssharp/"\
                          "delete/v1/24px.svg?download=true"
        icon_url_list = [alarm_icon_url, backup_icon_url, copyright_icon_url,
                         delete_icon_url]

        urldl.download_list(icon_url_list, "icons")

        for icon in os.listdir("icons"):
            self.assertEqual(md5(path.join("icons", icon)),
                             md5(path.join("test", "icons", icon)))

    def tearDown(self):
        if os.path.exists("example.com"):
            os.remove("example.com")
        if path.exists("valid_dir"):
            shutil.rmtree("valid_dir")
        if path.exists("black-18dp.zip"):
            os.remove("black-18dp.zip")
        if path.exists("24px.svg"):
            os.remove("24px.svg")
        if path.exists(path.join("icons")):
            shutil.rmtree("icons")


if __name__ == '__main__':
    unittest.main()
