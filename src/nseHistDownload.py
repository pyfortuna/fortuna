import nseUtil as nu
import datetime
import pandas as pd
import os
import zipfile
import fortunacommon as fc

e = datetime.datetime.now()
s = e - datetime.timedelta(days=700)
res = pd.DataFrame()
confDF = pd.read_table('/home/ec2-user/fortuna/fortuna/data/nselist.tsv', header=0)
companyList = confDF['companyCode'].unique()
companyList.sort()
for companyCode in companyList:
	df = nu.getHistoricPrice(companyCode,s,e)
	output_filename = '/home/ec2-user/plutus/nsedata/%s.csv' % companyCode
	df.to_csv(output_filename)
	print('DEBUG : Saved data for %s' % companyCode)
print('DEBUG : Download completed')

print('DEBUG : Compression started')
zipfile_path = '/home/ec2-user/plutus/nsedata.zip'
zipf = zipfile.ZipFile(zipfile_path, 'w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk('/home/ec2-user/plutus/nsedata/'):
	for file in files:
        	zipf.write(os.path.join(root, file),file)
zipf.close()
print('DEBUG : Compression completed')

fc.sendMail('NSE Data','NSE Data',zipfile_path)
