import re,os,math

MegaMillions=(5,56,1,46)
CashFive=(5,39,0,0)


def doPicks(nums,selections):
  "pick 'nums' numbers from range of selections"
  picks=[]
  choices=range(1,selections+1)
  for x in range(0,nums):
    pick=choices.pop(int(math.floor(random.random()*len(choices))))
    picks.append(pick)
  return picks,choices
#>>> picks,choices=getPicks(nums,selections); print picks; print choices



def getTicket(game=MegaMillions,plays=5):
  "simulate a Mega-Millions lottery session"
  ticket=""
  #plays=raw_input("Number of Plays?: ")
  num,sel,mul,vals=game
  for n in range(0,plays):
     picks="%s-%s-%s-%s-%s"%tuple(sorted(getPicks(num,sel)[0]))
     if mul:
       multp=": %s"%tuple(getPicks(mul,vals)[0])
     else:
       multp=""
     ticket+="%s %s\n"%(picks,multp)
  return ticket

#>>> game=MegaMillions; print PlayLotto(game,5)


def PlayLotto(ticket,plays=26):
  "find a winning lottery numbers in a list of tickets"
  ## this is a simulation of playing a 'ticket' for a number of games. It will evaluate the wins for the
  ## numbers entered based on the ticket:game. Default plays is 26, the max number of of 'multi-plays' allowed.
  ## The code also keeps track of the cost and winnings to evaluate ROI
  ##
  ## ticket={'game':gameObj,'picks':[picklist]}
  ## gameObj:
  ##  name:
  ##  payrules:
  ##  
  return cost,winnings,winlst


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