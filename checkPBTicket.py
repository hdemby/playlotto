#!/usr/bin/env python
"""
checkTicket.py

  check current ticket list for winner
"""
from playLotto import *
import sys

def main(ticket,draw,game=MegaMillions):
  "play the game, get your score"
  val=0
  for tkt in ticket.split("\n"):
    playresdict=getWinners(tkt,draw,game)
    if DEBUG: print playresdict
    if playresdict['value']>0:
      print "%16s\t%s"%(tkt,str(playresdict))
  #raw_input("hit return to play remaining %s plays"%(n-1))
      val+=playresdict['value']
  cost=len(ticket.split("\n"))
  winnings=val
  return cost,winnings

if __name__=="__main__":
  "run application"
  ## ./checkPBticket.py draw tktfile price game
  print "getting ticket..."
  try:
    ticket="".join("%s"%s for s in open(sys.argv[2],'r').readlines()).strip()
  except IndexError:
    ticket="".join("%s"%s for s in open('myPBticket.lst','r').readlines()).strip()
  try:
    game=eval(sys.argv[4])
  except IndexError:  
    game=MegaMillions
  try:
    price=int(sys.argv[3])
  except IndexError:  
    price=2
  except:
    print "USAGE: ./playlotto.py [game] [tktfile]"
    sys.exit()
  try:
    draw=sys.argv[1]
  except IndexError:
    draw=raw_input("what are the winning numbers?: ")
  resultdict=main(ticket,draw,game=PowerBall)
  cost=len(ticket.split("\n"))*price
  print "cost=$%s\twinnings=$%s"%(cost,resultdict)
