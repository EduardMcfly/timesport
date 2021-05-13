import os
from .session import session

s3 = session.client('s3')

bucket = os.getenv("BUCKET")


def getFile(key):
    file = s3.get_object(Bucket=bucket, Key=key)
    return file
