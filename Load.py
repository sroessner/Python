
"""
Created on Thu Apr 23 16:28:33 2015

Load File Script

@author: sroessner
"""

def text(FilePath, FileName):
	from pandas import read_table
        
	if FilePath.endswith('\\'):
		lastslash=''
	else:
		lastslash='\\'
            
	if FileName.endswith('.txt'):
		fext=''
	else:
		fext='.txt'
    
    
	fullpath=FilePath+lastslash+FileName+fext
	EmptyVar=read_table(fullpath)
	return EmptyVar;
## End of Function


def csv(FilePath, FileName):
	from pandas import read_csv
        
	if FilePath.endswith('\\'):
		lastslash=''
	else:
		lastslash='\\'
            
	if FileName.endswith('.csv'):
		fext=''
	else:
		fext='.csv'
    
    
	fullpath=FilePath+lastslash+FileName+fext
	EmptyVar=read_csv(fullpath)
	return EmptyVar;
## End of Function

def excel(FilePath, FileName, SheetNameOrNone, *args, **kwargs):
	IndexColumn = kwargs.get('IndexColumn',None)
	from pandas import read_excel
        
	if FilePath.endswith('\\'):
		lastslash=''
	else:
		lastslash='\\'
            
	if FileName.endswith('.xlsx'):
		fext=''
	else:
		fext='.xlsx'
	
	while True:
		try:
			fullpath=FilePath+lastslash+FileName+fext
			EmptyVar=read_excel(fullpath, SheetNameOrNone, index_col=IndexColumn, na_values=['NA'])
			break
		except:
			fext='.xls'
			fullpath=FilePath+lastslash+FileName+fext
			EmptyVar=read_excel(fullpath, SheetNameOrNone, index_col=IndexColumn, na_values=['NA'])
			break

	return EmptyVar;
## End of Function
