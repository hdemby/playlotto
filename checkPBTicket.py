#!/usr/bin/env python
"""
checkTicket.py

  check current ticket list for winner
"""
from playLotto import *
import sys

DEBUG=1

def main(ticket,draw,game=PowerBall):
  "play the game, get your score"
  val=0
  cost,playresdict=getWinners(ticket,draw,game)
  if DEBUG: print playresdict
  for tkt in playresdict.keys(): 
    if playresdict['value']>0:
      print "%16s\t%s"%(tkt,str(playresdict[tkt]))
  #raw_input("hit return to play remaining %s plays"%(n-1))
      val+=sum([playresdict[s]['value'] for s in playresdict.keys()])
  cost=len(ticket.split("\n"))
  winnings=val
  return cost,winnings

if __name__=="__main__":
  "run application"
  print "getting ticket..."
  ticket="".join("%s"%s for s in open("mynumbers.lst",'r').readlines())
  try:
    draw=sys.argv[1]
  except IndexError:
    draw=raw_input("what are the winning numbers?: ")
  cost,resultdict=main(ticket,draw,game=PowerBall)
  print "cost=$%s\twinnings=$%s"%(cost,resultdict,PowerBall)
