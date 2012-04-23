#!/usr/bin/env python
"""
playLotto.py

 Engine for running Lottery simulations
 
"""
import re,os,math,random,sys
from playLotto_conf import *

#=====================================================================================
##--------------------------
## formatting and test
##--------------------------

## check format of lottery string
## valid strings: "9-14-33[-45-55][:35]"
lottopatt=r"^((\s)?[0-9]{1,2}(\s)?-){2,4}[0-9]{1,2}(\s)?([:\|-](\s)?[0-9]{1,2}(\s)?)?$"
islotto=re.compile(lottopatt)
LottoVAl=lambda a:islotto.match(a)
#>>> LottoVAl("9-14-33-45-55:35")
#>>> LottoVAl("9-14-33-45-55-35")
#>>> LottoVAl("9 14 33 45 55 35")
#>>> LottoVAl("9,14,33,45,55,35")

def play2lst(play): #<-- %s  --> [balls]
  "convert play string to number list"
  try:
    assert LottoVAl(play), "'%s' is not a valid lotto string"%play
    balls=play.replace(":","-")
    balls=balls.replace("|","-")
    balls=balls.replace(" ","")
    #balls,bonus=balls.rsplit("-",1)
    balls=balls.split("-")
    #balls+=bonus
    return balls
  except AssertionError:
    print "ERROR!: '%s' is not a valid lotto string"%play
    print "Format must be: '[n]n-[n]n-[n]n[-[n]n-[n]n][:[n]n]'"
    return
  except TypeError:
    print "type of '%s': "%play,type(play)
  return
#>>> play="9-22-24-40-54 : 13"; play2lst(play)
#>>> play="12-20-21-27-29:5"; play2lst(play)
#>>> play="9-22-24-40-54-13"; play2lst(play)
#>>> play="9-22-24-40-54|13"; play2lst(play)

def lst2play(list): #<-- [] --> %(playstr)s
  "convert list of picks in a play string"
  pb=[]
  try:
    if len(list)<3 or len(list)>6:
      raise ValueError
    elif len(list)==6:
      list,pb=list[:5],list[5:]
    playstr="-".join("%s"%s for s in list)
    if pb:
      playstr+=":%s"%pb[0]
    return playstr
  except ValueError:
    print "The entered list cannot be converted to a lotery ticket: ",list
#>>> list=[9,12,24,40,54,13]; lst2play(list)
#>>> list=[9,12,24,40,54]; lst2play(list)
#>>> list=[19,22,24,40,45,1]; lst2play(list)
#>>> list=[19,22,24]; lst2play(list)
#>>> list=[19,22,24,40,45,54,13]; lst2play(list)
#>>> list=[19,22]; lst2play(list)

def GoodPair(l1,l2): #<-- [],[] --> True/False
  if DEBUG: print len(l1),len(l2), type(l1),type(l2)
  return len(l1)==len(l2) and type(l1)==type([]) and type(l2)==type([])
#>>> l1=[9,14,33,45,55,35]; l2=[9,14,33,45,55,35]; GoodPair(l1,l2)
#>>> l1=[9,14,33,45,55,35]; l2=[14,33,45,55,35]; GoodPair(l1,l2)

def cmprPlayDraw(play,draw): #<-- %(play)s,%(draw)s --> [result]
  "check for draw matches in play"
  ## calculates number of matches for each draw value, 
  ## 'bonus ball' is last value if it is used 
  play=play2lst(play)
  draw=play2lst(draw)
  try:
    ## verify 'play' and 'draw' are equivalent in format
    assert GoodPair(play,draw),"entries are not compatible: %s, %s"%(play, draw)
    result=[]
    for each in draw[:-1]:
      matches=0
      for pick in play[:-1]:
        if pick==each:
          matches=1
      result.append(matches)
    result.append(play[-1] and draw[-1]==play[-1] and 1 or 0)
  except AssertionError:
    print "Bad play!",play,draw
    result=[]
  return result
