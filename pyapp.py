import requests
import time
import pandas as pd
import json
import gmplot
from datetime import datetime
import os
SPRINT_VEL_MIN = 1.6

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
	dataframe = pd.DataFrame(data)
	print(dataframe.head())
	'''
	print(dataframe['latitude'])
	print(dataframe['altitude'])
	print(dataframe['velocity'])
	print(dataframe['heading'])
	print(dataframe['time'])
	print(dataframe['latitude'][0], dataframe['longitude'][0], type(dataframe['latitude'][0]), type(dataframe['longitude'][0]))
	'''
	gmap = gmplot.GoogleMapPlotter(dataframe['latitude'][0], dataframe['longitude'][0], 20)
	gmap.heatmap(dataframe['latitude'], dataframe['longitude'])
	now = datetime.now()
	dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
	path = os.getcwd()
	log_path = path + "\\Data\\"
	gmap.draw(log_path + dt_string + ".html")

if __name__ == "__main__":
	print(__file__)
	main()

