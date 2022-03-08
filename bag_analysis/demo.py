import navpy
from bagpy import*
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gmplot

SPRINT_VEL_MIN = 1.6


def lla2ned(df):
	lattitude, longitude, altitude = df['latitude'], df['longitude'], df['altitude']
	North, East, Down =[], [], []

	lat_ref, lon_ref, alt_ref = df['latitude'].mean() ,df['longitude'].mean() ,df['altitude'].mean()

	for i in range(len(lattitude)):
		N, E, D = navpy.lla2ned(lattitude[i], longitude[i],  altitude[i],lat_ref, lon_ref, alt_ref, latlon_unit='deg', alt_unit='m', model='wgs84')
		North.append(N)
		East.append(E)
		Down.append(D)

	df['North'] = North
	df['East'] = East
	df['Down'] = Down

	return df
	
	
def process_data(df):

	North, East, Down = df['North'], df['East'], df['Down'] 
	total_distance, sprint_distance, top_speed = 0, 0, 0
	
	for i in range(len(North)):
		if i > 1 and i < len(North) -1:
			dx = North[i + 1] - North[i - 1]
			dy = East[i + 1] - East[i - 1]
			ds = np.sqrt(dx**2 + dy**2)
			dt = df['time'][i + 1] - df['time'][i - 1]
			heading = df['heading'][i]#np.arctan2(dy,dx)
			velocity  = df['velocity'][i]#ds / dt
			rate = heading / dt
			if velocity > 0.2:
				total_distance += ds
			if velocity > SPRINT_VEL_MIN:
				sprint_distance +=ds

	df['Smoothed_Velocity'] = df['velocity'].ewm(span=10).mean()
	df['Smoothed_Heading'] = df['heading'].ewm(span=10).mean()
	top_speed = df['velocity'].max()
	print(f'Total Distance : {total_distance:.2f} meter	Sprint Distance : {sprint_distance:.2f} meter  Top Speed : {top_speed:.2f} meter/second')
	
	return df


def show_data(arg):

	df_gps =arg
	df_gps = lla2ned(df_gps)
	df_gps= process_data(df_gps)
	df_gps.plot(x ='North', y='East', kind = 'line', legend=False)
	#df_gps.plot(x ='Time', y='Velocity', kind = 'line')
	df_gps.plot(x ='time', y='Smoothed_Velocity', kind = 'line')
	#df_gps.plot(x ='Time', y='Heading', kind = 'line')
	df_gps.plot(x ='time', y='Smoothed_Heading', kind = 'line')
	plt.show()
	#gmap = gmplot.GoogleMapPlotter(df_gps['latitude'][0], df_gps['longitude'][0], 20)
	#gmap.heatmap(df_gps['latitude'], df_gps['longitude'])
	#gmap.draw("Player1.html")
if __name__ == "__main__":
	print(__file__)
	show_data()

