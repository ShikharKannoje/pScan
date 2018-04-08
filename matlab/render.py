from pymongo import MongoClient
import pandas as pd
import json

db = MongoClient()["data"]

def writeTheta(fname):
	dt = []
	for i in open(fname).readlines():
		dt.append(map(float, i.split()))
	db.theta.insert({fname.split(".")[0]: dt})

def writeTrain(fname):
	df = pd.read_csv(fname)
	df.rename(columns={'Jitter (local and absolute)': 'Jitter (local, absolute)',
			 'Shimmer (local and dB)': 'Shimmer (local, dB)'}, inplace=True)
	for i in json.loads(df.to_json(orient = "records")):
		db.train.insert(i)

#writeTheta("theta1.txt")
#writeTheta("theta2.txt")
writeTrain("train_data_1.csv")
