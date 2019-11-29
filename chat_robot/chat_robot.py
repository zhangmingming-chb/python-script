#-*-encoding:utf8-*-
import sqlite3
import time
import jieba
import random
# con=sqlite3.connect('weibo_words.db')
# cur=con.cursor()
# cur.execute("create table words(Id int PRIMARY KEY ,Words varchar(50))")
# f = open('res','r',encoding='utf-8')
# n = 1
# error=0
# start_time=time.time()
# for i in f:
#     try:
#         words=i.replace(' ','')
#         cur.execute("insert into words VALUES ({},'{}')".format(n,words))
#         print(f"第{n}条数据存入成功！发生错误数: {error}")
#         n+=1
#         if n%1000==0:
#             con.commit()
#     except:
#         error+=1
#         pass
# spend_time=time.time()-start_time
# print('全部{n} 条数据录入完成！','总共耗时:',spend_time)

def robot_chat(word):
    import sqlite3
    import time
    import jieba
    import random
    start_time = time.time()
    con = sqlite3.connect('weibo_words.db')
    cur = con.cursor()
    word_list = jieba._lcut(word)
    solved_words = sorted(word_list, key=lambda x: len(x))
    # print(solved_words)
    if len(solved_words) >= 5:
        solved_words = random.choice(sorted(word_list, key=lambda x: len(x))[-3:-1])
    elif 5>len(solved_words)>=1:
        solved_words =solved_words[-1]
    else:
        solved_words = '没有发现相关话题'
    cur.execute("select Words from words where Words LIKE '%{}%'".format(solved_words))
    data = cur.fetchall()
    con.close()
    end_time = time.time()
    spend_time = end_time - start_time
    print(f"[Spend_time]:{round(spend_time,2)}s [Keyword]:{solved_words}")
    if len(data) == 1:
        robot_words = data[0]
        return robot_words
    elif len(data) > 1:
        robot_words = random.choice(data)[0]
        return robot_words
    else:
        return '小K,听不懂你说的这个{}'.format(word)

a=robot_chat('千百度')
print(a)