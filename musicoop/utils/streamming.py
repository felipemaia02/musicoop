"""
    Modulo
"""
from functools import partial

def iterfile(file: str, start: int, end: int) -> None:
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
            file_iterator = iter(reader, bytes())
            for byte in file_iterator:
                yield byte

    finally:
        file_like.close()
