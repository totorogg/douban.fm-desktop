#!/usr/bin/python
#coding=utf-8

#datamanage.py

import ConfigParser, os

class CfgManage:
    def __init__(self):
        # config data
        self.volume     = 30
        self.channel    = 0

        # get config data from config file "douban.dat"
        self.fetch()
#        config=ConfigParser.ConfigParser()
#        try:
#            with open("douban.dat","r") as cfgfile:
#                config.readfp(cfgfile)
#                if config.has_section('basic'):
#                    try:
#                        self.volume = config.get('basic', 'valume')
#                    except ConfigParser.NoOptionError:
#                        print "No valume data exist"
#                        pass
#                                
#                    try:
#                        self.channel = config.get('basic', 'channel')
#                    except ConfigParser.NoOptionError:
#                        print "No channel data exist"
#                        pass
#        except IOError:
#            pass
#        self.store()
                    
    def getVolume(self):
        return self.volume

    def getChannel(self):
        return self.channel

    def setVolume(self, v):
        self.volume = v
        self.store()
        
    def setChannel(self, c):
        self.channel = c
        self.store()

    def setCfg(self,c,v):
        self.channel = c
        self.volume = v
        self.store()
        
    def store(self):
        config=ConfigParser.ConfigParser()
        config.add_section('basic')
        config.set('basic', 'valume', self.volume)
        config.set('basic', 'channel', self.channel)
#        print self.volume
#        print self.channel
        with open("douban.dat","w") as cfgfile:        
            config.write(cfgfile)
            
    def fetch(self):
        config=ConfigParser.ConfigParser()
        try:
            with open("douban.dat","r") as cfgfile:
                config.readfp(cfgfile)
                if config.has_section('basic'):
                    try:
                        self.volume = config.get('basic', 'valume')
                    except ConfigParser.NoOptionError:
                        print "No valume data exist"
                    
                    try:
                        self.channel = config.get('basic', 'channel')
                    except ConfigParser.NoOptionError:
                        print "No channel data exist"
                        
        except IOError:
            pass
#        print self.volume
#        print self.channel
        self.store()

if __name__=='__main__':
    cm = CfgManage()
    cm.setVolume(40)
    cm.setChannel(9)
            


