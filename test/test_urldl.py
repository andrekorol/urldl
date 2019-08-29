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
    def test_url_retrieve(self):
        self.valid_url_path = urldl.url_retrieve(self.valid_url)
        self.assertIsInstance(self.valid_url_path, str)
        self.assertEqual("example.com", path.basename(self.valid_url_path))
        self.assertEqual(md5(self.valid_url_path),
                         md5(path.join("test", "example.com")))

    def tearDown(self):
        os.remove(self.valid_url_path)


if __name__ == '__main__':
    unittest.main()
