import pymysql

from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QPushButton, QDialog, QFrame, QLabel, QToolButton, QFileDialog
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtCore import Qt
import sip
import sys

from bookIn import bookIn
from bookIn import singleBookIn
from bookIn import multiBookIn
from leftNavigation import leftNavigation
from bookSearch import bookSearch
from bookBorrow import bookBorrow
from bookReturn import bookReturn
from cardManage import cardManage

# db = pymysql.connect(host='aliyun', user='root', db='test')


class bookSystem(QMainWindow):
    '''
    图书管理系统，数据库为阿里云服务器上的mysql
    '''

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        '''
        初始化整体布局
        '''
        self.resize(1000, 800)
        self.desktopWidth = QApplication.desktop().width()  # 获取当前桌面的宽
        self.desktopHeight = QApplication.desktop().height()  # 获取当前桌面的高

        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_widget.setObjectName('main_widget')  # 对象命名
        self.main_layout = QGridLayout()  # 创建网格布局的对象
        self.main_widget.setLayout(self.main_layout)  # 将主部件设置为网格布局

        self.init_left()  # 初始化左侧空间
        self.init_right()  # 初始化右侧空间

        # 添加左侧导航栏，右侧主界面、图书入库界面(单本入库和多书籍文件导入)、书籍信息查询界面、借书界面、还书界面、借书证管理界面
        self.main_layout.addWidget(self.left_widget, 0, 0, 1, 1)
        self.main_layout.addWidget(self.right_widget, 0, 1, 1, 6)
        self.main_layout.addWidget(self.bookIn_widget, 0, 1, 1, 6)
        self.main_layout.addWidget(self.singleBookIn_widget, 0, 1, 1, 6)
        self.main_layout.addWidget(self.multiBookIn_widget, 0, 1, 1, 6)
        self.main_layout.addWidget(self.bookSearch_widget, 0, 1, 1, 6)
        self.main_layout.addWidget(self.bookSearch_widget.table_widget, 0, 1, 1, 6)  # Search界面的子界面，用于显示查询结果
        self.main_layout.addWidget(self.bookBorrow_widget, 0, 1, 1, 6)
        self.main_layout.addWidget(self.bookReturn_widget, 0, 1, 1, 6)
        self.main_layout.addWidget(self.cardManage_widget, 0, 1, 1, 6)
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件

        # 窗口属性设置
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框
        self.main_layout.setSpacing(0)  # 取出左右之间的缝隙

    def init_left(self):
        '''
        初始化左侧布局
        '''
        self.left_widget = leftNavigation()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')  # 左侧部件对象命名

        self.left_widget.left_close.clicked.connect(self.closeWindow)
        self.left_widget.left_mini.clicked.connect(self.minimizeWindow)
        self.visitFlag = False
        self.left_widget.left_visit.clicked.connect(self.visitWindow)

        self.left_widget.left_button1.clicked.connect(self.into_BookSearchView)
        self.left_widget.left_button4.clicked.connect(self.into_BookInView)
        self.left_widget.left_button2.clicked.connect(self.into_BookBorrowView)
        self.left_widget.left_button3.clicked.connect(self.into_BookReturnView)
        self.left_widget.left_button5.clicked.connect(self.into_CardManageView)

    def init_right(self):
        '''
        初始化右侧布局
        '''
        self.main_view()
        self.bookIn_view()
        self.search_view()
        self.borrow_view()
        self.return_view()
        self.card_view()

    def main_view(self):
        '''
        用于介绍的主界面
        '''
        self.right_widget = QWidget()  # 创建右侧界面1
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QGridLayout()  # 创建网格布局对象1
        self.right_widget.setLayout(self.right_layout)  # 设置右侧界面1的布局为网格布局
        # 支撑空间
        self.label1 = QLabel()
        self.right_layout.addWidget(self.label1, 0, 0, 2, 4)

        # self.noneLabel1_1 = QLabel()  # 用来支撑空间
        # self.right_layout.addWidget(self.noneLabel1_1, 1, 0, 2, 4)

        introduction = '''
            <div style="text-align:center; font-size: 60px;font-family:'Microsoft Yahei'; color:#F76677;"><b>图书管理系统</b></div> 
            <div style="text-align:center; font-size: 15px;font-family: 'Arial'; color:#F76677;"><b>author: 葛浩 3180103494</b><div>
            <div style="text-align:center; font-size: 15px;font-family: 'Arial'; color:#F76677;"><b>Zhejiang University</b></div>
            <div style="text-align:center; font-size: 15px;font-family: 'Arial'; color:#F76677;"><b>github: https://github.com/Sakura-gh</b></div>
        '''
        self.label_introduction = QLabel()
        self.label_introduction.setText(introduction)
        self.label_introduction.setObjectName('introduction')
        # self.label_introduction.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.label_introduction, 3, 1, 2, 2)

        self.noneLabel1_2 = QLabel()  # 用来支撑空间
        self.right_layout.addWidget(self.noneLabel1_2, 5, 0, 2, 4)

    def bookIn_view(self):
        '''
        图书入库: 页面选择：单本入库 or 批量入库
        '''
        # 创建图书入库引导页面
        self.bookIn_widget = bookIn()
        self.bookIn_widget.setObjectName('bookIn_widget')
        # 把切换界面的button和跳转函数绑定
        self.bookIn_widget.returnMain_button.clicked.connect(
            self.return_mainView)
        # 把切换到单书入库的界面与该按钮绑定
        self.bookIn_widget.bookIn_single.clicked.connect(
            self.into_SingleBookInView)
        # 把切换到多书入库的界面与该按钮绑定
        self.bookIn_widget.bookIn_multi.clicked.connect(
            self.into_MultiBookInView)
        # 初始状态：隐藏
        self.bookIn_widget.hide()

        # 创建单本入库页面
        self.singleBookIn_widget = singleBookIn()
        self.singleBookIn_widget.setObjectName('singleBookIn_widget')
        # 把切换回图书入库引导的界面与该按钮绑定
        self.singleBookIn_widget.return_button.clicked.connect(
            self.into_BookInView)
        # 初始状态：隐藏
        self.singleBookIn_widget.hide()

        # 创建多书入库页面
        self.multiBookIn_widget = multiBookIn()
        self.multiBookIn_widget.setObjectName('multiBookIn_widget')
        self.multiBookIn_widget.return_button.clicked.connect(
            self.into_BookInView)
        self.multiBookIn_widget.hide()

    def search_view(self):
        '''
        查询界面
        '''
        self.bookSearch_widget = bookSearch()
        self.bookSearch_widget.setObjectName('bookSearch_widget')
        self.bookSearch_widget.returnMain_button.clicked.connect(self.return_mainView)
        self.bookSearch_widget.hide()

    def borrow_view(self):
        '''
        借书界面
        '''
        self.bookBorrow_widget = bookBorrow()
        self.bookBorrow_widget.setObjectName('bookBorrow_widget')
        self.bookBorrow_widget.returnMain_button.clicked.connect(self.return_mainView)
        self.bookBorrow_widget.hide()

    def return_view(self):
        '''
        还书界面
        '''
        self.bookReturn_widget = bookReturn()
        self.bookReturn_widget.setObjectName('bookReturn_widget')
        self.bookReturn_widget.returnMain_button.clicked.connect(self.return_mainView)
        self.bookReturn_widget.hide()

    def card_view(self):
        '''
        借书证管理界面
        '''
        self.cardManage_widget = cardManage()
        self.cardManage_widget.setObjectName('cardManage_widget')
        self.cardManage_widget.returnMain_button.clicked.connect(self.return_mainView)
        self.cardManage_widget.hide()

    def return_mainView(self):
        self.right_widget.show()
        self.singleBookIn_widget.hide()
        self.multiBookIn_widget.hide()
        self.bookIn_widget.hide()
        self.bookSearch_widget.hide()
        self.bookSearch_widget.table_widget.hide()
        self.bookBorrow_widget.hide()
        self.bookReturn_widget.hide()
        self.cardManage_widget.hide()

    def into_SingleBookInView(self):
        '''
        切换到单书入库的界面
        '''
        self.singleBookIn_widget.show()
        self.multiBookIn_widget.hide()
        self.bookIn_widget.hide()
        self.right_widget.hide()
        self.bookSearch_widget.hide()
        self.bookSearch_widget.table_widget.hide()
        self.bookBorrow_widget.hide()
        self.bookReturn_widget.hide()
        self.cardManage_widget.hide()

    def into_BookInView(self):
        '''
        切换到图书入库界面
        '''
        self.bookIn_widget.show()
        self.singleBookIn_widget.hide()
        self.multiBookIn_widget.hide()
        self.right_widget.hide()
        self.bookSearch_widget.hide()
        self.bookSearch_widget.table_widget.hide()
        self.bookBorrow_widget.hide()
        self.bookReturn_widget.hide()
        self.cardManage_widget.hide()

    def into_MultiBookInView(self):
        '''
        多书入库界面
        '''
        self.multiBookIn_widget.show()
        self.singleBookIn_widget.hide()
        self.bookIn_widget.hide()
        self.right_widget.hide()
        self.bookSearch_widget.hide()
        self.bookSearch_widget.table_widget.hide()
        self.bookBorrow_widget.hide()
        self.bookReturn_widget.hide()
        self.cardManage_widget.hide()

    def into_BookSearchView(self):
        '''
        切换到图书查询界面
        '''
        self.bookSearch_widget.show()
        self.bookSearch_widget.table_widget.hide()
        self.singleBookIn_widget.hide()
        self.multiBookIn_widget.hide()
        self.bookIn_widget.hide()
        self.right_widget.hide()
        self.bookBorrow_widget.hide()
        self.bookReturn_widget.hide()
        self.cardManage_widget.hide()

    def into_BookBorrowView(self):
        '''
        切换到借书界面
        '''
        self.bookBorrow_widget.show()
        self.bookSearch_widget.hide()
        self.bookSearch_widget.table_widget.hide()
        self.singleBookIn_widget.hide()
        self.multiBookIn_widget.hide()
        self.bookIn_widget.hide()
        self.right_widget.hide()
        self.bookReturn_widget.hide()
        self.cardManage_widget.hide()

    def into_BookReturnView(self):
        '''
        切换到还书界面
        '''
        self.bookReturn_widget.show()
        self.bookBorrow_widget.hide()
        self.bookSearch_widget.hide()
        self.bookSearch_widget.table_widget.hide()
        self.singleBookIn_widget.hide()
        self.multiBookIn_widget.hide()
        self.bookIn_widget.hide()
        self.right_widget.hide()
        self.cardManage_widget.hide()

    def into_CardManageView(self):
        '''
        切换到借书证管理界面
        '''
        self.cardManage_widget.show()
        self.bookIn_widget.hide()
        self.singleBookIn_widget.hide()
        self.multiBookIn_widget.hide()
        self.right_widget.hide()
        self.bookSearch_widget.hide()
        self.bookSearch_widget.table_widget.hide()
        self.bookBorrow_widget.hide()
        self.bookReturn_widget.hide()

    def closeWindow(self):
        '''
        close按钮对应的关闭窗口
        '''
        self.close()

    def minimizeWindow(self):
        '''
        mini按钮对应的最小化窗口
        '''
        self.showMinimized()

    def visitWindow(self):
        '''
        visit按钮对应的全屏or还原窗口大小
        '''
        if self.visitFlag == False:
            # self.showFullScreen()
            # self.showMaximized()
            self.lastWidth = self.width()
            self.lastHeight = self.height()
            self.resize(self.desktopWidth, self.desktopHeight)
            x = (self.desktopWidth - self.width()) // 2
            y = (self.desktopHeight - self.height()) // 2
            self.move(x, y)
            # print('max')
            self.visitFlag = True
        else:
            self.resize(self.lastWidth, self.lastHeight)
            x = (self.desktopWidth - self.width()) // 2
            y = (self.desktopHeight - self.height()) // 2
            self.move(x, y)
            # print('origin')
            self.visitFlag = False

    def mousePressEvent(self, QMouseEvent):
        '''
        redefine已有的鼠标按下事件
        '''
        if QMouseEvent.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = QMouseEvent.globalPos()-self.pos()  # 获取鼠标相对窗口的位置
            QMouseEvent.accept()
            # self.setCursor(QCursor(Qt.WaitCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        '''
        redefine已有的鼠标移动事件
        '''
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos()-self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        '''
        redefine已有的鼠标释放事件
        '''
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))


def main():
    with open('app.qss', encoding='utf-8') as f:
        qss = f.read()
    app = QApplication(sys.argv)
    app.setStyleSheet(qss)
    gui = bookSystem()
    gui.setWindowIcon(QIcon('./img/book.ico'))
    gui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
