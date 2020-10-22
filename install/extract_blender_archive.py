__author__ = "Satish Goda <satishgoda@live.com>"

__doc__ = """
Extracts a Blender distribution archive using zipfile or shutil module.
"""

def extract_archive_using_zipfile(archive, destination):
    import zipfile
    zf = zipfile.ZipFile(archive)
    zf.extractall(path=destination)


def extract_archive_using_shutil(archive, destination):
    import shutil
    shutil.unpack_archive(archive, 
                          extract_dir=destination)


def delete_archive(archive):
    import os
    os.remove(archived_blender)


def extract_archive(archive, destination, strategy):
    if strategy == 'zipfile':
        extract_archive_using_zipfile(archive, destination)
    elif strategy == 'shutil':
        extract_archive_using_shutil(archive, destination)


archived_blender = r"""C:\Users\satish.goda\Downloads\blender-2.91.0-b0f34eee30c4-windows64.zip"""
unarchived_blender_root = r"""C:\prod\tools\blender"""


extract_archive(archived_blender, unarchived_blender_root, 'shutil')

delete_archive(archived_blender)
