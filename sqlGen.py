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
		df = self.data_df.groupby(self.tbl_name)
		tableStruct = {}
		for index in df:
		    tableStruct[index[0]] = index[1][self.col_name].tolist()
		return tableStruct

# # Code to parse score_netezza_metadata.csv 

# class ParseOraStagingMetadata:

# 	def __init__(self,fn):
# 		self.data_df = pandas.read_csv(fn,usecols=["TABLE_NAME", "COLUMN_NAME"])
# 		return


# 	def parse(self):
# 		df = self.data_df.groupby('TABLE_NAME')
# 		tableStruct = {}
# 		for index in df:
# 		    tableStruct[index[0]] = index[1]["COLUMN_NAME"].tolist()
# 		return tableStruct


# # Code to parse score_netezza_metadata.csv 

# class ParseScoreNetezzaMetadata:

# 	def __init__(self,fn):
# 		self.data_df = pandas.read_csv(fn,usecols=["NAME", "ATTNAME"])
# 		return


# 	def parse(self):
# 		df = self.data_df.groupby('NAME')
# 		tableStruct = {}
# 		for index in df:
# 		    tableStruct[index[0]] = index[1]["ATTNAME"].tolist()
# 		return tableStruct


#### Code for Parsing commonRecordStr.ecl

class ParseCommonRecordStr:

	def __init__(self,fn):
		self.fileName = fn
		return

	def chkTblStart(self,fline):
		if 'EXPORT' in fline:
			if 'RECORD' in fline:
					return True

		return False

	def parse(self):
		fp = open(self.fileName,"rb")
		ftext = fp.read()
		fp.close
		fLineList = ftext.split("\n")
		tblFlag = False
		tableStruct = {}
		attrList = []
		tName = None
		for fline in fLineList:

			if self.chkTblStart(fline): 
				tblFlag = True
				attrList = []
				tline  = fline.strip()
				tToken = tline.split(' ')
				tName = tToken[1]
				index = tName.find('_rec')
				tName = tName[:index].upper()
				continue

			fline = fline.strip()
			if  "END;" in fline :
#				print "Table ended"
				tableStruct[tName] = attrList
				tblFlag = False
				continue

			if tblFlag == True:	
					if fline == '': continue
					fToken = fline.split()
					attr = fToken[1].upper()
					attr = attr.replace(',','')
					attr = attr.replace(';','')
#					print "Attribute found: " + attr
					attrList.append(attr)


		return tableStruct




def genQuery(commonRecordStrDict, MetaDict, replaceStr = "[_ ]"):
	commonRecordQuery = ""
	for keys in commonRecordStrDict:
		values = MetaDict.get(keys)
		if values == None: continue
		val = commonRecordStrDict.get(keys)
		attrListMetadata = [x for x in values for y in val if x.replace(r'%s'%replaceStr,'').lower() == y.replace(r'%s'%replaceStr,'').lower()]

		if attrListMetadata == []: continue		
		query = "-- SQL query generated for Table :" + str(keys)
		query += "\n\nSELECT "
		attrList = ", ".join(attrListMetadata)
		query += attrList
		query += " FROM "
		query += str(keys)
		query += " ;\n\n\n"
		commonRecordQuery += query
	return commonRecordQuery

if __name__ == "__main__":

	config = ConfigObj('config.ini')

	commonRecordStrFile = config['commonRecordStrFile']
	commonRecordStrObj = ParseCommonRecordStr(commonRecordStrFile)
	commonRecordStrDict = commonRecordStrObj.parse()
	print len(commonRecordStrDict)

	commonRecordQuery = ""
	commonRecordQueryFile = config['commonRecordQueryFile']

	splChr = config['splChr']  # for removing special character pattern from attributes

	metaFileList = config['metaFile']['metaFileList']
	mflTok = metaFileList.split(",")
	for metafile in mflTok:
		MetadataFile = config['metaFile'][metafile]['MetadataFile']
		tbl_name = config['metaFile'][metafile]['tblName']
		col_name = config['metaFile'][metafile]['colName']
		MetadataObj = ParseMetadata(MetadataFile,tbl_name, col_name)
		MetadataDict = MetadataObj.parse()
		print len(MetadataDict)
		commonRecordQuery += genQuery(commonRecordStrDict,MetadataDict)




#	ScoreNetezzaMetadataFile = config['ScoreNetezzaMetadataFile']
#	ScoreNetezzaMetadataObj = ParseScoreNetezzaMetadata(ScoreNetezzaMetadataFile)
#	ScoreNetezzaMetadataObj = ParseMetadata(ScoreNetezzaMetadataFile,"NAME", "ATTNAME")
#	ScoreNetezzaMetadataDict = ScoreNetezzaMetadataObj.parse()
#	print len(ScoreNetezzaMetadataDict)

#	OraStagingMetadataFile = config['OraStagingMetadataFile']
#	OraStagingMetadataObj = ParseOraStagingMetadata(OraStagingMetadataFile)
#	OraStagingMetadataObj = ParseMetadata(OraStagingMetadataFile,"TABLE_NAME", "COLUMN_NAME")
#	OraStagingMetadataDict = OraStagingMetadataObj.parse()
#	print len(OraStagingMetadataDict)



#	commonRecordQuery += genQuery(commonRecordStrDict,OraStagingMetadataDict)
#	commonRecordQuery += genQuery(commonRecordStrDict,ScoreNetezzaMetadataDict)

	# for keys in commonRecordStrDict:
	# 	values = ScoreNetezzaMetadataDict.get(keys)
	# 	if values == None: continue
	# 	val = commonRecordStrDict.get(keys)
	# 	attrListScoreNetezzaMetadata = [x for x in values for y in val if x.replace('_','').replace(' ','').lower() == y.replace('_','').lower()]

	# 	if attrListScoreNetezzaMetadata == []: continue		
	# 	query = "-- SQL query generated for Table :" + str(keys)
	# 	query += "\n\nSELECT "
	# 	attrList = ", ".join(attrListScoreNetezzaMetadata)
	# 	query += attrList
	# 	query += " FROM "
	# 	query += str(keys)
	# 	query += " ;\n\n\n"
	# 	commonRecordQuery += query

	# for keys in commonRecordStrDict:
	# 	values = OraStagingMetadataDict.get(keys)
	# 	if values == None: continue
	# 	val = commonRecordStrDict.get(keys)
	# 	attrListOraStagingMetadata = [x for x in values for y in val if x.replace('_','').replace(' ','').lower() == y.replace('_','').lower()]

	# 	if attrListOraStagingMetadata == []: continue		
	# 	query = "-- SQL query generated for Table :" + str(keys)
	# 	query += "\n\nSELECT "
	# 	attrList = ", ".join(attrListOraStagingMetadata)
	# 	query += attrList
	# 	query += " FROM "
	# 	query += str(keys)
	# 	query += " ;\n\n\n"
	# 	commonRecordQuery += query


	fp = open(commonRecordQueryFile,"wb")
	fp.write(commonRecordQuery)
	fp.close()

