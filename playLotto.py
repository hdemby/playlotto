import re,os,math,random


MegaMillions=(5,56,1,46)
CashFive=(5,39,0,0)

DEBUG=0

##--------------------------
## formatting and test
##--------------------------

## check format of lottery string
## valid strings: "9-14-33[-45-55][:35]"
LottoVAl=lambda a:re.compile("^((\s)?[0-9]{1,2}(\s)?-){2,4}[0-9]{1,2}(\s)?([:\|-](\s)?[0-9]{1,2}(\s)?)?$").match(a)
#>>> LottoVAl("9-14-33-45-55:35")
#>>> LottoVAl("9-14-33-45-55-35")
#>>> LottoVAl("9 14 33 45 55 35")
#>>> LottoVAl("9,14,33,45,55,35")


def play2lst(play):
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


def lst2play(list):
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

def GoodPair(l1,l2):
  if DEBUG: print len(l1),len(l2), type(l1),type(l2)
  return len(l1)==len(l2) and type(l1)==type([]) and type(l2)==type([])
#>>> l1=[9,14,33,45,55,35]; l2=[9,14,33,45,55,35]; GoodPair(l1,l2)
#>>> l1=[9,14,33,45,55,35]; l2=[14,33,45,55,35]; GoodPair(l1,l2)
    

#=====================================================================================
##--------------------------
##  game logic
##--------------------------

def playChk(play,draw):
  "check for draw matches in play"
  ## calculates number of matches for each draw value, 
  ## 'bonus ball' is last value if it is used 
  play=play2lst(play)
  draw=play2lst(draw)
  try:
    ## verify 'play' and 'draw' are equivalent in format
    assert GoodPair(play,draw),"entries are not compatible: %s, %s"%(play, draw)
    #play=play.split("-")
    #draw=draw.split("-")
    result=[]
    for each in draw:
      matches=0
      for pick in play:
        if pick==each:
          matches=1
      result.append(matches)
    if draw[-1]==play[-1]:
      result[-1]=1
  except AssertionError:
    print "Bad play!",play,draw
    result=[]
  return result
#>>> play="9-14-33-45-55-35"; draw="9-14-33-45-55-35"; playChk(play,draw)
#>>> play="9-14-33-45-55-35"; draw="9-14-33-45-55-5"; playChk(play,draw)
#>>> play="9-14-33-45-55-35"; draw="19-24-33-5-15-3"; playChk(play,draw)
#>>> play="9-14-33-45-55:35"; draw="19-24-33-5-15:3"; playChk(play,draw)
#>>> play="3-5-9-45-51:5"; draw="19-24-33-5-15:35"; playChk(play,draw)
#>>> play="3-5-9-45-51:5"; draw="19-24-33-5-15:5"; playChk(play,draw)


def genPicks(nums,selections):
  "pick 'nums' numbers from range of selections"
  picks=[]
  choices=range(1,int(selections)+1)
  for x in range(0,int(nums)):
    pick=choices.pop(int(math.floor(random.random()*len(choices))))
    picks.append(pick)
  return picks,choices
#>>> picks,choices=getPicks(5,56); print picks; print choices

def getTicket(game=MegaMillions,plays=5):
  "simulate a Mega-Millions lottery session"
  ticket=""
  ## num= numbers to choose, sel= range of choices; pb=play powerball; vals= 
  num,sel,pp,vals=game
  for n in range(0,int(plays)):
     picks="%s-%s-%s-%s-%s"%tuple(sorted(genPicks(num,sel)[0]))
     if pp:
       pb=":%s"%tuple(genPicks(pp,vals)[0])
     else:
       pb=""
     ticket+="%s%s\n"%(picks,pb)
  return ticket
#>>> from playLotto import *
#>>> ticket=getTicket(); print ticket
#>>> draw=getTicket(plays=1); print draw

#>>> ticket=getTicket(MegaMillions,3); print ticket
#>>> draw=getTicket(plays=1); print draw


##--------------------------
##  simulations
##--------------------------

def getWinners(ticket,draw):
  "check ticket for wins"
  ## get the raw win data from a ticket  
  ##
  ##
  if DEBUG: print "**** Draw: %s ****"%draw
  if DEBUG: print "draw",draw
  #draw=play2lst(draw)
  #if DEBUG: print "newdraw:",draw
  cost=0
  results={}
  if DEBUG: print "========== results ====================="
  for play in ticket.strip().split("\n"):
    ## add cost of ticket to running total
    if play:
      cost+=1
      ## check the ticket and tally wins:
      if DEBUG: print "play:",play
      #plaset=play2lst(play)
      #if DEBUG: print "new play",plaset
      result=playChk(play,draw)
      if result:
	mesg1=""
        results.update({play:result})
        if DEBUG: print "%16s\t%s"%(play,result),
        degree=sum(result)
        if degree>0:
	  if degree>1:
	    mesg1="Winner! match %s"%degree
	  if result[-1]:
	    mesg1+=" and ** Power Ball!! **"
	if DEBUG: print mesg1    
  if DEBUG: print "=======================================\n"    
  return cost,results
#>>> from playLotto import *
#>>> ticket=getTicket(); print ticket
#>>> draw=getTicket(plays=1); print draw
#>>> cost,playresult=getWinners(ticket,draw); print rpt
#>>> ticket=ticket.split("\n")
#>>> for n in range(len(playresult.keys())): print ticket[n],playresult[ticket[n]]



def myNumsUp(ticlst):
  "simulate the number of lotteries it takes to hit"
  return numtries

def coldPlay(ticlst):
  "figure out the best numbers to play by creating the best set of numbers from a random set of 4096 draws"
  return numtries

 
def didIWin():
  "check most recent Lotto draw against your tickets for any wins"
  return 

  
  
samples="""

>>> MegaMillions=(5,56,1,46)
>>> game=MegaMillions; print PlayLotto(game,5)
12-30-34-46-52 : 14
2-13-40-43-51 : 9
3-15-20-27-31 : 30
12-23-30-41-51 : 37
26-41-43-44-52 : 37

>>> game=MegaMillions; print PlayLotto(game,5)
10-11-18-20-30 : 11
1-6-24-39-47 : 33
11-17-18-19-47 : 29
22-26-28-30-56 : 13
13-20-33-42-52 : 11

>>> game=MegaMillions; print PlayLotto(game,5)
3-20-34-45-46 : 18
9-18-19-33-34 : 13
7-20-33-43-50 : 31
1-6-27-37-46 : 3
13-21-34-52-53 : 41


>>> game=CashFive; print PlayLotto(game,5)

payouts:
MegaMillions:
#balls,MegaBall,prize
5,MB,$Jackpot
5,--,$250,000
4,MB,$10,000
4,--,$150
3,MB,$150
3,--,$7
2,MB,$10
1,MB,$3
0,MB,$2





"""