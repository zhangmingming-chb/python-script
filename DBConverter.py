#-*-coding:utf-8-*-
import sqlite3
import csv

# def select_to_csv(db_name,csv_filename,sql_cmd):
#     con = sqlite3.connect(db_name)
#     cur = con.cursor()
#     data = cur.execute(sql_cmd).fetchall()
#     with open(csv_filename,"w",newline="") as f:
#         writer = csv.writer(f)
#         writer.writerows(data)
#
# def table_to_csv()
#
#
# select_to_csv("data.db","test.csv","select name from user;")
#

class SqliteConverter(object):
    def __init__(self,db_name):
        import sqlite3
        self.db_name = db_name
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()


    def select_to_csv(self,csv_filename,sql_cmd):
        data = self.cur.execute(sql_cmd).fetchall()
        with open(csv_filename,"a",newline="") as f:
            writer = csv.writer(f)
            writer.writerows(data)

    def table_to_csv(self,csv_filename,table_name):
        col_data = self.cur.execute("PRAGMA table_info('{}');".format(table_name)).fetchall()
        cols = list(map(lambda x:x[1],col_data))
        with open(csv_filename,"w",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(cols)
        self.select_to_csv(csv_filename,"select * from {};".format(table_name))

    def finish(self):
        self.cur.close()
        self.con.close()

db = SqliteConverter("data.db")

db.select_to_csv("1.csv","select * from user;")
db.table_to_csv("2.csv","user")
db.finish()
