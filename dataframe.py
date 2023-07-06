import random, string
import pandas as pd
import pyperclip

from flask import url_for, request, session

#---------------------------

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

#---------------------------

def csv_function(client_name, key, server="local"):

    df = pd.read_csv("CSV/database.csv")

    if key == "random":
        key = randomword(10)

    client_name = client_name.lower()       # make it lowercase

    # check if client_name is in the database
    if client_name in df["client"].values:
        print("\nclient_name is in the database\n")

        df.loc[df["client"] == client_name, ["key", "server"]] = [key, server]

    else:
        print("client_name is not in the database")

        # add new row to the database
        df.loc[len(df.index)] = [server, client_name, key] 
    
    df.to_csv("CSV/database.csv", index=False)

    return key

#---------------------------

def dataframe_update(dic):

    if "client_local" in dic:

        key = csv_function(dic["client_local"], dic["key"])

        pyperclip.copy(request.root_url + url_for('blueprint.get_file') + "?key=" + key)
        return "local"

    elif "client_drive" in dic: 

        key = csv_function(dic["client_drive"], dic["key"], server=session["name"])

        pyperclip.copy(request.root_url + url_for('blueprint.get_file_drive') + "?key=" + key)
        return "drive"
    
#---------------------------

def key_valid(key, mode):
    
        df = pd.read_csv("CSV/database.csv")
    
        if mode == "local":
            if key in df.loc[df["server"] == "local", "key"].values:
                return True
            else:
                return False
    
        elif mode == "drive":
            if key in df.loc[df["server"] == session["name"], "key"].values:
                return True
            else:
                return False