# Import Location data from API

import http.client, urllib.request, urllib.parse, urllib.error, base64, pandas as pd
from io import BytesIO
import time
import os, os.path, subprocess, re, numpy as np, math

def get_API_positions(page_num):
    headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '62f8d7952d654af6b59958605b79a001',
    }
    
    params = urllib.parse.urlencode({
    })

    for i in range(0,page_num):
        try:
            conn = http.client.HTTPSConnection('gcc.azure-api.net')
            conn.request("GET", "/traffic/v1/movement/now?page={}&format=csv&%s".format(i) % params, "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            df1 = pd.read_csv(BytesIO(data))
            if i == 0:
                df = df1
            else:
                df = df.append(df1)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
    
    # Saves data collected to dataframe with the following columns    
    df.columns = ['latitude', 'longitude', 'flow', 'concentration', 'site', 'lastupdateutc', 'lastupdate', 'timestamp']
    df.to_csv('link_positions.csv')


def load_and_correct_junction_positions():
    EN = pd.read_csv("Traffic Signals Co-ordinates 2021.csv")
    EN_corrections = pd.read_csv("Replacement for Missing Data/missing data eastings and northings corrected bd v1.csv")

get_API_positions(30)

# Sets a savepath to extract each junction's data too
JunctionSavePath = 'E:/elija/OneDrive/OneDrive - University of Strathclyde/Dissertation/1. Extract Junction and Link Data/Junction Text Files/Individual-Junctions/'

# Removes irrelevant lines from the Junction-Links file
def RemoveLines(input_file, output_file, strings= []):
    with open(str(input_file) + ".txt", "r") as file_input:
        with open(str(output_file) + ".txt", "w") as output: 
            for line in file_input:
                if any (s in line.strip("\n") for s in strings) == False:
                    output.write(line)

# Cuts out unneeded section of line, by splitting it on a set delimiter
def TrimLine(input_file, output_file, delimiter, strings= []):
        with open(str(input_file) + ".txt", "r") as file_input:
            with open(str(output_file) + ".txt", "w") as output: 
                for line in file_input:
                    if any (s in line.strip("\n") for s in strings) == True:
                        split_line = line.split(str(delimiter),1)
                        output.write(split_line[0] + "\n")
                    elif any (s in line.strip("\n") for s in strings) == False:
                        output.write(line)

# Separates each Junction and it's related information into it's own text file for easier computer and human manipulation
def split_junctions(input_file):
    save_path = JunctionSavePath
    with open(input_file, 'r') as file:
        i = 0
        output = None
        
        for line in file:
            if not line.strip():
                if output:
                    output.close()
                output = None
            else:
                if output is None:
                    i += 1
                    print(f'Creating file "{i}.txt"')
                    completeName = os.path.join(save_path, str(i)+".txt")
                    output = open(completeName,'w')
                output.write(line)

        if output:
            output.close()
    print('-fini-')

# Combines all previous steps that involve preparing the textfile
def preprocess_text_file():
    # Runs shell script which strips out irrelevant data, to leave only lines between junction name and it's links
    subprocess.run(["bash", "./ext-jun-links.sh","NETL1405.TXT"], shell=True)

    # Removes lines with the strings Modified, Type and Regions 
    strings = ("Modified", "Type", "Region")
    RemoveLines("Junction-Links","Removed-Junction-Links", strings)

    # Splits lines on At and keeps the first half with the parent junction name
    TrimLine("Removed-Junction-Links","Trimmed-Junction-Links", "At", strings=["At"])

    # Splits each junction into it's own text file for future processing
    split_junctions('Trimmed-Junction-Links.txt')

# Finds the savepath for each text file, removes the unnecessary preceding SCN from the junction name, then strips any excess whitespace
def read_main_junction(filename, savepath):
    completeName = os.path.join(savepath, filename)
    with open(completeName) as f:
        main_junc = f.readline()
        main_junc = main_junc.replace('SCN','')
        main_junc = main_junc.strip()
        return(main_junc)

# Creates lists of Junctions and corresponding links
def map_junctions_to_series_to_dataframe(files_in_directory, upstream_pattern1, upstream_pattern2):
    
    # Assigns empty arrays of links and junctions
    links = []
    junctions = []

    # Itereates through each file in junction directory
    for i in files_in_directory:
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
                JunctionSeries = pd.Series(links, dtype='str')
                JunctionSeries = JunctionSeries.str.strip("[()]")

    # Process series and converts into a table of Node to Node connections
    df = JunctionSeries.str.split(', ', expand=True) # Splits Series on ,
    
    # Drops columns with non releveant info
    cols = [2,3]
    df.drop(df.columns[cols],axis=1,inplace=True)

    # Removes quotes from strings
    for j, col in enumerate(df.columns):
        df.iloc[:, j] = df.iloc[:, j].str.replace("'", '')

    # Names Columns and adds To_Node from junctions list to column
    df.columns = ['From_Node', 'To_Link']
    df.insert(1, 'To_Node', junctions)
    df['From'] = df['From_Node']
    df['To'] = df['To_Node'] + "_" + df["To_Link"]

    # Strips all strings of whitespace
    df['From_Node'] = df['From_Node'].str.strip()
    df['To_Link'] = df['To_Link'].str.strip()
    df['From'] = df['From'].str.strip()
    df['To'] = df['To'].str.strip()

    df['hasEntryLink'] = np.where(df['From']== '', True, False) # Marks blank From columns as Entry links for future processing

    df.to_csv('Junction-Links.csv') # Saves output to CSV


# Combines all previous steps including textfile processing up to creating the dataframe
def create_junction_dataframe():
    preprocess_text_file()

    # Using regex to extract upstream node pairs
    upstream_pattern1 = re.compile(r"(\w{2}\d{3}\w*)(?:\s{6})(\w)") # 1st group Node, 2nd group Link
    upstream_pattern2= re.compile(r"(\s{20})(\w)") # 1st group space, 2nd group Link

    # gets list of files in savepath
    arr = os.listdir(JunctionSavePath)

    map_junctions_to_series_to_dataframe(arr, upstream_pattern1, upstream_pattern2)

create_junction_dataframe()

# Loads in Junction Dataframe and Positonal Dataframe
Junctions = pd.read_csv('Junction-Links.csv',float_precision='round_trip')

def Prepare_Positional_Data():
    # Removes all columns bar Site ID and the Eastings and Northings
    Positions = pd.read_csv("Traffic Signals Co-ordinates 2021.csv",float_precision='round_trip')
    Positions = Positions[["FEID", "EASTINGS", "NORTHINGS"]]

    # Loads in Dunbartonshire links
    DD_Positions = pd.read_csv("Replacement for Missing Data/East Dunbartonshire (DD) Links.csv",float_precision='round_trip')

    # Adds DD Link values
    Positions = pd.concat([Positions, DD_Positions])

    # Loads in incorrect or missing links not in Dunbartonshire
    Position_replacement = pd.read_csv("Replacement for Missing Data/missing data eastings and northings corrected bd v1.csv")

    # Replaces incorrect values with corrected values
    Positions.set_index("FEID",inplace=True)
    Position_replacement.set_index("FEID",inplace=True)
    Positions.loc[Position_replacement.index, "EASTINGS"] = Position_replacement["Corrected Eastings"]
    Positions.loc[Position_replacement.index, "NORTHINGS"] = Position_replacement["Corrected Northings"]
    Positions.reset_index(inplace=True)

    Positions.to_csv("Traffic Signals Co-ordinates 2021.csv", index=False)

Prepare_Positional_Data()

From_Positions = pd.read_csv("Traffic Signals Co-ordinates 2021.csv",float_precision='round_trip')
From_Positions.rename(columns={'FEID': 'From'}, inplace=True)

To_Positions = pd.read_csv("Traffic Signals Co-ordinates 2021.csv",float_precision='round_trip')
To_Positions.rename(columns={'FEID': 'To_Node'}, inplace=True)

# Merges Junctions with Positions on From
Junctions = Junctions.merge(From_Positions, left_index=False, right_index=False, how='left', on=['From'])
Junctions.rename(columns={'EASTINGS': 'FROM_EASTINGS', 'NORTHINGS': 'FROM_NORTHINGS'}, inplace=True)

# Merges Junctions with Positions on To_Node
Junctions = Junctions.merge(To_Positions, left_index=False, right_index=False, how='left', on=['To_Node'])
Junctions.rename(columns={'EASTINGS': 'TO_EASTINGS', 'NORTHINGS': 'TO_NORTHINGS'}, inplace=True)

# Drops unneeded index column
Junctions.drop(['Unnamed: 0'], axis=1, inplace=True)

Junctions.drop_duplicates(keep=False, inplace=True)

# Flags all links that are bearings and removes to separate table
bearings = Junctions.loc[Junctions['hasEntryLink'] == True]
Junctions.drop(Junctions.loc[Junctions['hasEntryLink']==True].index, inplace=True)
bearings.to_csv("Bearing_Links.csv")

# Saves complete table to csv file
Junctions.to_csv("BNG Links without Bearings.csv", index=False)