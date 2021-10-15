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
    with open("musicoop/static/" + file, mode="rb") as file_like:
        yield from file_like
