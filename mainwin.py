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

class MainWin(wx.Panel):
    """
    the main window for the player
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        self.frame = parent
        
        self.createAllWidgets()
        self.layoutWidgets()
        self.bindWidgetsEvent()
        
        self.douban = DoubanProtocol()
        # hard coding for test
        # 0 int, 1 play, 2 pause, 3 stop
        self.state = 0


        
        self.createMenuBar()
        self.createPlayerUI()
        self.createStatusBar()
    
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
    
    def createPlayerUI(self):
        self.createSongInfoPanel()
        self.createProgressSlider()
        self.createControlToolbar()
        pass
    
    def createStatusBar(self):
        self.statusbar = self.frame.CreateStatusBar(number=3)
        self.statusbar.SetStatusText("channel", 0)
        self.statusbar.SetStatusText("song", 1)
        self.statusbar.SetStatusText("status", 2)
        self.statusbar.SetStatusWidths([-1, -3, -1])
        self.statusbar.SetStatusText("Playing", 2)
        pass
    
    def createSongInfoPanel(self):
        pass
    
    def createProgressSlider(self):
        #self.playbackSlider = wx.Slider(self, size=wx.DefaultSize)
        #self.Bind(wx.EVT_SLIDER, self.onSeek, self.playbackSlider)
        pass
    
    def createControlToolbar(self):
        pass
    
    
    def createAllWidgets(self):
        # playback
        self.mainwin_rew = wx.Button(self, -1, "|<", size=(36,24))
        self.mainwin_fwd = wx.Button(self, -1, ">|", size=(36,24))
        self.mainwin_eject = wx.Button(self, -1, u"△", size=(36,24))
        self.mainwin_play = wx.Button(self, -1, ">", size=(36,24))
        self.mainwin_pause = wx.Button(self, -1, "||", size=(36,24))
        self.mainwin_stop = wx.Button(self, -1, u"口", size=(36,24))

        self.mainwin_volume = wx.Slider(self, size=(120,24))
        self.mainwin_seeking = wx.Slider(self, size=(240,24))
        #
        self.mainwin_singer = wx.StaticText(self, -1, size=(120,24))
        self.mainwin_album = wx.StaticText(self, -1, size=(120,24))
        self.mainwin_song = wx.StaticText(self, -1, "Volume", size=(120,24))
        # status window
        
        try:
            self.mediaPlayer = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_WMP10)
            #self.Bind(wx.media.EVT_MEDIA_FINISHED, self.onSongEnd, self.mediaPlayer)
        except NotImplementedError:
            self.Destroy()
            raise
        pass
    
    def layoutWidgets(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        infoSizer = wx.BoxSizer(wx.HORIZONTAL)
        volumeSizer = wx.BoxSizer(wx.HORIZONTAL)
        seekingSizer = wx.BoxSizer(wx.HORIZONTAL)
        playbackSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        mainSizer.Add(infoSizer)
        mainSizer.Add(volumeSizer)
        mainSizer.Add(seekingSizer)
        mainSizer.Add(playbackSizer)
        
        #infoSizer.Add(self.mainwin_singer)
        #infoSizer.Add(self.mainwin_album)
        volumeSizer.Add(self.mainwin_song)
        volumeSizer.Add(self.mainwin_volume)
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
        self.mediaPlayer.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        pass
    
    def OnMediaLoaded(self, event):
        print "Loading ----> Loaded"
        self.startPlay()
    
    def startPlay(self):
        i = self.mediaPlayer.GetDownloadProgress()
        j = self.mediaPlayer.GetState()
        k = self.mediaPlayer.GetDownloadTotal()
        print "STATE:MEDIASTATE_STOPPED:%d MEDIASTATE_PAUSED:%d MEDIASTATE_PLAYING:%d" %(wx.media.MEDIASTATE_STOPPED, wx.media.MEDIASTATE_PAUSED, wx.media.MEDIASTATE_PLAYING)
        print "GetDownloadProgress:%d GetDownloadTotal:%d GetState:%d"  %(i, k, j)
#        while self.mediaPlayer.GetState() == -1:
#            time.sleep(1)
        if not self.mediaPlayer.Play():
            print "MC.Play Error"
 #           wx.MessageBox("Unable to Play media : Unsupported format?",
 #                         "ERROR",
 #                         wx.ICON_ERROR | wx.OK)
        else:
            self.mediaPlayer.SetInitialSize()
            self.GetSizer().Layout()
            self.playbackSlider.SetRange(0, self.mediaPlayer.Length())
            
    
    
    def onPlay(self, event):
        """
        Plays the music
        """
        i = self.mediaPlayer.GetDownloadProgress()
        j = self.mediaPlayer.GetState()
        k = self.mediaPlayer.GetDownloadTotal()
        print "STATE:MEDIASTATE_STOPPED:%d MEDIASTATE_PAUSED:%d MEDIASTATE_PLAYING:%d" %(wx.media.MEDIASTATE_STOPPED, wx.media.MEDIASTATE_PAUSED, wx.media.MEDIASTATE_PLAYING)
        print "GetDownloadProgress:%d GetDownloadTotal:%d GetState:%d"  %(i, k, j)

#        if not event.GetIsDown():
#            self.onPause(event)
#            return
        
        # if not load the song, loading
        if (self.state == 0): #init state
            self.state = 1
            self.loadNextAudio()
#        time.sleep(3)    
#        self.startPlay()
#        event.Skip()
        i = self.mediaPlayer.GetDownloadProgress()
        j = self.mediaPlayer.GetState()
        k = self.mediaPlayer.GetDownloadTotal()
        print "STATE:MEDIASTATE_STOPPED:%d MEDIASTATE_PAUSED:%d MEDIASTATE_PLAYING:%d" %(wx.media.MEDIASTATE_STOPPED, wx.media.MEDIASTATE_PAUSED, wx.media.MEDIASTATE_PLAYING)
        print "GetDownloadProgress:%d GetDownloadTotal:%d GetState:%d"  %(i, k, j)

        return True
    
    def loadNextAudio(self):
        """
        """
        
        if self.state == 1: # on playing
            song = self.doubanPlayList.nextSong()
            print song['url']
            if not self.mediaPlayer.LoadURI(song['url']):
                wx.MessageBox("Unable to load %s: Unsupported format?" % song['url'],
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
#            self.mediaPlayer.Play()

