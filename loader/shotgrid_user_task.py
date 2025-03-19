try :
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCore import QThread, Signal, QMetaObject, Qt
except Exception :
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QThread, Signal, QMetaObject, Qt
    
from shotgun_api3 import Shotgun 

import os, sys, time
from loader.ui.loading_ui import LoadingDialog
from systempath import SystemPath
from shotgridapi import ShotgridAPI

root_path = SystemPath().get_root_path()
sg = ShotgridAPI().shotgrid_connector()

class TaskInfoThread(QThread):
    finished_signal = Signal(object)  

    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id 

    def run(self):
        task_info = TaskInfo()
        task_info.get_user_task(self.user_id)
        task_dict = task_info.get_task_dict()  
        self.finished_signal.emit(task_info)