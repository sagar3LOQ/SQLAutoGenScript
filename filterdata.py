import pandas
from configobj import ConfigObj
from os.path import commonprefix


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

	def __init__(self,filename, outFile, commonDBList):
		sasObj = pandas.read_csv(filename,header=None,sep='\t')
		sasObj[1] = sasObj[1].str.upper()

		print sasObj.shape


		for data in sasObj[1]:
			for val in commonDBList:
				lst = list((data,val))
				st = commonprefix(lst)
				l1 = len(st)
				l2 = len(data)
				if l1 > 0.66*l2:
	#			print 'case........'
					sasObj = sasObj[sasObj[1]!=data]
	#			a = raw_input()
	#			print data, val, st
		sasObj = sasObj.reset_index()
		sasObj.to_csv(outFile, sep='\t', header=None,columns=[0,1])
		print sasObj.shape
  
 




if __name__ == "__main__":

	config = ConfigObj('config.ini')

	# commonRecordStrFile = config['commonRecordStrFile']
	# commonRecordStrObj = ParseCommonRecordStr(commonRecordStrFile)
	# commonRecordStrDict = commonRecordStrObj.parse()
	# print len(commonRecordStrDict)

	# commonRecordQuery = ""
	commonRecordQueryFile = config['commonDBListFile']

	# splChr = config['splChr']  # for removing special character pattern from attributes

	# sasObj = pandas.read_csv('ScoreCardDetailsTables.tsv',header=None,sep='\t')
	# sasObj[1] = sasObj[1].str.upper()

	# print sasObj.shape

	metaFileList = config['metaFile']['metaFileList']
	mflTok = metaFileList.split(",")
	commonDBList = []
	for metafile in mflTok:
		MetadataFile = config['metaFile'][metafile]['MetadataFile']
		tbl_name = config['metaFile'][metafile]['tblName']
		col_name = config['metaFile'][metafile]['colName']
		MetadataObj = ParseMetadata(MetadataFile,tbl_name, col_name)
		MetadataDict = MetadataObj.parse()
        commonDBList += list(set(MetadataDict))


	# for data in sasObj[1]:
	# 	for val in commonDBList:
	# 		lst = list((data,val))
	# 		st = commonprefix(lst)
	# 		l1 = len(st)
	# 		l2 = len(data)
	# 		if l1 > 0.66*l2:
	# #			print 'case........'
	# 			sasObj = sasObj[sasObj[1]!=data]
	# #			a = raw_input()
	# #			print data, val, st
	# sasObj = sasObj.reset_index()
	# sasObj.to_csv('ScoreCardDetailsTables_filter.tsv',header=None, sep='\t', columns=[0,1])


	scoreObj = ParseSASDict('ScoreCardDetailsTables.tsv', 'ScoreCardDetailsTables_filter.tsv',commonDBList)

	segmentObj = ParseSASDict('SegmentDetailsTables.tsv', 'SegmentDetailsTables_filter.tsv',commonDBList)
	# print sasObj.shape

	# sasObj = pandas.read_csv('SegmentDetailsTables.tsv',header=None,sep='\t')
	# sasObj[1] = sasObj[1].str.upper()

	# print sasObj.shape


	# for data in sasObj[1]:
	# 	for val in commonDBList:
	# 		lst = list((data,val))
	# 		st = commonprefix(lst)
	# 		l1 = len(st)
	# 		l2 = len(data)
	# 		if l1 > 0.66*l2:
	# #			print 'case........'
	# 			sasObj = sasObj[sasObj[1]!=data]
	# #			a = raw_input()
	# #			print data, val, st
	# sasObj = sasObj.reset_index()
	# sasObj.to_csv('SegmentDetailsTables_filter.tsv', sep='\t', header=None,columns=[0,1])
	# print sasObj.shape


#	print len(commonDBList)


