"""
Created on Thu Jun 18 2015

Quick Tableau-themed plots using matplotlib and the Tableau 20 color scheme

@author: sroessner

Created based on from Randal S Oslen's blog post:
http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/



"""

from matplotlib.pyplot import *
import matplotlib
import operator
import numpy as np
import pandas as pd
import math

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
  
# These are the "Tableau 20" colors as RGB.  
tableau20RGB = [(31, 119, 180), (255, 127, 14),   
			(44, 160, 44), (214, 39, 40),   
			(148, 103, 189), (140, 86, 75),   
			(227, 119, 194), (127, 127, 127),   
			(188, 189, 34), (23, 190, 207), 
			(174, 199, 232), (255, 187, 120),
			(152, 223, 138), (255, 152, 150),
			(197, 176, 213), (196, 156, 148),
			(247, 182, 210), (199, 199, 199),
			(219, 219, 141), (158, 218, 229)] 

tableau20 = [(31, 119, 180), (255, 127, 14),   
			(44, 160, 44), (214, 39, 40),   
			(148, 103, 189), (140, 86, 75),   
			(227, 119, 194), (127, 127, 127),   
			(188, 189, 34), (23, 190, 207), 
			(174, 199, 232), (255, 187, 120),
			(152, 223, 138), (255, 152, 150),
			(197, 176, 213), (196, 156, 148),
			(247, 182, 210), (199, 199, 199),
			(219, 219, 141), (158, 218, 229)]  

# Alignment and Offsets
hAlign = 'center'
vAlign = 'bottom'
offset = 0.01
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]
    tableau20[i] = (r / 255., g / 255., b / 255.)  


# List colors
def listColors():
	colorList = pd.DataFrame(tableau20RGB,columns=['R','G','B'])
	colorList['swatch']=np.arange(1,21)
	colorList['RGB'] = 'R:' + colorList["R"].map(str)+', G:'+colorList["G"].map(str)+', B:'+colorList["B"].map(str)+' Color ID:'

	horizBar(colorList,'swatch','RGB')

	return
	
	
def vertBar(DataFileName,ColumnWithValues,ColumnWithNames,*args,**kwargs):
	chartHeight = kwargs.get('chartHeight',7.5)
	chartWidth =kwargs.get('chartWidth',10)
	colorGroups = kwargs.get('colorGroups','sequential')
	rotate = kwargs.get('rotateLabels',0)
	chartTitle = kwargs.get('chartTitle','')
	subPlot = kwargs.get('subPlot',1)
	
	if subPlot == 1:
		subPlot = 1
	else:
		filterer = subPlot
		subPlot = DataFileName[filterer].nunique()
		ulist = DataFileName[filterer].unique()


	spCol = int(math.ceil(math.sqrt(subPlot)))
	spRow = int(math.ceil(subPlot/spCol))

	MaxY=max(DataFileName[ColumnWithValues])*1.2
	MinY=min(DataFileName[ColumnWithValues])*1.2 if min(DataFileName[ColumnWithValues])<0 else 0
	MaxX=DataFileName[ColumnWithNames].count()
	
	figure(figsize=(chartWidth,chartHeight))

	for i in range(subPlot):

		if subPlot==1:
			df = DataFileName
		else:
			df = DataFileName[DataFileName[filterer]==ulist[i]]
			chartTitle = ulist[i]

		sp = int(str(spRow) + str(spCol) + str(i+1))
		ax = subplot(sp)
		ax.spines["top"].set_visible(False)  
		ax.spines["bottom"].set_visible(True)  
		ax.spines["right"].set_visible(False)  
		ax.spines["left"].set_visible(False)
		ax.get_xaxis().tick_bottom()  
		ax.get_yaxis().tick_left()
		for y in range(int(MinY),int(MaxY), int((MaxY-MinY)/4)):  
			plot(range(-1, MaxX+1), [y] * len(range(-1, MaxX+1)), "--", lw=0.5, color="black", alpha=0.3)
			ax.axhline(y=0, color='black', linestyle='--', lw=0.5)
		ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") 
		
		if colorGroups == 'sequential':
			for row, Name in enumerate(df[ColumnWithNames]):
				NameValue = operator.itemgetter(row)(df[ColumnWithValues].values)
				bar(row,NameValue,lw=2.5,color=tableau20[row%20],edgecolor='none')
				text(row,NameValue+(-1.5*len(Name) if NameValue<0 else 1)+offset*MaxY,Name+'\n'+str(NameValue),color=tableau20[row%20],ha=hAlign,va=vAlign,size='large',rotation=rotate)

		elif (df[colorGroups] % 1 == 0).all():
			for row, Name in enumerate(df[ColumnWithNames]):
				NameValue = operator.itemgetter(row)(df[ColumnWithValues].values)
				ColorValue = operator.itemgetter(row)(df[colorGroups].values)-1
				bar(row,NameValue,lw=2.5,color=tableau20[int(ColorValue)],edgecolor='none')
				text(row,NameValue+(-1.5*len(Name) if NameValue<0 else 1)+offset*MaxY,Name+'\n'+str(NameValue),color=tableau20[int(ColorValue)],ha=hAlign,va=vAlign,size='large',rotation=rotate)

		else:
			distinctColors = df[colorGroups].unique()
			for row, Name in enumerate(df[ColumnWithNames]):
				NameValue = operator.itemgetter(row)(df[ColumnWithValues].values)
				tempColor =np.where(distinctColors == operator.itemgetter(row)(df[colorGroups].values))[0][0]
				try:
					pickedColor = operator.itemgetter(row)(df[colorGroups].values)-1
					bar(row,NameValue,lw=2.5,color=tableau20[pickedColor],edgecolor='none')
					text(row,NameValue+(-1.5*len(Name) if NameValue<0 else 1)+offset*MaxY,Name+'\n'+str(NameValue),color=tableau20[pickedColor],ha=hAlign,va=vAlign,size='large',rotation=rotate)
				except:
					bar(row,NameValue,lw=2.5,color=tableau20[tempColor%20],edgecolor='none')
					text(row,NameValue+(-1.5*len(Name) if NameValue<0 else 1)+offset*MaxY,Name+'\n'+str(NameValue),color=tableau20[tempColor%20],ha=hAlign,va=vAlign,size='large',rotation=rotate)
		title(chartTitle, fontsize='x-large')
	return

