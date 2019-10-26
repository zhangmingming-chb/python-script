import sqlite3
import sys
import time
con=sqlite3.connect('省市县区编号.db')
cur=con.cursor()
id_card=sys.argv[1]
# id_card=input()
#地址
user_province=cur.execute("""select Province from id_province where id={}""".format(id_card[0:2])).fetchall()[0][0]
user_municipality=cur.execute("""select  Municipality from id_municipality where id={}""".format(id_card[0:4])).fetchall()[0][0]
user_county=cur.execute("""select  County from id_county where id={}""".format(id_card[0:6])).fetchall()[0][0]

#出生日期
user_birth_year=id_card[6:10]
user_birth_month=id_card[10:12]
user_birth_day=id_card[12:14]

#年龄
user_age=str(time.localtime().tm_year-int(user_birth_year))

#性别
if int(id_card[16])%2==0:
    user_gender='女'
else:
    user_gender='男'

print('===============身份证查询结果===============')
print('[身份证号码]:{}'.format(id_card))
print('[性别]:{}'.format(user_gender))
print('[年龄]:{}岁'.format(user_age))
print('[出生]:{}年{}月{}日'.format(user_birth_year,user_birth_month,user_birth_day))
print('[地址]:{} {} {}'.format(user_province,user_municipality,user_county))