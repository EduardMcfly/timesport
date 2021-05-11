import uuid
import os


def uploadfile(file, path):
    key = uuid.uuid4().hex
    ext = os.path.splitext(file.filename)[1]
    newName = key+ext
    file.save(path + newName)
    return newName

def uploadfiles(files, path):
    paths = []
    for file in files:
        nameFile=uploadfile(file,path)
        paths.append(nameFile)
    return paths
