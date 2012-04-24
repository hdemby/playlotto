#!/usr/bin/env python
"""
checkTicket.py

  check current ticket list for winner
"""
from playLotto import *
import sys

def main(ticket,draw,game=MegaMillions):
  "play the game, get your score"
  if DEBUG: print ticket,draw,game
  val=0
  for tkt in ticket.split("\n"):
    playresdict=getWinners(tkt,draw,game)
    if playresdict['value']>0:
      print "%16s\t%s"%(tkt,str(playresdict))
      val+=playresdict['value']
  winnings=val
  return winnings

if __name__=="__main__":
  "run application"
  ## use command line parameters, take interactive input or use defaults
  ## parm=True and sys.argv[n] or (True and raw_input("What ticket file?: ") or DEFAULT)
  ##
  print "getting ticket..."
  try:
    ticket="".join("%s"%s for s in open(sys.argv[1],'r').readlines()).strip() # list to string w/o blank 
  except IndexError:
    ticketfile=True and raw_input("What ticket file?: ") or "mynumbers.lst"
    try:
      ticket="".join("%s"%s for s in open(ticketfile,'r').readlines()).strip()
    except IOError:
      print "That file dos not exist"
      raise ValueError
  if DEBUG: print ticketfile
  try:
    draw=sys.argv[2]
  except IndexError:
    draw=raw_input("what are the winning numbers?: ")
    if not draw:
      raise ValueError,"must enter a drawing result"
  if DEBUG: print draw
  try:
    game=eval(sys.argv[3])
  except IndexError:
    game=True and raw_input("What game?: ") or 'MegaMillions'
    game=eval(game)
    #game=MegaMillions
  if DEBUG: print game  
  try:
    price=int(sys.argv[4])
  except IndexError:  
    price=True and raw_input("cost per play?: ") or 1
    price=int(price)
  except ValueError:
    print "USAGE: ./checkTicket.py [<tktfile> <winning_numbers> <game> <price>]"
    sys.exit()
  if DEBUG: print price
  print "Draw:  %s"%draw  
  winnings=main(ticket,draw,game)
  cost=len(ticket.split("\n"))*price
  print "cost=$%s\twinnings=$%s\tnet=$%s"%(cost,winnings,(winnings-cost))
