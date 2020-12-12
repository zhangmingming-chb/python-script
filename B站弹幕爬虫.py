#-*-coding:utf-8-*-
import re
import time
import requests

class Bilibli:
    def __init__(self, bvid):
        self.bvid = bvid
        self.url = 'https://www.bilibili.com/video/' + self.bvid

    @property
    def cid(self):
        url = "https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp"
        res = requests.get(url.format(self.bvid))
        p_cid = re.findall('"cid":(\d+),',res.text)[0]
        self.title = re.findall('"part":"(.*?)",',res.text)[0]
        return p_cid

    def bullet_chat(self):
        # url = "https://api.bilibili.com/x/v2/dm/history?type=1&oid={}&date={}"
        url = "https://comment.bilibili.com/{}.xml"
        res = requests.get(url.format(self.cid))
        res.encoding = res.apparent_encoding
        return res.text

    def get_data(self, bullet_chat_page):
        print("【标题】%s 【链接】%s"%(self.title,self.url))
        values = re.findall('<d p="(.*?)"',bullet_chat_page)
        content = re.findall('">(.*?)</d>',bullet_chat_page)
        data = []
        for i in range(0,8):
            data.append(list(map(lambda x: x.split(',')[i], values)))
        data.append(content)
        return data

    def get_bullet_mode_desc(self, mode_value):
        desc = {1:'滚动弹幕',2:'滚动弹幕',3:'滚动弹幕',4:'底层弹幕',5:'顶层弹幕',6:'逆向弹幕',7:'精准定位弹幕',8:'高级弹幕'}
        return desc[int(mode_value)]

    def get_font_size_desc(self, font_size):
        desc = {12:'非常小',16:'特小',18:'小',25:'中',36:'大',45:'有点大',50:'很大',64:'特别大',65:'特别特别大',70:'非常大',80:'超级大'}
        return desc.get(int(font_size)) or int(font_size)

    def get_font_color_desc(self, font_color):
        return hex(int(font_color)).replace("0x","#")

    def get_row(self, data):
        for send_time,bullet_mode,font_size,font_color,timestamp,bullet_type,sender_id,row_id,content in zip(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]):
            yield send_time,self.get_bullet_mode_desc(bullet_mode),font_size,self.get_font_color_desc(font_color),time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(timestamp))),bullet_type,sender_id,row_id,content

    def get_processed_data(self):
        bullet_chat_page = self.bullet_chat()
        data = self.get_data(bullet_chat_page)

        bullet_chats = []
        for i in self.get_row(data):
            bullet_chats.append(i)

        return sorted(bullet_chats,key=lambda x:float(x[0]))


b =  Bilibli("BV1xa411A76q") # https://www.bilibili.com/video/BV1xa411A76q

print(b.get_processed_data())



