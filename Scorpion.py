# -*- coding: utf-8 -*-
from random import randint
import random
from math import *
import sys
import matplotlib.pyplot as plt

#INITIALISATION DE LA POPULATION

#Création d'un individu
def creationIndividu():
	return {tabCar[0]:randint(45, 90),tabCar[1]:randint(1, 10),tabCar[2]:randint(1, 10),tabCar[3]:randint(1, 10),tabCar[4]:randint(1, 10),tabCar[5]:randint(1, 10)}
	
#Création de la population
def creationPopulation(maxPop):
	population = []
	for i in range(0, maxPop):
		population.append(creationIndividu());
	return population
	
	
#EVALUATION DES INDIVIDUS

#Calcul du ressort
def calculK():
	r = 1-2*v
	if r != 0:
		return (E/r)/3
	return "err"
	
#Calcul de la longueur à vide
def calculLv(individu):
	r = pow(individu['lb'],2)-(0.25*pow(individu['lc'],2))
	if r >= 0:
		return sqrt(r)
	return "err"
	
#Calcul de la longueur du déplacement
def calculLd(individu):
	r = calculLv(individu)
	if r != "err" :
		return individu['lf'] - r
	return r
	
#Calcul de la masse du projectile
def calculMp(individu):
	return p * individu['b'] * individu['h'] * individu['lf']
	
#Calcul de la vélocité
def calculV(individu):
	K = calculK()
	#print "K: %.2f" % K
	Ld = calculLd(individu)
	Mp = calculMp(individu)
	if K != "err" and Ld != "err" and Mp !="err" and Mp != 0:
		r = (K * pow(Ld,2))/Mp
		if r >= 0:
			return sqrt(r)
		return "err"
	return "err"
	
#Calcul de l'énergie cinétique / Energie d'impact
def calculEc(individu):
	V = calculV(individu)
	Mp = calculMp(individu)
	if V != "err" and Mp !="err":
		return 0.5 * Mp * pow(V,2)
	return "err"

#Calcul de la portée
def calculP(individu):
	V = calculV(individu)
	if V != "err":
		return (pow(V,2)/g)*(sin(radians(2 * individu['a'])))
	return "err"

#Calcul du score de chaque individu
def calculScore(population):
	if(not population):
		print "PAS DE POPULATION, Gen : ",numGen
	#Calcul de l'énergie cinétique et de la portée
	Ec = []
	P = []
	for i in range (0, len(population)):
		tempEc = calculEc(population[i])
		tempP = calculP(population[i])
		#print "Individu : ",i," Ec : ",tempEc," P : ",tempP
		if tempEc != "err" and tempEc > 0:
			population[i]['Ec'] = tempEc
			Ec.append(tempEc)
		else:
			population[i]['Ec'] = 0
			Ec.append(0)
		
		if tempP != "err":
			population[i]['P'] = fabs(tempP-300)
			P.append(fabs(tempP-300))
		else:
			population[i]['P'] = 5000
			P.append(5000)
	plotEC.append(max(Ec))
	plotP.append(min(P))
	P2 = []
	#printPopulation(population)
	for i in range (0, len(P)):
		if(P[i] == -1):
			P2.append(0)
		else:
			P2.append(max(P) + 1 - P[i])
	
	#Calcul des scores de l'énergie cinétique et de la portée sur 100 puis du score global
	for i in range (0, len(population)):
		SEc = (100.0 * Ec[i]) / max(Ec)
		SP = (P2[i] * 100) / max(P2)
		#print "\n ",i
		#print "Ec : ",(SEc)
		#print "P : ",(SP)
		population[i]['S'] = (SEc + SP) / 2
	
	return creationCouples(population)

	
def calculProb(population):	
	#Calcul de la somme des scores
	somme = 0
	for i in range (0, len(population)):
		somme += population[i]['S']

	#Calcul de la probabilité de reproduction de chaque individu
	sommeProba = 0
	for i in range (0, len(population)):
		population[i]['Prob'] = sommeProba + (population[i]['S'] / somme)
		sommeProba += (population[i]['S'] / somme)
	
def choixCouple(population, couples):
	couple = []
	for j in range (2):
		number = random.uniform(0.0,1.0)
		for i in range (0, len(population)):
			if number < population[i]['Prob'] and number > population[i-1]['Prob']:
				#print("AJOUT N ",j," Gen",numGen, " Individu : ",population[i]['Ec'])
				couple.append(population[i])
				
	#print ("LEN COUPLE : ",len(couple))
	if(len(couple) == 2 and couple[0] <> couple[1]):
		couples.append([couple[0],couple[1]])
			
	else:
		#print "ERREUR Generation ",numGen
		couple = []
		couple = choixCouple(population, couples)
	return couples
	
