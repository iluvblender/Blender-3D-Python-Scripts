import os
import time
import shutil
import pathlib


import bpy

WORKAREA_LOCAL = 'WORKAREABLENDER'


def datestamp_get():
    localtime = time.localtime()
    datestamp = f'0{localtime.tm_mon}{localtime.tm_mday}{localtime.tm_year}'
    return datestamp


class WorkareaLocal:
    def __init__(self):
        pass
    
    def init(self):
        try:
            self._root = pathlib.Path(os.environ[WORKAREA_LOCAL])
        except KeyError:
            raise ValueError(f'The environment variable {WORKAREA_LOCAL} is not defined')

    def folders_create(self):
        if not self.today.exists():
            self.today.mkdir()
        
        if not self.task_folder.exists():
            self.task_folder.mkdir()

    def task_file_create(self):
        bpy.ops.wm.save_mainfile(filepath=str(self.task_filepath), 
                                 compress=False)

    def task_data_localize(self):
        bpy.ops.file.unpack_all(method='USE_LOCAL')

        bpy.ops.wm.save_mainfile(filepath=str(self.task_filepath),
                                 compress=True)

    @property
    def root(self):
        return self._root

    @property
    def today(self):
        return self._root / datestamp_get()
    
    @property
    def task_folder(self):
        return self.today / self.task_name

    @property
    def task_name(self):
        bpy.context.view_layer.name = 'Sketchfab'

        NAME_VIEWLAYER = bpy.path.clean_name(bpy.context.view_layer.name)

        collection = None
        for col in bpy.data.collections:
            if bpy.context.selected_objects[0].name in col.objects:
                collection = col
                break

        NAME_ASSET =  bpy.path.clean_name(collection.name)

        return f"{NAME_VIEWLAYER}-{NAME_ASSET}"

    @property
    def task_filepath(self):
        return self.task_folder / f"{self.task_name}.v001.blend"     
