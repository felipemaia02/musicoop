"""
    Modulo
"""
import os
from functools import partial
from dotenv import load_dotenv

load_dotenv()


def iterfile(file: str, start: int, end: int, path_type: str) -> None:
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
    with open(os.getenv('MUSIC_PATH') + path_type + "/" + file, mode="rb") as file_like:
        file_like.seek(start)
        reader = partial(file_like.read, end - start)
        file_iterator = iter(reader, bytes())
        for byte in file_iterator:
            if byte:
                yield byte
            else:
                file_like.close()
                break
