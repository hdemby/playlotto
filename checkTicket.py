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
    if playresdict['value']>0:
      print "%16s\t%s"%(tkt,str(playresdict))
      val+=playresdict['value']
  winnings=val
  return winnings


if __name__=="__main__":
  "run application"
  print "getting ticket..."
  try:
    ticket="".join("%s"%s for s in open(sys.argv[1],'r').readlines()).strip()
  except IndexError:
    ticket="".join("%s"%s for s in open('mynumbers.lst','r').readlines()).strip()
  try:
    draw=sys.argv[2]
  except IndexError:
    draw=raw_input("what are the winning numbers?: ")
  try:
    game=eval(sys.argv[3])
  except IndexError:  
    game=MegaMillions
  try:
    price=int(sys.argv[4])
  except IndexError:  
    price=1
  except:
    print "USAGE: ./playlotto.py [game] [tktfile]"
    sys.exit()
  print "Draw:  %s"%draw  
  winnings=main(ticket,draw,game)
  cost=len(ticket.split("\n"))*price
  print "cost=$%s\twinnings=$%s\tnet=$%s"%(cost,winnings,(winnings-cost))
