import pymysql

# 创建数据库的连接
conn = pymysql.connect(
    host='192.168.4.10',
    port=3306,
    user='root',
    password='111111',
    db='nsd1909',
    charset='utf8'
)

# 创建游标
cur = conn.cursor()

# 编写sql语句
create_dep = '''create table departments(
dep_id int, dep_name varchar(20), primary key(dep_id))'''

create_emp = '''create table employees(
emp_id int, emp_name varchar(20), birth_date date, email varchar(50),
dep_id int, primary key(emp_id), 
foreign key(dep_id) references departments(dep_id)
)'''
create_sal = '''create table salary(
id int, date date, emp_id int, basic int, awards int, 
primary key(id), foreign key(emp_id) references employees(emp_id)
)'''

# 执行sql语句
cur.execute(create_dep)
cur.execute(create_emp)
cur.execute(create_sal)

# 对数据库有改动,需要确认
conn.commit()

# 关闭游标,关闭连接
cur.close()
conn.close()