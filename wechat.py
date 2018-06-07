
import itchat

import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import re
import io
from os import path

import jieba
import os
import numpy as np
#import image
import random
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
from multiprocessing import Pool

class wechat_friends:

    def parse_friends(self):
        itchat.login()      #登录微信
        text = dict()       #创建字典
        friends = itchat.get_friends(update=True)[0:]
        print(friends)

        male = 'male'
        female = 'female'
        other = 'other'
        siglist = []

        for i in friends[1:]:
            sex = i['Sex']
            if sex == 1:
                text[male] = text.get(male,0) + 1
            elif sex == 2:
                text[female] = text.get(female,0) + 1
            else:
                text[other] = text.get(other,0) + 1
            signature = i['Signature'].strip().replace("span","").replace("class","").replace("emoji","")
            rep = re.compile("1f\d+\w*|[<>/=]")
            signature = rep.sub("",signature)
            siglist.append(signature)
        txt = "".join(siglist)
        with io.open('text.txt','a',encoding='utf-8') as f:
            wordlist = jieba.cut(txt,cut_all=True)
            word_space_split = " ".join(wordlist)
            f.write(word_space_split)
            f.close()

        total = len(friends[1:])

        print("男性好友： %.2f%%" % (float(text[male]) / total *100) + " "
              + "女性好友： %.2f%%" % (float(text[female]) / total * 100) + " "
              + "不明性别好友： %.2f%%" % (float(text[other]) / total * 100))

        self.draw(text)
        #self.draw_signature()


    def draw(self,datas):
        for key in datas.keys():
            plt.bar(key,datas[key])

        plt.legend()
        plt.xlabel('sex')
        plt.ylabel('rate')
        plt.title("Gender of Alfred's friends")
        plt.show()

    def draw_signature(self):
        txt = open(u'text.txt',encoding='utf-8').read()
        coloring = np.array(Image.open('3.png'))
        my_wordcloud = WordCloud(background_color="white",max_words=2000,mask=coloring,max_font_size=80,random_state=42,scale=5,font_path="DroidSansFallbackFull.ttf").generate(txt)
        image_colors = ImageColorGenerator(coloring)
        plt.imshow(my_wordcloud.recolor(color_func=image_colors))
        plt.imshow(my_wordcloud)
        plt.axis("off")
        plt.show()
if __name__ == '__main__':
    wechat = wechat_friends()
    pool = Pool(2)
    pool.apply_async(func=wechat.parse_friends,args=())
    pool.apply_async(func=wechat.draw_signature,args=())
    pool.close()
    pool.join()
#wechat.parse_friends()
#wechat.draw_signature()