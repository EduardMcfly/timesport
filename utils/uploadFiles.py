from aws.s3 import s3, bucket
import uuid
import os

bucket = os.getenv("BUCKET")


def uploadfile(file, path):
    key = uuid.uuid4().hex
    ext = os.path.splitext(file.filename)[1]
    newName = key+ext
    s3.put_object(Bucket = bucket, Key=path + newName, Body=file)
    return newName


def uploadfiles(files, path):
    paths = []
    for file in files:
        nameFile = uploadfile(file, path)
        paths.append(nameFile)
    return paths
