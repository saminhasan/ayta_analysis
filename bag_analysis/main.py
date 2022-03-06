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
	Velocity = []
	Heading = []
	
	Velocity.append(0)
	Heading.append(0)
	North, East, Down = df['North'], df['East'], df['Down'] 
	total_distance, sprint_distance, top_speed = 0, 0, 0
	
	for i in range(len(North)):
		if i > 1 and i < len(North) -1:
			dx = North[i + 1] - North[i - 1]
			dy = East[i + 1] - East[i - 1]
			ds = np.sqrt(dx**2 + dy**2)
			dt = df['Time'][i + 1] - df['Time'][i - 1]
			heading = np.arctan2(dy,dx)
			velocity  = ds / dt
			rate = heading / dt
			total_distance += ds
			if velocity > SPRINT_VEL_MIN:
				sprint_distance +=ds
			Velocity.append(velocity)
			Heading.append(rate)

	Velocity.append(0)
	Velocity.append(0)
	Heading.append(0)
	Heading.append(0)

	df['Velocity'] = Velocity
	df['Heading'] = Heading
	df['Smoothed_Velocity'] = df['Velocity'].ewm(span=10).mean()
	df['Smoothed_Heading'] = df['Heading'].ewm(span=10).mean()
	top_speed = df['Velocity'].max()
	print(f'Total Distance : {total_distance:.2f} meter	Sprint Distance : {sprint_distance:.2f} meter  Top Speed : {top_speed:.2f} meter/second')
	
	return df


def main():
	b = bagreader('4.bag')
	
	"""
	print(b.topic_table)
	[INFO]  Data folder 3 already exists. Not creating.
				  Topics                      Types       Message Count   Frequency
	0                   /fix      sensor_msgs/NavSatFix            239    0.999844
	1        /gy_87/imu_data            sensor_msgs/Imu          23622  100.026328
	2  /gy_87/magnetic_field  sensor_msgs/MagneticField          23611  100.083612
	
	"""
	
	
	gps_data = b.message_by_topic('/fix')
	imu_data = b.message_by_topic('/gy_87/imu_data')
	mag_data = b.message_by_topic('/gy_87/magnetic_field')

	df_gps = pd.read_csv(gps_data)
	df_imu = pd.read_csv(imu_data)
	df_mag = pd.read_csv(mag_data)
	
	
	"""
	print(df_gps.columns)
	Index(['Time', 'header.seq', 'header.stamp.secs', 'header.stamp.nsecs',
		   'header.frame_id', 'status.status', 'status.service', 'latitude',
		   'longitude', 'altitude', 'position_covariance_0',
		   'position_covariance_1', 'position_covariance_2',
		   'position_covariance_3', 'position_covariance_4',
		   'position_covariance_5', 'position_covariance_6',
		   'position_covariance_7', 'position_covariance_8',
		   'position_covariance_type'],
		  dtype='object')
	"""


	df_gps = lla2ned(df_gps)
	df_gps= process_data(df_gps)
	df_gps.plot(x ='North', y='East', kind = 'scatter')
	df_gps.plot(x ='Time', y='Velocity', kind = 'line')
	df_gps.plot(x ='Time', y='Smoothed_Velocity', kind = 'line')
	df_gps.plot(x ='Time', y='Heading', kind = 'line')
	df_gps.plot(x ='Time', y='Smoothed_Heading', kind = 'line')
	plt.show()
	gmap = gmplot.GoogleMapPlotter(df_gps['latitude'][0], df_gps['longitude'][0], 20)
	gmap.heatmap(df_gps['latitude'], df_gps['longitude'])
	gmap.draw("Player1.html")
if __name__ == "__main__":
	print(__file__)
	main()

