# coding: utf-8
import os
import sys
import shutil

from PyQt5.QtWidgets import QBoxLayout, QHBoxLayout, QGridLayout, QWidget, QApplication, QGroupBox
from PyQt5.QtWidgets import QSpinBox, QPushButton, QLabel, QLCDNumber, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QTimer

from save_urls import saveURL

import pyautogui

import time

from config import Config

'''
# 해상도 반환
def get_win_resolution_XY():
    res_x = pyautogui.size()[0]
    res_y = pyautogui.size()[1]

    return res_x, res_y

# 해상도를 구해서 Y값을 반환
def get_win_last_pos_y():
    return pyautogui.size()[1]

# 현재 위치를 구해서 반환
def get_position():
    x, y = pyautogui.position()
    return x, y
'''

class Form(QWidget):
    def get_win_resolution_XY(self):
        res_x = pyautogui.size()[0]
        res_y = pyautogui.size()[1]

        return res_x, res_y

    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        self.dirty_flag = False

        self.res_x, self.res_y = self.get_win_resolution_XY()

        self.setWindowTitle("Save URLs")
        #self.setFixedWidth(480)
        #self.setFixedHeight(680)
        #self.setFixedWidth(640)
        #self.setFixedHeight(480)
        self.setMaximumWidth(self.res_x)
        self.setMaximumHeight(self.res_y)

        # start location
        self.move(self.res_x-500, 200)

        # 환경 변수 파일 이름
        self.config_filename = "./config.txt"

        self.cfg = Config(self.config_filename)

        layout_base = QBoxLayout(QBoxLayout.TopToBottom, self)
        self.setLayout(layout_base)

        ##########################################################
        # 영번째 그룹 (타이머 표시)
        ##########################################################
        self.remain_time = 0

        ## 0.1 Timer
        self.flag = 1 # 0 : 시작위치, 1 : 저장위치

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)

        ## 0.2 LCD
        self.lcd = QLCDNumber(self)
        self.lcd.setMinimumHeight(80)

        ## 0번째 그룹 설정
        grp_0 = QGroupBox("Lcd..")
        layout_base.addWidget(grp_0)
        layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        layout.addWidget(self.lcd)
        grp_0.setLayout(layout)

        ##########################################################
        # 첫번째 그룹 (사용자 입력값 받기, QGridLayout)
        ##########################################################
        ## 1.1 최하단 위치
        self.lbl_max_y = QLabel(str(self.cfg.win_last_pos_y))

        ## 1.2 전체 URL 수
        self.sb_url_t = QSpinBox()
        self.sb_url_t.setMinimum(1)
        self.sb_url_t.setMaximum(200)
        self.sb_url_t.setValue(self.cfg.total_url_count)
        self.sb_url_t.setSingleStep(1)

        self.lbl_url_t = QLabel(str(self.cfg.total_url_count))

        ## 1.3 화면 URL 수
        self.sb_url_w = QSpinBox()
        self.sb_url_w.setMinimum(1)
        self.sb_url_w.setMaximum(100)
        self.sb_url_w.setValue(self.cfg.win_url_count)
        self.sb_url_w.setSingleStep(1)

        self.lbl_url_w = QLabel(str(self.cfg.win_url_count))

        ## 1.4 첫번째 URL의 시작위치 (X, Y)
        self.btn_s_url_XY = QPushButton('Get', self)
        self.btn_s_url_XY.setMaximumWidth(200)
        self.lbl_s_url_XY = QLabel("({},{})".format(self.cfg.win_s_pos_x, self.cfg.win_s_pos_y))

        ## 1.5 파일 입력 창 위치 (X, Y)
        self.btn_save_XY = QPushButton('Get', self)
        self.btn_save_XY.setMaximumWidth(200)
        self.lbl_save_XY = QLabel("({},{})".format(self.cfg.win_out_file_pos_x, self.cfg.win_out_file_pos_y))

        ## 1.6 prefix
        self.lbl_prefix = QLabel(self.cfg.prefix)
        self.le_prefix = QLineEdit(self)
        self.le_prefix.setMaximumWidth(100)

        ## 1.7 save directory
        self.lbl_save_dir = QLabel(self.reduce_string(self.cfg.save_dir))
        #self.lbl_save_dir = QLabel(self.cfg.save_dir)
        self.pb_save_dir = QPushButton("Choose")
        self.pb_save_dir.setMaximumWidth(200)


        ## 1번째 그룹 설정
        grp_1 = QGroupBox("Check Inputs")

        layout_base.addWidget(grp_1)
        layout = QGridLayout()

        # Grid ( , 0)
        layout.addWidget(QLabel('최하단 위치(Y)'), 0, 0)
        layout.addWidget(QLabel('전체 URL 수'), 1, 0)
        layout.addWidget(QLabel('화면 URL 수'), 2, 0)
        layout.addWidget(QLabel('시작위치'), 3, 0)
        layout.addWidget(QLabel('파일입력창 위치'), 4, 0)
        layout.addWidget(QLabel('파일시작명'), 5, 0)
        layout.addWidget(QLabel('파일저장 위치'), 6, 0)

        # Grid ( , 1)
        layout.addWidget(self.sb_url_t, 1, 1)
        layout.addWidget(self.sb_url_w, 2, 1)
        layout.addWidget(self.btn_s_url_XY, 3, 1)
        layout.addWidget(self.btn_save_XY, 4, 1)
        layout.addWidget(self.le_prefix, 5, 1)
        layout.addWidget(self.pb_save_dir, 6, 1)

        # Grid ( , 2)
        layout.addWidget(self.lbl_max_y, 0, 2)
        layout.addWidget(self.lbl_url_t, 1, 2)
        layout.addWidget(self.lbl_url_w, 2, 2)
        layout.addWidget(self.lbl_s_url_XY, 3, 2)
        layout.addWidget(self.lbl_save_XY, 4, 2)
        layout.addWidget(self.lbl_prefix, 5, 2)
        layout.addWidget(self.lbl_save_dir, 6, 2)

        grp_1.setLayout(layout)

        # 1번째 그룹 이벤트 정리
        self.sb_url_t.valueChanged.connect(self.value_changed_t)
        self.sb_url_w.valueChanged.connect(self.value_changed_w)
        self.btn_s_url_XY.clicked.connect(self.get_s_url_XY)
        self.btn_save_XY.clicked.connect(self.get_save_XY)
        self.le_prefix.textChanged[str].connect(self.onChanged)
        self.pb_save_dir.clicked.connect(self.get_save_dir)


        ##########################################################
        # 두번째 그룹 (실행부, QBoxLayout)
        ##########################################################
        # 2번째 그룹 변수들
        self.btn_test = QPushButton("Test")
        self.btn_clear = QPushButton("Clear")
        self.btn_run  = QPushButton("Run")
        self.btn_quit  = QPushButton("Quit")

        # 2번째 그룹 설정
        grp_2 = QGroupBox("Run...")
        layout_base.addWidget(grp_2)
        layout = QHBoxLayout()
        layout.addWidget(self.btn_test)
        layout.addWidget(self.btn_clear)
        layout.addWidget(self.btn_run)
        layout.addWidget(self.btn_quit)
        grp_2.setLayout(layout)

        # 2번째 그룹 이벤트 정리
        """
        self.btn_test.clicked.connect(self.printMessage("Test"))
        self.btn_run.clicked.connect(self.printMessage("Run"))
        self.btn_quit.clicked.connect(self.printMessage("Quit"))
        """
        self.btn_test.clicked.connect(self.printMessage_test)
        self.btn_clear.clicked.connect(self.printMessage_clear)
        self.btn_run.clicked.connect(self.printMessage_run)
        #self.btn_quit.clicked.connect(self.printMessage_quit)
        #self.btn_quit.clicked.connect(self.close)
        self.btn_quit.clicked.connect(self.printMessage_quit)

        ##########################################################
        # 세번째 그룹 (메시지 출력부)
        ##########################################################
        # 3번쨰 그룹 변수들
        self.lbl_msg = QLabel()

        # 3번째 그룹 설정
        grp_3 = QGroupBox("Message..")
        layout_base.addWidget(grp_3)
        layout = QBoxLayout(QBoxLayout.TopToBottom, self)
        layout.addWidget(self.lbl_msg)
        grp_3.setLayout(layout)


    def onChanged(self, text):
        self.cfg.prefix = text
        self.lbl_prefix.setText(self.cfg.prefix)
        self.lbl_prefix.adjustSize()

    '''
    def printMessage_save(self):
        self.lbl_msg.setText("'Save' button pressed...")
        time.sleep(2)
        msg = """self.cfg.win_last_pos_y = {}
self.cfg.total_url_count = {}
self.cfg.win_url_count = {}
self.cfg.win_s_pos_(x,y) = ({},{})
self.cfg.win_out_file_pos_(x,y) = ({},{})
self.cfg.prefix = {}
self.cfg.stop_count = {}""".format(self.cfg.win_last_pos_y, self.cfg.total_url_count, self.cfg.win_url_count, self.cfg.win_s_pos_x, self.cfg.win_s_pos_y, self.cfg.win_out_file_pos_x, self.cfg.win_out_file_pos_y, self.cfg.prefix, self.cfg.stop_count)
        self.lbl_msg.setText(msg)

        self.update_config_file()
    '''

    def printMessage_test(self):
        self.update_config_file()
        su = saveURL(self.config_filename, False, False, False)
        for i in range(self.cfg.stop_count):
            msg = "{}th url processing...".format(i+1)
            self.lbl_msg.setText(msg)
            self.lbl_msg.repaint()
            su.save_current_url(i)

        msg = "test completed...."
        self.lbl_msg.setText(msg)
        self.lbl_msg.repaint()

    def printMessage_clear(self):

        self.dirty_flag = False

        if not os.path.exists(self.cfg.save_dir):
            msg = "{} not found..".format(self.cfg.save_dir)
            self.lbl_msg.setText(msg)
            self.lbl_msg.repaint()
            return

        msg = "clearing output directory...\n [{}]".format(self.cfg.save_dir)
        self.lbl_msg.setText(msg)
        self.lbl_msg.repaint()

        time.sleep(0.5)

        shutil.rmtree(self.cfg.save_dir, ignore_errors=True)
        os.makedirs(self.cfg.save_dir)

        msg = "clearing output directory completed...\n [{}]".format(self.cfg.save_dir)
        self.lbl_msg.setText(msg)
        self.lbl_msg.repaint()

    def printMessage_run(self):
        self.update_config_file()

        err_no = self.check_save_dir()

        if err_no < 0:
            msg = "error no : {}".format(err_no)
            self.lbl_msg.setText(msg)
            self.lbl_msg.repaint()

            return

        su = saveURL(self.config_filename, False, True, True)
        for i in range(self.cfg.total_url_count):
            msg = "{}th url processing...".format(i+1)
            self.lbl_msg.setText(msg)
            self.lbl_msg.repaint()
            su.save_current_url(i)

        msg_1 = "python ~/webhack_storage/PROJECT_K/ZAP_RESULT/XSS/22.MAKE_XSS_URL_FROM_DIR.py --input_dir {}\n".format(self.cfg.save_dir)
        msg_2 = "python ~/webhack_storage/PROJECT_K/ZAP_RESULT/SQLInjection/22.MAKE_SQL_MAP_URL.py --input_dir {}\n".format(self.cfg.save_dir)
        msg = "{}{}".format(msg_1, msg_2)
        self.lbl_msg.setText(msg)
        self.lbl_msg.repaint()

        self.dirty_flag = True

    def printMessage_quit(self):
        self.lbl_msg.setText("'Quit' button pressed...")
        if self.dirty_flag:
            msg_1 = "python ~/webhack_storage/PROJECT_K/ZAP_RESULT/XSS/22.MAKE_XSS_URL_FROM_DIR.py \n\t--input_dir {}\n".format(self.cfg.save_dir)
            msg_2 = "python ~/webhack_storage/PROJECT_K/ZAP_RESULT/SQLInjection/22.MAKE_SQL_MAP_URL.py \n\t--input_dir {}\n".format(self.cfg.save_dir)
            print ("\n{}{}".format(msg_1, msg_2))
        self.close()

    def printMessage_lcd(self, sec):
        self.lbl_msg.setText("{} seconds remained...".format(sec))

    def value_changed_t(self):
        self.cfg.total_url_count = self.sb_url_t.value()
        self.lbl_url_t.setText(str(self.cfg.total_url_count))

    def value_changed_w(self):
        self.cfg.win_url_count = self.sb_url_w.value()
        self.lbl_url_w.setText(str(str(self.cfg.win_url_count)))

    def timeout(self):
        if self.remain_time <= 0:
            self.timer.stop()
            x = pyautogui.position()[0]
            y = pyautogui.position()[1]

            xy = "({},{})".format(x, y)

            if self.flag == 0:
                self.cfg.win_s_pos_x = x
                self.cfg.win_s_pos_y = y
                self.lbl_s_url_XY.setText(xy)
            else:
                self.cfg.win_out_file_pos_x = x
                self.cfg.win_out_file_pos_y = y
                self.lbl_save_XY.setText(xy)

            return

        sender = self.sender()
        self.remain_time = self.remain_time - 1
        if id(sender) == id(self.timer):
            self.lcd.display(str(self.remain_time))
        self.lbl_msg.setText("{} seconds remained..".format(self.remain_time))

    def get_s_url_XY(self):
        #self.lbl_msg.setText("5 seconds remained...")
        self.remain_time = 6
        self.flag = 0
        self.timer.start()

    def get_save_XY(self):
        #self.lbl_msg.setText("5 seconds remained...")
        self.remain_time = 6
        self.flag = 1
        self.timer.start()

    def get_save_dir(self):
        """
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.DirectoryOnly)
        save_dir = QFileDialog.getOpenFileName()
        self.lbl_save_dir.setText(save_dir[0])
        """
        new_save_dir = QFileDialog.getExistingDirectory(self, "Choose Directory", self.cfg.save_dir)
        if new_save_dir == '':
            self.lbl_msg.setText("Choose Directory Canceled...")
            self.lbl_msg.repaint()
            return

        self.lbl_msg.setText(new_save_dir)
        self.lbl_msg.repaint()
        self.cfg.save_dir = new_save_dir
        self.lbl_save_dir.setText(self.reduce_string(self.cfg.save_dir))
        #self.lbl_save_dir.setText(self.cfg.save_dir)
        self.lbl_save_dir.repaint()

    def make_30_chars(self, str):
        if len(str) <= 30:
            return str
        new_str = "..{}".format(str[-28:])

        return new_str

    def reduce_string(self, str, max_chars=40):
        if len(str) <= max_chars:
            return str

        sp = (max_chars * -1) + 2
        new_str = "..{}".format(str[sp:])

        return new_str

    def update_config_file(self):
        self.cfg.make_config_dict_from_self()
        self.cfg.save_config_file()

    def get_file_list(self):
        fileList = []
        rootdir = self.cfg.save_dir

        for root, subFolders, files in os.walk(rootdir):
            for file in files:
                fileList.append(os.path.join(root, file))

        return fileList

    def check_save_dir(self):
        if not os.path.exists(self.cfg.save_dir):
            reply = QMessageBox.question(self, "Message", "Do you want to make save_dir?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                os.makedirs(self.cfg.save_dir)
                return 0
            else:
                return -1001


        file_list = self.get_file_list()
        if len(file_list) > 0:
            reply = QMessageBox.question(self, "Message", "Do you want to remove all files?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

            if reply == QMessageBox.Yes:
                shutil.rmtree(self.cfg.save_dir, ignore_errors=True)
                os.makedirs(self.cfg.save_dir)
                return 0
            else:
                return -2000

        return 0

if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = Form()
    form.show()
    exit(app.exec_())
