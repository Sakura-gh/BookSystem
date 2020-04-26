from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QStyleOption, QStyle, QToolButton, QTextEdit, QFileDialog
from PyQt5.QtGui import QPainter
import pymysql


class cardManage(QWidget):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        self.cardManage_layout = QGridLayout()
        self.setLayout(self.cardManage_layout)

        self.returnMain_button = QPushButton('返回主界面')
        self.cardManage_layout.addWidget(self.returnMain_button, 0, 0, 1, 6)

        # 弹簧标签，用于撑开空间
        self.space_label1 = QLabel()
        self.cardManage_layout.addWidget(self.space_label1, 1, 0, 1, 6)
        self.space_label1.setObjectName('cardManage_spaceLabel')

        self.card_number_label = QLabel('借书证号')
        self.cardManage_layout.addWidget(self.card_number_label, 3, 1, 1, 1)
        self.card_number_label.setObjectName('cardManage_label')
        self.card_number = QLineEdit()
        self.cardManage_layout.addWidget(self.card_number, 3, 2, 1, 3)
        self.card_number.setObjectName('cardManage_edit')

        self.name_label = QLabel('姓名')
        self.cardManage_layout.addWidget(self.name_label, 4, 1, 1, 1)
        self.name_label.setObjectName('cardManage_label')
        self.name = QLineEdit()
        self.cardManage_layout.addWidget(self.name, 4, 2, 1, 3)
        self.name.setObjectName('cardManage_edit')

        self.department_label = QLabel('学院')
        self.cardManage_layout.addWidget(self.department_label, 5, 1, 1, 1)
        self.department_label.setObjectName('cardManage_label')
        self.department = QLineEdit()
        self.cardManage_layout.addWidget(self.department, 5, 2, 1, 3)
        self.department.setObjectName('cardManage_edit')

        self.type_label = QLabel('类别')
        self.cardManage_layout.addWidget(self.type_label, 6, 1, 1, 1)
        self.type_label.setObjectName('cardManage_label')
        self.type = QLineEdit('T or S')
        self.cardManage_layout.addWidget(self.type, 6, 2, 1, 3)
        self.type.setObjectName('cardManage_edit')

        self.addCard_button = QPushButton('添加借书证')
        self.cardManage_layout.addWidget(self.addCard_button, 7, 1, 1, 2)
        self.addCard_button.setObjectName('cardManage_button')
        self.addCard_button.clicked.connect(self.addCard)

        self.deleteCard_button = QPushButton('删除借书证')
        self.cardManage_layout.addWidget(self.deleteCard_button, 7, 3, 1, 2)
        self.deleteCard_button.setObjectName('cardManage_button')
        self.deleteCard_button.clicked.connect(self.deleteCard)

        self.updateCard_button = QPushButton('修改借书证')
        self.cardManage_layout.addWidget(self.updateCard_button, 8, 2, 1, 2)
        self.updateCard_button.setObjectName('cardManage_button')
        self.updateCard_button.clicked.connect(self.updateCard)

        # 弹簧标签，用于撑开空间
        self.space_label2 = QLabel()
        self.cardManage_layout.addWidget(self.space_label2, 9, 0, 1, 6)
        self.space_label2.setObjectName('cardManage_spaceLabel')

        self.label = QLabel('借书证管理')
        self.label.setObjectName('cardManage_title')
        self.cardManage_layout.addWidget(self.label, 10, 4, 2, 2)

    def addCard(self):
        '''
        添加借书证
        '''
        cno = self.card_number.text()
        name = self.name.text()
        department = self.department.text()
        _type = self.type.text()

        conn = pymysql.connect(host='47.115.54.28', user='root', db='bookSystem')
        cursor = conn.cursor()
        try:
            query = ''
            if cno != '':
                if _type not in ('T', 'S'):
                    raise Exception
                query = "insert into card values ('%s', '%s', '%s', '%s');" % (cno, name, department, _type)
                print(query)
                cursor.execute(query)
            else:
                raise Exception

        except Exception as e:
            conn.rollback()
            print('事务处理失败', e)

            QMessageBox.critical(self, '添加失败', '请检查您输入的信息！', QMessageBox.Ok)
        else:
            conn.commit()
            print('事务处理成功！')
            QMessageBox.information(self, '添加成功', '成功添加借书证！')

    def deleteCard(self):
        '''
        删除借书证
        '''
        cno = self.card_number.text()

        conn = pymysql.connect(host='47.115.54.28', user='root', db='bookSystem')
        cursor = conn.cursor()
        try:
            query = ''
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

                query = "delete from card where cno = '%s';" % cno
                print(query)
                cursor.execute(query)
            else:
                raise Exception

        except Exception as e:
            conn.rollback()
            print('事务处理失败', e)

            QMessageBox.critical(self, '删除失败', '借书证不存在或者该证还有书没归还！', QMessageBox.Ok)
        else:
            conn.commit()
            print('事务处理成功！')
            QMessageBox.information(self, '删除成功', '成功删除借书证！')

    def updateCard(self):
        '''
        修改借书证
        '''
        cno = self.card_number.text()
        name = self.name.text()
        department = self.department.text()
        _type = self.type.text()

        conn = pymysql.connect(host='47.115.54.28', user='root', db='bookSystem')
        cursor = conn.cursor()
        try:
            query = ''
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

                if _type not in ('T', 'S', ''):
                    raise Exception
                if name != '':
                    query = "update card set name = '%s' where cno = '%s' ;" % (name, cno)
                    print(query)
                    cursor.execute(query)
                if department != '':
                    query = "update card set department = '%s' where cno = '%s' ;" % (department, cno)
                    print(query)
                    cursor.execute(query)
                if _type != '':
                    query = "update card set type = '%s' where cno = '%s' ;" % (_type, cno)
                    print(query)
                    cursor.execute(query)
            else:
                raise Exception

        except Exception as e:
            conn.rollback()
            print('事务处理失败', e)

            QMessageBox.critical(self, '修改失败', '请检查您输入的信息！', QMessageBox.Ok)
        else:
            conn.commit()
            print('事务处理成功！')
            QMessageBox.information(self, '修改成功', '成功修改借书证！')

    def paintEvent(self, event):
        '''
        避免多重传值后的功能失效，从而可以继续使用qss设置样式
        '''
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
