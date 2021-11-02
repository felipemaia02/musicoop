"""
    Modulo
"""
import os
import s3fs
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

    if os.getenv("SERVER_TYPE") == "PROD":
        file_path = "s3://" + os.getenv("BUCKET_NAME") + "/" + path_type + file
        aws_file = s3fs.S3FileSystem(key=os.getenv(
            "ACCESS_KEY"), secret=os.getenv("ACCESS_SECRET"))
        file_to_open = aws_file.open(file_path, mode="rb")

    else:
        file_path = os.getenv('MUSIC_PATH') + path_type + file
        file_to_open = open(file_path, mode="rb")

    with file_to_open as file_like:
        file_like.seek(start)
        reader = partial(file_like.read, end - start)
        file_iterator = iter(reader, bytes())
        for byte in file_iterator:
            if byte:
                yield byte
            else:
                file_like.close()
                break
