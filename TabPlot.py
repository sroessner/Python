"""
Created on Thu Jun 18 2015

Quick Tableau-themed plots using matplotlib and the Tableau 20 color scheme

@author: sroessner

Created with help from Randal S Oslen's blog post:
http://www.randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/



"""

from matplotlib.pyplot import *
import operator
import numpy
  
  # These are the "Tableau 20" colors as RGB.  
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]  
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
for i in range(len(tableau20)):  
    r, g, b = tableau20[i]  
    tableau20[i] = (r / 255., g / 255., b / 255.)  
	
def Bar(DataFileName,ColumnWithValues,*args,**kwargs):
	Chart_Height = kwargs.get('Chart_Height',7.5)
	Chart_Width =kwargs.get('Chart_Width',10)
	
	MaxY=max(DataFileName[ColumnWithValues])
	MaxX=DataFileName[ColumnWithNames].count()
	
	figure(figsize=(Chart_Width,Chart_Height))
	ax = subplot(111)  
	ax.spines["top"].set_visible(False)  
	ax.spines["bottom"].set_visible(True)  
	ax.spines["right"].set_visible(False)  
	ax.spines["left"].set_visible(False)
	ax.get_xaxis().tick_bottom()  
	ax.get_yaxis().tick_left()
	for y in range(MaxY/4,MaxY+1, MaxY/4):  
		plot(range(0, MaxX+1), [y] * len(range(0, MaxX+1)), "--", lw=0.5, color="black", alpha=0.3)
	ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") 
	
	for row, Name in enumerate(DataFileName[ColumnWithNames]):
		bar(row,operator.itemgetter(row)(DataFileName[ColumnWithValues].values),lw=2.5,color=tableau20[row],edgecolor='none')
		text(row,-1,Name,color=tableau20[row])
	return
	
def Line(DataFileName,ColumnWithXAxis,*args,**kwargs):
	Chart_Height = kwargs.get('Chart_Height',7.5)
	Chart_Width =kwargs.get('Chart_Width',10)
	try:
		MaxY=DataFileName.drop(ColumnWithXAxis,axis=1).max().max()
	finally:
		MaxY=DataFileName.max().max()
	MaxX=DataFileName[ColumnWithXAxis].max()
	MinX=DataFileName[ColumnWithXAxis].min()
	
	figure(figsize=(Chart_Width,Chart_Height))
	ax = subplot(111)  
	ax.spines["top"].set_visible(False)  
	ax.spines["bottom"].set_visible(True)  
	ax.spines["right"].set_visible(False)  
	ax.spines["left"].set_visible(False)
	ax.get_xaxis().tick_bottom()  
	ax.get_yaxis().tick_left()
	
	for y in range(int(MaxY/4),int(MaxY+1),int(MaxY/4)):  
		plot(range(MinX, int(MaxX+abs(MaxX-MinX)*0.1)), [y] * len(range(MinX, int(MaxX+abs(MaxX-MinX)*0.1))), "--", lw=0.5, color="black", alpha=0.3)
	'''plt.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") '''
	
	for row, Name in enumerate(DataFileName.drop(ColumnWithXAxis,axis=1).columns):
		plot(DataFileName[ColumnWithXAxis].values,DataFileName.drop(ColumnWithXAxis.replace("\n"," "),axis=1)[Name].values,lw=2.5,color=tableau20[row])
		text(MaxX+.5,DataFileName.drop(ColumnWithXAxis.replace("\n"," "),axis=1)[Name].values[-1],Name,color=tableau20[row])
	return
	
def TimeLine(DataFileName,ColumnWithSeries,ColumnWithStart,ColumnWithMagnitude,*args,**kwargs):
	Chart_Height = kwargs.get('Chart_Height',7.5)
	Chart_Width =kwargs.get('Chart_Width',10)
	
	MaxX=int(max(DataFileName[ColumnWithStart]+DataFileName[ColumnWithMagnitude]))
	MaxY=DataFileName[ColumnWithSeries].count()
	
	figure(figsize=(Chart_Width,Chart_Height))
	ax = subplot(111)  
	ax.spines["top"].set_visible(False)  
	ax.spines["bottom"].set_visible(True)  
	ax.spines["right"].set_visible(False)  
	ax.spines["left"].set_visible(False)
	ax.get_xaxis().tick_bottom()  
	ax.get_yaxis().tick_left()
	
	for y in range(0,MaxY+1, 1):  
		plot(range(0, MaxX+1), [y] * len(range(0, MaxX+1)), "--", lw=0.5, color="black", alpha=0.3)
	'''ax.tick_params(axis="both", which="both", bottom="off", top="off", labelbottom="off", left="off", right="off", labelleft="on") '''
	
	for row, Name in enumerate(DataFileName[ColumnWithSeries]):
		barh(row+.1,operator.itemgetter(row)(DataFileName[ColumnWithMagnitude].values),left=operator.itemgetter(row)(DataFileName[ColumnWithStart].values),lw=2.5,color=tableau20[row],edgecolor='none')
		text(MaxX+1,row+.5,Name,color=tableau20[row])
	return
