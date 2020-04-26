from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QStyleOption, QStyle, QToolButton, QTextEdit, QFileDialog
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import pymysql


class bookIn(QWidget):
    '''
    图书入库界面
    '''

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.bookIn_layout = QGridLayout()  # 创建网格布局对象2
        self.setLayout(self.bookIn_layout)  # 设置右侧界面2的布局为网格布局
        self.returnMain_button = QPushButton()  # 加一个用来界面跳转的returnMain_button
        self.returnMain_button.setText('返回主界面')
        self.bookIn_layout.addWidget(self.returnMain_button, 0, 0, 1, 7)

        # 单数入库
        self.bookIn_single = QToolButton()
        self.bookIn_single.setText('单本入库')
        self.bookIn_single.setObjectName('bookInLibrary')
        self.bookIn_single.setIcon(
            QtGui.QIcon('./img/bookinlibrary_single.png'))
        self.bookIn_single.setIconSize(QtCore.QSize(150, 150))
        self.bookIn_single.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.bookIn_layout.addWidget(self.bookIn_single, 3, 1, 2, 2)

        # 多书入库
        self.bookIn_multi = QToolButton()
        self.bookIn_multi.setText('批量入库')
        self.bookIn_multi.setObjectName('bookInLibrary')
        self.bookIn_multi.setIcon(
            QtGui.QIcon('./img/bookinlibrary_multi.png'))
        self.bookIn_multi.setIconSize(QtCore.QSize(150, 150))
        self.bookIn_multi.setToolButtonStyle(
            Qt.ToolButtonTextUnderIcon)
        self.bookIn_layout.addWidget(self.bookIn_multi, 3, 4, 2, 2)

        # 图书入库页面选择
        self.bookIn_label = QLabel('图书入库')
        self.bookIn_label.setObjectName('bookInLibrary_label')
        self.bookIn_layout.addWidget(self.bookIn_label, 5, 5, 1, 2)

    def paintEvent(self, event):
        '''
        避免多重传值后的功能失效，从而可以继续使用qss设置样式
        '''
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


