# minimax.py handles the ai and win detection
# January 4, 2018
__author__ = 'Trevor Nelson'
# alpha-beta pruning adapted from https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
from copy import *
import random

# gets all possible columns a piece could go
def getPossibleMoves(board):
    moves = []
    for c in range(len(board[0])):
        if board[0][c] == 0:
            moves.append(c)
    return moves

# recursively figures out the best place for the computer to move
def performMinimax(board, player, depth, move, pcolor, ocolor, alpha, beta, maximizing):
    opp = 2 if player == 1 else 1
    if move:
        # returns (score, move)
        if isTerminalState(board, ocolor, move):
            return (None, 10 - depth)
        elif isTerminalState(board, pcolor, move):
            return (None, depth - 10)
        elif isFull(board) or depth > 4:
            return (None, 0)
    
    # emergency abort if recursion gets out of hand, should never run
    if len(getPossibleMoves(board)) == 0 or depth > 10:
        print('PROBLEM')
        print(board)
        return

    # go through all moves, running minimax for each, and find the best ones
    best = []
    if maximizing:
      # ai is playing as itself
      o = (None,-1000)
      c = 0
      for col in getPossibleMoves(board):
        tboard = deepcopy(board)
        
        # perform the move
        row = len(tboard) - 1
        while tboard[row][col] != 0:
            row -= 1
        tboard[row][col] = player
        
        # run minimax on that board with opposite player
        result = (col, performMinimax(tboard, opp, depth + 1, (row, col), pcolor, ocolor, alpha, beta, False)[1])
        
        # see if that is better than the current best
        if result[1] > o[1]:
          o = (result[0],result[1])
          best = []
          best.append(o)
        elif result[1] == o[1]:
          # add any moves with the same score as the best to the optimal array
          best.append(result)
        
        # alpha-beta magic
        if o[1] > alpha:
          alpha = o[1]
        if alpha > beta:
          break
        c += 1
    else:
      # ai is playing as human player
      o = (None,1000)
      c = 0
      for col in getPossibleMoves(board):
        tboard = deepcopy(board)
        
        # perform the move
        row = len(tboard) - 1
        while tboard[row][col] != 0:
            row -= 1
        tboard[row][col] = player
        
        # run minimax on that board with opposite player
        result = (col, performMinimax(tboard, opp, depth + 1, (row, col), pcolor, ocolor, alpha, beta, True)[1])
        
        # see if that is better than the current best
        if result[1] < o[1]:
          o = (result[0],result[1])
          best = []
          best.append(o)
        elif result[1] == o[1]:
          # add any moves with the same score as the best to the optimal array
          best.append(result)
        
        # alpha-beta magic
        if o[1] < beta:
          beta = o[1]
        if alpha > beta:
          break
        
        c += 1
    
    # pick random move from the best moves
    return random.choice(best)

# gets the value of a square on the board, wrapper to avoid wrapping around the board with negatives
def getSquare(board, r, c):
    if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]):
        return -1
    else:
        return board[r][c]

# checks if a player has won
# this is like one of those russian nesting dolls, but with for loops
def isTerminalState(board, player, move):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    # down, right, right+down, left+down
    for d in directions:
        for offset in range(4):
            original = getSquare(board, move[0] - d[0] * offset, move[1] - d[1] * offset)
            if original != player or original == -1:
                continue
            c = True
            for position in range(1, 4):
                s = getSquare(board, move[0] + d[0] * position - d[0] * offset,
                              move[1] + d[1] * position - d[1] * offset)
                if s != original or s == -1:
                    # square is not owned by the player being tested or out of range
                    c = False
                    break
            if c:
                return True
    return False

# checks if the board is full
def isFull(board):
    for r in board:
        if 0 in r:
            return False
    return True
