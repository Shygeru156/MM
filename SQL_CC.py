#requête SQL pour stocker mes listes de CC

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3
import os
import time
from MM.triangleCC import *

conn = sqlite3.connect('ma_base.db')
cur = conn.cursor()


cur.execute("""
DROP TABLE quotes
""")
conn.commit()

cur.execute("""create table QUOTES(
id int,
exchange varchar,
curr1 varchar,
curr2 varchar,
last float)""")
conn.commit()


data = lQuotes()

# pour l'import depuis un dictionnaire  cur.execute(""" INSERT INTO quotes(exchange,curr1,curr2,last) VALUES(:exchange, :curr1, :curr2, :last)""",data)
for i in range(len(MarketData)): 
	cur.execute("""INSERT INTO quotes(id,exchange,curr1,curr2,last) VALUES(?,?,?,?,?)""",tuple(data[i]))
	
#exemple pour modifier les entrés
#cursor.execute("""UPDATE users SET age = ? WHERE id = 2""", (31,))

conn.commit()



# lecture des données
def readCC():
	cur.execute("""SELECT id, exchange,curr1,curr2,last FROM Quotes""")
	for row in cur:
		print('{0}, {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))
	conn.commit()


#on choisi une pair triangulable avec leur id et leur valeur
def select(arg):
	t0 = ((CC_triangle()[arg])[0])[2]
	t1 = ((CC_triangle()[arg])[1])[2]
	t2 = ((CC_triangle()[arg])[2])[2]
	PT_arg = [t0, t1, t2]
	table = []
	for a in PT_arg:
		cur.execute("""SELECT id, exchange,curr1, curr2, last FROM Quotes WHERE id=?""", (a,))
		table.append(cur.fetchall())
	return table			
conn.commit()

#calcul de l'arbitrage
def calculARB(arg):
	tps1 = time.clock()
	s1curr1 = ((select(arg)[0])[0])[2] 
	s1curr2 = ((select(arg)[0])[0])[3] 

	s2curr1 = ((select(arg)[1])[0])[2] 
	s2curr2 = ((select(arg)[1])[0])[3] 

	s3curr1 = ((select(arg)[2])[0])[2]
	s3curr2 = ((select(arg)[2])[0])[3]

	s1 = ((select(arg)[0])[0])[4]
	s2 = ((select(arg)[1])[0])[4]
	s3 = ((select(arg)[2])[0])[4]
	if s1curr2 == s2curr1:
		tempC = s1 * s2
		if s2curr2 == s3curr1:
			tempC2 = tempC * s3
		elif s2curr2 == s3curr2:
			tempC2 = tempC * (1/s3)
	elif s1curr2 == s2curr2:
		tempC = s1*(1/s2)
		if s2curr2 == s3curr1:
			tempC2 = tempC * s3
		elif s2curr2 == s3curr2:
			tempC2 = tempC * (1/s3)
	elif s1curr2 == s3curr1:
		tempC = s1 * s3
		if s3curr2 == s2curr1:
			tempC2 = tempC * s2
		elif s3curr2 == s2curr2:
			tempC2 = tempC * (1/s2)
	elif s1curr2 == s3curr2:
		tempC = s1 * (1/s3)
		if s3curr2 == s2curr1:
			tempC2 = tempC * s2
		elif s2curr2 == s3curr2:
			tempC2 = tempC * (1/s2)
	tps2 = time.clock()
	tcalcul = tps2 - tps1
	print("Calcul du coefficient d'arbitrage sur le triangle {} Le temps de calcul est de {} secondes ... :(".format(select(arg),tcalcul))
	print("L'arbitrage est de :")
	return tempC2
	
	