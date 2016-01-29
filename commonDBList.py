import pandas
from configobj import ConfigObj

# Code to parse any Meta File 

class ParseMetadata:

	def __init__(self,fn,tbl_name,col_name):
		self.data_df = pandas.read_csv(fn,usecols=[tbl_name, col_name])
#		self.data_df['colDigest'] = self.data_df[col_name].str.lower().str.replace(r'[_ ]+','')
		self.tbl_name = tbl_name
		self.col_name = col_name
		return

	def parse(self):
		return  self.data_df[self.tbl_name].tolist()

class ParseSASDict:

	def __init__(self,filename):
		text = open(filename).read()
		text  = text.replace('{'," ")
		text  = text.replace('}'," ")
		text  = text.strip()
		token = text.split('\n')
		self.dbList = []
		for t in token:
		#	a = raw_input()
			t = t[:-2]
			spl = t.split(':')
			row = spl[1].replace('[','').replace(']','').split(',')
  			for x in row:
					if x not in self.dbList:
						self.dbList.append(x.strip().upper())

	def parse(self):
		return self.dbList
  
 




if __name__ == "__main__":

	config = ConfigObj('config.ini')

	# commonRecordStrFile = config['commonRecordStrFile']
	# commonRecordStrObj = ParseCommonRecordStr(commonRecordStrFile)
	# commonRecordStrDict = commonRecordStrObj.parse()
	# print len(commonRecordStrDict)

	# commonRecordQuery = ""
	commonRecordQueryFile = config['commonDBListFile']

	# splChr = config['splChr']  # for removing special character pattern from attributes

	sasObj = ParseSASDict('parsedSAS_Test.txt')
	sasDbList = sasObj.parse()

	metaFileList = config['metaFile']['metaFileList']
	mflTok = metaFileList.split(",")
	commonDBList = []
	for metafile in mflTok:
		MetadataFile = config['metaFile'][metafile]['MetadataFile']
		tbl_name = config['metaFile'][metafile]['tblName']
		col_name = config['metaFile'][metafile]['colName']
		MetadataObj = ParseMetadata(MetadataFile,tbl_name, col_name)
		MetadataDict = MetadataObj.parse()
        commonDBList += list(set(MetadataDict) & set(sasDbList))

	print len(commonDBList)

	fp = open(commonRecordQueryFile,"wb")
	fp.write(str(commonDBList))
	fp.close()

