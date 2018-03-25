import os
import pandas as pd 
import numpy as np 
from email.parser import Parser
from collections import Counter
import sys  
from datetime import datetime



enc = sys.getdefaultencoding()

start_time = datetime.now()

rootdir = "/Users/mattanderson/Desktop/UNCC/AML/enron_proj/maildir"

colnames_info = ['Message-ID','Date','From','To','Subject','Mime-Version','Content-Type',
				'Content-Transfer-Encoding','X-From','X-To','X-cc','X-bcc','X-Folder','X-Origin',
				'X-FileName','Cc','Bcc','Time','Attendees','Re']

colnames_text = ['Message-ID','Msg-Text']

NUM_EMAILS = 517403
email_info = pd.DataFrame(columns = colnames_info, index = range(NUM_EMAILS))
email_text = pd.DataFrame(columns= colnames_text, index = range(NUM_EMAILS))
error_list =  []

def email_analyse(inputfile, email_info = email_info, email_text=email_text, email_count=0):
	content = []
	with open(inputfile,"r",encoding='cp1252') as f:
		data = f.read()
	email = Parser().parsestr(data)

	#Get Message Info for email
	email_text['Message-ID'].loc[email_count] = email['Message-ID']
	email_text['Msg-Text'].loc[email_count] = email.get_payload()


	#Loop through all other data and append to dataframe
	for data in email:
		if data in colnames_info:
			content.append(email[data])
			email_info[data].loc[email_count] = content.pop() 
		else:
			error_list.append(email_count)
			error_list.append(data)
			error_list.append(email[data])
			error_list.append("\n")

def status_update(email_count, start_time = start_time, NUM_EMAILS=NUM_EMAILS):
	pct_complete = email_count / NUM_EMAILS
	timedelta =  datetime.now() - start_time
	est_time = timedelta / pct_complete
	print("email_count".format(email_count))
	print("pct status:{0:.00f}".format(pct_complete))
	print("current duration:{}".format(timedelta))
	print("estimated remaining time = {}".format(est_time))

#Loops through directory returning folders/subfolders/files
email_count = 0 
for directory, subdirectory, filenames in os.walk(rootdir):
	for filename in filenames:
		path = os.path.join(directory,filename)
		email_analyse(path, email_count = email_count)
		email_count += 1
		#if email_count % 1000 == 0:
		#	status_update(email_count=email_count)
		
print("EMAIL COUNT = {}".format(email_count))
email_info = email_info[:email_count]
email_text = email_text[:email_count]

email_info.to_csv('/Users/mattanderson/Desktop/UNCC/AML/enron_proj/email_info.csv')
email_text.to_csv('/Users/mattanderson/Desktop/UNCC/AML/enron_proj/email_text.csv')

np.savetxt("error.txt", error_list, delimiter=",", fmt='%s')