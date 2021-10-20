"""
    Modulo
"""

from functools import partial

def iterfile(file, start, end):
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
            for chunk in file_iterator:
                if chunk:
                    yield chunk
                else:
                    break
    finally:
        file_like.close()