#>>> play="9-14-33-45-55-35"; draw="9-14-33-45-55-35"; cmprPlayDraw(play,draw)
#>>> play="9-14-33-45-55-35"; draw="9-14-33-45-55-5"; cmprPlayDraw(play,draw)
#>>> play="9-14-33-45-55-35"; draw="19-24-33-5-15-3"; cmprPlayDraw(play,draw)
#>>> play="9-14-33-45-55:35"; draw="19-24-33-5-15:3"; cmprPlayDraw(play,draw)
#>>> play="3-5-9-45-51:5"; draw="19-24-33-5-15:35"; cmprPlayDraw(play,draw)
#>>> play="3-5-9-45-51:5"; draw="19-24-33-5-15:5"; cmprPlayDraw(play,draw)

def playval(result,rules=MegaMillions['rules']): #<-- [result],{rules} --> int
  "calculate the value of a ticket result"
  ## setting rules:
  ## ex. MegaMillions payouts:
  ## balls	MegaBall	prize
  ## 5		MB		$Jackpot
  ## 5		--		$250,000
  ## 4		MB		$10,000
  ## 4		--		$150
  ## 3		MB		$150
  ## 3		--		$7
  ## 2		MB		$10
  ## 1		MB		$3
  ## 0		MB		$2
  ## So:
  ## {2:0,3:7,4:150,5:250000,'0p':2,'1p':3,'2p':10,'3p':150,'4p':10,000,'5p':MMJACK}
  if sum(result[:-1]) and result[-1]:
      value=rules["%sp"%sum(result[:-1])]
  elif sum(result[:-1])>2 and not result[-1] :
    value=rules[sum(result[:-1])]
  else:
    value=0
  return value
#>>> results=[[0,0,0,0,0,0],[0,0,1,0,0,0],[1,0,1,0,0,0],[1,0,1,0,0,1],[1,0,1,0,1,0],[1,0,1,0,1,1],[1,1,1,0,1,0],[1,1,1,0,1,1],[1,1,1,1,1,0],[1,1,1,1,1,1]]
#>>> for result in results: playval(result)

def playlotto(play,draw,game=MegaMillions): #<-- %(play)s,%(draw)s,{dict} --> {result}
  "return teh results for a single lotto play"
  result={'result':[],'matchs':0,'pball':0,'value':0,'mesg':""}
  ## add cost of ticket to running total
  ## check the ticket and tally wins:
  if DEBUG: print "play:",play
  result['result']=cmprPlayDraw(play,draw)
  result['matchs']=sum(result['result'][:-1])
  result['pball']=result['result'][-1]
  result['value']=playval(result['result'],game['rules'])
  wins=result['matchs']
  ## DEBUG report
  if wins>=1 and result['pball']:
    mesg1="$%(value)s Winner! matched %(matchs)s and ** Power Ball!! **"%result
  elif wins>1 and not result['pball']:
    mesg1="$%(value)s Winner! matched %(matchs)s!! **"%result
  elif not wins and result['pball']:
    mesg1="$%(value)s Winner! Got the powerball"%result
  else:
    mesg1=""
  result.update({'mesg':mesg1})
  if DEBUG: print result['mesg']
  return result #> {dict}

def genPicks(nums,selections): #<-- #,# --> [picks][remaining]
  "elimination pick of 'nums' numbers from pool in selection range"
  picks=[]
  choices=range(1,int(selections)+1)
  for x in range(0,int(nums)):
    pick=choices.pop(int(math.floor(random.random()*len(choices))))
    picks.append(pick)
  return picks,choices
#>>> picks,choices=getPicks(5,56); print picks; print choices

def genTicket(game=MegaMillions,plays=5): #<-- {game},int --> %(multi-playTicket)s
  "simulate a Mega-Millions lottery session"
  ticket=""
  game=game['parms']
  ## num= numbers to choose, sel= range of choices; pb=play powerball; vals= 
  num,sel,pp,vals=game[:4]
  for n in range(0,int(plays)):
     picks="%s-%s-%s-%s-%s"%tuple(sorted(genPicks(num,sel)[0]))
     if pp:
       pb=":%s"%tuple(genPicks(pp,vals)[0])
     else:
       pb=""
     ticket+="%s%s\n"%(picks,pb)
  return ticket #> "str"
#>>> from playLotto import *
#>>> ticket=genTicket(); print ticket
#>>> draw=genTicket(plays=1); print draw

