import pathlib
from cgi import parse_header
from typing import List, Optional, Sequence
from urllib.parse import unquote, urlparse

import httpx


def download(url: str, filename: Optional[str] = '',
             save_dir: Optional[str] = '',
             client: Optional[httpx.Client] = httpx.Client()) -> str:
    """Download the file found at the given URL."""
    with client.stream('GET', url) as resp:
        if not filename:
            params = {}
            if 'Content-Disposition' in resp.headers:
                content_disposition = resp.headers.get('Content-Disposition')
                _, params = parse_header(content_disposition)
            if params and 'filename*' in params:
                filename_str = params['filename*']
                encoding, filename = filename_str.split("''")
                filename = unquote(filename, encoding)
            elif params and 'filename' in params:
                filename = unquote(params['filename'])
            else:
                parsed_url = urlparse(url)
                filename = unquote(pathlib.PurePath(parsed_url.path).name)

        if save_dir:
            pathlib.Path(save_dir).mkdir(exist_ok=True)

        with open(pathlib.PurePath(save_dir, filename), 'wb') as f:
            for chunk in resp.iter_bytes():
                f.write(chunk)

    return filename


def download_files(urls: Sequence[str],
                   filenames: Optional[List[str]] = [],
                   save_dir: Optional[str] = '',
                   client: Optional[httpx.Client] = httpx.Client()) \
        -> List[str]:
    """Download the files found at the given URLs."""
    file_list = []
    for url in urls:
        if filenames:
            filename = filenames.pop(0)
        else:
            filename = ''

        downloaded_file = download(url, filename, save_dir, client)
        file_list.append(downloaded_file)

    return file_list
