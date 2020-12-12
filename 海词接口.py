#-*-coding:utf-8-*-
import requests
from lxml import etree
import re
class HaiCi(object):
    def __init__(self, word):
        self.word = word
        self.res = requests.get("https://dict.cn/search?q={}".format(word))
        self.html = etree.HTML(self.res.text)
    def _exclude_word(self, phrase_meaning):
        words = "abcdefghijklmnopqrstuvwxyz"
        back_item = list()
        for p in phrase_meaning:
            if p not in words:
                back_item.append(p)
        back_item = "".join(back_item).replace(' ','').replace('()','').replace('〔〕','').replace(';','').replace("'",'')
        back_item = list(map(lambda x:x.split(';')[0] if x[-1] == ';' else x,back_item))
        back_item = list(map(lambda x:x.split(',')[0] if x[-1] == ',' else x,back_item))
        back_item = "".join(back_item)
        return back_item
    def _exclude_other(self, w_type_name):
        words = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in w_type_name:
            if i in words:
                return False
        return True

    # 单词音标
    def word_symbol(self):
        symbol_en = self.html.xpath('//div[@class="phonetic"]/span[1]/bdo/text()')[0][1:-1]
        symbol_us = self.html.xpath('//div[@class="phonetic"]/span[2]/bdo/text()')[0][1:-1]
        return symbol_en,symbol_us
    # 单词发音
    def word_voice(self, sender="man"):
        if sender == "man":
            voice_param = self.html.xpath('//i[@class="sound"]/@naudio')
            voice_en = "http://audio.dict.cn/" + voice_param[0]
            voice_us = "http://audio.dict.cn/" + voice_param[1]
            return voice_en, voice_us
        elif sender == "woman":
            voice_param = self.html.xpath('//i[@class="sound fsound"]/@naudio')
            voice_en = "http://audio.dict.cn/" + voice_param[0]
            voice_us = "http://audio.dict.cn/" + voice_param[1]
            return voice_en,voice_us
    # 单词解释
    def word_meaning(self):
        res = requests.get("https://dict.cn/search?q={}".format(self.word))
        html = etree.HTML(res.text)
        w_type = html.xpath('//div[@class="basic clearfix"]/ul[@class="dict-basic-ul"]/li/span/text()')
        w_meaning = html.xpath('//div[@class="basic clearfix"]/ul[@class="dict-basic-ul"]/li/strong/text()')
        explain_data = dict(zip(w_type,w_meaning))
        return explain_data
    # 单词形态
    def word_form(self):
        form_name = self.html.xpath('//div[@class="shape"]/label/text()')
        form_name = list(map(lambda x:x.split(':')[0],form_name))
        form = self.html.xpath('//div[@class="shape"]/a/text()')
        form = list(map(lambda x:x.replace('\n','').replace('\t',''),form))
        return dict(zip(form_name,form))

    # 释义-详尽释义
    def paraphrase_detail(self):
        w_type = self.html.xpath('//div[@class="layout detail"]/span/text()')
        w_type = list(map(lambda x:x.replace('\n','').replace('\t',''),w_type))
        w_type = list(filter(lambda x:x != '',w_type))
        w_meaning = list()
        for i in range(1,len(w_type)+1):
            w_meaning.append(self.html.xpath(f'//div[@class="layout detail"]/ol[{i}]/li/text()'))
        return dict(zip(w_type,w_meaning))
    # 释义-双解释义
    def paraphrase_ch_en(self):
        w_type = self.html.xpath('//div[@class="layout dual"]/span/text()')
        w_type = list(map(lambda x:x.replace('\n','').replace('\t',''),w_type))
        w_type = list(filter(lambda x:x != '',w_type))
        en_meaning = list()
        ch_meaning = list()
        for i in range(1,len(w_type)+1):
            ch_meaning.append(self.html.xpath(f'//div[@class="layout dual"]/ol[{i}]/li/strong/text()'))
        for i in range(1, len(w_type) + 1):
            en_meaning.append(list(map(lambda x:x.lstrip(),self.html.xpath(f'//div[@class="layout dual"]/ol[{i}]/li/text()'))))
        return dict(zip(w_type,ch_meaning)),dict(zip(w_type,en_meaning))
    # 释义-英英释义
    def paraphrase_en_en(self):
        w_type = self.html.xpath('//div[@class="layout en"]/span/text()')
        w_meaning = list()
        for i in range(1,len(w_type)+1):
            sentence = self.html.xpath(f'//div[@class="layout en"]/ol[{i}]/li/text()')
            sentence = list(map(lambda x:x.replace('\n','').replace('\t','').replace(';',''),sentence))
            sentence = list(filter(lambda x:x != '',sentence))
            w_meaning.append(sentence)
        return dict(zip(w_type,w_meaning))
    # 用例-例句
    def exmple_sentence(self):
        w_type = self.html.xpath('//div[@class="layout sort"]/div/b/text()')
        w_type = list(map(lambda x:x.replace('\t','').replace('\n',''),w_type))
        s_sentence_explain = []
        all_data = []
        for i in range(1,len(w_type)+1):
            data = self.html.xpath(f'//div[@class="layout sort"]/ol[{i}]/li/text()')
            sentence = [data[i] for i in range(len(data)) if i%2==0]
            sentence_explain = [data[i] for i in range(len(data)) if i%2!=0]
            for j,k in zip(sentence,sentence_explain):
                s_sentence_explain.append([j,k])
            all_data.append(s_sentence_explain)
        return dict(zip(w_type,all_data))
    # 用例-常见句型
    def practical_expression(self):
        w_type = self.html.xpath('//div[@class="layout patt"]/b/text()')
        w_type = list(filter(lambda x:self._exclude_other(x),w_type))
        s_sentence_explain = []
        all_data = []
        for i in range(1,len(w_type)+1):
            data = self.html.xpath(f'//div[@class="layout patt"]/ol[{i}]/li/text()')
            sentence = [data[i] for i in range(len(data)) if i%2==0]
            sentence_explain = [data[i] for i in range(len(data)) if i%2!=0]
            for j, k in zip(sentence, sentence_explain):
                s_sentence_explain.append([j, k])
            all_data.append(s_sentence_explain)
        return dict(zip(w_type, all_data))
    # 用例-常用短语
    def useful_expression(self):
        phrase = self.html.xpath('//div[@class="layout phrase"]/dl/dt/b/text()')
        phrase_meaning = self.html.xpath('//div[@class="layout phrase"]/dl/dd/ol/text()')
        phrase_meaning = list(map(lambda x: x.replace('\t','').replace('\n',''),phrase_meaning))
        phrase_meaning = list(filter(lambda x: x != '',phrase_meaning))
        phrase_meaning = list(map(self._exclude_word,phrase_meaning))
        phrase = list(filter(lambda x: self.word in x,phrase))
        phrase = list(map(lambda x: x.split('(')[0] if '(' and ')' in x else x,phrase))
        phrase_data = dict(zip(phrase,phrase_meaning))
        return phrase_data
    # 用例-词汇搭配
    def lexical_collocation(self):
        use_way = self.html.xpath('//div[@class="layout coll"]/b/text()')
        phrases = list()
        for i in range(1,len(use_way)+1):
            phrase_explain = self.html.xpath(f'//div[@class="layout coll"]/ul[{i}]/li/text()')
            phrase_explain = list(map(lambda x:x.replace('\n','').replace('\t',''),phrase_explain))
            phrase_explain = list(filter(lambda x:x != '',phrase_explain))
            phrase = self.html.xpath(f'//div[@class="layout coll"]/ul[{i}]/li/a/text()')
            phrase = list(map(lambda x:x.replace('\n','').replace('\t',''),phrase))
            phrase = list(filter(lambda x:x != '',phrase))
            phrases.append(dict(zip(phrase,phrase_explain)))
        return phrases
    # 用例-经典引文
    def classical_quote(self):
        quote = self.html.xpath('//div[@class="layout auth"]/ul/li/p/text()')
        quote_from = self.html.xpath('//div[@class="layout auth"]/ul/li/b/text()')
        quote_from = list(map(lambda x:x.replace('\t','').replace('\n',''),quote_from))
        quote_from = list(map(lambda x:x.split('：')[-1],quote_from))
        return dict(zip(quote,quote_from))

    # 讲解-词语用法
    def word_use(self):
        w_type = self.html.xpath('//div[@class="layout ess"]/span/text()')
        w_type = list(map(lambda x:x.replace('\n','').replace('\t',''),w_type))
        w_type = list(filter(lambda x:x != '',w_type))
        all_use_info = list()
        for i in range(1,len(w_type)+1):
            use_info = self.html.xpath(f'//div[@class="layout ess"]/ol[{i}]/li/text()')
            use_info = list(map(lambda x: x.replace('\n', '').replace('\t', ''), use_info))
            use_info = list(filter(lambda x: x != '', use_info))
            use_info = list(map(lambda x: x[1:] if x[0] == "的" else x, use_info))
            all_use_info.append(use_info)
        return dict(zip(w_type,all_use_info))
    # 讲解-词源解说
    def word_from(self):
        info = self.html.xpath('//div[@class="layout etm"]/ul/li/text()')[0]
        return info.split('☆ ')[-1]
    # 讲解-词义辨析
    def word_judge(self):
        all_data = list()
        all_sum = self.html.xpath('//div[@class="layout discrim"]/dl/dt/b/text()')
        for i in range(1,len(all_sum)+1):
            phrase = self.html.xpath(f'//div[@class="layout discrim"]/dl[{i}]/dt/b/text()')[0]
            judgement = self.html.xpath(f'//div[@class="layout discrim"]/dl[{i}]/dd/li/text()')
            data = {'phrase':phrase,'judgement':judgement}
            all_data.append(data)
        return all_data
    # 讲解-常见错误
    def word_mistake(self):
        w_type = self.html.xpath('//div[@class="layout comn"]/span/text()')
        w_type = list(map(lambda x:x.replace('\n','').replace('\t',''),w_type))
        w_type = list(filter(lambda x:x != '',w_type))
        all_data = list()
        for i in range(1,len(w_type)+1):
            sentence = self.html.xpath(f'//div[@class="layout comn"]/ol[{i}]/text()')
            sentence = list(map(lambda x: x.replace('\n', '').replace('\t', ''),sentence))
            sentence = list(filter(lambda x: x != '', sentence))
            for s in sentence:
                sentence_fault = re.findall(f"{s}.*?<b>误</b>(.*?)</p>",self.res.text, re.S)[0].strip()
                sentence_right = re.findall(f"{s}.*?<b>正</b>(.*?)</p>", self.res.text, re.S)[0].strip()
                sentence_judge = re.findall(f"{s}.*?<b>析</b>(.*?)</p>", self.res.text, re.S)[0].strip()
                data = {s:{'误':sentence_fault,'正':sentence_right,'析':sentence_judge}}
                all_data.append(dict(zip(w_type[i-1], [data])))
            return all_data

    # 相关-近反义词
    def nearly_opposite(self):
        nearly_words = self.html.xpath('//div[@class="layout nfo"]/ul[1]/li/a/text()')
        nearly_words = list(map(lambda x:x.replace('\t','').replace('\n',''),nearly_words))
        opposite_words = self.html.xpath('//div[@class="layout nfo"]/ul[2]/li/a/text()')
        opposite_words = list(map(lambda x:x.replace('\t','').replace('\n',''),opposite_words))
        return nearly_words,opposite_words
    # 相关-临近单词
    def closely_word(self):
        words = self.html.xpath('//div[@class="layout nwd"]/a/text()')
        words = list(map(lambda x:x.replace('\t','').replace('\n',''),words))
        return words


h = HaiCi('make')
print(h.word_judge())