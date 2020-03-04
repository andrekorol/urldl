import asyncio
from pathlib import Path, PurePath
from typing import List, Optional, Sequence, Union

import aiofiles
from httpx import AsyncClient, Client, HTTPError
from httpx.exceptions import HTTPError, InvalidURL, NetworkError

from .helpers import get_filename


def download(url: str, filename: Optional[str] = '',
             save_dir: Optional[str] = '',
             client: Optional[Client] = Client()) -> Union[str, Exception]:
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
    :returns: name of the file if the download was successful, if not,
    an exception to be either handled or raised.
    """
    try:
        with client.stream('GET', url) as resp:
            resp.raise_for_status()

            if not filename:
                filename = get_filename(resp.headers, url)

            if save_dir:
                Path(save_dir).mkdir(parents=True, exist_ok=True)

            with open(PurePath(save_dir, filename), 'wb') as f:
                for chunk in resp.iter_bytes():
                    if chunk:
                        f.write(chunk)

    except (InvalidURL, NetworkError, HTTPError, PermissionError) as e:
        return e

    return filename


def multi_download(urls: Sequence[str],
                   filenames: Optional[List[str]] = [],
                   save_dir: Optional[str] = '',
                   client: Optional[Client] = Client()) -> List[
                       Union[str, Exception]]:
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
    :returns: list of filenames (successfull downloads)
    and exceptions (failed downloads).
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
                       client: Optional[AsyncClient] = AsyncClient()) -> Union[
                           str, Exception]:
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
    :returns: name of the file if the download was successful, if not,
    an exception to be either handled or raised.
    """
    try:
        async with client.stream('GET', url) as resp:
            resp.raise_for_status()

            if not filename:
                filename = get_filename(resp.headers, url)

            if save_dir:
                Path(save_dir).mkdir(parents=True, exist_ok=True)

            async with aiofiles.open(PurePath(save_dir, filename), 'wb') as f:
                async for chunk in resp.aiter_bytes():
                    if chunk:
                        await f.write(chunk)

    except (InvalidURL, NetworkError, HTTPError, PermissionError) as e:
        return e

    return filename


async def aio_multi_download(urls: Sequence[str],
                             filenames: Optional[List[str]] = [],
                             save_dir: Optional[str] = '',
                             client: Optional[AsyncClient] = AsyncClient()) \
        -> List[Union[str, Exception]]:
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
    :returns: list of filenames (successfull downloads)
    and exceptions (failed downloads).
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
