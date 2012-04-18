import re,os,math,random

## lottery type,(balls,range,pball,range,cost,extra),{ <payout-rules> }
MegaMillions=[0,(5,56,1,46,1,2),{3:7,4:150,5:250000,'pb':2,'1p':3,'2p':10,'3p':150,'4p':10000,'5p':JACKPOT}]
PowerBall=[0,(5,59,1,35,2,3),{3:7,4:100,5:1000000,'pb':4,'1p':4,'2p':7,'3p':100,'4p':10000,'5p':JACKPOT}]
CashFive=[0,(5,39,0,0),{2:1,3:JACKPOT*.074,4:JACKPOT*.1476,5:JACKPOT*.5471}]
Pick4=[1,('x4',9,0,0,.5,1),{'exact':2500,'exact+':2500,'any-4a':600,'any-4e':3100,'any-6a':400,'any-6e':2900,'any-12a':200,'any-12e':2700,'any-24a':100,'any-24e':2600,'combo':2500,'combo+':5000}]
Pick3=[1,(),{}]

DEBUG=0

#=====================================================================================
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

def GoodPair(l1,l2):
  if DEBUG: print len(l1),len(l2), type(l1),type(l2)
  return len(l1)==len(l2) and type(l1)==type([]) and type(l2)==type([])
#>>> l1=[9,14,33,45,55,35]; l2=[9,14,33,45,55,35]; GoodPair(l1,l2)
#>>> l1=[9,14,33,45,55,35]; l2=[14,33,45,55,35]; GoodPair(l1,l2)
    
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

def getTicket(game=MegaMillions[0],plays=5):
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

def playval(result,rules={3:7,4:150,5:250000,'pb':2,'1p':3,'2p':10,'3p':150,'4p':10000,'5p':JACKPOT},pb=PB):
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
  ## {2:0,3:7,4:150,5:250,00,'pb':2,'1p':3,'2p':10,'3p':150,'4p':10,000,'5p':jackpot}
  if pb and result[-1]:
    if sum(result):
      value=rules["%sp"%sum(result[:-1])]
    else:
      value=rules['pb']
  elif sum(result[:-1])>2:
    value=rules[sum(result[:-1])]
  else:
    value=0
  return value
#>>> results=[[0,0,0,0,0,0],[0,0,1,0,0,0],[1,0,1,0,0,0],[1,0,1,0,0,1],[1,0,1,0,1,0],[1,0,1,0,1,1],[1,1,1,0,1,0],[1,1,1,0,1,1],[1,1,1,1,1,0],[1,1,1,1,1,1]]
#>>> for result in results: playval(result)

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
      result=playChk(play,draw)
      if result:
        results.update({play:{'result':result,'match':sum(result[:-1]),'pb':result[-1],'value':playval(result)}})
        if DEBUG: print "%16s\t%s"%(play,str(results))
        wins=results['match']
        ## DEBUG report
	mesg1=""
        if wins>0:
	  if wins>1:
	    mesg1="Winner! match %s"%wins
	  if result[-1]:
	    mesg1+=" and ** Power Ball!! **"
	if DEBUG: print mesg1    
  if DEBUG: print "=======================================\n"    
  return cost,results
#>>> from playLotto import *
#>>> ticket=getTicket(); print ticket
#>>> draw=getTicket(plays=1); print draw
#>>> cost,playresdict=getWinners(ticket,draw)
#>>> for tkt in playresdict.keys(): print "%16s\t%s"%(tkt,str(playresdict[tkt]))

