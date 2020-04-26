#### 编译环境和流程说明

- 本次实验的依赖环境：(无需本地配置mysql)

    ~~~python
    python3 3.6.8
    pyqt5   5.14.2
    pymysql 0.9.3
    ~~~

    本次开发代码支持跨平台编译，只需下载上述依赖环境即可

- 编译流程：

    本次工程的文件组织形式如下：

    ~~~python
    bookSystem.py
    	- app.qss
        - bookBorrow.py
        - bookIn.py
        - bookReturn.py
        - bookSearch.py
        - cardManage.py
        - leftNavigation.py
    ~~~

    因此使用vscode或其他代码编辑器，打开src整个工程文件夹，并切换到bookSystem.py文件下，直接运行该文件即可
    
- 使用说明：

    详见实验报告：document.md / document.pdf