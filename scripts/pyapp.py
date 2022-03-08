import os
import navpy
import time
import json
import gmplot
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


SPRINT_VEL_MIN = 1.6


def foo(df):

	total_distance, sprint_distance, top_speed = 0, 0, 0
	gmap = gmplot.GoogleMapPlotter(df['latitude'][0], df['longitude'][0], 20)
	gmap.heatmap(df['latitude'], df['longitude'])
	now = datetime.now()
	dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
	path = os.getcwd()
	log_path = path + "\\Data\\"
	gmap.draw(log_path + dt_string + ".html")
	top_speed = df['velocity'].max()
	print(f'Total Distance : {total_distance:.2f} meter	Sprint Distance : {sprint_distance:.2f} meter  Top Speed : {top_speed:.2f} meter/second')
	
	
def main():
	start_cmd = "http://192.168.1.105:5000/start"
	resp = requests.get(start_cmd)
	print(resp.status_code)
	print(resp.text)
	time.sleep(10)
	stop_cmd = "http://192.168.1.105:5000/stop"
	data = requests.get(stop_cmd)
	print(data.status_code)
	data = json.loads(data.text)
	df = pd.DataFrame(data)
	foo(df)
	#print(df.head())
	'''
	print(df['latitude'])
	print(df['altitude'])
	print(df['velocity'])
	print(df['heading'])
	print(df['time'])
	print(df['latitude'][0], df['longitude'][0], type(df['latitude'][0]), type(df['longitude'][0]))
	'''
	
if __name__ == "__main__":
	print(__file__)
	main()

