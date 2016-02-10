import math
import random
import numpy as np
from sets import Set
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
# from PIL import Image
import os

winConditions = [['B1','B2','B3','B4','B5'], ['I1','I2','I3','I4','I5'], ['N1','N2','N3','N4','N5'], ['G1','G2','G3','G4','G5'], ['O1','O2','O3','O4','O5'], ['B1','I1','N1','G1','O1'], ['B2','I2','N2','G2','O2'], ['B3','I3','N3','G3','O3'], ['B4','I4','N4','G4','O4'], ['B5','I5','N5','G5','O5'], ['B1','I2','N3','G4','O5'], ['B5','I4','N3','G2','O1']]

class bingoCard:
	"""creates a bingo card with random numbers for each position"""

	def __init__(self,name):
		self.allNumbPos = {}	#dictionary for (key,val) pairs where (number,position)
		self.allPosNumb = {}	#dictionary for (key,val) pairs where (position,number)
		self.numsMarked = []
		self.positionsMarked = ['N3']	
		self.winningCondition = 'did not win yet'
		self.populateCard()
		self.name = str(name)

	def getCardName(self):
		return self.name

	def populateCard(self):
		Bpositions = ['B1','B2','B3','B4','B5']
		Ipositions = ['I1','I2','I3','I4','I5']
		Npositions = ['N1','N2','N3','N4','N5']
		Gpositions = ['G1','G2','G3','G4','G5']
		Opositions = ['O1','O2','O3','O4','O5']

		Brandom = random.sample(range(1,16),5)
		Irandom = random.sample(range(16,31),5)
		Nrandom = random.sample(range(31,46),5)
		Grandom = random.sample(range(46,61),5)
		Orandom = random.sample(range(61,76),5)
		for x in range(5):
			self.allNumbPos[Brandom[x]] = Bpositions[x]
			self.allNumbPos[Irandom[x]] = Ipositions[x]
			self.allNumbPos[Nrandom[x]] = Npositions[x]
			self.allNumbPos[Grandom[x]] = Gpositions[x]
			self.allNumbPos[Orandom[x]] = Opositions[x]

			self.allPosNumb[Bpositions[x]] = Brandom[x]
			self.allPosNumb[Ipositions[x]] = Irandom[x]
			self.allPosNumb[Npositions[x]] = Nrandom[x]
			self.allPosNumb[Gpositions[x]] = Grandom[x]
			self.allPosNumb[Opositions[x]] = Orandom[x]

		self.markNumber(self.allPosNumb['N3'])

	def getCard(self):
		return self.allNumbPos

	def seeCard(self):
		letterAxis = ['B','I','N','G','O']
		numberAxis = range(1,6)

		print '------------------------------------'
		print "{}\t{}\t{}\t{}\t{}".format('B','I','N','G','O')
		print '------------------------------------'

		for numberLoc in numberAxis:
			rowVals = []
			for letterLoc in letterAxis:
				cardCoordinate = letterLoc + str(numberLoc)
				rowVals.append(self.allPosNumb[cardCoordinate])

			line = ''
			for number in rowVals:
				line = line + str(number) + '\t'

			print line + '\n'
		print '------------------------------------'

	def hasNumber(self, n):
		if n in self.allNumbPos:
			return True
		else:
			return False

	def getPosForNumber(self, n):
		return self.allNumbPos[n]

	def getNumForPos(self,pos):
		return self.allPosNumb[pos]

	def markNumber(self,number):
		self.numsMarked.append(number)
		if self.getPosForNumber(number) != 'N3':
			if self.allNumbPos[number]:
				self.positionsMarked.append(self.getPosForNumber(number))

	def getAllMarkedNums(self):
		return self.numsMarked

	def getAllMarkedPos(self):
		return self.positionsMarked

	def stopPlaying(self):
		gameOn = False
		for condition in winConditions:
			conditionSet = Set(condition)
			markedPosSet = Set(self.getAllMarkedPos())

			if conditionSet.issubset(markedPosSet):
				gameOn = True
				self.winningCondition = str(condition)
				# print condition
				break

		return gameOn

	def wonWithCondition(self):
		return self.winningCondition

