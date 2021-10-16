"""
    Modulo
"""

def iterfile(file):
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
            yield from file_like
    finally:
        file_like.close()
