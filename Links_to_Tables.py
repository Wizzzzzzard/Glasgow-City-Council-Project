import os
import os.path
import subprocess
import re
import pandas as pd
import numpy as np

JunctionSavePath = 'E:/elija/OneDrive/OneDrive - University of Strathclyde/Dissertation/1. Extract Junction and Link Data/Junction Text Files/Individual-Junctions/'

def read_main_junction(filename, savepath):
    completeName = os.path.join(savepath, filename)
    with open(completeName) as f:
        main_junc = f.readline()
        main_junc = main_junc.replace('SCN','')
        main_junc = main_junc.strip()
        return(main_junc)

#upstream_downstream_pattern = re.compile(r"(\w{2}\d{3}\w*)(?:\s{6})(\w)(?:\s{11})(\w{2}\d{3,4}\w*)(?:\s{4})(\w)") # 1st group usNode, 2nd group usLink, 3rd group dsNode, 4th group dsLink

upstream_pattern1 = re.compile(r"(\w{2}\d{3}\w*)(?:\s{6})(\w)") # 1st group Node, 2nd group Link
upstream_pattern2= re.compile(r"(\s{20})(\w)") # 1st group space, 2nd group Link  # Try if line.strip = just \w
#downstream_pattern1 = re.compile(r"(?:\s{11})(\w{2}\d{3,4}\w*)(?:\s{4})(\w)") # 1st group Node, 2nd group Link
#downstream_pattern2= re.compile(r"(?:\s{32})(\w{2}\d{3,4}\w*)(?:\s{4})(\w)") # 1st group Node, 2nd group Link

arr = os.listdir(JunctionSavePath)

links = []
junctions = []
for i in arr:
    completeName = os.path.join(JunctionSavePath, i)
    with open(completeName) as f:
        for line in f:
            if re.search(upstream_pattern1, line):
                links.append(re.findall(upstream_pattern1, line))
                junctions.append(read_main_junction(i, JunctionSavePath))
            if re.search(upstream_pattern2, line):
                links.append(re.findall(upstream_pattern2, line))
                junctions.append(read_main_junction(i, JunctionSavePath))
            links = list(filter(None, links))
            links = list(map(str, links))
            mySeries = pd.Series(links, dtype='str')
            mySeries = mySeries.str.strip("[()]")


df = mySeries.str.split(', ', expand=True)
cols = [2,3]
df.drop(df.columns[cols],axis=1,inplace=True)
for j, col in enumerate(df.columns):
    df.iloc[:, j] = df.iloc[:, j].str.replace("'", '')
df.columns = ['From_Node', 'To_Link']
df.insert(1, 'To_Node', junctions)
df['From'] = df['From_Node']
df['To'] = df['To_Node'] + "_" + df["To_Link"]

df['From_Node'] = df['From_Node'].str.strip()
df['To_Link'] = df['To_Link'].str.strip()
df['From'] = df['From'].str.strip()
df['To'] = df['To'].str.strip()

df['hasEntryLink'] = np.where(df['From']== '', True, False)

df.to_csv('Junction-Links.csv')
print(df)




#print(df)

#links = pd.read_csv("E:/elija/OneDrive/OneDrive - University of Strathclyde/Dissertation/1. Extract Junction and Link Data/Junction Text Files/Sample_Links.csv")


#df = pd.DataFrame(columns=['From Junction','From Node','To Junction','To Node'])