class singleBookIn(QWidget):
    '''
    单书入库的界面:书号, 类别, 书名, 出版社, 年份, 作者, 价格, 数量
    注意：pyqt5中继承QWidget的类不能直接导入qss样式(天坑)，需要重载函数paintEvent
    '''

    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        '''
        填写表单和提交按钮
        '''
        self.singleBookIn_layout = QGridLayout()
        self.setLayout(self.singleBookIn_layout)

        # 返回图书入库界面的按钮
        self.return_button = QPushButton('返回上一界面')
        self.singleBookIn_layout.addWidget(self.return_button, 0, 0, 1, 6)

        # 弹簧标签，用于撑开空间
        self.space_label1 = QLabel()
        self.singleBookIn_layout.addWidget(self.space_label1, 1, 0, 1, 6)
        self.space_label1.setObjectName('singleBookIn_spaceLabel1')

        self.book_number_label = QLabel('书号')
        self.singleBookIn_layout.addWidget(self.book_number_label, 2, 1, 1, 1)
        self.book_number_label.setObjectName('singleBookIn_label')
        self.book_number = QLineEdit()
        self.singleBookIn_layout.addWidget(self.book_number, 2, 2, 1, 3)

        self.category_label = QLabel('类别')
        self.singleBookIn_layout.addWidget(self.category_label, 3, 1, 1, 1)
        self.category_label.setObjectName('singleBookIn_label')
        self.category = QLineEdit()
        self.singleBookIn_layout.addWidget(self.category, 3, 2, 1, 3)

        self.title_label = QLabel('书名')
        self.singleBookIn_layout.addWidget(self.title_label, 4, 1, 1, 1)
        self.title_label.setObjectName('singleBookIn_label')
        self.title = QLineEdit()
        self.singleBookIn_layout.addWidget(self.title, 4, 2, 1, 3)

        self.press_label = QLabel('出版社')
        self.singleBookIn_layout.addWidget(self.press_label, 5, 1, 1, 1)
        self.press_label.setObjectName('singleBookIn_label')
        self.press = QLineEdit()
        self.singleBookIn_layout.addWidget(self.press, 5, 2, 1, 3)

        self.year_label = QLabel('年份')
        self.singleBookIn_layout.addWidget(self.year_label, 6, 1, 1, 1)
        self.year_label.setObjectName('singleBookIn_label')
        self.year = QLineEdit()
        self.singleBookIn_layout.addWidget(self.year, 6, 2, 1, 3)

        self.author_label = QLabel('作者')
        self.singleBookIn_layout.addWidget(self.author_label, 7, 1, 1, 1)
        self.author_label.setObjectName('singleBookIn_label')
        self.author = QLineEdit()
        self.singleBookIn_layout.addWidget(self.author, 7, 2, 1, 3)

        self.price_label = QLabel('价格')
        self.singleBookIn_layout.addWidget(self.price_label, 8, 1, 1, 1)
        self.price_label.setObjectName('singleBookIn_label')
        self.price = QLineEdit()
        self.singleBookIn_layout.addWidget(self.price, 8, 2, 1, 3)

        self.stock_label = QLabel('数量')
        self.singleBookIn_layout.addWidget(self.stock_label, 9, 1, 1, 1)
        self.stock_label.setObjectName('singleBookIn_label')
        self.stock = QLineEdit()
        self.singleBookIn_layout.addWidget(self.stock, 9, 2, 1, 3)

        self.submit_button = QPushButton('提交')
        self.singleBookIn_layout.addWidget(self.submit_button, 11, 2, 1, 2)
        self.submit_button.setObjectName('singleBookIn_button')
        self.submit_button.clicked.connect(self.submit)

        # 弹簧标签，用于撑开空间
        self.space_label2 = QLabel()
        self.singleBookIn_layout.addWidget(self.space_label2, 12, 0, 2, 6)

        self.label = QLabel('单书入库')
        self.singleBookIn_layout.addWidget(self.label, 13, 4, 2, 2)
        self.label.setObjectName('singleBookIn_title')

    def submit(self):
        '''
        如果primary key：book_number为空，则弹窗提示错误，否则成功写入
        '''
        try:
            conn = pymysql.connect(host='47.115.54.28', user='root', db='bookSystem')
            cursor = conn.cursor()

            bno = self.book_number.text()
            if not bno:
                QMessageBox.warning(self, '入库失败', '书名不能为空！',
                                    QMessageBox.Ok)
                raise Exception
                # QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            else:
                category = self.category.text()
                title = self.title.text()
                press = self.press.text()
                year = self.year.text()
                author = self.author.text()
                price = self.price.text()
                stock = self.stock.text()
                temp = (bno, category, title, press, int(year),
                        author, float(price), int(stock), int(stock))

                '''更正：总藏书量为当前书的累计入库值，而不是所有书的库存'''
                # 插入语句(包括额外处理的total_num)
                insertSQL1 = "insert into book values " + str(temp) + " on duplicate key update stock = stock + " + stock + ", total = total + " + stock + ";"
                # insertSQL2 = "set @total_num = (select sum(stock) from book);"
                # insertSQL3 = "update book set total = @total_num;"
                print(insertSQL1)
                # 执行插入语句
                cursor.execute(insertSQL1)
                # cursor.execute(insertSQL2)
                # cursor.execute(insertSQL3)
        except Exception as e:
            conn.rollback()
            print('事务处理失败', e)
            QMessageBox.critical(
                self, '插入失败', '请检查您输入的信息！', QMessageBox.Ok)
        else:
            conn.commit()
            print('事务处理成功', cursor.rowcount)
            QMessageBox.information(
                self, '插入成功', '您的书籍已成功入库！', QMessageBox.Ok)

            cursor.close()
            conn.close()

    def paintEvent(self, event):
        '''
        避免多重传值后的功能失效，从而可以继续使用qss设置样式
        '''
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


