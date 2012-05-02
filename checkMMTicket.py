#!/usr/bin/env python
"""
checkTicket.py

  check current ticket list for winner
"""
from playLotto import *
import sys

def main(ticket,draw,game=MegaMillions['parms']):
  "play the game, get your score"
  val=0
  for tkt in ticket.split("\n"):
    playresdict=getWinners(tkt,draw)
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
  print "getting ticket..."
  ticket="".join("%s"%s for s in open("myMMticket.lst",'r').readlines())
  try:
    draw=sys.argv[1]
  except IndexError:
    draw=raw_input("what are the winning numbers?: ")
  cost,resultdict=main(ticket,draw)
  print "cost=$%s\twinnings=$%s"%(cost,resultdict)
