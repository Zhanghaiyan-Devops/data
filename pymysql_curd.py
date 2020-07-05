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

# 执行sql语句
# 创建部门
# insert1 = 'insert into departments values(%s, %s)'
# hr = [(1, '人事部')]
# deps = [(2,'ops'), (3, 'dev'), (4, 'qa'), (5, 'market'), (6, 'sales')]
#
# cur.executemany(insert1, hr)
# cur.executemany(insert1, deps)
########################################################
# 查询
# select1 = 'select * from departments'
# cur.execute(select1)
# result1 = cur.fetchone()
# print(result1)
# result2 = cur.fetchmany(2)
# print(result2)
# result3 = cur.fetchall()
# print(result3)

##########################################################
# 移动游标
# select1 = 'select * from departments'
# cur.execute(select1)
# cur.scroll(2,mode='absolute')
# result1 = cur.fetchone()
# print(result1)
# cur.scroll(1)
# result2 = cur.fetchone()
# print(result2)
####################################################
# 修改
# update1 = 'update departments set dep_name=%s where dep_name=%s'
# cur.execute(update1, ('人力资源部', '人事部'))
#######################################
# 删除
# delete1 = 'delete from departments where dep_id=%s'
# cur.execute(delete1, (6,))

# 对数据库有改动,需要确认
conn.commit()

# 关闭游标,关闭连接
cur.close()
conn.close()