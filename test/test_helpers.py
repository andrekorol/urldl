import hashlib
import unittest
from collections import OrderedDict

import httpx

from urldl.helpers import get_filename

from .tools import internet


class HelpersTestCase(unittest.TestCase):
    def setUp(self):
        self.urls = [
            'https://www.dropbox.com/s/a0lj1ddd54ns8qy/All-Age-Faces%20Datas'
            'et.zip?dl=1',
            'https://oi859.photobucket.com/albums/ab152/bandido_90/f01z0z.png',
            'https://images.dog.ceo/breeds/husky/n02110185_13704.jpg'
        ]
        self.resp_headers = OrderedDict()
        for url in self.urls:
            self.resp_headers[url] = httpx.get(url).headers

    @unittest.skipIf(not internet(), 'requires an internet connection')
    def test_get_filename(self):
        correct_filenames = OrderedDict()
        correct_filenames = {
            'encoded_filename_parameter': 'All-Age-Faces Dataset.zip',
            'simple_filename_parameter': 'f01z0z.png',
            'filename_from_parsed_url': 'n02110185_13704.jpg'
        }

        obtained_filenames = [get_filename(headers, url)
                              for url, headers in self.resp_headers.items()]

        for fname in obtained_filenames:
            self.assertIsInstance(fname, str)

        for correct, obtained in zip(correct_filenames.values(),
                                     obtained_filenames):
            self.assertEqual(correct, obtained)


if __name__ == '__main__':
    unittest.main()
