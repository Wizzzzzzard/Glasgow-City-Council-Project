import os.path
import subprocess
import re
import math
import pandas as pd
import numpy as np


links = pd.read_csv("E:/elija/OneDrive/OneDrive - University of Strathclyde/Dissertation/1. Extract Junction and Link Data/Junction Text Files/Sample_Links.csv")
positions = pd.read_csv('E:/elija/OneDrive/OneDrive - University of Strathclyde/Dissertation/1. Extract Junction and Link Data/API/link_positions.csv')

links["From"] = links["From_Node"] + "_" + links["From_Link"]
links["To"] = links["To_Node"] + "_" + links["To_Link"]

links = links.astype(str)

links = pd.merge(links, positions, how='left', left_on='From', right_on= 'site')
links = pd.merge(links, positions, how='left', left_on='To', right_on= 'site')

links.drop(['Unnamed: 0_x', 'site_x', 'Unnamed: 0_y', 'site_y'], axis=1, inplace=True)
links.columns = ['From_Node', 'From_Link', 'To_Node', 'To_Link', 'From', 'To', 'From_Lat', 'From_Long', 'To_Lat', 'To_Long']

#links["Bearing"] = get_bearing(links["From_Lat"], links["From_Long"], links["To_Lat"], links["To_Long"])

print(links)
links.to_csv('example_link.csv')
#print(positions)