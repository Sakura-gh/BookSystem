from PyQt5.QtWidgets import QStyleOption, QStyle, QWidget, QLabel, QPushButton, QLineEdit, QTableView, QGridLayout, QFileDialog, QMessageBox, QTableWidget, QFrame, QTableWidgetItem
from PyQt5.QtGui import QPainter, QFont
import sip
import pymysql


class bookSearch(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.bookSearch_layout = QGridLayout()
        self.setLayout(self.bookSearch_layout)

        self.returnMain_button = QPushButton('返回主界面')
        self.bookSearch_layout.addWidget(self.returnMain_button, 0, 0, 1, 6)

        self.space_label1 = QLabel()
        self.bookSearch_layout.addWidget(self.space_label1, 1, 0, 1, 6)
        self.space_label1.setObjectName('bookSearch_spaceLabel1')

        self.book_number_label = QLabel('书号')
        self.bookSearch_layout.addWidget(self.book_number_label, 2, 1, 1, 1)
        self.book_number_label.setObjectName('bookSearch_label')
        self.book_number = QLineEdit()
        self.bookSearch_layout.addWidget(self.book_number, 2, 2, 1, 3)
        self.book_number.setObjectName('bookSearch_edit')

        self.category_label = QLabel('类别')
        self.bookSearch_layout.addWidget(self.category_label, 3, 1, 1, 1)
        self.category_label.setObjectName('bookSearch_label')
        self.category = QLineEdit()
        self.bookSearch_layout.addWidget(self.category, 3, 2, 1, 3)
        self.category.setObjectName('bookSearch_edit')

        self.title_label = QLabel('书名')
        self.bookSearch_layout.addWidget(self.title_label, 4, 1, 1, 1)
        self.title_label.setObjectName('bookSearch_label')
        self.title = QLineEdit()
        self.bookSearch_layout.addWidget(self.title, 4, 2, 1, 3)
        self.title.setObjectName('bookSearch_edit')

        self.press_label = QLabel('出版社')
        self.bookSearch_layout.addWidget(self.press_label, 5, 1, 1, 1)
        self.press_label.setObjectName('bookSearch_label')
        self.press = QLineEdit()
        self.bookSearch_layout.addWidget(self.press, 5, 2, 1, 3)
        self.press.setObjectName('bookSearch_edit')

        self.year_label = QLabel('年份')
        self.bookSearch_layout.addWidget(self.year_label, 6, 1, 1, 1)
        self.year_label.setObjectName('bookSearch_label')
        self.year1 = QLineEdit()
        self.bookSearch_layout.addWidget(self.year1, 6, 2, 1, 1)
        self.year1.setObjectName('bookSearch_edit_two')
        self.to1 = QLabel('to')
        self.bookSearch_layout.addWidget(self.to1, 6, 3, 1, 1)
        self.to1.setObjectName('bookSearch_label_to')
        self.year2 = QLineEdit()
        self.bookSearch_layout.addWidget(self.year2, 6, 4, 1, 1)
        self.year2.setObjectName('bookSearch_edit_two')

        self.author_label = QLabel('作者')
        self.bookSearch_layout.addWidget(self.author_label, 7, 1, 1, 1)
        self.author_label.setObjectName('bookSearch_label')
        self.author = QLineEdit()
        self.bookSearch_layout.addWidget(self.author, 7, 2, 1, 3)
        self.author.setObjectName('bookSearch_edit')

        self.price_label = QLabel('价格区间')
        self.bookSearch_layout.addWidget(self.price_label, 8, 1, 1, 1)
        self.price_label.setObjectName('bookSearch_label')
        self.price1 = QLineEdit()
        self.bookSearch_layout.addWidget(self.price1, 8, 2, 1, 1)
        self.price1.setObjectName('bookSearch_edit_two')
        self.to = QLabel('to')
        self.bookSearch_layout.addWidget(self.to, 8, 3, 1, 1)
        self.to.setObjectName('bookSearch_label_to')
        self.price2 = QLineEdit()
        self.bookSearch_layout.addWidget(self.price2, 8, 4, 1, 1)
        self.price2.setObjectName('bookSearch_edit_two')

        self.search_button = QPushButton('Search')
        self.bookSearch_layout.addWidget(self.search_button, 11, 2, 1, 2)
        self.search_button.setObjectName('bookSearch_button')
        self.search_button.clicked.connect(self.search)

        # 弹簧标签，用于撑开空间
        self.space_label2 = QLabel()
        self.bookSearch_layout.addWidget(self.space_label2, 12, 0, 2, 6)
        # self.space_label2.setObjectName('bookSearch_spaceLabel2')

        self.label = QLabel('图书查询')
        self.bookSearch_layout.addWidget(self.label, 13, 4, 2, 2)
        self.label.setObjectName('bookSearch_title')

        # Search界面的子界面，用于显示查询结果
        self.table_widget = searchTable(None)
        self.table_widget.setObjectName('table_widget')
        # 用于子界面回到母查询界面
        self.table_widget.returnSearch_button.clicked.connect(self.returnSearch)

    def search(self):
        '''
        查询操作
        '''
        bno = self.book_number.text()
        category = self.category.text()
        title = self.title.text()
        press = self.press.text()
        author = self.author.text()
        year1 = self.year1.text()
        year2 = self.year2.text()
        price1 = self.price1.text()
        price2 = self.price2.text()

        query = ''
        flag = 0
        if bno:
            if flag == 0:
                query += "bno = '%s'" % bno
                flag = 1
            else:
                query += " and bno = '%s'" % bno
        if category:
            if flag == 0:
                query += "category = '%s'" % category
                flag = 1
            else:
                query += " and category = '%s'" % category
        if title:
            if flag == 0:
                query += "title = '%s'" % title
                flag = 1
            else:
                query += " and title = '%s'" % title
        if press:
            if flag == 0:
                query += "press = '%s'" % press
                flag = 1
            else:
                query += " and press = '%s'" % press
        if author:
            if flag == 0:
                query += "author = '%s'" % author
                flag = 1
            else:
                query += " and author = '%s'" % author
        if year1:
            if flag == 0:
                query += "_year > %d" % (int(year1))
                flag = 1
            else:
                query += " and _year > %d" % (int(year1))
        if year2:
            if flag == 0:
                query += "_year < %d" % (int(year2))
                flag = 1
            else:
                query += " and _year < %d" % (int(year2))
        if price1:
            if flag == 0:
                query += "price > %.2f" % (float(price1))
                flag = 1
            else:
                query += " and price > %.2f" % (float(price1))
        if price2:
            if flag == 0:
                query += "price < %.2f" % (float(price2))
                flag = 1
            else:
                query += " and price < %.2f" % (float(price2))

        conn = pymysql.connect(host='47.115.54.28', user='root', db='bookSystem')
        cursor = conn.cursor()
        # 查询语句,如果什么都不输入，默认查询全部书籍信息
        if query != '':
            selectSQL = "select * from book where " + query
        else:
            selectSQL = "select * from book"
        # 执行查询
        try:
            print(selectSQL)
            cursor.execute(selectSQL)
            data = cursor.fetchall()
        except Exception as e:
            conn.rollback()
            print('事务处理失败', e)
            QMessageBox.critical(
                self, '查询失败', '请检查您输入的信息！', QMessageBox.Ok)
        else:
            conn.commit()
            print(data)
            print('事务处理成功')
            # 如果有返回数据
            if len(data) > 0:
                QMessageBox.information(
                    self, '查询成功', '所有符合条件的记录都已显示！', QMessageBox.Ok)
                self.showTable(cursor, data)
            else:
                QMessageBox.information(
                    self, '查询成功', '没有符合条件的记录！', QMessageBox.Ok)

        cursor.close()
        conn.close()

    def showTable(self, cursor, data):
        '''
        把pymysql返回的表显示出来
        '''
        # 列名
        column = [s[0] for s in cursor.description]
        # 数据大小
        row = len(data)
        vol = len(data[0])
        # 插入表格
        table = QTableWidget(row, vol)
        # font = QFont('微软雅黑', 10)
        table.setHorizontalHeaderLabels(column)
        table.verticalHeader().setVisible(False)
        table.setFrameShape(QFrame.NoFrame)

        for i in range(row):
            for j in range(vol):
                table.setItem(i, j, QTableWidgetItem(str(data[i][j])))

        # self.bookSearch_layout.addWidget(self.table)
        self.table_widget.delete()
        self.table_widget.addTable(table)
        self.table_widget.show()
        self.hide()

    def returnSearch(self):
        self.show()
        self.table_widget.hide()

    def paintEvent(self, event):
        '''
        避免多重传值后的功能失效，从而可以继续使用qss设置样式
        '''
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


class searchTable(QWidget):
    def __init__(self, table):
        super().__init__()
        self.init(table)

    def init(self, table):
        self.table_layout = QGridLayout()
        self.setLayout(self.table_layout)
        self.returnSearch_button = QPushButton('返回查询界面')
        self.table_layout.addWidget(self.returnSearch_button, 0, 0, 1, 6)

        # 弹簧标签，用于撑开空间
        self.space_label1 = QLabel()
        self.table_layout.addWidget(self.space_label1, 1, 0, 1, 6)

        # 弹簧标签，用于撑开空间
        self.space_label2 = QLabel()
        self.table_layout.addWidget(self.space_label2, 6, 0, 1, 6)

        self.addTable(table)
        # 初始化隐藏
        self.hide()

    def delete(self):
        '''
        删除上一次查询的表
        '''
        if self.table:
            self.table_layout.removeWidget(self.table)
            sip.delete(self.table)

    def addTable(self, table):
        '''
        新增这一次查询的表
        '''
        if table:
            self.table = table
            self.table_layout.addWidget(self.table, 2, 0, 4, 6)
            self.table.setObjectName('search_result')
        else:
            self.table = None

    def paintEvent(self, event):
        '''
        避免多重传值后的功能失效，从而可以继续使用qss设置样式
        '''
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
