import os

def get_path(file, level='.'):
    path = os.path.dirname(os.path.realpath(file))
    levels = level.count('.')
    if levels > 1:
        for l in range(levels-1):
            path = "/".join(path.split("/")[:-1])
    return path