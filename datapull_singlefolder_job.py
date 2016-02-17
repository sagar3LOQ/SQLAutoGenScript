import sys
import os
import subprocess
import datetime
import logging

logging.basicConfig(level=logging.DEBUG)



'''
This is the list of the jobs that have been build from talend and all reside in a single folder.
Essentially, we want to run it for the entire folder instead of selected list.
It'll be greate if you could add a way to provide option to do both but that is not essential at this moment
'''
#master_list = ['int_casa_accounts','fct_pos_txn','int_fct_atm_txn_dly','int_fct_branch_txn_dly','int_fct_pos_txn_dly']
#master_list = ['fct_accnt_summ_month1']
master_list = ['int_casa_accounts']

def getMonthVar(mnth=None):
	if not mnth:
		today = datetime.date.today()
		newtoday = datetime.date(today.year + 6, today.month, today.day)
	else:
		newtoday = mnth
	first = newtoday.replace(day=1)
	lastmonth = first - datetime.timedelta(days=1)
	return lastmonth

def startExe(fileName, monthVar1, monthVar2, monthVar3, debug=1):
	'''
	simply create the command and executes it.
	takes three parameter, all in datetime.date format. (All the jobs take these three parameters only
	'''
	cmd = 'bash '+fileName
	cmd = cmd + ' --context_param monthVar1='+monthVar1.strftime("%Y%m%d")
	cmd = cmd + ' --context_param monthVar2='+monthVar2.strftime("%Y%m%d")
	cmd = cmd + ' --context_param monthVar3='+monthVar3.strftime("%Y%m%d")
	print cmd
	if debug==1:
		print cmd
		return 0
	else:
		p = subprocess.Popen(cmd , stdout=subprocess.PIPE, shell=True).wait()
		return p

def dataPullJob1(folderPath, debug=1):

	logger = logging.getLogger(__name__)
	fileList = []
	for root, dirs, files in os.walk(folderPath):
		print root
		#print dirs
		#print files
		if master_list == []:
			for each in files:
				if each.endswith('.sh') :
					fileList.append(os.path.join(root, each))
		else:
			for each in files:
				if each.endswith('.sh') and each[:-7] in master_list:
					fileList.append(os.path.join(root, each))
	retcode = 1
	mnth =1 
	monthVar1 = getMonthVar()
	monthVar2 = getMonthVar(monthVar1)
	monthVar3 = getMonthVar(monthVar2)
	while (mnth < 4):
		monthVar1 = getMonthVar(monthVar1)
		monthVar2 = getMonthVar(monthVar2)
		monthVar3 = getMonthVar(monthVar3)
		for each in fileList:
			print each
			#retcode = startExe(each, monthVar1, monthVar2, monthVar3, debug)
			cnt = 0
			while(retcode != 0 and cnt < 10):
				cnt = cnt + 1
				retcode = startExe(each, monthVar1, monthVar2, monthVar3, debug)
				#We want to add logger here in case there is some error (stack trace) than we want only the first line and not
				#the entire stack trace

				if retcode == 0: 
					logger.debug('In debug mode')
				else: 
					log = retcode.split('\n')[0]
					logger.info(log)
		mnth = mnth + 1


def dataPullJob(folderPath, debug=1):

	logger = logging.getLogger(__name__)
	fileList = ['hello','how','are','khana','khake','jana']
	print "master list"
	print master_list
	mnth =3
        retcode = 1
	while (mnth < 4):
		for each in fileList:
			print each
			#retcode = startExe(each, monthVar1, monthVar2, monthVar3, debug)
			cnt = 0
			while(retcode != 0 and cnt < 10):
				cnt = cnt + 1
				#retcode = startExe(each, monthVar1, monthVar2, monthVar3, debug)

				retcode = "Hello this is stack trace\n It is used for \n testing this logger"
				if cnt==1: retcode = 0
				if retcode == 0: 

					logger.debug('In debug mode')

					retcode = "Hello this is stack trace\n It is used for \n testing this logger"
				else: 
					log = retcode.split('\n')[0]
					logger.info(log)
					
				#We want to add logger here in case there is some error (stack trace) than we want only the first line and not
				#the entire stack trace
		mnth = mnth + 1


if __name__=='__main__':
	if len(sys.argv) < 2 or len(sys.argv) > 4:
		print 'Usage: python '+__file__ + ' <folderPath> <overwrite debug (start execution) - 1/0> <add "ALL" to execute all files in directory>'
	elif len(sys.argv) == 4:
		 
		
		if (sys.argv[2] == '0' or sys.argv[2] == '1') and (sys.argv[3].upper() == 'ALL'):
			master_list = []
			dataPullJob(sys.argv[1], sys.argv[2])
		else:
			print 'Usage: python '+__file__ + ' <folderPath> <overwrite debug (start execution) - 1/0> <add "ALL" to execute all files in directory>'

		
	elif len(sys.argv) == 3:
		if sys.argv[2] == '0' or sys.argv[2] == '1':
			dataPullJob(sys.argv[1], sys.argv[2])
		elif sys.argv[2].upper() == 'ALL':
			master_list = []
			dataPullJob(sys.argv[1])
		else:
			print 'Usage: python '+__file__ + ' <folderPath> <overwrite debug (start execution) - 1/0> <add "ALL" to execute all files in directory>'
	else:
		dataPullJob(sys.argv[1])
