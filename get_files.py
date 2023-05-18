import os
import random

# Get all files in a directory
direc = "adverts"

files = os.listdir(direc)
files = [f for f in files if os.path.isfile(direc+'/'+f)] #Filtering only the files.

# return a random file
def fetch_file():
    return random.choice(files)