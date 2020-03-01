import pathlib
from cgi import parse_header
from typing import List, Optional, Sequence
from urllib.parse import unquote, urlparse

from httpx import AsyncClient, Client


def download(url: str, filename: Optional[str] = '',
             save_dir: Optional[str] = '',
             client: Optional[Client] = Client()) -> str:
    """Use an HTTP `client` to download the file found at `url`
    and save it to `save_dir` as `filename`.
    """
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
                if chunk:
                    f.write(chunk)

    return filename


def multi_download(urls: Sequence[str],
                   filenames: Optional[List[str]] = [],
                   save_dir: Optional[str] = '',
                   client: Optional[Client] = Client()) -> List[str]:
    """Use an HTTP `client` to download multiple files found at `urls`
    and save them to `save_dir` as `filenames`.
    """
    file_list = []
    for url in urls:
        if filenames:
            filename = filenames.pop(0)
        else:
            filename = ''

        downloaded_file = download(url, filename, save_dir, client)
        file_list.append(downloaded_file)

    return file_list
