import json
import shutil
import os
import collections
from datetime import  date, datetime, timedelta

# read file from url
"""
import urllib2, json
url = urllib2.urlopen('http://site.com/sample.json')
obj = json.load(url)
"""

#load medical dictionnary file in .json format, this file will associate for each disease the score which it relates
def load_from_medical_dictionnary_file():
	medical_dictionnary_file = "medical_dictionnary.json"
	with open(medical_dictionnary_file, 'r') as dis:
		diseases_dictionnary = json.load(dis)
		return diseases_dictionnary

# load .json descriptive file of the sick person
def load_medical_file(medical_file):
	with open(medical_file, 'r') as f:
		json_keys = json.load(f)
	return json_keys

# calculate label diseases score
def label_score_calculator(json_keys, diseases_dictionnary):
	labels_list = json_keys["labels"].split(',')
	label_score = 0
	for label in labels_list:
		label_score = label_score + int(diseases_dictionnary[label])
	return label_score

# calculate the tardyness  score
def depo_score_calculator(json_keys):
	depo_date = json_keys["depo_date"]
	depo_date_day = depo_date["day"]
	depo_date_mounth = depo_date["mounth"]
	depo_date_year = depo_date["year"]
	depo = date(depo_date_year, depo_date_mounth, depo_date_day)
	today = date.today()
	diff = today - depo
	last_depo_score = abs(diff.days)
	return last_depo_score

# calculate for each descriptive .json file, the final score
def score_calculator(medical_file):
	score = depo_score_calculator(load_medical_file(medical_file)) * 5 + label_score_calculator(load_medical_file(medical_file), load_from_medical_dictionnary_file() ) * 10
	return score

# return the folder hashes , which will be indicated in the .json file, so we can retrieve the information
def getHash(medical_file):
	jsonkeys = load_medical_file(medical_file)
	return jsonkeys["hash"]

# sort the execution order, which the administration must respect
def append_sorted_map(mp,s, medical_file):
	h = getHash(medical_file)
	mp.update({s:h})
	od = collections.OrderedDict(reversed(sorted(mp.items())))
	return od

def test_path_or_create(folderPath):
	if not os.path.exists(folderPath):
		os.mkdir(folderPath)

def treat_file(mp, medical_file):
	medical_file_path =  ".\\json-files-stock\\"+medical_file
	s = score_calculator(medical_file_path)
	print("The Score of the file '"+medical_file+"' is : "+str(s))
	mp = append_sorted_map(mp,s, medical_file_path)
	print(mp)
	if s>1000:
		folderPath = (os.getcwd() + "\\critical\\")
		test_path_or_create(folderPath)
		shutil.copy(medical_file_path, folderPath+medical_file)
		print("Moved to Critical Folder")
	elif (s <1000) & (s>= 500):
		folderPath = (os.getcwd() + "\\medium\\")
		test_path_or_create(folderPath)
		shutil.copy(medical_file_path, folderPath+medical_file)

		print("Moved to Medium Priority Folder")
	else:
		folderPath = (os.getcwd() + "\\low\\")
		test_path_or_create(folderPath)
		shutil.copy(medical_file_path, folderPath+medical_file)
		print("Moved to Low Priority Folder")
	return mp
def main():

	# mp returns the execution
	mp = {}

	for filename in os.listdir(".\\json-files-stock"):
		treat_file(mp, filename)
	#


main()

