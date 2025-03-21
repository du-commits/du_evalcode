try : 
    from PySide2.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QApplication
except Exception :
    from PySide6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QApplication
import maya.cmds as cmds

from loader.event.event_handler import LoaderEvent

class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """
        로그인 화면 UI 초기화
        """
        layout = QVBoxLayout(self)

        # 네임 입력
        self.name_input = QLineEdit("")  
        self.name_input.setPlaceholderText("NAME")
        
        # 이메일 입력
        self.email_input = QLineEdit("")
        self.email_input.setPlaceholderText("EMAIL")

        # 엔터(RETURN) 키를 누르면 로그인 버튼 클릭과 동일하게 동작
        self.email_input.returnPressed.connect(lambda:LoaderEvent.on_login_clicked(self))
        self.name_input.returnPressed.connect(lambda:LoaderEvent.on_login_clicked(self))

        # 로그인 버튼
        self.login_btn = QPushButton("LOGIN")
        self.login_btn.clicked.connect(lambda:LoaderEvent.on_login_clicked(self))

        # 레이아웃 설정
        layout.addWidget(self.name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.login_btn)

        self.center_window()

    def center_window(self):
        """주어진 위젯을 화면 중앙으로 이동"""
        screen_geometry = QApplication.primaryScreen().geometry()  
        widget_geometry = self.frameGeometry()  
        center_point = screen_geometry.center() 
        widget_geometry.moveCenter(center_point)
        self.move(widget_geometry.topLeft())