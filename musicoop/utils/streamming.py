"""
    Modulo
"""
from functools import partial
from os import read
CHUNK_SIZE = 1024*1024


def iterfile(file: str, start: int, end: int, size: int, path_type: str) -> None:
    """
        Description
        -----------
        Parameters
        ----------
        Returns
        -------
        Raises
        ------
    """

    file_like = None
    with open("musicoop/static/" + path_type + "/" + file, mode="rb") as file_like:
        file_like.seek(start)
        reader = partial(file_like.read, end - start)
        if size < CHUNK_SIZE:
            reader = partial(file_like.read)
        file_iterator = iter(reader, bytes())
        for byte in file_iterator:
            if byte:
                yield byte
            else:
                break
