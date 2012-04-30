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
import wx.media
from douban_playlist import DoubanPlayList



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


class PlayBack:
    
    '''
    The State of the player, idle, loading, playing, pause, stop.
    '''
    PLAYER_STATE_IDLE       = 0
    PLAYER_STATE_LOADING    = 1
    PLAYER_STATE_LOADED     = 2
    PLAYER_STATE_PLAYING    = 3
    PLAYER_STATE_PAUSED     = 4
    PLAYER_STATE_STOPPED    = 5
    PLAYER_STATE_SONGEND    = 6
    
    text_state = ("Idle","Loading","Loaded",\
                  "Playing","Pause","Stop",\
                  "SongEnd")
    
    def __init__(self, parent, playlist):
        # create the media ctrl object
        try:
            self.mediaPlayer = wx.media.MediaCtrl(parent, style=wx.SIMPLE_BORDER, szBackend=wx.media.MEDIABACKEND_WMP10)
            #self.mediaPlayer = wx.media.MediaCtrl(parent, style=wx.SIMPLE_BORDER)
            self.mediaPlayer.Bind(wx.media.EVT_MEDIA_FINISHED, self.onSongEnd)
            self.mediaPlayer.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        except NotImplementedError:
            self.Destroy()
            raise
        
        self.state = PlayBack.PLAYER_STATE_IDLE
        self.parent = parent
        self.volume = 50
        self.setVolume()
        self.length = 0
        #self.playlist = playlist
    
    def toState(self,state):
        self.state = state
    
    def getState(self):
        '''
        Get the current state of player.
        return value is
                        [
                            PLAYER_STATE_IDLE       = 0
                            PLAYER_STATE_LOADING    = 1
                            PLAYER_STATE_LOADED     = 2
                            PLAYER_STATE_PLAYING    = 3
                            PLAYER_STATE_PAUSED     = 4
                            PLAYER_STATE_STOPPED    = 5
                            PLAYER_STATE_SONGEND    = 6                            
                        ]
        '''
        return self.state
    
    def getTextState(self, state):
        '''
        Get the current state of player.
        return value is
                        [
                            'IDLE'     TO PLAYER_STATE_IDLE       = 0
                            'LOADING'  TO PLAYER_STATE_LOADING    = 1
                            'LOADED'   TO PLAYER_STATE_LOADED     = 2
                            'PLAYING'  TO PLAYER_STATE_PLAYING    = 3
                            'PAUSED'   TO PLAYER_STATE_PAUSED     = 4
                            'STOPPED'  TO PLAYER_STATE_STOPPED    = 5
                            'SONGED'   TO PLAYER_STATE_SONGEND    = 6
                        ]
        '''
        return PlayBack.text_state[state]
    
    def getVolume(self):
        '''
        Get the current volume.
        return value scale [0,1] type float. 0 stand for mute.
        '''
        return self.volume
    
    def setVolume(self, volume=50):
        '''
        Set the volume.
        set the volume, scale [0,1].
        '''
        self.volume = volume
        self.mediaPlayer.SetVolume(self.volume * 0.01)
    
    # media player contrl, play, pause, stop, ff, fb, volume
    def play(self):
        '''
        Play the current track.
        It work only in state [PLAYER_STATE_PAUSED, PLAYER_STATE_LOADING, PLAYER_STATE_STOPPED]
        '''
#        if (self.state == PlayBack.PLAYER_STATE_LOADED or self.state == PlayBack.PLAYER_STATE_PLAYING or self.state == PlayBack.PLAYER_STATE_PAUSED):
            #if not self.mediaPlayer.Play():
            #    wx.MessageBox("playing error", "ERROR", wx.ICON_ERROR | wx.OK)
            #else:
            #    pass
            
            # always success
#            self.mediaPlayer.Play()
#            self.toState(PlayBack.PLAYER_STATE_PLAYING)
        self.mediaPlayer.Play()
        self.toState(PlayBack.PLAYER_STATE_PLAYING)
        pass

    def pause(self):
        '''
        Pause the current track.
        It works only in state [PLAYER_STATE_PLAYING]
        '''
        if self.state == PlayBack.PLAYER_STATE_PLAYING:
            self.mediaPlayer.Pause()
            self.toState(PlayBack.PLAYER_STATE_PAUSED)
        
    def stop(self):
        '''
        Stop the current track.
        It works only in state [PLAYER_STATE_PLAYING, PLAYER_STATE_PAUSED, PLAYER_STATE_LOADING]
        '''
        self.mediaPlayer.Stop()
        self.toState(PlayBack.PLAYER_STATE_STOPPED)
        
    
    def fastforward(self):
        pass
    
    def fastbackward(self):
        pass
    
    def volume_up(self):
        pass
    
    def volumn_down(self):
        pass
    
    def get_passtime(self):
        '''
        Get the point of the track playing.
        '''
        offset = self.mediaPlayer.Tell()
        return offset
    
    def get_length(self):
        return self.length
    
    def set_passtime(self, offset):
        '''
        Set the point of the track where start to play.
        '''
        self.mediaPlayer.Seek(offset)
        pass
    
    #--------------------------------------------------------------------------#
    #help functions
    def load(self, song):
        """
        Load the song. When loaded, play it.
        """
        if not self.mediaPlayer.LoadURI(song):
            wx.MessageBox("Error in Loading [%s]" % song,
                          "ERROR",
                          wx.ICON_ERROR | wx.OK)
        
        self.toState(PlayBack.PLAYER_STATE_LOADING)
    
    def OnMediaLoaded(self, event):
        print "Loading ----> Loaded"
        self.toState(PlayBack.PLAYER_STATE_LOADED)
        self.mediaPlayer.SetInitialSize()
        # to be done [tag need modify]
        self.length = self.mediaPlayer.Length()
        self.parent.mainwin_seeking.SetRange(0, self.length)
        self.play()
        self.parent.UIUpdate()

    def onSongEnd(self, event):
        print "song end"
        self.toState(PlayBack.PLAYER_STATE_SONGEND)
        #play next song
        #self.loadNextAudio()

    
    def update(self, audioplayer):
        i = audioplayer.mc.GetDownloadProgress()
        j = audioplayer.mc.GetState()
        k = audioplayer.mc.GetDownloadTotal()
        print "STATE:MEDIASTATE_STOPPED:%d MEDIASTATE_PAUSED:%d MEDIASTATE_PLAYING:%d" %(wx.media.MEDIASTATE_STOPPED, wx.media.MEDIASTATE_PAUSED, wx.media.MEDIASTATE_PLAYING)
        print "GetDownloadProgress:%d GetDownloadTotal:%d GetState:%d"  %(i, k, j)
    
#------------------------------------------------------------------------------#

