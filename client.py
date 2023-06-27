#!/usr/bin/env python
import requests
import argparse
import pandas as pd
from requests.auth import HTTPBasicAuth

# currently the demo just has one function that gets the contents of gambl_samples_available
parser = argparse.ArgumentParser(
                    prog='GAMpyLER',
                    description='Demo of the Python companion to GAMBL and GAMBLR')

# TODO: update help to say what functions are available
parser.add_argument('function_name')


username = "GAMBLR"
password = "letmein"
# comment out the two lines below to see what happens for GAMBLR users, who have a more complete "scope" of data access
#username = "undergrad"
#password = "opensesame"

#password = "wrongpassword"

api_url = "http://localhost:5678/GAMBL/api/v0.1"

args = parser.parse_args()
function_name = args.function_name

def get_gambl_metadata(url):
    what = "metadata" #currently the only option
    #what = "nothing" #for testing
    response = requests.get(f"{api_url}/{what}",auth=HTTPBasicAuth(username,password))
    as_pd = pd.json_normalize(response.json())
    return(as_pd)

def get_coding_ssm(url):
    what = "coding_ssm" #currently the only option
    #what = "nothing" #for testing
    response = requests.get(f"{api_url}/{what}",auth=HTTPBasicAuth(username,password))
    as_pd = pd.json_normalize(response.json())
    return(as_pd)

if(function_name=="get_gambl_metadata"):
    print("TESTING get_gambl_metadata")
    meta = get_gambl_metadata(url=api_url)
    print(meta)
elif(function_name=="get_coding_ssm"):
    print("TESTING get_coding_ssm")
    df = get_coding_ssm(url=api_url)
    print(df)
else:
    print(f"function {function_name} not supported")