def creationCouples(population):
	#Calcul de la probabilité de reproduction de chaque individu
	calculProb(population)
	
	#Création des couples
	couples = []
	for k in range (0, len(population)/2):
		#print "----------- Couples ",k," : -----------"
		couples = choixCouple(population, couples)
		
	#creation des enfants
	return creationEnfants(couples)

def creationEnfants(couples):
	newPop = []
	for i in range (0, len(couples)):
	
		#Si la hauteur de la coupe varie
		if(randint(1,10) < txVarCoupe):
			hCoupe = randint(0,len(tabCar))
		#Si la hauteur de la coupe reste à 50%
		else:
			hCoupe = len(tabCar)/2
		
		enfant1 = {}
		enfant2 = {}
		
		#Pour chaque caractéristique, croisement des gènes des parents entre les 2 enfants
		for j in range (0, len(tabCar)):
			if j < hCoupe:
				enfant1[tabCar[j]] = couples[i][0][tabCar[j]]
				enfant2[tabCar[j]] = couples[i][1][tabCar[j]]
			else:
				enfant1[tabCar[j]] = couples[i][1][tabCar[j]]
				enfant2[tabCar[j]] = couples[i][0][tabCar[j]]
		
		#Mutation d'un gène pour l'enfant 1
		if(randint(1,100) <= txMutation):
			print "MUTATION ENFANT 1"
			car = randint(0,5)
			if car == 0:
				enfant1[tabCar[randint(0,5)]] = randint(45, 90)
			else:
				enfant1[tabCar[randint(0,5)]] = randint(1, 10)
		
		#Mutation d'un gène pour l'enfant 2
		if(randint(1,100) <= txMutation):
			print "MUTATION ENFANT 2"
			car = randint(0,5)
			if car == 0:
				enfant2[tabCar[randint(0,5)]] = randint(45, 90)
			else:
				enfant2[tabCar[randint(0,5)]] = randint(1, 10)
		
		newPop.append(enfant1)
		newPop.append(enfant2)
	
	global numGen
	#print numGen
	if numGen < nbGen:
		numGen += 1
		#print "----------- Generation ",numGen," : -----------"
		calculScore(newPop)
	else:
		return newPop

#MAIN

#Fonction d'affichage de la population
def printPopulation(population):
	for i in range(0, len(population)):
		print population[i]

def main(args):
	#Déclaration des constantes globales
	global cible 
	cible = 300 #distance de la cible
	global p 
	p = 2700 #Masse volumique de la flèche -> Aluminium
	global E  
	E = 62.0 #Module de Young de l'Aluminium
	global v 
	v = 0.30 #Coefficient de Poisson de l'Aluminium
	global g
	g = 9.81 #Gravité de la Terre
	global txVarCoupe
	txVarCoupe = 5 #Taux de variation de la hauteur de coupe -> 50%
	global txMutation
	txMutation = 1 #Taux de mutation -> 1%
	global tabCar
	tabCar = ['a','lb','b','h','lc','lf'] #Tableau contenant le nom des différentes caractéristiques
	global numGen
	numGen = 1 #Numéro de la génération courante
	
	#Taille de la population
	maxPop = input("Taille de la population (paire) : ")
	
	global nbGen
	#Nombre de générations
	nbGen = input("Nombre de generations : ")
	
	#Création de la population et de ses individus
	population = []
	population = creationPopulation(maxPop)
	
	global plotEC 
	plotEC = []
	
	global plotP
	plotP = []
	
	#print "----------- Population : -----------"
	
	lastPop = []
	lastPop = calculScore(population)
	
	#printPopulation(lastPop)
	axeGen = []
	for i in range(0,nbGen):
		axeGen.append(i)
	#print "EC : ",plotEC
	#print "Gen : ",axeGen
	#print "P : ",plotP
	plt.subplot(211)
	plt.plot(axeGen, plotEC)
	plt.xlabel('Generations')
	plt.ylabel('Energie cinetique')
	#plt.axis([0, nbGen, 0, max(plotEC)])
	
	plt.subplot(212)
	plt.plot(axeGen, plotP)
	plt.xlabel('Generations')
	plt.ylabel('Distance de la cible')
	
	plt.show()
	
#Fonction d'entrée python    
if __name__ == '__main__': 
    main(sys.argv)