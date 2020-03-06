import numpy as np
import itertools
from itertools import compress
import json
import pycurl
from io import BytesIO
import requests

def generateTileList():
    # return a list of uint8 arrays in  order
    # these are all the permutations of tiles possible
    finalState = [1,2,3,4,5,0]
    allStates = [list(pm) for pm in itertools.permutations(finalState)]
    return allStates, finalState

def findStateInArray(state, allStates):
    #finds the index of a state in the list of all states
    idx = [state == testState for testState in allStates]
    #assert np.any(idx) 
    idx = list(compress(range(len(idx)), idx))
    if (len(idx) == 1):
        return idx[0]
    elif (len(idx) == 0):
        return []
    else:
        assert(False)

def swapElem(state, x, y):
    #swaps two elements, x and y, in list 'state'
    newState = state.copy()
    z = state[x]
    newState[x] = state[y]
    newState[y] = z
    return newState

def listPossibleMoves(currentState):
    #given a tile configuration, list all the possible moves a user can make.
    #this is purely a function of where the '0' tile is (the empty spot).
    #there are 2 possible moves when empty spot is at a corner, and 3 when 
    # empty spot is on an edge
    i = currentState.index(0) #find the empty spot
    assert (i < 6)
    if (i == 0):
        return [swapElem(currentState, 0, 1),
                swapElem(currentState, 0, 3)]
    elif (i == 1):
        return [swapElem(currentState, 1, 0),
                swapElem(currentState, 1, 2),
                swapElem(currentState, 1, 4)]
    elif (i == 2):
        return [swapElem(currentState, 2, 1),
                swapElem(currentState, 2, 5)]
    elif (i == 3):
        return [swapElem(currentState, 3, 0),
                swapElem(currentState, 3, 4)]
    elif (i == 4):
        return [swapElem(currentState, 4, 1),
                swapElem(currentState, 4, 3),
                swapElem(currentState, 4, 5)]
    elif (i == 5):
        return [swapElem(currentState, 5, 2),
                swapElem(currentState, 5, 4)]
    else:
        assert(False)

def populateTileList(allStates, finalState):

    #pre-define distance vector with -1's (assume nothing has a path to end yet)
    distList = [-1] * len(allStates)
    distList[0] = 0 #of course, the final state has path length 0

    #pre-define pointer vector with -1's (assume nothing has a path to end yet)
    pntrList = [-1] * len(allStates)
    pntrList[0] = 0

    #this is the list of nodes to investigate.  when this is empty, the graph is closed
    edgeNodes = [finalState]

    #use bfs starting at the end state and generate the full graph
    while len(edgeNodes) > 0:
        edgeNode = edgeNodes[0] #bfs
        edgeIdx = findStateInArray(edgeNode, allStates)
        adjNodes = listPossibleMoves(edgeNode)
        for j in range(len(adjNodes)):
            adjIdx = findStateInArray(adjNodes[j], allStates)
            if (pntrList[adjIdx] == -1): #a new move, cool!
                distList[adjIdx] = distList[edgeIdx] + 1
                pntrList[adjIdx] = edgeIdx
                if not findStateInArray(adjNodes[j], edgeNodes):
                    edgeNodes.append(adjNodes[j]) #if not already on our hit list, add it
            if (distList[adjIdx] > distList[edgeIdx] + 1): #if we find a "faster way" to the end
                distList[adjIdx] = distList[edgeIdx] + 1
                pntrList[adjIdx] = edgeIdx
        edgeNodes.remove(edgeNode)


    # checksum that we get the right # of states
    validStates = 0
    for i in range(len(allStates)):
        if not (distList[i] == -1):
            validStates += 1
    assert(validStates == (len(allStates)/2))
    return distList, pntrList

def localTest(userState, verbose):
    # %% this is where you test your answers locally!

    #generate all the permutations
    allStates, finalState = generateTileList()
    distList, pntrList = populateTileList(allStates, finalState)
    userState_idx = findStateInArray(userState, allStates)

    if not (distList[userState_idx] == -1):
        if (True == verbose):
            print('user state  ' + str(userState) + ' solved in ' + str(distList[userState_idx]) + ' moves! :')
            tmpState = userState
            while not (tmpState == finalState):
                idx_tmp = findStateInArray(tmpState, allStates)
                idx_new = pntrList[idx_tmp]
                tmpState = allStates[idx_new]
                print('next move : ' + str(tmpState))
        else:
            print(str(distList[userState_idx]))
    else:
        print('user state ' + str(userState) + ' can not be solved!')

def solvePuzzleSimple(userState):
    # THIS is just a simple solver, returns the # of steps without walking through them all
    #  the client/server solution uses this

    #generate all the permutations
    allStates, finalState = generateTileList()
    distList, pntrList = populateTileList(allStates, finalState)
    userState_idx = findStateInArray(userState, allStates)
    return str(distList[userState_idx])

def solvePuzzleVerbose(userState):
    # THIS is just a simple solver, returns the # of steps without walking through them all
    #  the client/server solution uses this
    output = ''
    #generate all the permutations
    allStates, finalState = generateTileList()
    distList, pntrList = populateTileList(allStates, finalState)
    userState_idx = findStateInArray(userState, allStates)
    if not (distList[userState_idx] == -1): #if the puzzle can be solved
        output = output + 'user state  ' + str(userState) + ' solved in ' + str(distList[userState_idx]) + ' moves! :\n'
        tmpState = userState
        while not (tmpState == finalState):
            idx_tmp = findStateInArray(tmpState, allStates)
            idx_new = pntrList[idx_tmp]
            tmpState = allStates[idx_new]
            output = output + 'next move : ' + str(tmpState) + '\n'
    else:
        output = output + 'can not be solved'

    return output

def remoteTest(userState, verbose, ip, port):
    # %% this is where you test your answers remotely!
    url = 'http://' + ip + ':' + str(port)
    #url = 'http://httpbin.org/post' #use this to loopback your request (for testing)
    myobj = {'puzzle_values': userState, 'verbose': verbose}
    x = requests.post(url, json = myobj)
    print(x.text)
