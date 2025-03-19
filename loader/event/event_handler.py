try : 
    from PySide2.QtWidgets import QApplication, QLabel, QMessageBox, QWidget, QHBoxLayout, QTableWidgetItem, QAbstractItemView
    from PySide2.QtGui import QPixmap, QPainter, QColor, Qt
except Exception :
    from PySide6.QtWidgets import QApplication, QLabel, QMessageBox, QWidget, QHBoxLayout, QTableWidgetItem, QAbstractItemView
    from PySide6.QtGui import QPixmap, QPainter, QColor, Qt
    
import maya.cmds as cmds
import maya.utils as mu
import os, sys
from loader.shotgrid_user_task import ClickedTask
from loader.event.custom_dialog import CustomDialog
from loader.shotgrid_user_task import UserInfo
from loader.ui.loader_ui import UI as loaderUIClass
from loader.core.add_new_task import *
from systempath import SystemPath
from shotgridapi import ShotgridAPI

from loader.ui.loading_ui import LoadingDialog
from loader.shotgrid_user_task import TaskInfoThread

def on_login_clicked(ui_instance):                        
    """
    로그인 버튼 실행
    """
    user = UserInfo()

    name = ui_instance.name_input.text()
    email = ui_instance.email_input.text()

    if name and email: #이름과 이메일에 값이 있을 때
        is_validate = user.is_validate(email, name)
        if not is_validate:
            popup = QMessageBox()
            popup.setIcon(QMessageBox.Warning)
            popup.setWindowTitle("Failure")
            popup.setText("아이디 또는 이메일이 일치하지 않습니다")
            popup.exec()

        else:  # 로그인 성공!
            ui_instance.close()

            # 로딩창 먼저 띄우기
            ui_instance.loading_window = LoadingDialog()
            ui_instance.loading_window.show()
            QApplication.processEvents()  # UI 즉시 업데이트

            ui_instance.task_thread = TaskInfoThread(user.id)
            ui_instance.task_thread.start()
            ui_instance.task_thread.finished_signal.connect(
                lambda task_info: LoaderEvent.show_loader_ui(user, name, ui_instance.loading_window, task_info)
            )

    else: # 이름과 이메일에 값이 없을 때
        popup = QMessageBox()
        popup.setIcon(QMessageBox.Warning)
        popup.setWindowTitle("Failure")
        popup.setText("이름과 이메일을 입력해주세요")
        popup.exec()
            
def show_loader_ui(user, name, loading_window, task_info):
    """
    로딩이 끝나면 로더 UI 실행
    """
    loader_window = loaderUIClass(task_info)
    loader_window.user = user
    loader_window.user_name = name
    loader_window.input_name = name
    loader_window.setFixedSize(1100, 800)
    loader_window.setCentralWidget(loader_window.setup_layout())
    loader_window.center_window()
    # 로딩창 닫기
    loading_window.close()
    # 로더 UI 실행
    loader_window.show()

def on_sort_changed(ui_instance):
    """
    콤보박스 선택 변경 시 정렬 수행
    """
    selected_option = ui_instance.sort_combo.currentText()

    if selected_option == "data : latest":
        ascending = True
    elif selected_option == "date : earlist":
        ascending = False
    else:
        return  # 정렬이 아닌 경우 종료

    sort_table_by_due_date(ui_instance, ui_instance.task_table, ascending)


def sort_table_by_due_date(ui_instance, table_widget, ascending=True):
    tuple_list = []
    print(12345,ui_instance.task_data_dict)
    for index, data in enumerate(ui_instance.task_data_dict):
        due_date = data["due_date"] 
        data_index_tuple = (due_date, index)
        tuple_list.append(data_index_tuple)

    tuple_list.sort(key=lambda x: x[0], reverse=not ascending)

    new_task_list = []
    for _, index  in tuple_list:
        new_task_list.append(ui_instance.task_data_dict[index])

    table_widget.setRowCount(0)

    ui_instance.task_table_item(new_task_list)


def search_task(ui_instance):
    """
    검색 기능
    """
    search_text = ui_instance.search_input.text().strip().lower()

    for row in range(ui_instance.task_table.rowCount()):
        item = ui_instance.task_table.cellWidget(row, 1)  # Task Info 컬럼의 내용을 가져옴
        if item:
            labels = item.findChildren(QLabel)  # QLabel들 가져오기
            match = False
            for label in labels:
                if search_text in label.text().lower():  # 검색어가 포함된 경우
                    match = True
                    break

            ui_instance.task_table.setRowHidden(row, not match)  # 일치하지 않으면 숨김