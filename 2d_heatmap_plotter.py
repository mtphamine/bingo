import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
# from PIL import Image
import os
import csv
import numpy as np


XnumberOfPlayers = []
YnumberOfTurns = range(0,76)
Zlayers = []

YbarMeans = []

dummyZ = []

readfile = open('histogram_data_1-100.csv', 'r')
# writefile = open('table_mean_turns_to_win_1-100.csv', 'w')

# writefile.write('players,mean turns,median,s\n')

for unsplitLine in readfile:
	line = unsplitLine.split(',')
	XnumberOfPlayers.append(line[0])

	histoRow = {}
	for x in range(1,76):
		count = 0
		for val in line[1:]:
			if val == str(x):
				count += 1

		histoRow[x] = count

	dummyZ.append(histoRow)
	print str(line[0]) + '\n' + str(histoRow) + '\n'

	lineForMean = []
	for val in line[1:]:
		lineForMean.append(int(val))
	YbarMeans.append(np.mean(lineForMean))
	# writefile.write(str(line[0]) + ',' + str(round(np.mean(lineForMean),2)) + ',' + str(np.median(lineForMean)) + ',' + str(round(np.std(lineForMean),2)) + '\n')

########################################################
## To generage heat map (gives z axis)
####################################################
for x in range(1,76):
	layer = []
	for histo in dummyZ:
		layer.append(histo[x])

	Zlayers.append(layer)

print XnumberOfPlayers
print Zlayers[25]
print YnumberOfTurns

data = [
	go.Heatmap(
		z=Zlayers,
		x=XnumberOfPlayers,
		y=YnumberOfTurns,
	)
]

layout = go.Layout(
	title='Heatmap of turns for Bingo win',
	hovermode='closest',
	xaxis=dict(
		title='Number of players',
		ticklen=5,
		gridwidth=2,
		dtick=10
		),
	yaxis=dict(
		title='Number of turns',
		ticklen=5,
		gridwidth=2,
		),
	width=800,
	height=600,
	)

plot_url = py.plot(data, layout=layout, filename='bingo_heatmap')

# fig = go.Figure(data=data, layout=layout)
# py.image.save_as(fig, 'bingo_heatmap_axes.png')

# #################################################################
# ##	To generate bar graph of means
# ##############################################################
dataBar = [
	go.Bar(
		x=XnumberOfPlayers,
		y=YbarMeans
	)
]

layout = go.Layout(
	title='Mean number of turns for Bingo win',
	hovermode='closest',
	xaxis=dict(
		title='Number of players',
		ticklen=5,
		gridwidth=2,
		dtick=10
		),
	yaxis=dict(
		title='Mean number of turns',
		ticklen=5,
		gridwidth=2,
		),
	width=800,
	height=600,
	)

plot_url = py.plot(dataBar, layout=layout, filname='bingo_means')

# fig = go.Figure(data=dataBar, layout=layout)
# py.image.save_as(fig, 'bingo_means_axes.png')

readfile.close()
# writefile.close()