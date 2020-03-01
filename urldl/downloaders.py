import asyncio
import pathlib
from cgi import parse_header
from typing import List, Optional, Sequence
from urllib.parse import unquote, urlparse

import aiofiles
from httpx import AsyncClient, Client


def download(url: str, filename: Optional[str] = '',
             save_dir: Optional[str] = '',
             client: Optional[Client] = Client()) -> str:
    """Use an HTTP `client` to download the file found at `url`
    and save it to `save_dir` as `filename`.

    :param url: URL of a file to be downloaded.
    :param filename: name to use when saving the downloaded file.
    Defaults to the filename given in the response headers (if present),
    or to the filename parsed from the URL.
    :param save_dir: directory to save downloaded file.
    If omitted, the file is saved in the current working directory.
    :param client: HTTPX client to be used when making requests.
    Defaults to a basic client, but a client with any valid optional parameters
    can be passed.
    :returns: name of the downloaded file.
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

    :param urls: Sequence of URLs of files to be downloaded.
    :param filenames: List of names to use when saving the downloaded files.
    If the list is empty or exhausted, the names will default to the filenames
    given in the response headers (if present),
    or to the filenames parsed from the URLs.
    :param save_dir: directory to save downloaded files.
    If omitted, the files are saved in the current working directory.
    :param client: HTTPX client to be used when making requests.
    Defaults to a basic client, but a client with any valid optional parameters
    can be passed.
    :returns: list of names of the downloaded files.
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


async def aio_download(url: str, filename: Optional[str] = '',
                       save_dir: Optional[str] = '',
                       client: Optional[AsyncClient] = AsyncClient()) -> str:
    """Use an async HTTP `client` to download the file found at `url`
    and save it to `folder` as `filename`.

    :param url: URL of a file to be scheduled for download.
    :param filename: name to use when saving the downloaded file.
    Defaults to the filename given in the response headers (if present),
    or to the filename parsed from the url.
    :param save_dir: directory to save downloaded file.
    If omitted, the file is saved in the current working directory.
    :param client: HTTPX async client to be used when scheduling requests.
    Defaults to a basic async client, but a client with any valid optional
    parameters can be passed.
    :returns: name of the downloaded file
    """
    async with client.stream('GET', url) as resp:
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

        async with aiofiles.open(pathlib.PurePath(save_dir, filename),
                                 'wb') as f:
            async for chunk in resp.aiter_bytes():
                if chunk:
                    await f.write(chunk)

    return filename


async def aio_multi_download(urls: Sequence[str],
                             filenames: Optional[List[str]] = [],
                             save_dir: Optional[str] = '',
                             client: Optional[AsyncClient] = AsyncClient()) \
        -> List[str]:
    """Use an async HTTP `client` to download multiple files found at `urls`
    and save them to `save_dir` as `filenames`.

    :param urls: Sequence of URLs of files to be scheduled for download.
    :param filenames: List of names to use when saving the downloaded files.
    If the list is empty or exhausted, the names will default to the filenames
    given in the response headers (if present),
    or to the filenames parsed from the URLs.
    :param save_dir: directory to save downloaded files.
    If omitted, the files are saved in the current working directory.
    :param client: HTTPX async client to be used when scheduling requests.
    Defaults to a basic async client, but a client with any valid optional
    parameters can be passed.
    :returns: list of names of the downloaded files.
    """
    tasks = []
    for url in urls:
        if filenames:
            filename = filenames.pop(0)
        else:
            filename = ''

        tasks.append(asyncio.create_task(
            aio_download(url, filename, save_dir, client)))

    file_list = await asyncio.gather(*tasks)

    return file_list
