﻿#!/usr/local/bin
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
    def __init__(self, channel = 1):
        self.channel = channel
        self.length = 0
        self.currentSongIndex = 0
        # protocol to get the list
        self.douban = DoubanProtocol()
        self.playlist = self.nextPlayList()
        #pass
    
    def nextPlayList(self):
        playlist = self.douban.getNewPlayList(self.channel)
        self.length = len(playlist)
        self.currentSongIndex = 0
        
        return playlist
    #
    def nextSong(self):
        """
        get next song in the playlist
        if current list is exhaused, auto fetch next playlist
        return a song object
        """
        if self.currentSongIndex >= self.length:
            self.playlist = self.nextPlayList()
        song = self.playlist[self.currentSongIndex]
        self.currentSongIndex += 1
        return song
        
    def currentSong(self):
        #print self.currentSongIndex, self.length
        if self.currentSongIndex == 0:
            return None
        song = self.playlist[self.currentSongIndex-1]
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
        """
        return the URL of the song
        """
        return self['url']