def horizBar(DataFileName,ColumnWithValues,ColumnWithNames,*args,**kwargs):
	chartHeight = kwargs.get('chartHeight',7.5)
	chartWidth = kwargs.get('chartWidth',10)
	colorGroups = kwargs.get('colorGroups','sequential')
	chartTitle = kwargs.get('chartTitle','')
	subPlot = kwargs.get('subPlot',1)
	

	if subPlot == 1:
		subPlot = 1
	else:
		filterer = subPlot
		subPlot = DataFileName[filterer].nunique()
		ulist = DataFileName[filterer].unique()

	spCol = int(math.ceil(math.sqrt(subPlot)))
	spRow = int(math.ceil(subPlot/spCol))

	MaxY=DataFileName[ColumnWithNames].count()
	MaxX=DataFileName[ColumnWithValues].max()*1.2

	figure(figsize=(chartWidth,chartHeight))

	for i in range(subPlot):

		if subPlot==1:
			df = DataFileName
			subTitle = ''
		else:
			df = DataFileName[DataFileName[filterer]==ulist[i]]
			chartTitle = ulist[i]

		sp = int(str(spRow) + str(spCol) + str(i+1))
		ax = subplot(sp)
		ax.spines["top"].set_visible(False)  
		ax.spines["bottom"].set_visible(True)  
		ax.spines["right"].set_visible(False)  
		ax.spines["left"].set_visible(False)
		ax.get_xaxis().tick_bottom()  
		ax.get_yaxis().tick_left()
		for x in range(int(MaxX/4),int(MaxX+1), int(MaxX/4)):  
			plot([x] * len(range(0, MaxY+1)), range(0, MaxY+1), "--", lw=0.5, color="black", alpha=0.3)
		ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="off") 
		
		if colorGroups == 'sequential':
			for row, Name in enumerate(df[ColumnWithNames]):
				NameValue = operator.itemgetter(row)(df[ColumnWithValues].values)
				barh(1+row,NameValue,lw=2.5,color=tableau20[row%20],edgecolor='none')
				text(NameValue+MaxX*offset,1+row,Name+': '+str(NameValue),color=tableau20[row%20],va='center',ha='left',size='large')

		elif (df[colorGroups] % 1 == 0).all():
			for row, Name in enumerate(df[ColumnWithNames]):
				NameValue = operator.itemgetter(row)(df[ColumnWithValues].values)
				ColorValue = operator.itemgetter(row)(df[colorGroups].values)-1
				barh(1+row,NameValue,lw=2.5,color=tableau20[int(ColorValue)],edgecolor='none')
				text(NameValue+MaxX*offset,1+row,Name+': '+str(NameValue),color=tableau20[int(ColorValue)],va='center',ha='left',size='large')

		else:
			distinctColors = df[colorGroups].unique()
			for row, Name in enumerate(df[ColumnWithNames]):
				NameValue = operator.itemgetter(row)(df[ColumnWithValues].values)
				tempColor = np.where(distinctColors == operator.itemgetter(row)(df[colorGroups].values))[0][0]
				try:
					pickedColor = operator.itemgetter(row)(df[colorGroups].values)-1
					barh(1+row,NameValue,lw=2.5,color=tableau20[pickedColor],edgecolor='none')
					text(NameValue+MaxX*offset,1+row,Name+': '+str(NameValue),color=tableau20[pickedColor],va='center',ha='left',size='large')
				except:
					barh(1+row,NameValue,lw=2.5,color=tableau20[tempColor%20],edgecolor='none')
					text(NameValue+MaxX*offset,1+row,Name+': '+str(NameValue),color=tableau20[tempColor%20],va='center',ha='left',size='large')
		title(chartTitle, fontsize='x-large')
	return

