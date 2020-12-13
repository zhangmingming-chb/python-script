#-*-coding:utf-8-*-
import re
import sys
import time
import requests

class Bilibli:
    def __init__(self, bvid):
        self.bvid = bvid
        self.url = 'https://www.bilibili.com/video/' + self.bvid
        self.get_description()

    def get_description(self):
        url = "https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp"
        res = requests.get(url.format(self.bvid))
        # p_cid = re.findall('"cid":(\d+),',res.text)[0]
        self.title = re.findall('"part":"(.*?)",',res.text)[0]
        return self.title,self.url

    def bullet_chat(self, cid):
        # url = "https://api.bilibili.com/x/v2/dm/history?type=1&oid={}&date={}"
        url = "https://comment.bilibili.com/{}.xml"
        res = requests.get(url.format(cid))
        res.encoding = res.apparent_encoding
        return res.text

    def get_data(self, bullet_chat_page):
        # print("【标题】%s 【链接】%s"%(self.title,self.url))
        values = re.findall('<d p="(.*?)"',bullet_chat_page)
        content = re.findall('">(.*?)</d>',bullet_chat_page)
        data = []
        for i in range(0,8):
            data.append(list(map(lambda x: x.split(',')[i], values)))
        data.append(content)
        return data

    def get_info(self):
        url = "https://www.bilibili.com/video/{}"
        res = requests.get(url.format(self.bvid))
        # pages = re.findall('"page":(\d+),',res.text)
        # print(res.text)
        titles = re.findall('"page":\d+,"from":"\w+","part":"(.*?)",',res.text)
        cids = re.findall('"cid":(\d+),"page"',res.text)
        return dict(zip(cids,titles))

    def bullet_mode_desc(self, mode_value):
        desc = {1:'滚动弹幕',2:'滚动弹幕',3:'滚动弹幕',4:'底层弹幕',5:'顶层弹幕',6:'逆向弹幕',7:'精准定位弹幕',8:'高级弹幕'}
        return desc[int(mode_value)]

    def font_size_desc(self, font_size):
        desc = {12:'非常小',16:'特小',18:'小',25:'中',36:'大',45:'有点大',50:'很大',64:'特别大',65:'特别特别大',70:'非常大',80:'超级大'}
        return desc.get(int(font_size)) or int(font_size)

    def font_color_desc(self, font_color):
        return hex(int(font_color)).replace("0x","#")

    def get_row(self, data):
        for send_time,bullet_mode,font_size,font_color,timestamp,bullet_type,sender_id,row_id,content in zip(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]):
            yield send_time,self.bullet_mode_desc(bullet_mode),font_size,self.font_color_desc(font_color),time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(timestamp))),bullet_type,sender_id,row_id,content

    def get_processed_data(self):
        items = self.get_info().items()
        pages = len(items)
        page = 1
        all_bullet_chats = []
        for cid,title in items:
            bullet_chats = []
            print("【序号】 {} 【视频】{} 【链接】{}".format(page,title,self.url+"?p="+str(page)))
            bullet_chat_page = self.bullet_chat(cid)
            data = self.get_data(bullet_chat_page)
            for i in self.get_row(data):
                i = list(i)
                i.insert(0, page)
                i.insert(1,title)
                i.insert(2,self.url+"?p="+str(page))
                bullet_chats.append(i)
            all_bullet_chats.append(sorted(bullet_chats, key=lambda x: float(x[3])))
            page += 1
        return all_bullet_chats

try:
    if sys.argv[1]:
        bvid = sys.argv[1]
        b = Bilibli(bvid)  # https://www.bilibili.com/video/BV1xa411A76q
        for i in b.get_processed_data():
            for j in i:
                print(j)
except:
    pass
