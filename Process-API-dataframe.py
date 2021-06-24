import pandas as pd, numpy as np

df = pd.read_csv('link_positions.csv')
link_lat_long = df[["site", "latitude", "longitude"]]
# print(link_lat_long.site.unique())
# print(link_lat_long.pivot_table(index=['site'], aggfunc='size'))

link_lat_long = link_lat_long.drop_duplicates(subset='site', keep="first")
link_lat_long.to_csv('link_positions.csv')