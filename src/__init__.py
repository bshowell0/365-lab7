import os

# get files in the current file's directory
files = os.listdir(os.path.dirname(os.path.realpath(__file__)))
files = [file[:-3] for file in files if file.endswith(".py") and "_script" not in file and file != "__init__.py"]

__all__ = files
