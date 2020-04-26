from PyQt5.QtWidgets import QStyleOption, QStyle, QWidget, QLabel, QPushButton, QLineEdit, QTableView, QGridLayout, QFileDialog, QMessageBox, QTableWidget, QFrame, QTableWidgetItem
from PyQt5.QtGui import QPainter, QFont
import sip
import pymysql


class bookReturn(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.bookReturn_layout = QGridLayout()
        self.setLayout(self.bookReturn_layout)

        self.returnMain_button = QPushButton('返回主界面')
        self.bookReturn_layout.addWidget(self.returnMain_button, 0, 0, 1, 6)

        self.book_number_label = QLabel('书籍编号')
        self.bookReturn_layout.addWidget(self.book_number_label, 2, 1, 1, 1)
        self.book_number_label.setObjectName('bookReturn_label')
        self.book_number = QLineEdit()
        self.bookReturn_layout.addWidget(self.book_number, 2, 2, 1, 3)
        self.book_number.setObjectName('bookReturn_edit')

        self.card_number_label = QLabel('借书证号')
        self.bookReturn_layout.addWidget(self.card_number_label, 3, 1, 1, 1)
        self.card_number_label.setObjectName('bookReturn_label')
        self.card_number = QLineEdit()
        self.bookReturn_layout.addWidget(self.card_number, 3, 2, 1, 3)
        self.card_number.setObjectName('bookReturn_edit')

        self.Return_button = QPushButton('Return')
        self.bookReturn_layout.addWidget(self.Return_button, 4, 2, 1, 2)
        self.Return_button.setObjectName('bookReturn_button')
        self.Return_button.clicked.connect(self.Return)

        self.record_label = QLabel('当前已借书籍：')
        self.bookReturn_layout.addWidget(self.record_label, 5, 2, 1, 2)
        self.record_label.setObjectName('bookBorrow_already')

        self.returnRecord_table = QTableWidget()
        self.bookReturn_layout.addWidget(self.returnRecord_table, 6, 1, 4, 4)
        self.returnRecord_table.hide()

        self.label = QLabel('返还书籍')
        self.label.setObjectName('bookReturn_title')
        self.bookReturn_layout.addWidget(self.label, 10, 4, 2, 2)

    def Return(self):
        '''
        还书
        '''
        conn = pymysql.connect(host='47.115.54.28', user='root', db='bookSystem')
        cursor = conn.cursor()

        bno = self.book_number.text()
        cno = self.card_number.text()
        try:
            query = ''
            flag = 0
            data = ''
            if cno != '':
                # 先检查该借书证是否存在
                query = "select * from card where cno = '%s';" % cno
                print(query)
                cursor.execute(query)
                tmp = cursor.fetchall()
                if len(tmp) == 0:
                    print(tmp)
                    print('借书证号不存在！')
                    raise Exception
            if bno != '':
                # 检查该书号是否存在
                query = "select * from book where bno = '%s';" % bno
                print(query)
                cursor.execute(query)
                tmp = cursor.fetchall()
                if len(tmp) == 0:
                    print(tmp)
                    print('该书号不存在！')
                    raise Exception

            # 只输入了借书证号
            if cno != '' and bno == '':
                # 读取当前用户已借书籍
                query = "select * from book as b where b.bno in (select bno from borrow where cno = '%s');" % cno
                print(query)
                cursor.execute(query)
                data = cursor.fetchall()
            elif cno != '' and bno != '':
                '''修正：借书还书都不会影响总藏书量，之前理解有误。。。'''
                # 检查该借书关系是否存在
                query = "select * from borrow where bno = '%s' and cno = '%s' ;" % (bno, cno)
                print(query)
                cursor.execute(query)
                tmp = cursor.fetchall()
                if len(tmp) == 0:
                    print(tmp)
                    print('你并不需要归还该书籍！')
                    raise Exception

                # 还书，库存加一，更新总藏书数，borrow记录减少一条
                query1 = "update book set stock = stock + 1 where bno = '%s';" % bno
                # query2 = "set @total_num = (select sum(stock) from book);"
                # query3 = "update book set total = @total_num;"
                query4 = "delete from borrow where (cno, bno) = ('%s','%s');" % (cno, bno)  # 该语句会自动检测cno是否存在
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
                QMessageBox.information(self, '还书成功', '您已成功归还该书籍！', QMessageBox.Ok)

            # 如果有返回数据，说明当前用户确实有尚未消除的借书记录，那就显示出来
            if len(data) > 0:
                print(data)
                self.showTable(cursor, data)
                if flag == 0:  # 如果只是做了查询而没有还书，给出提示
                    QMessageBox.warning(self, '查询成功', '您也许忘了填写书号，因此这里只返回借书证号对应的所有已借书籍，而不会执行还书操作！')
            else:  # 如果没有返回数据，说明该用户目前没有要还的书
                QMessageBox.information(self, '查询成功', '该借书证暂无已借书籍！', QMessageBox.Ok)
                self.showTable(cursor, data)
                # self.bookReturn_layout.removeWidget(self.returnRecord_table)
                # sip.delete(self.returnRecord_table)
                # # 添加空表
                # self.returnRecord_table = table
                # self.bookReturn_layout.addWidget(self.returnRecord_table, 6, 1, 4, 4)

        cursor.close()
        conn.close()

    def showTable(self, cursor, data):
        '''
        显示用户已借书籍
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
            if self.returnRecord_table:
                self.bookReturn_layout.removeWidget(self.returnRecord_table)
                sip.delete(self.returnRecord_table)
            # 保存得到的当前记录表
            self.returnRecord_table = table
        else:
            # 如果data不存在，则创建空表
            self.returnRecord_table = QTableWidget()
        # 重新添加该表
        self.bookReturn_layout.addWidget(self.returnRecord_table, 6, 1, 4, 4)

    def paintEvent(self, event):
        '''
        避免多重传值后的功能失效，从而可以继续使用qss设置样式
        '''
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
