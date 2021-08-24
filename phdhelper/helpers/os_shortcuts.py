import os


def get_path(file, level="."):
    path = os.path.dirname(os.path.realpath(file))
    levels = level.count(".")
    if levels > 1:
        for l in range(levels - 1):
            path = "/".join(path.split("/")[:-1])
    return path


def new_path(path, extension=""):
    def f(filename):
        # return path + "/" + extension
        return f"{path}{'/' + extension if extension != '' else ''}/{filename}"

    return f
