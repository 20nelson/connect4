# main.py handles the main game logic and rendering
# January 4, 2018
__author__ = 'Trevor Nelson'

import minimax
from copy import *
import time
import sys

# initializes an empty board
def createBoard():
    board = []
    for i in range(6):
        board.append([])
        for j in range(7):
          board[i].append(0)
    return board

# prints whitespace for alignment
def clearScreen():
  for i in range(0,30):
    print()

# prints the board, clearing the screen beforehand
def printBoard(board, slots=False):
    clearScreen()
    print('\033[34m┌──────────CONNECT─4──────────┐\033[0m')
    print('\033[34m│┌───╥───╥───╥───╥───╥───╥───┐│\033[0m')
    for r in range(len(board)):
        print('\033[34m││\033[0m', end='')
        for c in range(len(board[r])):
            color = '\033[31m' if board[r][c] == 1 else ''
            piece = 'O' if board[r][c] > 0 else ' '
            print(' ' + color + piece + '\033[0m ', end='')
            if c < len(board[r])-1:
              print('\033[34m║\033[0m',end='')
            else:
              print('\033[34m│\033[0m',end='')
        print('\033[34m│\033[0m',end='')
        if (r < len(board) - 1):
            print('\n\033[34m│╞═══╬═══╬═══╬═══╬═══╬═══╬═══╡│\033[0m')
        else:
            print('\n\033[34m│└─0─╨─1─╨─2─╨─3─╨─4─╨─5─╨─6─┘│\033[0m',end='')
            if slots:
              print('\n\033[34m└─═══─═══─═══─═══─═══─═══─═══─┘\033[0m')
            else:
              print('\n\033[34m└─────────────────────────────┘\033[0m')
            sys.stdout.flush()

# animates a piece being dropped and updates the board
def move(board, col, player):
  if board[0][col] != 0:
    return False
  cur = 0
  while cur + 1 < len(board) and board[cur + 1][col] == 0:
    displayboard = deepcopy(board)
    displayboard[cur][col] = player
    printBoard(displayboard)
    print('Please wait...')
    cur += 1
    time.sleep(0.1)
  board[cur][col] = player
  printBoard(board)
  print('Please wait...')
  time.sleep(0.5)
  return (cur, col)

# check if board is empty, helper for clear animation
def boardEmpty(board):
  for r in board:
    if r != [0, 0, 0, 0, 0, 0, 0]:
      return False
  return True

# animates pieces falling out of the board
def clearBoard(board):
  displayboard = deepcopy(board)
  printBoard(displayboard,True)
  print('Please wait...')
  time.sleep(0.1)
  while not boardEmpty(displayboard):
    displayboard.insert(0, [0, 0, 0, 0, 0, 0, 0])
    del displayboard[len(displayboard) - 1]
    printBoard(displayboard,True)
    print('Please wait...')
    time.sleep(0.1)
  time.sleep(0.4)

# main method
def main():
  firstplay = True
  while True:
    
    # setup game
    clearScreen()
    board = createBoard()
    mirrormode = False
    
    # ask player what color they want
    pcolor = None
    while not (pcolor == 1 or pcolor == 2):
      
      printBoard(board)
      
      if firstplay:
        print("Welcome to Connect 4!")
        
      pcolor = input("Would you like to be red or black? (Red goes first)\n>")
      
      if 'red' in pcolor.lower():
        pcolor = 1
        print("Red it is!", end='')
        sys.stdout.flush()
        time.sleep(1)
        
      elif 'black' in pcolor.lower():
        pcolor = 2
        print("Black it is!", end='')
        sys.stdout.flush()
        time.sleep(1)
        
      elif 'mirror' in pcolor.lower():
        # debug mode
        pcolor = 1
        print("Mirroring!", end='')
        mirrormode = True
        sys.stdout.flush()
        time.sleep(1)
        
      else:
        
        print("Sorry, that\'s not a color I recognize.", end='')
        sys.stdout.flush()
        time.sleep(1)
        clearScreen()
            
    # initialize game
    ocolor = 2 if pcolor == 1 else 1
    currentplayer = 1
    firstplay = False
    lmove = None
    mcount = 0
      
    # game loop
    while True:
      
      # print the board
      printBoard(board)
      
      # reset success
      success = False
      
      if currentplayer == pcolor:
        if not mirrormode:
          
          # human move
          pmove = input('Type a column number to move\nthere, or "end" to end the game.\n>')
        
        else:
         
          # ai move
          pmove = str(minimax.performMinimax(board, pcolor, 0, lmove, ocolor, pcolor, -1000, 1000, True)[0])
       
        if pmove.lower() == 'end':
          break
        
        # check if integer
        try:
          pmove = int(pmove)
          
          # check if in range
          if pmove >= 0 and pmove <= 6:
            
            # check if there's room in column
            if board[0][pmove] == 0:
              lmove = move(board, int(pmove), pcolor)
              success = True
              currentplayer = ocolor
              
            else:
              
              print('That column is full!')
              time.sleep(1)
              
          else:
            
            print('%d is out of range!' % pmove)
            time.sleep(1)
            
        except:
          
          print('%s is not a number!' % pmove)
          time.sleep(1)
          
      else:
        # ai move
        print('Let me think...')
        mv = minimax.performMinimax(board, ocolor, 0, lmove, pcolor, ocolor, -1000, 1000, True)[0]
        lmove = move(board, mv, ocolor)
        success = True
        currentplayer = pcolor
      
      # did a successful move occur?
      if success:
        
        # add to move counter (debug)
        mcount += 1
        
        # check if human won
        if minimax.isTerminalState(board, pcolor, lmove):
          printBoard(board)
          print('You win!')
          break
        
        # check if ai won
        if minimax.isTerminalState(board, ocolor, lmove):
          printBoard(board)
          print('I win!')
          break
        
        # check if board is full
        if minimax.isFull(board):
          printBoard(board)
          print('The board filled up.')
          break
          
    # ask player if they want to rematch
    again = input('Would you like to play again?\n>')
    if 'y' in again.lower():
      clearBoard(board)
    else:
      # display exit message
      print('Thanks for playing Connect 4!')
      break

# entry
if __name__ == '__main__':
    main()
