import hashlib
import socket


def internet(host: str = "8.8.8.8", port: int = 53, timeout: int = 3) -> bool:
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
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as err:
        print(err)
        return False


def md5(fname: str) -> str:
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
