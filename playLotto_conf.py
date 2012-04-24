DEBUG=1

## game constants
LIMIT=150	#maximus $ loss limit
MPX=False	#play multiplier

##-------------------------------------------
## game models:
##-------------------------------------------

## lottery type,(balls,range,pball,range,cost,extra),{ <payout-rules> }
PBJACK=173000000
MMJACK=76000000
C5JACK=57000

MegaMillions={'typ':0,'parms':[5,56,1,46,1,2],'rules':{3:7,4:150,5:250000,'0p':2,'1p':3,'2p':10,'3p':150,'4p':10000,'5p':MMJACK}}
PowerBall={'typ':0,'parms':[5,59,1,35,2,3],'rules':{3:7,4:100,5:1000000,'0p':4,'1p':4,'2p':7,'3p':100,'4p':10000,'5p':PBJACK}}
CashFive={'typ':0,'parms':[5,39,0,0,.5,1],'rules':{2:1,3:C5JACK*.074,4:C5JACK*.1476,5:C5JACK*.5471}}
Pick4={'typ':1,'parms':[4,9,0,0,.5,1],'rules':{'exact':2500,'exact+':5000,'any-4a':600,'any-4e':3100,'any-6a':400,'any-6e':2900,'any-12a':200,'any-12e':2700,'any-24a':100,'any-24e':2600,'combo':2500,'combo+':5000}}
Pick3={'typ':1,'parms':[3,9,0,0,.5,1],'rules':{'exact':250,'exact+':500,'any-3a':80,'any-3e':160,'any-6a':40,'any-6e':80,'50-50.3':80,'50/50.3e':330,'50/50.6':40,'50/50.6e':290,'combo':250,'combo+':500}}