class multiBookIn(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.multiBookIn_layout = QGridLayout()
        self.setLayout(self.multiBookIn_layout)

        # 返回图书入库界面的按钮
        self.return_button = QPushButton('返回上一界面')
        self.multiBookIn_layout.addWidget(self.return_button, 0, 0, 1, 6)

        # 弹簧标签，用于撑开空间
        self.space_label1 = QLabel()
        self.multiBookIn_layout.addWidget(self.space_label1, 1, 0, 1, 6)
        self.space_label1.setObjectName('multiBookIn_spaceLabel1')

        self.bookDataEdit = QTextEdit()
        self.bookDataEdit.setObjectName('textEdit')
        self.data = self.bookDataEdit.toPlainText()  # 返回文本框内的内容
        self.multiBookIn_layout.addWidget(self.bookDataEdit, 2, 1, 4, 4)

        self.chooseFile_button = QPushButton('选择文件')
        self.chooseFile_button.setObjectName('chooseFile')
        self.multiBookIn_layout.addWidget(self.chooseFile_button, 7, 1, 1, 2)
        self.chooseFile_button.clicked.connect(self.chooseFile)

        self.submit_button = QPushButton('提交')
        self.submit_button.setObjectName('submit')
        self.multiBookIn_layout.addWidget(self.submit_button, 7, 3, 1, 2)
        self.submit_button.clicked.connect(self.submit)

        # 弹簧标签，用于撑开空间
        self.space_label2 = QLabel()
        self.multiBookIn_layout.addWidget(self.space_label2, 8, 0, 2, 6)
        self.space_label2.setObjectName('multiBookIn_spaceLabel2')

        self.label = QLabel('多书入库')
        self.label.setObjectName('multiBookIn_title')
        self.multiBookIn_layout.addWidget(self.label, 9, 4, 2, 2)

    def chooseFile(self):
        '''
        打开文件，并显示在文本框中
        '''
        fname = QFileDialog.getOpenFileName(
            self, '多书入库(txt文件)', './', 'Txt(*.txt)')
        if fname[0]:
            with open(fname[0], 'r', encoding='utf-8') as f:
                self.data = f.read()
                self.bookDataEdit.setText(self.data)

    def submit(self):
        '''
        多书同时入库提交，QTextEdit.clear()清空文本框
        '''
        try:
            conn = pymysql.connect(host='47.115.54.28', user='root', db='bookSystem')
            cursor = conn.cursor()

            self.data = self.bookDataEdit.toPlainText()
            ls = self.data.split('\n')
            for line in ls:
                item = line.strip('(').strip(')').split(',')
                for i in range(len(item)):
                    item[i] = item[i].strip(' ')
                if len(item) == 8:
                    # 插入语句(包括额外处理的total_num)
                    temp = (item[0], item[1], item[2], item[3], int(item[4]), item[5], float(item[6]), int(item[7]), int(item[7]))

                    # insertSQL1 = "insert into book values " + str(temp) + " on duplicate key update stock = stock + " + item[7] + ";"
                    # insertSQL2 = "set @total_num = (select sum(stock) from book);"
                    # insertSQL3 = "update book set total = @total_num;"
                    # # 执行插入语句
                    # cursor.execute(insertSQL1)
                    # cursor.execute(insertSQL2)
                    # cursor.execute(insertSQL3)

                    # 之前好像把总藏书量误解成了所有书的库存的累计合。。。
                    insertSQL1 = "insert into book values " + str(temp) + " on duplicate key update stock = stock + " + item[7] + ", total = total + " + item[7] + ";"
                    print(insertSQL1)
                    cursor.execute(insertSQL1)

                elif line != ls[-1]:
                    raise Exception

        except Exception as e:
            conn.rollback()
            print('事务处理失败', e)
            QMessageBox.critical(
                self, '插入失败', '请检查您输入的信息！', QMessageBox.Ok)
        else:
            conn.commit()
            print('事务处理成功')
            QMessageBox.information(
                self, '插入成功', '您的书籍已成功入库！', QMessageBox.Ok)

        cursor.close()
        conn.close()

    def paintEvent(self, event):
        '''
        避免多重传值后的功能失效，从而可以继续使用qss设置样式
        '''
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
