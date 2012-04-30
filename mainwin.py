#!/usr/bin/python
# coding=utf-8

#----------------------------------------------------------------------
# mainwin.py
#
# 2012-04-10  Erik Guo
#
# player UI
#----------------------------------------------------------------------

import os
import wx
import time
import wx.media

from douban import DoubanProtocol
from douban_playlist import DoubanPlayList
from playback import PlayBack

class MainWin(wx.Panel):
    """
    the main window for the player
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        
        self.douban = DoubanProtocol()
        self.doubanPlayList = DoubanPlayList()
        self.playback = PlayBack(self, self.doubanPlayList)
        
        self.createAllWidgets()
        self.layoutWidgets()
        self.bindWidgetsEvent()
        self.createMenuBar()
        self.createStatusBar()
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)
    
    def createMenuBar(self):
        """
        Creates a menu
        """
        menubar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        #local play
        open_file_menu_item = fileMenu.Append(wx.NewId(), "&Open", "Open a File")
        #self.frame.Bind(wx.EVT_MENU, self.onBrowse, open_file_menu_item)
        menubar.Append(fileMenu, '&File')

        #play douban audio
        fmMenu = wx.Menu()
        menubar.Append(fmMenu, u'&Douban.fm')
        channelList = self.douban.getChannelList()
        for channel in channelList:
            #print channelList[channel]
            menu_item = fmMenu.Append(channel, channelList[channel], channelList[channel], wx.ITEM_RADIO)
            self.frame.Bind(wx.EVT_MENU, self.onChangeChannel, menu_item)
        
        self.doubanPlayList = DoubanPlayList()
        #self.doubanPlayList.changeChannel(channel)
        #open_douban_menu_item = fileMenu.Append(wx.NewId(), "&douban.fm", "Play douban.fm")
        #self.frame.Bind(wx.EVT_MENU, self.onRequestAudio, open_douban_menu_item)
        
        self.frame.SetMenuBar(menubar)
        pass
    
        #----------------------------------------------------------------------
    def onChangeChannel(self, event):
        """
        change the channel
        """
        #self.channel = event.GetId()
        channel = event.GetId()
        self.doubanPlayList.changeChannel(channel)
        menu_item = self.frame.GetMenuBar().FindItemById(channel)
        self.statusbar.SetStatusText(menu_item.GetLabel(), 0)
    
    
    def onTimer(self, event):
        """
        Keeps the player slider updated
        """
        
        #offset = self.mediaPlayer.Tell()
        #self.playbackSlider.SetValue(offset)
        
        #update status bar
        #self.statusbar.SetStatusText("channel", 0)
    
    def createStatusBar(self):
        self.statusbar = self.frame.CreateStatusBar(number=3)
        self.statusbar.SetStatusText("channel", 0)
        self.statusbar.SetStatusText("song", 1)
        self.statusbar.SetStatusText("status", 2)
        self.statusbar.SetStatusWidths([-1, -3, -1])
        self.statusbar.SetStatusText("Playing", 2)
        pass
    
    
    def createAllWidgets(self):
        # playback
        self.mainwin_rew = wx.Button(self, -1, "|<", size=(36,24))
        self.mainwin_fwd = wx.Button(self, -1, ">|", size=(36,24))
        self.mainwin_eject = wx.Button(self, -1, u"△", size=(36,24))
        self.mainwin_play = wx.Button(self, -1, ">", size=(36,24))
        self.mainwin_pause = wx.Button(self, -1, "||", size=(36,24))
        self.mainwin_stop = wx.Button(self, -1, u"口", size=(36,24))

        self.mainwin_volume = wx.Slider(self, size=(240,24))
        self.mainwin_volume.SetRange(0, 100)
        self.mainwin_volume.SetValue(50)
        
        self.mainwin_seeking = wx.Slider(self, size=(240,24))
        #
        #self.mainwin_singer = wx.StaticText(self, -1, size=(120,24))
        #self.mainwin_album = wx.StaticText(self, -1, size=(120,24))
        self.mainwin_tsong = wx.StaticText(self, -1, "Volume[50 - 100]", size=(120,24))
        self.mainwin_tseeking = wx.StaticText(self, -1, "Position[00:00 - 00:00]", size=(120,24))
        
        pass
    
    def layoutWidgets(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        #infoSizer = wx.BoxSizer(wx.HORIZONTAL)
        volumeSizer = wx.BoxSizer(wx.HORIZONTAL)
        seekingSizer = wx.BoxSizer(wx.HORIZONTAL)
        playbackSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        #mainSizer.Add(infoSizer)
        mainSizer.Add(volumeSizer)
        mainSizer.Add(seekingSizer)
        mainSizer.Add(playbackSizer)
        
        #infoSizer.Add(self.mainwin_singer)
        #infoSizer.Add(self.mainwin_album)
        volumeSizer.Add(self.mainwin_tsong)
        volumeSizer.Add(self.mainwin_volume)
        seekingSizer.Add(self.mainwin_tseeking)
        seekingSizer.Add(self.mainwin_seeking)
        playbackSizer.Add(self.mainwin_rew)
        playbackSizer.Add(self.mainwin_play)
        playbackSizer.Add(self.mainwin_pause)
        playbackSizer.Add(self.mainwin_stop)
        playbackSizer.Add(self.mainwin_fwd)
        playbackSizer.Add(self.mainwin_eject)

        self.SetSizer(mainSizer)
        self.Layout()
    
    def bindWidgetsEvent(self):
        self.mainwin_play.Bind(wx.EVT_BUTTON, self.onPlay)
        self.mainwin_volume.Bind(wx.EVT_SLIDER, self.onSetVolume)
        self.mainwin_seeking.Bind(wx.EVT_SLIDER, self.onSeek)
        #self.mediaPlayer.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        pass
    
    
#------------------------------------------------------------------------------#
    
    def onTimer(self, event):
        state = self.playback.getState()
        #
        if state == PlayBack.PLAYER_STATE_SONGEND:
            self.loadNextSong()
        
        #show the volume
        #show current position
        offset = self.playback.get_passtime()
        length = self.playback.get_length()
        self.mainwin_seeking.SetValue(offset)
        sec_length = int(length / 1000.0)
        sec_offset = int(offset / 1000.0)
        self.mainwin_tseeking.SetLabel("Position[%d:%02d - %d:%02d]" % (sec_offset/60, sec_offset%60, sec_length/60, sec_length%60))
        pass
    
    def onPlay(self, event):
        state = self.playback.getState()
        if state == PlayBack.PLAYER_STATE_IDLE or state == PlayBack.PLAYER_STATE_STOPPED:
            self.loadNextSong()
        else:
            self.playback.play()
        pass
        
    def loadNextSong(self):
        song = self.doubanPlayList.nextSong()
        print song['url']
        self.playback.load(song['url'])
    
    def onSetVolume(self, event):
        """
        Sets the volume of the music player
        """
        currentVolume = self.mainwin_volume.GetValue()
        print "setting volume to: %s" % int(currentVolume)
        self.playback.setVolume(currentVolume)
        self.mainwin_tsong.SetLabel("Volume[%d - %d]" % (currentVolume, 100))
    
    def onSeek(self, event):
        """
        Seeks the media file according to the amount the slider has
        been adjusted.
        """
        offset = self.mainwin_seeking.GetValue()
        self.playback.set_passtime(offset)
        pass
        
