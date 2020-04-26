from PyQt5.QtWidgets import QStyleOption, QStyle, QWidget, QLabel, QPushButton, QLineEdit, QTableView, QGridLayout, QFileDialog, QMessageBox, QTableWidget, QFrame, QTableWidgetItem
from PyQt5.QtGui import QPainter, QFont
import sip
import pymysql
import datetime


class bookBorrow(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.bookBorrow_layout = QGridLayout()
        self.setLayout(self.bookBorrow_layout)

        self.returnMain_button = QPushButton('返回主界面')
        self.bookBorrow_layout.addWidget(self.returnMain_button, 0, 0, 1, 6)

        self.book_number_label = QLabel('书籍编号')
        self.bookBorrow_layout.addWidget(self.book_number_label, 2, 1, 1, 1)
        self.book_number_label.setObjectName('bookBorrow_label')
        self.book_number = QLineEdit()
        self.bookBorrow_layout.addWidget(self.book_number, 2, 2, 1, 3)
        self.book_number.setObjectName('bookBorrow_edit')

        self.card_number_label = QLabel('借书证号')
        self.bookBorrow_layout.addWidget(self.card_number_label, 3, 1, 1, 1)
        self.card_number_label.setObjectName('bookBorrow_label')
        self.card_number = QLineEdit()
        self.bookBorrow_layout.addWidget(self.card_number, 3, 2, 1, 3)
        self.card_number.setObjectName('bookBorrow_edit')

        self.return_date_label = QLabel('还书日期')
        self.bookBorrow_layout.addWidget(self.return_date_label, 4, 1, 1, 1)
        self.return_date_label.setObjectName('bookBorrow_label')
        self.return_date = QLineEdit()
        self.bookBorrow_layout.addWidget(self.return_date, 4, 2, 1, 3)
        self.return_date.setObjectName('bookBorrow_edit')

        self.Borrow_button = QPushButton('Borrow')
        self.bookBorrow_layout.addWidget(self.Borrow_button, 5, 2, 1, 2)
        self.Borrow_button.setObjectName('bookBorrow_button')
        self.Borrow_button.clicked.connect(self.borrow)

        self.record_label = QLabel('当前已借书籍：')
        self.bookBorrow_layout.addWidget(self.record_label, 6, 2, 1, 2)
        self.record_label.setObjectName('bookBorrow_already')

        self.borrowRecord_table = QTableWidget()
        self.bookBorrow_layout.addWidget(self.borrowRecord_table, 7, 1, 4, 4)
        self.borrowRecord_table.hide()

        self.label = QLabel('借阅书籍')
        self.label.setObjectName('bookBorrow_title')
        self.bookBorrow_layout.addWidget(self.label, 11, 4, 2, 2)

    def borrow(self):
        '''
        借书
        '''
        conn = pymysql.connect(host='47.115.54.28', user='root', db='bookSystem')
        cursor = conn.cursor()

        bno = self.book_number.text()
        cno = self.card_number.text()
        rdate = self.return_date.text()
        try:
            query = ''
            flag = 0
            data = ''
            # 只输入了借书证号
            if cno != '' and (bno == '' or rdate == ''):
                # 读取当前用户已借书籍
                query = "select * from book as b where b.bno in (select bno from borrow where cno = '%s');" % cno
                print(query)
                cursor.execute(query)
                data = cursor.fetchall()
            elif cno != '' and bno != '' and rdate != '':
                query = "select stock from book where bno = '%s';" % bno
                print(query)
                cursor.execute(query)
                tmp = cursor.fetchall()
                # 如果没有返回信息，说明用户输入的信息跟数据库里的数据不匹配，可能该书号根本就不存在
                if len(tmp) > 0:
                    stock = int(tmp[0][0])
                else:
                    raise Exception

                if stock == 0:
                    query = "select min(return_date) from borrow where bno = '%s';" % bno
                    cursor.execute(query)
                    return_date = cursor.fetchall()[0][0]
                    QMessageBox.warning(self, '借书失败', '该书库存为零！该书最近一次归还的时间为%d' % int(return_date))
                else:
                    '''修正：借书还书都不会影响总藏书量，之前理解有误。。。'''
                    # 借书，库存减一，更新总藏书数，borrow借书记录增加一条
                    query1 = "update book set stock = stock - 1 where bno = '%s';" % bno
                    # query2 = "set @total_num = (select sum(stock) from book);"
                    # query3 = "update book set total = @total_num;"
                    query4 = "insert into borrow values ('%s','%s',%d,%d);" % (cno, bno, int(datetime.datetime.now().year), int(rdate))
                    cursor.execute(query1)
                    # cursor.execute(query2)
                    # cursor.execute(query3)
                    cursor.execute(query4)
                    flag = 1
                    # 读取当前用户已借书籍
                    query = "select * from book as b where b.bno in (select bno from borrow where cno = '%s');" % cno
                    cursor.execute(query)
                    data = cursor.fetchall()
                    # print(query1, '\n', query2, '\n', query3, '\n', query4, '\n', query)
                    print(query1, '\n', query4, '\n', query)
            else:
                print('借书证不能为空！')
                raise Exception
        except Exception as e:
            conn.rollback()
            print('事务处理失败', e)

            QMessageBox.critical(self, '查询失败', '请检查您输入的信息！', QMessageBox.Ok)
        else:
            conn.commit()
            print('事务处理成功')
            if flag == 1:
                QMessageBox.information(self, '借书成功', '您已成功借到该书籍！', QMessageBox.Ok)
            # 如果有返回数据
            if len(data) > 0:
                print(data)
                self.showTable(cursor, data)
                if flag != 1:
                    QMessageBox.warning(self, '查询成功', '由于您没有输入三个完整的信息，这里只返回借书证号对应的所有已借书籍，而不会执行借书操作！')
            else:
                self.showTable(cursor, data)  # 传入空数据
                if flag == 1:
                    QMessageBox.information(self, '查询成功', '该借书证暂无已借书籍！', QMessageBox.Ok)
                else:
                    QMessageBox.information(self, '查询成功', '该借书证暂无已借书籍！(由于输入信息不完整，只返回借书证号对应的所有已借书籍，而不会执行借书操作！)')

        cursor.close()
        conn.close()

    def showTable(self, cursor, data):
        '''
        将用户已借书籍显示出来
        '''
        if data:
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

            # 删除上次记录
            if self.borrowRecord_table:
                self.bookBorrow_layout.removeWidget(self.borrowRecord_table)
                sip.delete(self.borrowRecord_table)
            # 重新添加该表
            self.borrowRecord_table = table
        else:
            # 如果数据不存在，则创建空表
            self.borrowRecord_table = QTableWidget()

        # 重新添加该表
        self.bookBorrow_layout.addWidget(self.borrowRecord_table, 7, 1, 4, 4)

    def paintEvent(self, event):
        '''
        避免多重传值后的功能失效，从而可以继续使用qss设置样式
        '''
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
