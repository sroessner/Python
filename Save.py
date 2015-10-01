"""
Created on 07OCT2015
@author: sroessner

Save File Script

"""

def text(DataFile, FilePath, FileName):
	import pandas
	
	if FilePath.endswith('/'):
		lastslash=''
	else:
		lastslash='/'
            
	if FileName.endswith('.txt'):
		fext=''
	else:
		fext='.txt'
		
	fullpath=FilePath+lastslash+FileName+fext
	DataFile.to_csv(fullpath, sep='\t')
	print('File saved as '+fullpath);

## End of Function

def csv(DataFile, FilePath, FileName):
	import pandas
        
	if FilePath.endswith('/'):
		lastslash=''
	else:
		lastslash='/'
            
	if FileName.endswith('.csv'):
		fext=''
	else:
		fext='.csv'
    
    
	fullpath=FilePath+lastslash+FileName+fext
	DataFile.to_csv(fullpath)
	print('File saved as '+fullpath)
## End of Function

def excel(DataFile,FilePath, FileName, *args, **kwargs):
	SheetName = kwargs.get('SheetName','Sheet1')
	from pandas import read_excel
        
	if FilePath.endswith('/'):
		lastslash=''
	else:
		lastslash='/'
            
	if FileName.endswith('.xlsx'):
		fext=''
	else:
		fext='.xlsx'
	
	fullpath=FilePath+lastslash+FileName+fext
	DataFile.to_excel(fullpath, sheet_name=SheetName)
	print('File saved as '+fullpath);
## End of Function
