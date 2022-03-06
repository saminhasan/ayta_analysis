import navpy
from bagpy import*
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import integrate
import matplotlib.pyplot as plt
plt.axis("equal")
b1 = bagreader('3.bag')
g1 = b1.message_by_topic('/fix')
g1_df = pd.read_csv(g1)
w = 3
g1_df['latitude'] = g1_df['latitude'].rolling(window=w).mean()
g1_df['longitude'] = g1_df['longitude'].rolling(window=w).mean()

plt.plot(g1_df["longitude"], g1_df["latitude"])
plt.show()