def line(DataFileName,ColumnWithXAxis,*args,**kwargs):
	chartHeight = kwargs.get('chartHeight',7.5)
	chartWidth =kwargs.get('chartWidth',10)
	chartTitle = kwargs.get('chartTitle','')

	MaxY=DataFileName.drop(ColumnWithXAxis,axis=1).max().max()

	if is_number(DataFileName[ColumnWithXAxis].max()):
		MaxX=DataFileName[ColumnWithXAxis].max()
		MinX=DataFileName[ColumnWithXAxis].min()
	else:
		MinX=0
		MaxX=len(DataFileName[ColumnWithXAxis])
	
	figure(figsize=(chartWidth,chartHeight))
	ax = subplot(111)  
	ax.spines["top"].set_visible(False)  
	ax.spines["bottom"].set_visible(True)  
	ax.spines["right"].set_visible(False)  
	ax.spines["left"].set_visible(False)
	ax.get_xaxis().tick_bottom()  
	ax.get_yaxis().tick_left()
	
	for y in range(int(MaxY/4),int(MaxY+1),int(MaxY/4)):  
		plot(range(MinX, int(MaxX+abs(MaxX-MinX)*0.1)), [y] * len(range(MinX, int(MaxX+abs(MaxX-MinX)*0.1))), "--", lw=0.5, color="black", alpha=0.3)
	ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on")
	
	for row, Name in enumerate(DataFileName.drop(ColumnWithXAxis,axis=1).columns):
		plot(DataFileName[ColumnWithXAxis].values,DataFileName.drop(ColumnWithXAxis.replace("\n"," "),axis=1)[Name].values,lw=2.5,color=tableau20[row%20])
		text(MaxX+.5,DataFileName.drop(ColumnWithXAxis.replace("\n"," "),axis=1)[Name].values[-1],Name,color=tableau20[row%20])
	title(chartTitle, fontsize='x-large')
	return

