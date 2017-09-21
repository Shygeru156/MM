import os
from poloniex import Poloniex
polo = Poloniex()
# from MM.triangleCC import *
MarketData = polo.returnTicker()


#création d'une liste de toutes les pairs de devises
listCC = []
for key, value in MarketData.items():
    temp_bis = [key,value.get('id')]
    listCC.append(temp_bis)

#Extraction d'une paire de devise	
def capture(arg):
	cc1 = (listCC[arg])[0]
	lc1 = [(cc1.partition('_'))[0],(cc1.partition('_'))[2],(listCC[arg])[1]]
	return lc1

compteur = []
for i in range(100):
	compteur.append(i)

#on cherche la liste des pairs où la première devise de la pairs est présente	
def cherche1(s):
	listCC_t1 = []
	for i in compteur:
		if i !=s:
		
			if capture(i)[0] == capture(s)[0] or capture(i)[1] == capture(s)[0]:
				listCC_t1.append(capture(i))
	return listCC_t1 #liste contenant toutes les pairs ayant au moins la première devise de capture =(0)

#on cherche la liste des pairs où la deuxième devise de la pairs est présente
def cherche2(s):
	listCC_t2 = []
	for i in compteur:
		if i !=s:
			if capture(i)[1] == capture(s)[1] or capture(i)[1] == capture(s)[1]:
				listCC_t2.append(capture(i))
	return listCC_t2

# création d'une liste de CC triangulable
def cherche3(s):
	listCC_t3 = []
	t1 = (capture(s))[0] # BTC
	t2 = (capture(s))[1] #BCN
	if len(cherche2(s)) > 0:
		for e in range(len(cherche2(s))):
			ch20 = (cherche2(s)[e])[0] # xmr
			ch21 = (cherche2(s)[e])[1] # bcn
			if t2 == ch20: # si bcn égal à bcn
				for i in range(len(cherche1(s))): 
					ch10 = (cherche1(s)[i])[0] # une des première devise
					ch11 = (cherche1(s)[i])[1] # une des deuxième devise
					if ch10 == ch21 and ch11 == t1: # si une des première devise égal à xmr et l'autre à BTC
						listCC_t3.append(cherche1(s)[i])
					if ch10 == t1 and ch11 == ch21: # si une des deuxièmes devise égal à xmr
						listCC_t3.append(cherche1(s)[i])
			if t2 == ch21: # si bcn égal à bcn
				for i in range(len(cherche1(s))): 
					ch10 = (cherche1(s)[i])[0] # une des première devise
					ch11 = (cherche1(s)[i])[1] # une des deuxième devise
					if ch10 == ch20 and ch11 == t1: # si une des première devise égal à xmr et l'autre à BTC
						listCC_t3.append(cherche1(s)[i])
					if ch10 == t1 and ch11 == ch20: # si une des deuxièmes devise égal à xmr
						listCC_t3.append(cherche1(s)[i])
			listCC_t3.append(cherche2(s)[e])
			listCC_t3.append(capture(s))
			
			return listCC_t3	
	
#extraction des listes de CC triangulable
def CC_triangle():
	lcct = []
	for i in range(len(MarketData)):
		if type(cherche3(i)) == list:
			lcct.append(cherche3(i))
	return lcct

#Donne des infos sur la triangulation
def InfoCC():
	print("J'ai trouvé {} triangles de pair de devise parmi {} différentes devises disponible sur Poloniex".format(len(CC_triangle()),len(listCCsolo())))

#extraction des données du dico dans une liste	

def lQuotes():
	listQuotes = []
	for k, v in MarketData.items():
		temp = [v.get('id'),k,(k.partition('_'))[0], (k.partition('_'))[2],v.get('last')]
		listQuotes.append(temp)
	return listQuotes

#création de la liste de toutes les CC
listCCs = ['BTC','ETH']
def listCCsolo():
	for i in range(len(listCC)):
		cc1 = (listCC[i])[0]
		t0 = (cc1.partition('_'))[0]
		t2 = (cc1.partition('_'))[2]
		lc1 = [t0, t2]
		if lc1[0] not in listCCs:
			listCCs.append(lc1[0])
		elif lc1[1] not in listCCs:
			listCCs.append(lc1[1])
	return listCCs

os.system("pause")

# from MesModules.triangleCC import *
# pour r = 0, si 'ETH' est différent de listCCs[1] qui est égal à 'BTC'
