#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 06:34:34 2020

@author: davabrams
"""

# tile game problem
# given an NxM (2x3 in this case) board with tiles numbered 1-5 and one empty space
# what are the minimum number of moves required to reset to the final state:
#  tile name                   index in list
# -------------                -------------
# | 1 | 2 | 3 |                | 0 | 1 | 2 |
# -------------        -->     -------------
# | 4 | 5 |   |                | 3 | 4 | 5 | 
# -------------                -------------
#


# main entry point
userState = [4,3,1,5,2,0] #this is the user-provided state of the tile game

#pick whether you want the algorithm to run locally or on server
#  IF You want it to run on the server, first start 'gameServer.py'
runLocal = False

#pick whether you want verbose or brief outputs
verbose = True

if (True == runLocal):
	from tileGameAlgo import localTest
	localTest(userState, verbose)
else:
	from tileGameAlgo import remoteTest
	from tileGameServerSettings import PORT, ip
	remoteTest(userState, verbose, ip, PORT)