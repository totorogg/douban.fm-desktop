#!/usr/bin/python
# coding=utf-8

#----------------------------------------------------------------------
# player.py
#
# 2012-04-10  Erik Guo
#
# Media Player ctrl
#----------------------------------------------------------------------

import time
import wx
import threading
import wx.media
from douban_playlist import DoubanPlayList

'''
The State of the player, idle, loading, playing, pause, stop.

'''
PLAYER_STATE_IDLE       = 0
PLAYER_STATE_LOADING    = 1
PLAYER_STATE_PLAYING    = 2
PLAYER_STATE_PAUSED     = 3
PLAYER_STATE_STOPPED    = 4

'''
The State of the player, play, pause, stop, next music, previous music, .
'''
PLAYER_EVENT_PLAY       = 0
PLAYER_EVENT_PAUSE      = 1
PLAYER_EVENT_STOP       = 2
PLAYER_EVENT_NEXT       = 3
PLAYER_EVENT_PREV       = 4
PLAYER_EVENT_VOLMUP     = 5
PLAYER_EVENT_VOLMDN     = 6

class PlayerInfo:
    def __init__(self):
        self.state = PLAYER_STATE_IDLE
        
class PlayerNotifier:
    def update(self, audioplayer):
        i = audioplayer.mc.GetDownloadProgress()
        j = audioplayer.mc.GetState()
        k = audioplayer.mc.GetDownloadTotal()
        print "STATE:MEDIASTATE_STOPPED:%d MEDIASTATE_PAUSED:%d MEDIASTATE_PLAYING:%d" %(wx.media.MEDIASTATE_STOPPED, wx.media.MEDIASTATE_PAUSED, wx.media.MEDIASTATE_PLAYING)
        print "GetDownloadProgress:%d GetDownloadTotal:%d GetState:%d"  %(i, k, j)


#class AudioPlayer(wx.media.MediaCtrl, threading.Thread):
class AudioPlayer(wx.Panel, threading.Thread):
    def __init__(self, parent, notifier):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.state = PLAYER_STATE_IDLE
        self.nt = notifier;
        self.mc = wx.media.MediaCtrl(parent, style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_WMP10)
        try:
            threading.Thread.__init__(self) 
#            wx.media.MediaCtrl.__init__(self, parent=parent, style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_QUICKTIME)
            #bind event, todo
            self.mc.Bind(wx.media.EVT_MEDIA_FINISHED, self.onSongEnd)
        except NotImplementedError:
            self.Destroy()
            raise
        self.mc.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        
    def OnMediaLoaded(self, event):
        print "Loading ----> Loaded"
        self.play()

    def onSongEnd(self, event):
        print "song end"
        self.playNextSong()

    def run(self):
        while True:
            if self.state == PLAYER_STATE_LOADING:
                print "STATE:LOADING"
            elif self.state == PLAYER_STATE_PLAYING:
                print "STATE:PLAYING"
            elif self.state == PLAYER_STATE_PAUSED:
                print "STATE:PAUSED"
            elif self.state == PLAYER_STATE_STOPPED:
                print "STATE:STOPPED"
            else:
                print ""
            self.nt.update(self)
            time.sleep(4)
            
             
    def toState(self,state):    
        self.state = state
    
    
    def load(self, song):
#        song1="F:/tears.mp3"
        if not self.mc.LoadURI(song):
            print "Error in Loading [%s]" % song
        else:
            self.parent.Refresh()
            self.toState(PLAYER_STATE_LOADING)
        
    def loadAndPlay(self, song):
        self.toState(PLAYER_STATE_LOADING)
        
    def play(self):
        self.mc.Play()
        self.toState(PLAYER_STATE_PLAYING)
        
    def pause(self):
        self.mc.Pause()
        self.toState(PLAYER_STATE_PAUSED)
        
    def stop(self):
        self.mc.Stop()
        self.toState(PLAYER_STATE_STOPPED)
        
    
    def fastforward(self):
        pass
    
    def fastbackward(self):
        pass
    
    def volume_up(self):
        pass
    
    def volumn_down(self):
        pass
    
    def get_passtime(self):
        pass
# create the audio player app
class MyApp(wx.App, wx.Frame):
    """
    Audio Player Application Class
    """
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        wx.Frame.__init__(self, None, wx.ID_ANY, "Player", size=(200,150))
        self.Show()
    def OnInit(self):
       
        return True

def main():
    app = MyApp()
    doubanPlayList = DoubanPlayList()
    pn = PlayerNotifier()
    ap = AudioPlayer(app, pn)
    ap.start()
    app.SetTopWindow(app)
    song = doubanPlayList.nextSong()
    print song['url']
    ap.load(song['url'])
    app.MainLoop()
    while True:
        event = raw_input('Load L Play P STOP S PAUSE T ;)')
        if event in [ 'l', 'L' ]:
            song = doubanPlayList.nextSong()
            print song['url']
            ap.load(song['url'])
            
        elif event in [ 'p', 'P' ]:
            ap.play()

        elif event in [ 's', 'S' ]:
            ap.stop()
            
        elif event in [ 't', 'T' ]:
            ap.pause()
            
        else:
            print ""
    


if __name__ == "__main__":
    main()
