from cgi import parse_header
from pathlib import PurePath
from urllib.parse import unquote, urlparse

from httpx import Headers


def get_filename(headers: Headers, url: str) -> str:
    """Get the filename parameter from the Content-Disposition response
    header, if present. If not, parse the URL for the filename. In both
    cases, the function returns an unquoted filename.

    :param headers: response headers for an HTTP GET request.
    :param url: URL to extract the filename from.
    :returns: the name of the file.
    """
    params = {}
    if 'Content-Disposition' in headers:
        content_disposition = headers.get('Content-Disposition')
        _, params = parse_header(content_disposition)
    if params and 'filename*' in params:
        filename_str = params['filename*']
        encoding, filename = filename_str.split("''")
        filename = unquote(filename, encoding)
    elif params and 'filename' in params:
        filename = unquote(params['filename'])
    else:
        parsed_url = urlparse(url)
        filename = unquote(PurePath(parsed_url.path).name)

    return filename
