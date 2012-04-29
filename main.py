#!/usr/bin/python
# coding=utf-8

#----------------------------------------------------------------------
# main.py
#
# 2012-04-10  Erik Guo
#
# app main
#----------------------------------------------------------------------

import wx

from mainwin import MainWin

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Python Music Radio")
        self.SetSize((500,160))
        # player
        #self.player = AudioPlayer(self)
        # playlist
        self.playlist = None
        # player ui
        self.mainwin = MainWin(self)
        #panel = MainPlayerPanel(self)


class MusicRadioApp(wx.App):
    """
    Music Radio Player Application Class
    """
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        
    def OnInit(self):
        # the main play frame
        self.mainFrame = MainFrame()
        self.mainFrame.Center()
        self.mainFrame.Show()
        self.SetTopWindow(self.mainFrame)

        return True


def main():
    app = MusicRadioApp()
    app.MainLoop()


if __name__ == "__main__":
    main()
