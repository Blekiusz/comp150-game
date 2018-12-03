"""
Load and save files.

Driver: Ashley
"""
import pathlib
import os


def load_files_form_directory(directory, file_type):
    """
    Get a list of files in a directory. Do not include sub folders.

    Also un-set EditorStore.update_image_directory.
    :param directory:   the directory to search.
    :param file_type:   the extension so search for.
    :return:            list of files including directory.
    """
    file_list = []
    files = pathlib.Path(directory)

    for f in files.iterdir():

        if f.is_file() and os.path.splitext(f)[1] == file_type:
            file_list.append(str(f.absolute()))

    return file_list


def get_file_names_in_directory(directory, file_type):
    """
    Get a list of files in a directory. Do not include sub folders.

    Also un-set EditorStore.update_image_directory.
    :param directory:   the directory to search.
    :param file_type:   the extension so search for.
    :return:            list of files names only (excluding directory).
    """
    file_list = []
    files = pathlib.Path(directory)

    for f in files.iterdir():

        if f.is_file() and os.path.splitext(f)[1] == file_type:
            file_list.append(os.path.basename(f.absolute()))

    return file_list
