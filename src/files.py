import glob

excludedFiles = [
    "lootboxnano.lua"
]


def isFileAllowed(filename):
    """
    checks for files that can not be used

    Args:
        filename (str): the path to the file

    Returns:
        bool: a evaluation of the file
    """
    for fileExclude in excludedFiles:
        if fileExclude in filename:
            return False
    return True


def getFiles():
    """
    find all unit files in the repo

    Returns:
        list[str]: a list of paths to unit files
    """
    files = glob.glob('./repo/units/**/*.lua', recursive=True)

    filteredFiles = list(filter(isFileAllowed, files))

    return filteredFiles