def numCalls():
	"""establishes the order in which the numbers are called for a bingo game"""
	callOrder = range(1,76)
	random.shuffle(callOrder)
	return callOrder

def runBingoGame(numPlayers,gameNumber):
	"""runs a game of bingo for a given number of players, numPlayers"""
	allPlayers = []
	for playerNum in range(numPlayers):
		newPlayer = bingoCard(playerNum)
		allPlayers.append(newPlayer)
		newPlayer.seeCard()
	
	callList = numCalls()
	print 'call order: ' + str(callList) + '\n'

	# turn = 1
	# winCallHistory = []
	# for number in callList:
	# 	for player in allPlayers:
	# 		if player.stopPlaying():
	# 			if player.hasNumber(number):
	# 				player.markNumber(number)
				
	# 			if number not in winCallHistory:
	# 				winCallHistory.append(number)
	# 			# turn += 1
	# 		else:
	# 			winner = player
	# 			break

			# turn += 1
			# callHistory.append(number)

	winCallHistory = []
	winner = allPlayers[0]
	for number in callList:
		if winner.stopPlaying():
			break

		for player in allPlayers:
			if player.stopPlaying():
				winner = player
				break

			else:
				if player.hasNumber(number):
					player.markNumber(number)
					
		if number not in winCallHistory:
				winCallHistory.append(number)

	if winner == allPlayers[0]:
		numTurnsToWin = len(winCallHistory)
	else:
		numTurnsToWin = len(winCallHistory)-1

	if gameNumber/50 == 0:
		print 'game number: ' + str(gameNumber) + '/1000\n'
		print 'turn completed: ' + str(numTurnsToWin)
		print 'calls until win: ' + str(winCallHistory) + '\n'
		print 'player ' + str(winner.getCardName()) + ' won with ' + str(winner.wonWithCondition()) + '\n'
		# print 'bingo! \n'
		print 'bingo! \ncard has marked numbers: ' + str(winner.getAllMarkedNums())
		print 'card has marked positions: ' + str(winner.getAllMarkedPos()) + '\n'

	return numTurnsToWin


# readfile = open('table_turnsToWin.csv', 'r')
outfile = open('new_table_turnsToWin.csv', 'w')
outfileHistos = open('histogram_data.csv', 'w')
outfile.write('number of players,mean turns to win,median turns to win,standard deviation\n')

# for line in readfile:
# 	outfile.write(line)

# readfile.close()

for x in range(89,90):		#range is how many players playing
	totalWinTurns = []
	howManyPlayers = x+1

	outfileHistos.write(str(howManyPlayers))

	for game in range(1000):	#range is how many games there are to average
		turnsToEnd = runBingoGame(howManyPlayers,game)
		totalWinTurns.append(turnsToEnd)
		outfileHistos.write(','+str(turnsToEnd))

	outfileHistos.write('\n')

	meanTurnsToWin = np.mean(totalWinTurns)
	medianTurnsToWin = np.median(totalWinTurns)
	stdTurnsToWin = np.std(totalWinTurns)

	print 'Total number of turns to win: ', str(totalWinTurns)
	print 'mean number of turns to win for ', str(howManyPlayers), ' players: ', str(meanTurnsToWin)
	print 'median number of turns to win: ', str(medianTurnsToWin)
	print 'standard deviation of turns to win: ', str(stdTurnsToWin)

	x = totalWinTurns
	filename = str(howManyPlayers)+'playerBingo.png'

	data = [go.Histogram(x=x)]

	# os.chdir('histograms')
	# py.image.save_as({'data': data}, filename)
	# os.chdir('..')

	outfile.write(str(howManyPlayers) + ',' + str(meanTurnsToWin) + ',' + str(medianTurnsToWin) + ',' + str(stdTurnsToWin) + '\n')

outfile.close()
outfileHistos.close()