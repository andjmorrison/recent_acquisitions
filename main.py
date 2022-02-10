# dependencies
from config import api_key
import csv
import datetime
from lxml import etree 
import pandas as pd
import requests
import time

# main
def main():
	'''
	Function performs the following actions to build recent acq list:
	1. Import MMS ids via .csv.
	2. Query Alma Bibs API with each MMS id.
	3. Parse XML response using XPath, pull information on each bib.
	4. Correct quoting/delimiters and save as .txt.
	'''

	# base route
	base_url = 'https://api-na.hosted.exlibrisgroup.com/almaws/v1/bibs'

	# set paths
	path_read = 'mmsids.csv'

	today = datetime.date.today()
	first = today.replace(day=1)
	last = first - datetime.timedelta(days=1)
	path_export = f"{last.strftime('%b %Y')}.txt"
	print(f'Generating {path_export}...')

	# read csv
	df = pd.read_csv(path_read)

	# set array
	mmsids = df['MMS Id']

	# query records
	records = []

	for index, mmsid in enumerate(mmsids):
		print(f'{index}: {mmsid}')

		# url, request
		url = f'{base_url}/{mmsid}/?apikey={api_key}'
		print(url)
		req = requests.get(url)
		
		# xpath parsing
		record = etree.fromstring(bytes(req.text, encoding='utf-8')).findall('record')[0]
		subfields_692 = record.findall('datafield[@tag="692"]/subfield[@code="a"]')
		subfields_100 = " ".join(record.xpath('//datafield[@tag="100"]/subfield[@code != "0" and @code != "1"]/text()'))
		subfields_245 = " ".join(record.xpath('//datafield[@tag="245"]/subfield/text()'))
		subfields_250 = "".join(record.xpath('//datafield[@tag="250"]/subfield/text()'))
		subfields_264 = " ".join(record.xpath('//datafield[@tag="264" and @ind2="1"]/subfield[not(contains(., "©"))]/text()'))
		subfields_300 = " ".join(record.xpath('//datafield[@tag="300"]/subfield/text()'))
		subfields_050 = " ".join(record.xpath("//datafield[@tag='050']/subfield[@code='a' or @code='b']/text()"))
		subfields_090 = " ".join(record.xpath("//datafield[@tag='090']/subfield[@code='a' or @code='b']/text()"))

		# set vals
		fields = {}
		fields['692'] = '";"'.join([x.text for x in subfields_692])
		fields['AUTHOR'] = subfields_100
		fields['TITLE'] = subfields_245
		fields['EDITION'] = subfields_250
		fields['IMPRINT'] = subfields_264
		fields['DESCRIPT'] = subfields_300
		if subfields_090 != '':
			fields['CALL #'] = subfields_090
		else:
			fields['CALL #'] = subfields_050

		records.append(fields)
		time.sleep(1)

	# load df
	df = pd.DataFrame(records)
	df.sort_values('692', inplace=True)

	# save df
	df.to_csv(path_export, index=False, quoting=csv.QUOTE_ALL)

	# replace "";"" => ";"
	lines = []

	# open and replace
	with open(path_export, mode='r+') as file:
		for x in file:
			print(x)
			# replace double quotes
			x = x.replace('"";""','";"')
			# remove special char
			x = x.replace('�','')
			print(x)
			lines.append(x)
			print('---'*10)
	file.close()

	# save new lines
	with open(path_export, mode='w') as file:
		for x in lines:
			file.write(x)
	file.close()

	# verify
	with open(path_export, mode='r+') as file:
		for x in file:
			print(x)

if __name__ == '__main__':
    main()