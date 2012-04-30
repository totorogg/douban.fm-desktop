#!/usr/bin/python
#coding=utf-8

#douban.py

"""
class for douban request
"""

import random
import urllib
import urllib2
import json
import wx

class DoubanProtocol:
    """
    request douban data
    """
    baseURL = "http://douban.fm/j/mine/playlist"
    
    def __init__(self):
        pass
    
    def getChannelList(self):
        return {1: u"华语", 2: u"欧美", 4: u"八零", 61: u"新歌", 9: u"轻音乐", 6: u"粤语", 32: u"NESCAPE咖啡", 
                5: u"九零", 8: u"民谣", 27: u"古典", 16: u"R&B", 20: u"女声", 
                17: u"日语", 18: u"韩语", 13: u"爵士", 10: u"电影原声", 22: u"法语", 
                3: u"七零", 28: u"动漫", 7: u"摇滚", 15: u"说唱", 26: u"豆瓣音乐人", 14: u"电子", 
                #
                168: u"CrossPolo跨界", 170: u"愤怒的小鸟太空", 173: u"海尔灵感DJ", 174: u"包豪斯之旅"}
    
    def login(self, username, passwd):
        pass
    
    def getNewPlayList(self, channel):
        params = urllib.urlencode({"type": "n", "channel": channel, "from": "radio", "r": random.random()})
        url = DoubanProtocol.baseURL + "?%s" % params
        req = urllib2.urlopen(urllib2.Request(url))
        
        assert req.code == 200
        
        obj = json.load(req)
        if obj['r'] != 0:
            wx.MessageBox("Get New PlayList Error", "ERROR", wx.ICON_ERROR | wx.OK)
        #print obj
        # for test
        #for s in obj['song']:
        #    print s['url']
        
        req.close()
        return obj['song']
    
    def gettest(self):
        f = urllib2.urlopen('http://www.douban.com')
        data = f.read()
        print f.geturl()
        #print f.info()
        print f.code
        #print data
        f.close()
    
    def posttest(self):
        params = urllib.urlencode({"username": "abc", "password": "123"})
        f = urllib2.urlopen('http://coolsite.example.com/login/', params)
        data = f.read()
        print f.geturl()
        #print f.info()
        print f.code
        #print data
        f.close()

if __name__ == "__main__":
    #for test
    douban = DoubanProtocol()
    douban.getNewPlayList(2)
