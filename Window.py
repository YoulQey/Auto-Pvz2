import sys
from PyQt5.QtWidgets import (QApplication, QWidget,QLabel, QVBoxLayout, QGridLayout, QSpacerItem, QSizePolicy,
                             QHBoxLayout, QTextEdit, QPushButton)
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
import time
import var
fps = 0
suns = 0


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()


    def closeEvent(self, event):
        # 在窗口关闭时调用 sys.exit() 以终止脚本
        stop_fps(fps, start_time)

    def initUI(self):
        self.setWindowTitle('Auto-Pvz2')
        self.setGeometry(1120, 30, 800, 720)  # 窗口生成位置，宽高

        self.label = QLabel(self)
        self.label.setFixedSize(800, 454)  # 固定大小
        self.label.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()        # 创建一个布局，用于显示帧画面
        vbox.addWidget(self.label)
        vbox.setContentsMargins(0, 0, 0, 0)  # 边距设置为0 0 0 0 ，无白边

        self.fps_label = QLabel(f"FPS:{-1}", self)  # 显示fps
        self.fps_label.setFixedHeight(90)
        self.fps_label.setMinimumWidth(250)  # 设置最小宽度，确保标签有足够空间
        self.fps_label.setStyleSheet("font-size: 25px; color: #2CFF19;padding-left: 85px; font-weight: bold;")  # 标签字体大小与颜色 向右偏移 加粗
        self.ms_label = QLabel(f"ms:{-1}", self)  # 显示ms
        self.ms_label.setFixedHeight(130)
        self.ms_label.setMinimumWidth(250)  # 设置最小宽度，确保标签有足够空间
        self.ms_label.setStyleSheet("font-size: 25px; color: #2CFF19;padding-left: 85px; font-weight: bold;")  # 标签字体大小与颜色

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(2)  # 设置格子之间的间距为2像素
        self.grid_labels = [[QLabel(self) for _ in range(9)] for _ in range(5)]     # 创建网格标签
        for i in range(5):
            for j in range(9):
                self.grid_layout.addWidget(self.grid_labels[i][j], i, j)

        # 创建一个水平布局，用于右对齐网格布局
        hbox = QHBoxLayout()
        hbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        hbox.addLayout(self.grid_layout)

        # 创建一个垂直布局用于放置文本框和sun_hbox
        text_and_sun_vbox = QVBoxLayout()

        # 添加一个 QTextEdit 用于显示输出文本
        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)  # 设置为只读
        self.text_output.setFixedHeight(170)  # 文本框的高度
        text_and_sun_vbox.addWidget(self.text_output)


        # 创建一个新的网格布局用于显示内容
        self.Card_layout = QHBoxLayout()

        # 添加一个空白项将 网格向右移动2个像素。防止贴边
        self.Card_layout.addSpacerItem(QSpacerItem(2, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        self.Card_layout.setSpacing(2)  # 设置格子之间的间距为2像素
        self.new_grid_labels = [QLabel(self) for _ in range(7)]  # 创建7个标签
        for i in range(7):
            self.Card_layout.addWidget(self.new_grid_labels[i])  # 添加到水平布局中


        text_and_sun_vbox.addLayout(self.Card_layout)  # 添加水平布局到垂直布局中

        sun_hbox = QHBoxLayout()    # 创建一个水平布局，用于显示 sun 变量和功能按钮

        # 添加一个空白项将 Sun: 0 标签向右移动5个像素。防止贴边
        sun_hbox.addSpacerItem(QSpacerItem(5, 0, QSizePolicy.Fixed, QSizePolicy.Minimum))

        # 添加用于显示 suns 变量的标签
        self.sun_label = QLabel(f"阳光:{suns}", self)   # 显示阳光
        self.sun_label.setFixedHeight(30)
        self.sun_label.setStyleSheet("font-size: 20px;")  # 标签字体大小
        sun_hbox.addWidget(self.sun_label)

        # 添加用于显示 suns 变量的标签
        self.Card_label = QLabel(f"光:{var.光植},攻{var.攻植}", self)  # 显示光植与攻植
        self.Card_label.setFixedHeight(20)
        self.Card_label.setStyleSheet("font-size: 20px;")  # 标签字体大小
        sun_hbox.addWidget(self.Card_label)

        # self.button1 = QPushButton('AUTO-开关', self)
        # self.button1.setFixedSize(120, 30)
        # self.button1.setCheckable(True)  # 设置按钮为可切换状态
        # self.button1.clicked.connect(self.toggle_resolution)
        # sun_hbox.addWidget(self.button1)

        self.button2 = QPushButton('结束', self)
        self.button2.setFixedSize(60, 30)
        self.button2.clicked.connect(lambda: stop_fps(fps, start_time))      # 需要使用lambda: 表达式来传递函数
        sun_hbox.addWidget(self.button2)

        text_and_sun_vbox.addLayout(sun_hbox)   # 将 sun_hbox 添加到 text_and_sun_vbox 中

        # 创建一个水平布局，将 text_and_sun_vbox 放在左边，网格布局放在右边
        main_hbox = QHBoxLayout()
        main_hbox.addLayout(text_and_sun_vbox)
        main_hbox.addLayout(hbox)

        # 创建一个垂直布局，用于底部对齐网格布局
        vbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        vbox.addLayout(main_hbox)

        self.setLayout(vbox)
        self.show()


    def update_sun_value(self, suns, fps, ms):
        self.sun_label.setText(f'Sun:{suns}')  # 更新标签文本
        self.Card_label.setText(f"光植:{var.光植},攻植{var.攻植}")  # 更新标签文本
        self.fps_label.setText(f"FPS:{fps}")  # 更新标签文本
        self.ms_label.setText(f"ms:{ms}")  # 更新标签文本


    # def toggle_resolution(self):
    #     self.is_resolution_reset = not self.is_resolution_reset  # 切换变量状态     要多线程，就先不做了
    #     if self.is_resolution_reset:
    #         var.Auto = True
    #         out_text("Auto-开启")
    #     else:
    #         var.Auto = False
    #         out_text("Auto-关闭")


    def updateFrame(self, frame):
        h, w, ch = frame.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_BGR888)  # 颜色空间BGR
        p = convertToQtFormat.scaled(800, 454, Qt.KeepAspectRatio)
        self.label.setPixmap(QPixmap.fromImage(p))

    def updateGrid(self, grid_data):
        for i in range(5):
            for j in range(9):
                cell_data = grid_data[i][j]
                painter = QPainter()
                pixmap = QPixmap(50, 50)
                pixmap.fill(Qt.white)
                painter.begin(pixmap)

                if cell_data['p'] == 1:
                    painter.setBrush(QColor(0, 255, 0))  # 绿色表示攻植
                    painter.drawEllipse(5, 5, 20, 20)  # 圆点的x,y, 长宽
                elif cell_data['p'] == 2:
                    painter.setBrush(QColor(255, 255, 0))   # 黄色代表光植或其他植物
                    painter.drawEllipse(5, 5, 20, 20)   # 圆点的x,y, 长宽
                elif cell_data['p'] == 3:
                    painter.setBrush(QColor(84, 235, 255))   # 蓝色代表卷心菜等待瞬发
                    painter.drawEllipse(5, 5, 20, 20)   # 圆点的x,y, 长宽
                elif cell_data['p'] == 4:
                    painter.setBrush(QColor(0, 0, 0))   # 黑色代表墓碑
                    painter.drawEllipse(5, 5, 20, 20)   # 圆点的x,y, 长宽
                elif cell_data['p'] == 5:
                    painter.setBrush(QColor(200, 200, 200))   # 白灰色代表其他植物
                    painter.drawEllipse(5, 5, 20, 20)   # 圆点的x,y, 长宽

                if cell_data['z'] == 1:
                    painter.setBrush(QColor(255, 0, 0))  # 红色表示僵尸
                    painter.drawEllipse(25, 5, 20, 20)
                painter.setPen(Qt.black)
                if cell_data['p'] or cell_data['z'] != 0:
                    painter.drawText(5, 45, f"P:{cell_data['p_t']} Z:{cell_data['z_t']}")  # 显示计时器

                painter.end()
                self.grid_labels[i][j].setPixmap(pixmap)

    def Card_update(self):
        # print(var.Card_tf)
        for i in range(7):
            painter = QPainter()
            pixmap = QPixmap(43, 43)
            pixmap.fill(Qt.white)
            painter.begin(pixmap)

            if var.Card_tf[i] == True:
                painter.setBrush(QColor(0, 255, 0))  # 绿色
                painter.drawEllipse(0, 0, 42, 42)  # 画一个圆
                painter.drawText(11, 25, "就绪")  # 显示计时器
            else:
                painter.setBrush(QColor(255, 0, 0))  # 红色
                painter.drawEllipse(0, 0, 42, 42)  # 画一个圆
                painter.drawText(5, 25, "不可用")  # 显示计时器

            painter.end()
            self.new_grid_labels[i].setPixmap(pixmap)

    def appendText(self, text):
        self.text_output.append(text)


def 显示窗口():
    global player, app, start_time     # 定义全局变量
    start_time = time.perf_counter() + 2.5  # 定义开始时间戳，因为yolo开启有延迟，延迟2.5秒
    app = QApplication(sys.argv)
    player = VideoPlayer()


def 处理帧与格子(result, grid1, suns1):
    global fps
    fps = fps + 1

    frame = result.plot(line_width=1)         # 1 可注释这两个，会掉帧30%
    player.updateFrame(frame)  # 窗口显示帧     # 2

    player.updateGrid(grid1)  # 窗口显示格子
    player.Card_update()    # 更新卡片状态

    var.a_time = time.perf_counter()  # 定义时间戳 计算延迟

    fps2 = round(1 / (var.a_time - var.s_time), 1)  # 计算fps与ms
    ms = round(1000 * (var.a_time - var.s_time), 1)
    player.update_sun_value(suns1, fps2, ms)  # 更新文本标签
    app.processEvents()  # 处理事件，确保界面响应

    var.s_time = time.perf_counter()  # 定义时间戳

def out_text(txt):
    player.appendText(txt)

def stop_fps(fps,start_time):   # 计算帧数
    after_time = time.perf_counter()
    FPS = fps / (after_time - start_time)
    print(f"平均画面帧数为:{FPS}")
    sys.exit()
