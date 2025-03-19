try : 
    from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QToolButton
    from PySide2.QtWidgets import QVBoxLayout, QLabel, QLineEdit
    from PySide2.QtWidgets import QHBoxLayout, QPushButton, QFileDialog
    from PySide2.QtWidgets import QMessageBox, QPlainTextEdit
    from PySide2.QtWidgets import QComboBox
    from PySide2 import QtCore
except Exception :
    from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QToolButton
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QLineEdit
    from PySide6.QtWidgets import QHBoxLayout, QPushButton, QFileDialog
    from PySide6.QtWidgets import QMessageBox, QPlainTextEdit
    from PySide6.QtWidgets import QComboBox
    from PySide6 import QtCore

import sys, os, re
import maya.cmds as cmds

from publisher.core.play_blast import PlayblastManager
from publisher.event.event_handler import *
from loader.core.video_player import VideoPlayer
from publisher.core.publish import PublishManager

def version_name(self):
    file_name = self.filename_input.text()
    version_match = re.search(r'v\d+', file_name)
    
    if version_match:
        return version_match.group()  # "v005" 반환
    else:
        return None

def cleanup_video_player(self):
    """ 비디오 플레이어 종료 및 리소스 정리 """
    if hasattr(self, "preview_frame") and self.preview_frame:

        if hasattr(self.preview_frame, "video_thread") and self.preview_frame.video_thread:
            self.preview_frame.video_thread.stop()
            self.preview_frame.video_thread.quit()
            self.preview_frame.video_thread.wait()

        if hasattr(self.preview_frame, "video_thread") and self.preview_frame.video_thread.cap:
            self.preview_frame.video_thread.cap.release()

        self.preview_frame.setParent(None)
        self.preview_frame.deleteLater()
        self.preview_frame = None

def convert_to_save_path(file_path):
    """새로 저장할 경로"""
    directory_path = os.path.dirname(file_path)
    path_parts = directory_path.strip("/").split("/")

    if "work" in path_parts:
        work_index = path_parts.index("work")
        path_parts[work_index] = "pub"

    new_path = "/" + "/".join(path_parts)
    return new_path

def close_event(self, event=None):
    """ UI 창이 닫힐 때 비디오 플레이어 종료 및 정리 """
    # 비디오 플레이어 종료 함수 호출
    self.cleanup_video_player()
    # UI 닫기 실행
    if event:
        event.accept()  # X 버튼을 눌렀을 때 호출되는 경우
    else:
        self.close()  # "Cancel" 버튼을 눌렀을 때 호출되는 경우

def publish_final_output(self):
    """ 
    1. 파일 저장 (save_file_as)
    2. 슬레이트 mov 2개 저장 (save_playblast_files)
    3. 비디오 플레이어 종료
    4. 원본 Playblast 삭제
    5. UI 닫기
    """
    version = self.version_name()

    # 슬레이트 mov 3개 저장
    PlayblastManager(self.file_path, self.file_name).save_playblast_files(version)
    # 비디오 플레이어 종료 (중복 코드 제거하고 함수 호출)
    self.cleanup_video_player()
    # # 원본 Playblast .mov 삭제
    playblast_path = f"{self.filepath_input.text()}/playblast.mov"
    if os.path.exists(playblast_path):
        try:
            os.remove(playblast_path)
            print(f"원본 Playblast 파일 삭제 완료: {playblast_path}")
        except PermissionError:
            print("파일이 아직 사용 중이라 삭제할 수 없습니다.")
            return
    else:
        print("원본 Playblast 파일이 이미 삭제되었거나 존재하지 않습니다.")
    self.close_event()
    print("퍼블리셔 UI 종료")