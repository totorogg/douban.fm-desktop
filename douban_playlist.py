#!/usr/local/bin
# coding=utf-8

#douban_playlist.py

"""
class for playlist model
"""

import urllib
import urllib2
import json

from douban import DoubanProtocol

class DoubanPlayList:
    def __init__(self, channel = 61):
        self.channel = channel
        self.length = 0
        self.currentSong = 0
        # protocol to get the list
        self.douban = DoubanProtocol()
        self.playlist = self.nextPlayList()
        #pass
    
    def nextPlayList(self):
        playlist = self.douban.getNewPlayList(self.channel)
        self.length = len(playlist)
        self.currentSong = 0
        
        return playlist
    #
    def nextSong(self):
        if self.currentSong >= self.length:
            self.playlist = self.nextPlayList()
        song = self.playlist[self.currentSong]
        self.currentSong += 1
        return song
        
    def previousSong(self):
        # not allowed now
        pass
        
    def changeChannel(self, channel):
        self.channel = channel
        self.playlist = self.nextPlayList()
    
"""
class for the song
"""
class Song:
    """
    picture:
    albumtitle
    company
    rating_avg
    public_time
    ssid
    album
    like
    artist
    url
    title
    subtype
    length
    sid
    aid
    """
    def __init__(self):
        pass
        
    def getURL(self):
        pass



