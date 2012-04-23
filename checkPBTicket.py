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
  try:
    ticket="".join("%s"%s for s in open(sys.argv[2],'r').readlines()).strip()
  except IndexError:
    ticket="".join("%s"%s for s in open('mynumbers.lst','r').readlines()).strip()
  try:
    game=eval(sys.argv[1])
  except IndexError:  
    game=MegaMillions
  try:
    price=int(sys.argv[4])
  except IndexError:  
    price=1
  except:
    print "USAGE: ./playlotto.py [game] [tktfile]"
    sys.exit()
  try:
    draw=sys.argv[3]
  except IndexError:
    draw=raw_input("what are the winning numbers?: ")
  resultdict=main(ticket,draw,game=PowerBall)
  cost=len(ticket.split("\n")*price
  print "cost=$%s\twinnings=$%s"%(cost,resultdict,PowerBall)