def area(DataFileName,ColumnWithValues,ColumnWithXAxis,areaGroups,*args,**kwargs):
	chartHeight = kwargs.get('chartHeight',7.5)
	chartWidth =kwargs.get('chartWidth',10)
	rotate = kwargs.get('rotateLabels',0)
	chartTitle = kwargs.get('chartTitle','')
	subPlot = kwargs.get('subPlot',1)
	colorGroups = kwargs.get('colorGroups','sequential')
	
	if subPlot == 1:
		subPlot = 1
	else:
		filterer = subPlot
		subPlot = DataFileName[filterer].nunique()
		ulist = DataFileName[filterer].unique()


	spCol = int(math.ceil(math.sqrt(subPlot)))
	spRow = int(math.ceil(subPlot/spCol))

	MaxY=max(DataFileName[ColumnWithValues])*1.2
	MaxX=DataFileName[ColumnWithXAxis].count()
	
	figure(figsize=(chartWidth,chartHeight))

	for i in range(subPlot):

		if subPlot==1:
			df = DataFileName
		else:
			df = DataFileName[DataFileName[filterer]==ulist[i]]
			chartTitle = ulist[i]

		areaLabels = DataFileName[areaGroups].unique()
		for i in range(DataFileName[areaGroups].nunique()):
		    tempValue = DataFileName[DataFileName[areaGroups]==areaLabels[i]]
		    emptyArray = np.zeros(DataFileName[ColumnWithXAxis].nunique())
		    for j in range(len(tempValue)):
			    row = int(tempValue.iloc[[j]][ColumnWithXAxis].values[0])
			    emptyArray[row] =  tempValue.iloc[[j]][ColumnWithValues].values[0]
		    if i==0:
		        y = emptyArray
		    else:
		        y = np.vstack([y, emptyArray])

		if colorGroups == 'sequential':
			for i in range(DataFileName[areaGroups].nunique()):
				if i ==0:
					areaColors = tableau20[0]
				else:
					areaColors = np.vstack([areaColors, tableau20[i]])
		else:
			for i in range(DataFileName[areaGroups].nunique()):
				tempValue = DataFileName[DataFileName[areaGroups]==areaLabels[i]]
				selectedColors = int(tempValue.iloc[[0]][colorGroups].values[0])
				if i ==0:
					areaColors = tableau20[selectedColors-1]
				else:
					areaColors = np.vstack([areaColors, tableau20[selectedColors-1]])

		
		stackplot(DataFileName[ColumnWithXAxis].unique(), y, labels=areaLabels, colors = areaColors)
		legend(loc='upper right')
	return

	
def gantt(DataFileName,ColumnWithSeries,ColumnWithStart,ColumnWithMagnitude,*args,**kwargs):
	chartHeight = kwargs.get('chartHeight',7.5)
	chartWidth =kwargs.get('chartWidth',10)
	colorGroups = kwargs.get('colorGroups','sequential')
	
	MaxX=int(max(DataFileName[ColumnWithStart]+DataFileName[ColumnWithMagnitude]))
	MaxY=DataFileName[ColumnWithSeries].count()
	
	figure(figsize=(chartWidth,chartHeight))
	ax = subplot(111)  
	ax.spines["top"].set_visible(False)  
	ax.spines["bottom"].set_visible(True)  
	ax.spines["right"].set_visible(False)  
	ax.spines["left"].set_visible(False)
	ax.get_xaxis().tick_bottom()  
	ax.get_yaxis().tick_left()
	
	ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="on", left="off", right="off", labelleft="off")
	
	for row, Name in enumerate(DataFileName[ColumnWithSeries]):
		barh(row,operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values),left=operator.itemgetter(row)(DataFileName[ColumnWithStart].values),lw=2.5,color=tableau20[row%20],edgecolor='none')
		text((operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values) + operator.itemgetter(row)(DataFileName[ColumnWithStart].values))+MaxX*0.01,row,Name,color=tableau20[row%20],va='center',ha='left',size='large')
	

	if colorGroups == 'sequential':
			for row, Name in enumerate(DataFileName[ColumnWithSeries]):
				barh(row,operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values),left=operator.itemgetter(row)(DataFileName[ColumnWithStart].values),lw=2.5,color=tableau20[row%20],edgecolor='none')
				text((operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values) + operator.itemgetter(row)(DataFileName[ColumnWithStart].values))+MaxX*0.01,row,Name,color=tableau20[row%20],va='center',ha='left',size='large')
	else:
		distinctColors = DataFileName[colorGroups].unique()
		for row, Name in enumerate(DataFileName[ColumnWithSeries]):
			tempColor = np.where(distinctColors == operator.itemgetter(row)(DataFileName[colorGroups].values))[0][0]
			try:
				pickedColor = operator.itemgetter(row)(DataFileName[colorGroups].values)-1
				barh(row,operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values),left=operator.itemgetter(row)(DataFileName[ColumnWithStart].values),lw=2.5,color=tableau20[pickedColor],edgecolor='none')
				text((operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values) + operator.itemgetter(row)(DataFileName[ColumnWithStart].values))+MaxX*0.01,row,Name,color=tableau20[pickedColor],va='center',ha='left',size='large')
			except:
				barh(row,operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values),left=operator.itemgetter(row)(DataFileName[ColumnWithStart].values),lw=2.5,color=tableau20[tempColor%20],edgecolor='none')
				text((operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values) + operator.itemgetter(row)(DataFileName[ColumnWithStart].values))+MaxX*0.01,row,Name,color=tableau20[tempColor%20],va='center',ha='left',size='large')
	return
