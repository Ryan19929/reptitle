import selenium
from bs4 import BeautifulSoup
import requests
import re
import bs4
import urllib
from urllib.parse import unquote
import string
from urllib.parse import quote
from lxml import etree
from selenium import webdriver
import time
import types
import codecs
from pachong import Mysql



def findName(item,na1):
    name=''
    for (tag,tag1) in zip(item.children,na1):
        if not isinstance(tag, bs4.element.Tag):
            name=name+tag
            if isinstance(tag1, bs4.element.Tag):
                name = name+str(tag1)[29:].replace("</font>", "")
    return name
"""
findName（item，na1）用来爬取商品名称
例子如下  
<a class="shenqingGY" href="http://www.manmanbuy.com/redirectUrl.aspx?webid=1&amp;tourl=http://item.jd.com/100001860767.html" target="_blank">
 Apple 
 <font class="spnamehighword">iPhone</font> 
 <font class="spnamehighword">XS</font> 
 Max (A2103) 256GB 金色 全网通（移动4G优先版） 双卡双待
</a>
该for循环其中zip（）里的只要有一个到尾端就会停止循环
目前未掌握如何在一个变量到尾端的时候另一个变量继续循环
而且该网站名字格式不一，获取正确的全名目前有些难度
"""
def main():
    r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-/:;<=>?@，.。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'#正则表达式 用来保留数字内容

    goods=input("输入要对比的商品（英文）")

    url0="http://s.manmanbuy.com/default.aspx?key="+goods.replace(" ","+")
    """
    此爬虫是通过爬取 慢慢买 这个比价网页来获取数据 
    但组合url的时候，直接使用中文组合会输先乱码，结果不一致，url里中文的部分应该是gb2312转urlcode
    但每次都失败 无法解决目前
    """
    """
    使用无头浏览器进行加载动态数据
    使用前要安装chrome.drive
    """
    conn = Mysql.connection_sql("test1", host='127.0.0.1', user='root', passwd='1234', port=3306, charset='utf8')
    opt = webdriver.ChromeOptions()
    opt.headless = True
    browser = webdriver.Chrome(options=opt)
    browser.set_page_load_timeout(60)
    time.sleep(3)
    browser.get(url0)
    """
    browser = webdriver.Chrome()
    browser.set_page_load_timeout(60)
    time.sleep(3)
    browser.get(url0)
    这是在未掌握无头浏览器前使用的代码
    """
    soup=BeautifulSoup(browser.page_source)
    Is=soup.find_all('div',class_="p AreaPrice")
    Ia=soup.find_all('p',class_="m")
    In=soup.find_all('div',class_="t")
    with open("../source/result.txt", 'w',encoding="utf-8") as fp:
        for (I,A,N) in zip(Is,Ia,In):
            na1 = N.find_all('font')
            na=findName(N.a,na1)
            s0=N.find_all('a',target="_blank")
            s=I.find_all('span',class_="listpricespan")
            s1=A.find_all('span',class_="shenqingGY")
            new_s=filter(str.isdigit, str(s)[29:34])
            new_s1=str(s1)
            #new_href=str(s0)[29:90]
            """
            在对于天猫的商品链接
            有点难度，未实现，但其他电商均实现
            """

            print("*********************************************************")
            """
            print(na)#名称
            print(re.sub(r1,'',new_s1).lstrip())#电商名称
            print(''.join(list(new_s)))#价格
            #print("购买链接:"+new_href)#购买链接
            """
            fp.write(u"商品名称" + ": " + na)
            fp.write("\n")
            fp.write("电商名称" + ": " +re.sub(r1,'',new_s1).lstrip())
            fp.write("\n")
            fp.write("价格" + ": " + ''.join(list(new_s)))
            fp.write("\n")
            fp.write("\n")
            print("*********************************************************\n")

main()