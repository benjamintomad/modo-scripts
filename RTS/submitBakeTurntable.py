#python

import os
from pyModo import pyModo as pym


currentScene = pym.Scene_Current_Index_Get()
Scene = pym.Scene_FilePath(currentScene)[0]

os.system("W:\WG\WG_IT\__Jej\Super-Tool-Modo\_Testing_Baker.cmd %s" % Scene)