
try :
    from PySide2.QtWidgets import QDialog, QVBoxLayout, QLabel
    from PySide2.QtCore import Qt, QTimer, QMetaObject
except Exception :
    from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QApplication
    from PySide6.QtCore import Qt, QTimer
    
from loader.core.video_player import VideoPlayer
from systempath import SystemPath

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading...")
        self.setModal(True)
        self.setFixedSize(200, 200)
        self.setStyleSheet("background-color:black; color:white;")

        loading_mov = f"{root_path}/elements/loading.mp4"

        layout = QVBoxLayout()

        self.loading_text = QLabel("데이터 불러오는 중...")
        self.loading_text.setStyleSheet("font-size: 10px;")
        self.video_widget = VideoPlayer(loading_mov)
        self.video_widget.setScaledContents(True)

        layout.addWidget(self.video_widget, alignment=Qt.AlignCenter)
        layout.addWidget(self.loading_text, alignment=Qt.AlignCenter)

        self.setLayout(layout)