def getWinners(ticket,draw,game=MegaMillions): #<-- %(multi-playTicket)s,%(draw)s,{game} --> int,{results}
  "return multi-play ticket results, matches, pb, payvalue"
  ## get the raw win data from a ticket
  try:
    assert type(ticket)==type(""), "ticket must be a string"
    assert type(draw)==type(""), "draw must be type string"
    assert type(game)==type({}), "game must be type dictionary"
    if DEBUG: print "**** Draw: %s ****"%draw
    if DEBUG: print "draw",draw
    #draw=play2lst(draw)
    #if DEBUG: print "newdraw:",draw
    results={}
    if DEBUG: print "========== results ====================="
    draw=draw.strip()
    for play in ticket.strip().split("\n"):
      result=playlotto(play,draw)
      if DEBUG: print result['mesg']
      results.update(result)
    if DEBUG: print "=======================================\n"   
  except AssertionError:
    print "Huston! (you know there I'm going with this)..."
    results={}
  return results #> int,{dict}
#>>> from playLotto import *
#>>> ticket=genTicket(); print ticket
#>>> draw=genTicket(plays=1); print draw
#>>> cost,playresdict=getWinners(ticket,draw)
#>>> for tkt in playresdict.keys(): print "%16s\t%s"%(tkt,str(playresdict[tkt]))

#>>> ticket="".join("%s"%s for s in open('mynumbers.lst','r').readlines()); print ticket
#>>> draw=genTicket(plays=1); print draw
#>>> cost,playresdict=getWinners(ticket,draw)
#>>> for tkt in playresdict.keys(): print "%16s\t%s"%(tkt,str(playresdict[tkt]))

def main(ticket,draw,game=MegaMillions,price=1):
  "play the game, get your score"
  if DEBUG: print "parms:",ticket,draw,game,price
  val=0
  for tkt in ticket.split("\n"):
    playresdict=getWinners(tkt,draw,game)
    if DEBUG: print "dict: ",playresdict
    if playresdict['value']>1:
      print "%16s\t%s"%(tkt,str(playresdict))
      val+=playresdict['value']
  cost=price*len(ticket.split("\n"))
  winnings=val
  return cost,winnings

if __name__=="__main__":
  "run the app"
  try:
    ticket="".join("%s"%s for s in open(sys.argv[2],'r').readlines()).strip()
  except IndexError:
    ticket="".join("%s"%s for s in open('mynumbers.lst','r').readlines()).strip()
  try:
    game=eval(sys.argv[1])
  except IndexError:  
    game=MegaMillions
  try:
    price=int(sys.argv[3])
  except IndexError:  
    price=1
  except:
    print "USAGE: ./playlotto.py [game] [tktfile]"
    sys.exit()
  accost=0; acwin=0;
  tktsplayed=0
  while acwin-accost > -LIMIT:
    draw=genTicket(plays=1)
    cost,wins=main(ticket,draw,game,price=price);accost+=cost;acwin+=wins;
    tktsplayed+=1
    print "cost=$%s\twinnings=$%s\ttotal cost:$%s\t  net winnings: $%s"%(cost,wins,accost,acwin)
    if acwin > accost:
      ans=raw_input("You're ahead! Continue?: ")
      if ans in ['Y','y','yes','Yes','YES']:
	continue
      else:
	print "Good move!"
	break
  plays=len(ticket.split("\n"))
  print "plays/tkt: %s: tkts played: %s spent: $%s won: $%s Net: %s"%(plays,tktsplayed,accost,acwin,(acwin-accost))
#>>> from playLotto import *
#>>> ticket="".join("%s"%s for s in open("mynumbers.lst",'r').readlines())
#>>> accost=0; acwin=0; plays=1;
#>>> for play in range(plays): draw=genTicket(plays=1);print "\nDraw",draw,; cost,wins=main(ticket,draw); accost+=cost;acwin+=wins-cost; print "cost=$%s\twinnings=$%s\ttotal cost:$%s\t  net winnings: $%s"%(cost,wins,accost,acwin)

#>>> ticket="".join("%s"%s for s in open("myPBticket.lst",'r').readlines()).strip()
#>>> accost=0; acwin=0; plays=1; game=PowerBall
#>>> for play in range(plays): draw=genTicket(plays=1,game=game);print "\nDraw",draw,; cost,wins=main(ticket,draw,price=3); accost+=cost;acwin+=wins-cost; print "cost=$%s\twinnings=$%s\ttotal cost:$%s\t  net winnings: $%s"%(cost,wins,accost,acwin)


