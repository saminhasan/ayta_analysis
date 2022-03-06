import navpy
from bagpy import*
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import integrate
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch

pd.set_option("display.max_rows", None, "display.max_columns", None)
SHOW_PLOTS = True
def integrate(x, y):
    area = np.trapz(y=y, x=x)
    return area
def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def main(df):

	df['velocity'] = np.sqrt(df['twist.twist.linear.x']**2 + df['twist.twist.linear.y']**2)


	"""
	>>>list(df))
	>>>['Time', 'header.seq', 'header.stamp.secs', 'header.stamp.nsecs', 'header.frame_id', 'child_frame_id', 
	'pose.pose.position.x', 'pose.pose.position.y', 'pose.pose.position.z', 
	'pose.pose.orientation.x', 'pose.pose.orientation.y', 'pose.pose.orientation.z', 'pose.pose.orientation.w', 'pose.covariance', 
	'twist.twist.linear.x', 'twist.twist.linear.y', 'twist.twist.linear.z', 
	'twist.twist.angular.x', 'twist.twist.angular.y', 'twist.twist.angular.z', 'twist.covariance']
	"""
	rows, cols = df.shape
	top_speed = df['velocity'].max()
	avg_speed = df['velocity'].mean()
	df['velocity_smoothed'] = df['velocity'].rolling(window=300).mean()
	total_distance = 0.0
	sprint_distance = 0.0
	for i in range(2,rows - 2):
		if df['velocity_smoothed'][i] > 3/3.6 :
			total_distance += (df['Time'][i + 1] - df['Time'][i-1]) * df['velocity_smoothed'][i] 
		if df['velocity_smoothed'][i] > avg_speed:
				sprint_distance += (df['Time'][i + 1] - df['Time'][i-1]) * df['velocity_smoothed'][i] 
	print("Top Speed : " + str(top_speed), "Average Speed : " + str(avg_speed))
	print("Total Distance : " + str(total_distance) + " Sprint Distance : " + str(sprint_distance))
	if SHOW_PLOTS:
		df.plot(kind='scatter',x='pose.pose.position.x',y='pose.pose.position.y',color='blue')
		plt.show()
		df.plot(kind='line',x='Time',y='velocity_smoothed',color='blue')
		plt.show()

	total_time = df['Time'].max() - df['Time'].min()
	print("Total time : " + str(total_time))

	dframe = pd.DataFrame({'total_time':[total_time],'top_speed':[top_speed], 'total_distance':[total_distance], 'sprint_distance':[sprint_distance]})  

	#dframe['X'] = df['pose.pose.position.x']
	#dframe['Y'] = df['pose.pose.position.y']
	#dframe['Time'] = df['Time'] 
	#dframe['Velocity'] = df['velocity_smoothed']
	dframe = pd.concat([dframe,df['pose.pose.position.x'], df['pose.pose.position.y'], df['Time'], df['velocity']], axis=1, ignore_index=True)

	dframe.columns =['total_time', 'top_speed', 'total_distance', 'total_distance',  'X', 'Y','Time', 'velocity']




	dframe.to_csv('outout.csv', encoding='utf-8')
	#print(df)
if __name__ == "__main__":
	b = bagreader('3.bag')
	#fused = b.message_by_topic('/odometry/filtered')
	gps = b.message_by_topic('/fix')
	df_gps = pd.read_csv(gps)
	#df_fused = pd.read_csv(fused)
	main(df_gps)
	if SHOW_PLOTS:
		sns.kdeplot(df_gps['pose.pose.position.x'], df_gps['pose.pose.position.y'],shade = True,thresh=0.05,alpha=.86,n_levels=1000,cmap = 'RdYlGn_r')
		plt.scatter(df_gps['pose.pose.position.x'], df_gps['pose.pose.position.y'])