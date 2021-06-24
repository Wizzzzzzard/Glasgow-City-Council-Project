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
        print(main_junc)
        return(main_junc)

read_main_junction("1.txt", JunctionSavePath)

raw_df = pd.DataFrame(columns=['Upstream_Node','Upstream_Link','Downstream_Node','Downstream_Link'])

upstream_downstream_pattern = re.compile(r"(\w{2}\d{3}\w*)(?:\s{6})(\w)(?:\s{11})(\w{2}\d{3,4}\w*)(?:\s{4})(\w)") # 1st group usNode, 2nd group usLink, 3rd group dsNode, 4th group dsLink

upstream_pattern1 = re.compile(r"(\w{2}\d{3}\w*)(?:\s{6})(\w)") # 1st group Node, 2nd group Link
upstream_pattern2= re.compile(r"(?:\w\s{56})(\s{2})(\w)") # 1st group space, 2nd group Link
upstream_pattern3= re.compile(r"(?:\w\s{78})(\s{2})(\w)") # 1st group space, 2nd group Link  # Try if line.strip = just \w
downstream_pattern1 = re.compile(r"(?:\s{11})(\w{2}\d{3,4}\w*)(?:\s{4})(\w)") # 1st group Node, 2nd group Link
downstream_pattern2= re.compile(r"(?:\s{32})(\w{2}\d{3,4}\w*)(?:\s{4})(\w)") # 1st group Node, 2nd group Link


#def extract_us_and_ds_data(filename):
#    with open(filename):

links = pd.read_csv("E:/elija/OneDrive/OneDrive - University of Strathclyde/Dissertation/1. Extract Junction and Link Data/Junction Text Files/Sample_Links.csv")

#df = pd.DataFrame(columns=['From Junction','From Node','To Junction','To Node'])