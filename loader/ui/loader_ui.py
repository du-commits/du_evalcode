try : 
    from PySide2.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox
    from PySide2.QtWidgets import QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QTableWidgetItem, QSizePolicy
    from PySide2.QtGui import QPixmap, QPainter, QColor
    from PySide2.QtWidgets import QHeaderView, QAbstractItemView
    from PySide2.QtCore import Qt
    import maya.cmds as cmds
    
except Exception :
    from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QComboBox
    from PySide6.QtWidgets import QVBoxLayout, QLabel, QMainWindow, QHBoxLayout, QTableWidgetItem, QSizePolicy
    from PySide6.QtGui import QPixmap, QPainter, QColor
    from PySide6.QtWidgets import QHeaderView, QAbstractItemView
    from PySide6.QtCore import Qt
    
from loader.shotgrid_user_task import UserInfo, TaskInfo
from loader.core.video_player import VideoPlayer
from loader.core.data_managers import previous_data, task_data
from systempath import SystemPath

class UI(QMainWindow):
    def __init__(self, task_info):
        super().__init__()        

        self.setWindowTitle("EVAL LOADER")
        self.center_window()

        self.work_table = QTableWidget(0,3)
        self.work_table.setSelectionBehavior(QTableWidget.SelectRows) 
        self.work_table.setEditTriggers(QTableWidget.NoEditTriggers)  
        self.work_table.horizontalHeader().setVisible(False)  
        self.work_table.verticalHeader().setVisible(False) 
        self.pub_table = QTableWidget(0,3)
        self.pub_table.setSelectionBehavior(QTableWidget.SelectRows)  
        self.pub_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.pub_table.horizontalHeader().setVisible(False) 
        self.pub_table.verticalHeader().setVisible(False)  

    def setup_layout(self):
        """
        레이아웃 세팅
        """
        # 왼쪽 Task Table UI 생성
        self.task_container = self.make_task_table()
        self.task_container.setMinimumWidth(570)
        self.task_container.setMaximumWidth(570)  # TASK 최소 너비 지정, 안하면 너무 작아짐.
        self.task_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # 가로/세로 확장 허용
        #self.task_container.setEditTriggers(QAbstractItemView.NoEditTriggers)  
        
        file_table_widget = QWidget()
        file_table_layout = QVBoxLayout(file_table_widget)

        # WORK 버전 UI 생성
        work_label = QLabel("WORK")
        work_label.setStyleSheet("font-weight : bold;padding-left: 10px;")
        work_label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

        # PUB 버전 UI 생성
        pub_label = QLabel("PUB")
        pub_label.setStyleSheet("font-weight : bold;padding-left: 10px;")
        pub_label.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

        file_table_layout = QVBoxLayout()
        file_table_layout.addWidget(work_label)
        file_table_layout.addWidget(self.work_table)
        file_table_layout.addWidget(pub_label)
        file_table_layout.addWidget(self.pub_table)

        # PREVIOUS BLAST UI 생성
        previous_container = previous_data(self)

        widget = QWidget()
        layout = QHBoxLayout(widget)
        # 유저 레이아웃
        user_layout = QHBoxLayout()
        none_label = QLabel()
        user_name = QLabel(self.input_name)
        user_name.setStyleSheet("font-weight: bold;")
        user_name.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        user_name.setAlignment(Qt.AlignRight)
        user_layout.addWidget(none_label)
        user_layout.addWidget(user_name)

        # work, pub, pb, 유저이름 레이아웃 세팅
        self.right_layout = QVBoxLayout()
        self.right_layout.addLayout(user_layout)
        self.right_layout.addWidget(previous_container, 2)
        self.right_layout.addWidget(work_label)
        self.right_layout.addWidget(self.work_table, 2)
        self.right_layout.addWidget(pub_label)
        self.right_layout.addWidget(self.pub_table, 1)

        # 메인 레이아웃 세팅
        layout.addWidget(self.task_container, 3)
        layout.addLayout(self.right_layout, 2)

        return widget

    def previous_work_item(self, user, pb, status_color, status_text, cmt_txt):
        """
        외부에서 데이터를 받아서 Previous_work에 추가하는 함수
        """
        #동영상파일 재생
        self.video_widget = VideoPlayer(pb)
        self.video_widget.setStyleSheet("border: 2px solid #555; border-radius: 5px;")

        #정보 라벨
        previous_work = QLabel("PREVIOUS WORK")
        previous_work.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        previous_work.setStyleSheet("font-weight: bold;")

        # 원 색칠
        status_pixmap = QPixmap(10, 10) 
        status_pixmap.fill(QColor("transparent"))  
        painter = QPainter(status_pixmap)
        painter.setBrush(QColor(status_color)
        painter.setPen(QColor(status_color)) 
        painter.drawEllipse(0, 0, 10, 10)
        painter.end()
        self.state_image.setPixmap(status_pixmap)

        status_wdidget = QWidget()
        status_layout = QHBoxLayout(status_wdidget)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(2)

        # 상태 아이콘 QLabel
        status_icon_label = QLabel()

        status_icon_label.setPixmap(status_pixmap)

        status_text_label = QLabel(status_text)

        # 레이아웃에 아이콘과 텍스트 추가
        status_layout.addWidget(status_icon_label)
        status_layout.addWidget(status_text_label)

        self.info_table.setCellWidget(3, 2, status_wdidget)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.info_table)
        info_layout.addWidget(comment_label)
        info_layout.addWidget(self.comment_text)

        # PB 레이아웃
        pre_layout = QHBoxLayout()
        pre_layout.setSpacing(20)
        pre_layout.addWidget(self.video_widget)
        pre_layout.addLayout(info_layout)

        widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(previous_work)
        layout.addLayout(pre_layout)
        widget.setLayout(layout)

        return widget

    def make_task_table(self):
        """
        Task UI (테이블 목록) 생성
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 테스크 검색, 정렬 UI 생성
        task_label = QLabel("TASK")
        task_label.setStyleSheet("font-weight: bold;")
        self.search_input = QLineEdit(
        self.search_but = QPushButton("SEARCH")
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("data : latest")
        self.sort_combo.addItem("date : earlist")

        # 테스크 검색, 정렬 레이아웃 정렬
        h_layout = QHBoxLayout()
        h_layout.addWidget(task_label)
        h_layout.addWidget(self.search_input)
        h_layout.addWidget(self.search_but)
        h_layout.addWidget(self.sort_combo)

        # 테이블 위젯 생성 (초기 행 개수: 0, 2개 컬럼)
        self.task_table = QTableWidget(0, 3)
        self.task_table.setSelectionBehavior(QTableWidget.SelectRows) 
        self.task_table.setEditTriggers(QTableWidget.NoEditTriggers) 
        self.task_table.setHorizontalHeaderLabels(["Thumbnail", "Task Info", "Task ID"])
        self.task_table.setColumnHidden(2, True) 

        from loader.event.event_handler import LoaderEvent
        # 테이블 이벤트 처리
        self.task_table.cellClicked.connect(lambda row,col:LoaderEvent.on_cell_clicked(self,row,col))
        self.search_but.clicked.connect(lambda:LoaderEvent.search_task(self))
        self.search_input.returnPressed.connect(lambda:LoaderEvent.search_task(self))
        self.search_input.textChanged.connect(lambda:LoaderEvent.search_task(self))
        self.sort_combo.currentIndexChanged.connect(lambda:LoaderEvent.on_sort_changed(self))

        # 테이블 크기설정
        self.task_table.setColumnWidth(0, 180)  
        self.task_table.setColumnWidth(1, 300)  
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)  
        self.task_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)  
        self.task_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  
        self.task_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.task_table.resizeRowsToContents()
        self.task_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.task_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff) 
        self.task_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  
        self.task_table.verticalHeader().setVisible(False) 

        # UI 레이아웃 적용
        none_label = QLabel()
        layout.addWidget(none_label)
        layout.addLayout(h_layout)
        layout.addWidget(self.task_table)

        # 테스크 데이터 업데이트 
        task_data(self, self.task_table)
        self.task_table_item(self.task_data_dict)
        return widget  # QWidget 반환

    def task_table_item(self,task_data_dict):

        row = task_table.rowCount()
        task_table.insertRow(row)  # 새로운 행 추가
        task_table.setItem(row, 2, QTableWidgetItem(str(task_id)))
        task_table.setRowHeight(row, 108)
        task_table.setColumnWidth(0, 192)  
        task_table.resizeRowsToContents()

        task_name = QLabel(task_name)
        task_name.setStyleSheet("font-size: 16pt;")
        task_step = QLabel(step)
        task_step.setStyleSheet("color: grey")
        task_step.setAlignment(Qt.AlignRight)

        # 프로젝트 네임
        task_name_layout = QHBoxLayout()
        task_name_layout.addWidget(task_name)
        task_name_layout.addWidget(task_step)

        # 썸네일
        task_thumb = QLabel()
        task_thumb.setFixedWidth(192)
        task_thumb.setFixedHeight(108)
        pixmap = QPixmap(thumb)  # 이미지 파일 경로
        task_thumb.setPixmap(pixmap.scaled(192, 108))  # 크기 조절
        task_thumb.setAlignment(Qt.AlignCenter)  # 이미지를 중앙 정렬
        # task_thumb.setScaledContents(True)  # QLabel 크기에 맞게 이미지 조정
        task_table.setCellWidget(row, 0, task_thumb)

        # 상태 표시 (● 빨간색 원)
        task_status = QLabel()
        status_pixmap = QPixmap(12, 12)  # 작은 원 크기 설정
        status_pixmap.fill(QColor("transparent"))  # 배경 투명

        painter = QPainter(status_pixmap)
        painter.setBrush(QColor(status_color))  # 빨간색 (Hex 코드 사용 가능)
        painter.setPen(QColor(status_color))  # 테두리도 빨간색
        painter.drawEllipse(0, 0, 12, 12)  # (x, y, width, height) 원 그리기
        painter.end()
        task_status.setPixmap(status_pixmap)

        # 작업 유형
        data_set = QLabel(data_set)
        date_set = QLabel(date_set)
        status = QLabel(status)
        status.setStyleSheet("font-size: 10pt; color: grey")

        # 상태와 작업 유형을 수평 정렬
        status_layout = QHBoxLayout()
        status_layout.addWidget(task_status)  # 빨간 원 (●)
        status_layout.addWidget(status)
        
        #status_layout.addWidget(task_step)  # Animation
        status_layout.addStretch()  # 남은 공간 정렬

        text_layout = QVBoxLayout()

        #text_layout.addWidget(task_name)
        text_layout.addLayout(task_name_layout)
        text_layout.addLayout(status_layout)  # 상태 + 작업 유형
        text_layout.addWidget(data_set)
        text_layout.addWidget(date_set)

        widget = QWidget()
        layout = QHBoxLayout()

        layout.addLayout(text_layout)  # 오른쪽: 텍스트 그룹
        layout.setContentsMargins(5, 5, 5, 5)  # 여백 조정
        widget.setLayout(layout)

        # 테이블 위젯 추가
        task_table.setCellWidget(row, 1, widget)
    
    def center_window(self):
        frame_geometry = self.frameGeometry()  # 창의 프레임 가져오기
        screen = QApplication.primaryScreen()  # 현재 사용 중인 화면 가져오기
        screen_geometry = screen.availableGeometry().center()  # 화면의 중앙 좌표
        frame_geometry.moveCenter(screen_geometry)  # 창의 중심을 화면 중심으로 이동
        self.move(frame_geometry.topLeft())  # 최종적으로 창을 이동