"""
    Modulo
"""

import os
import boto3
from dotenv import load_dotenv

load_dotenv()


def connection_aws():
    """
    """
    return boto3.client('s3',
                        aws_access_key_id=os.getenv("ACCESS_KEY"),
                        aws_secret_access_key=os.getenv("ACCESS_SECRET")
                        )
