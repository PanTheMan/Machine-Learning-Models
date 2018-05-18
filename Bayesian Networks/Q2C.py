from Factors import *

def Part2CMain():
	# Initial setup
	hiddenVariables = ['Trav','FP','Fraud','IP','OC','CRP']
	factorTrav = Factor(['Trav'], [[True],[False]], [0.05,0.95])

	factorOC = Factor(['OC'],[[True],[False]],[0.6,0.4])
	factorCRP = Factor(["CRP","OC"], [[True,True],[True,False],[False,True],[False,False]],[0.1,0.001,0.9,0.999])
	factorFP = Factor(["FP","Fraud","Trav"], [[True,True,True],[True,True,False],[True,False,True],[True,False,False],[False,True,True],[False,True,False],[False,False,True],[False,False,False]], [0.9,0.1,0.9,0.01,0.1,0.9,0.1,0.99])
	factorFraud = Factor(["Fraud","Trav"],[[True,True],[True,False],[False,True],[False,False]],[0.01,0.004,0.99,0.996])
	factorIP = Factor(["IP","Fraud","OC"], [[True,True,True],[True,True,False],[True,False,True],[True,False,False],[False,True,True],[False,True,False],[False,False,True],[False,False,False]], [0.02,0.011,0.01,0.001,0.98,0.989,0.99,0.999])
	# Use all factors since they are all relevant because of evidence
	inference([factorTrav,factorFraud,factorFP,factorIP,factorOC,factorCRP],['Fraud'],hiddenVariables,[['FP',True],['CRP',True],['IP',False],['Trav',True]])

Part2CMain()