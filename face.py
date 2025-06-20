#!/usr/bin/python3

import os
import os.path
#import pprint
import wx
from wxface.wxmemoface import wxMemoFace

#list_eng = os.environ
#pprint.pprint(dict(list_eng),width=1)
#working_path = os.path.dirname(os.environ["_"])
working_path = os.path.dirname(os.getcwd())

w = wx.App()
mb = wxMemoFace(title="Server Interface")
w.MainLoop()
