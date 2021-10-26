"""
    Modulo
"""
from functools import partial
CHUNK_SIZE = 1024*1024

def iterfile(file: str, start: int, end: int, size:int) -> None:
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
    try:
        with open("musicoop/static/" + file, mode="rb") as file_like:
            file_like.seek(start)
            reader = partial(file_like.read, end - start)
            if size < CHUNK_SIZE:
                reader = partial(file_like.read)
            file_iterator = iter(reader, bytes())
            for byte in file_iterator:
                yield byte

    finally:
        file_like.close()
