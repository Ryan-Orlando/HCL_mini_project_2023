import os
import random
from werkzeug.utils import secure_filename

# Get all files in a directory
direc = "adverts"

# return a random file
def fetch_file():
    files = os.listdir(direc)
    files = [f for f in files if os.path.isfile(direc+'/'+f)] #Filtering only the files.
    return random.choice(files)

def upload_file(file):
    filename = secure_filename(file.filename)
    file.save(os.path.join(direc, filename))