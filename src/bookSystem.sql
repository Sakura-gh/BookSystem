drop database bookSystem;
create database if not exists bookSystem;
use bookSystem;
create table if not exists book(			 #书
	bno			char(25),    	#书号
	category	varchar(25), 	#类别
	title		varchar(25), 	#书名
	press		varchar(25), 	#出版社
	_year		int,		 	#年份
	author		varchar(25), 	#作者
	price		decimal(7,2),	#价格
	stock		int, 			#库存
	total		int, 			#总藏书量
	primary key(bno)
);

create table if not exists card(			 #借书证
	cno			char(25),	 #卡号
    name		varchar(25) not null, #姓名
    department	varchar(40) not null, #单位
    type		char(1) not null,	 #类别(教师/学生)
    primary key(cno),
    check(type in('T','S'))
);
create table if not exists borrow(		 #借书记录 
	cno			char(25),	 #卡号
    bno			char(25),	 #书号
    borrow_date	int,		 #借书日期
    return_date	int, 		 #还书日期
    primary key(cno,bno),
    foreign key(cno) references card(cno),
    foreign key(bno) references book(bno)
);



