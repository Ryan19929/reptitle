#!/user/bin/python
# -*- coding: utf-8 -*-
"""
@author: yhj
@time: 2018/10/14 13:19
@desc: 导入数据到数据库
"""

import codecs
from pachong import Mysql


column_map = {u"商品名称": "name", u"电商名称": "com", u"价格": "price"}


def insert_data(conn):
    cursor = conn.cursor()
    fp = codecs.open("../source/result.txt", "r", encoding="utf-8")
    insert_data = dict()
    for line in fp:
        line = line.strip()  # 去掉换行等前后空白符
        if line == "":
            inser_sql = Mysql.add_sql("ddd", **insert_data)
            cursor.execute(inser_sql)
            insert_data.clear()
        else:
            key, value = line.split(":", 1)
            if key == u"商品名称" or key == u"电商名称":
                value = value.split(";")[0]
            insert_data[column_map[key]] = value
    conn.commit()


def insert_expert(conn):
    cursor = conn.cursor()
    cursor.execute("insert into expert (name, unit) select author,unit from paper group by author, unit")
    conn.commit()

    # cursor = conn.cursor()
    # columns = ["author", "unit"]
    # expert_set = set()  # set去除重复的同单位下的同名的人
    # select_sql = mysql_operate.select_sql("paper", *columns)
    # cursor.execute(select_sql)
    # for author, unit in cursor.fetchall():
    #     if author + "\t" + unit not in expert_set:
    #         inser_sql = mysql_operate.add_sql("expert", name=author, unit=unit)
    #         cursor.execute(inser_sql)
    #         expert_set.add(author + "\t" + unit)
    # conn.commit()


def insert_join(conn):
    cursor = conn.cursor()
    cursor.execute("insert into ddd (expert_id, expert_name, paper_id, paper_name) "
                   "select expert_id, expert.name, paper_id, paper.name from paper "
                   "join expert on expert.name = paper.author and expert.unit = paper.unit")
    conn.commit()


if __name__ == '__main__':
    conn = Mysql.connection_sql("test1", host='127.0.0.1', user='root', passwd='1234', port=3306, charset='utf8')
    insert_data(conn)
    #insert_expert(conn)
    #insert_join(conn)
    Mysql.close_sql(conn)
