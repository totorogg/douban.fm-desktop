#!/usr/bin/python
# coding=utf-8

#----------------------------------------------------------------------
# mainwin.py
#
# 2012-04-10  Erik Guo
#
# player UI
#----------------------------------------------------------------------

import wx

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
        self.douban = DoubanProtocol()
        self.doubanPlayList = DoubanPlayList()

        self.createAllWidgets()
        self.layoutWidgets()
        
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
            menu_item = fmMenu.Append(channel, channelList[channel], channelList[channel])
            #self.frame.Bind(wx.EVT_MENU, self.onChangeChannel, menu_item)
        
        #open_douban_menu_item = fileMenu.Append(wx.NewId(), "&douban.fm", "Play douban.fm")
        #self.frame.Bind(wx.EVT_MENU, self.onRequestAudio, open_douban_menu_item)
        
        self.frame.SetMenuBar(menubar)
        pass
    
    def createPlayerUI(self):
        self.createSongInfoPanel()
        self.createProgressSlider()
        self.createControlToolbar()
        pass
    
    def createStatusBar(self):
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
        self.mainwin_song = wx.StaticText(self, -1, size=(120,24))
        # status window
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
        
        infoSizer.Add(self.mainwin_singer)
        infoSizer.Add(self.mainwin_album)
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

