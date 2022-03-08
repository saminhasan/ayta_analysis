import os
import navpy
import time
import json
import gmplot
import requests
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from datetime import datetime

from demo import*


class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.master.geometry("320x240")
		self.pack()
		self.create_widgets()

	def create_widgets(self):
		self.start = tk.Button(self)
		self.start["text"] = "Start"
		self.start["command"] = self.started
		self.start.pack(fill = "both", expand = True, pady=5)

		self.stop = tk.Button(self)
		self.stop["text"] = "Stop"
		self.stop["command"] = self.stoped
		self.stop.pack(fill = "both", expand = True, pady=5)
		
		# TextBox Creation
		self.inputtxt = tk.Text(self, height = 1, width = 24)
		self.inputtxt.insert(tk.END, "192.168.1.109")
		self.inputtxt.pack(fill = "both", expand = True, pady=5)


	def started(self):
		self.start.configure(bg="green")
		self.stop.configure(bg="white")
		print("Command Sent: start")
		inp = self.inputtxt.get(1.0, "end-1c")
		#print(inp)
		start_cmd = "http://"+ str(inp) +":5000/start"
		resp = requests.get(start_cmd)
		print(resp.status_code)
		print(resp.text)

	
	def stoped(self):
		self.start.configure(bg="white")
		self.stop.configure(bg="red")
		print("Command Sent: Stoped")
		inp = self.inputtxt.get(1.0, "end-1c")
		#print(inp)
		stop_cmd = "http://"+ str(inp) +":5000/stop"
		data = requests.get(stop_cmd)
		print(data.status_code)
		data = json.loads(data.text)
		df = pd.DataFrame(data)
		#print(df.columns)
		print(df.head())

		self.foo(df)

	@staticmethod
	def foo(df):

		total_distance, sprint_distance, top_speed = 0, 0, 0
		gmap = gmplot.GoogleMapPlotter(df['latitude'][0], df['longitude'][0], 20)
		gmap.heatmap(df['latitude'], df['longitude'])
		now = datetime.now()
		dt_string = now.strftime("%Y-%m-%d-%H-%M-%S")
		path = os.getcwd()
		log_path = path #+ "\\Data\\"
		gmap.draw(log_path + dt_string + ".html")
		top_speed = df['velocity'].max()
		print(f'Total Distance : {total_distance:.2f} meter	Sprint Distance : {sprint_distance:.2f}')
		show_data(df)
def main():
	try:
		root = tk.Tk()
		app = Application(master=root)
		app.mainloop()
		'''
		while True:
			pass
		'''
	except KeyboardInterrupt:
		print("KeyboardInterrupt")
if __name__ == "__main__":
	main()


