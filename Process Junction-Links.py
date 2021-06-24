import os.path
import subprocess
import re

separateJunctionSavePath = 'E:/elija/OneDrive/OneDrive - University of Strathclyde/Dissertation/1. Extract Junction and Link Data/Junction Text Files/Individual-Junctions/'

subprocess.run(["bash", "./ext-jun-links.sh","NETL1405.TXT"], shell=True)

# Removes irrelevant lines from the Junction-Links file

def RemoveLines(input_file, output_file, strings= []):
    with open(str(input_file) + ".txt", "r") as file_input:
        with open(str(output_file) + ".txt", "w") as output: 
            for line in file_input:
                if any (s in line.strip("\n") for s in strings) == False:
                    output.write(line)

# Cuts out unneeded section of line

def TrimLine(input_file, output_file, delimiter, strings= []):
        with open(str(input_file) + ".txt", "r") as file_input:
            with open(str(output_file) + ".txt", "w") as output: 
                for line in file_input:
                    if any (s in line.strip("\n") for s in strings) == True:
                        split_line = line.split(str(delimiter),1)
                        output.write(split_line[0] + "\n")
                    elif any (s in line.strip("\n") for s in strings) == False:
                        output.write(line)

# Removes gap between link and letter denotation

def RemoveLinkSpace(input_file, output_file, pattern):
    with open(str(input_file) + ".txt", "r") as file_input:
        with open(str(output_file) + ".txt", "w") as output: 
            for line in file_input:
                line = re.sub(pattern,r"\1_\2", line)
                output.write(line)

strings = ("Modified", "Type", "Region")
RemoveLines("Junction-Links","Clean-Junction-Links", strings)

TrimLine("Clean-Junction-Links","Clean-Junction-Links1", "At", strings=["At"])

# As pattern will be used multiple times, compile
upstream_pattern = re.compile(r"([A-Z]{2}[0-9]{3}[0-9A-Z])[ ]{6,}([A-Z])")
downstream_pattern = re.compile(r"([A-Z]{2}[0-9]{3}[0-9A-Z])[ ]{4,}([A-Z])")
delimiter_pattern = re.compile(r"\n\s{80}")

#RemoveLinkSpace("Clean-Junction-Links1","Clean-Junction-Links2",upstream_pattern)
#RemoveLinkSpace("Clean-Junction-Links2","Clean-Junction-Links3",downstream_pattern)

def split_junctions(input_file):
    save_path = separateJunctionSavePath
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

split_junctions('Clean-Junction-Links1.txt')
