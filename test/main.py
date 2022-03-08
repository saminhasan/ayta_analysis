import json
import socket
import requests
from demo import*

import pandas as pd
import tkinter as tk


class Application(tk.Frame):
	def __init__(self, master=None):
		self.DEVICE_IP = self.find_device()

		super().__init__(master)
		self.master = master
		self.master.geometry("320x240")
		self.pack()
		self.create_widgets()
		self.recording = False

		
	def find_device(self):
		IP = ''
		while True:
			try:
				IP = socket.gethostbyname('raspberrypi.local')
				print(f' Device IP  = {IP}')
				if IP:
					break
			except Exception as e:
				print('Error! Code : {c}, Message :  {m}'.format(c = type(e).__name__, m = str(e)))
				#print(type(e).__name__)
				#if 
				print("Device Not Found")
		return IP
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
		self.inputtxt.insert(tk.END, self.DEVICE_IP)
		self.inputtxt.pack(fill = "both", expand = True, pady=5)


	def started(self):
		self.start.configure(bg="green")
		self.stop.configure(bg="white")
		self.recording = True

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
		df = df.fillna(0)
		df = df.fillna(0)
		#print(df.columns)
		#print(df.head())
		if self.recording and len(df) > 10:
			self.recording = False 
			self.foo(df)

	@staticmethod
	def foo(df):
		show_data(df)
		
		
def main():
	

	
	root = tk.Tk()
	app = Application(master=root)
	app.mainloop()
	'''
	try:
		while True:
			pass
	except KeyboardInterrupt:
		print("KeyboardInterrupt")
	'''
if __name__ == "__main__":
	main()


