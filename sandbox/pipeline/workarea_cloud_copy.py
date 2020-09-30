import os
import pathlib
import shutil
import filecmp

import bpy

# Environment variables related to Workarea
WORKAREA_LOCAL = 'WORKAREABLENDER'
WORKAREA_CLOUD = 'ONEDRIVECONSUMER'


class WorkareaCloud:
    def __init__(self):
        pass
    
    def init(self):
        try:
            self._root = pathlib.Path(os.environ[WORKAREA_CLOUD])
        except KeyError:
            raise ValueError(f'The environment variable {WORKAREA_LOCAL} is not defined')

        if not bpy.data.filepath:
            raise ValueError("File is not saved")

        try:
            bpy.ops.wm.save_mainfile(compress=True)
        except Exception as e:
            raise ValueError("Error while saving file: " + str(e))

        REL_FILEPATH = os.path.relpath(self.task_filepath,
                                       os.environ[WORKAREA_LOCAL]
                                       )
        DIRS_TO_CREATE = REL_FILEPATH.split('\\')[:-1]
        self._task_folder = (self.root / 'blog').joinpath(*DIRS_TO_CREATE)
        self._task_file = REL_FILEPATH.split('\\')[-1]

    def folders_create(self):
        if not self.task_folder.exists():
            self.task_folder.mkdir(parents=True)

    def task_file_create(self):
        src = self.task_filepath
        dst = self.task_folder / self.task_file
        try:
            if filecmp.cmp(src, dst, shallow=False):
                print(f"Files are same: {src} == {dst}")
                return
        except FileNotFoundError as fnfe:
            print(f"Error while comparing files: {fnfe}")
        shutil.copy2(src, dst)
        shutil.copymode(src, dst)
        shutil.copystat(src, dst)

    def task_data_localize(self, folder_name):
        folder = self.task_filepath.parent / folder_name
        folder_dst = self.task_folder / folder_name

        files = None

        try:
            files = tuple(folder.iterdir())

            if files:
                folder_dst.mkdir()
        except FileNotFoundError as fnfe:
            print(fnfe)
        except FileExistsError as fee:
            print(fee)

        if files:
            for file in files:
                file_dst = folder_dst / file.name
                try:
                    if filecmp.cmp(file, file_dst, shallow=False):
                        continue
                    else:
                        print(f"\t\t\t{file.name} is different")
                except FileNotFoundError as fnfe:
                    print(f"Error while comparing files: {fnfe}")
                
                try:
                    print(f"\t\t\t Copying file: {file_dst}")
                    shutil.copyfile(file, 
                                    file_dst)
                    shutil.copymode(file, file_dst)
                    shutil.copystat(file, file_dst)
                except Exception as e:
                    print(e)

    @property
    def root(self):
        return self._root

    @property
    def task_folder(self):
        return self._task_folder

    @property
    def task_file(self):
        return self._task_file

    @property
    def task_filepath(self):
        return pathlib.Path(bpy.data.filepath)
