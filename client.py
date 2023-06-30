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
parser.add_argument('seq_type')
parser.add_argument('projection')

username = "GAMBLR"
password = "letmein"
# comment out the two lines below to see what happens for GAMBLR users, who have a more complete "scope" of data access
username = "undergrad"
password = "opensesame"

#username="reddy"
#password="reddyornot"
#password = "wrongpassword"

api_url = "http://localhost:5678/GAMBL/api/v0.1"

args = parser.parse_args()
function_name = args.function_name
projection = args.projection
seq_type = args.seq_type

#these arguments aren't all used yet. See hard-coded section at the end

def get_gambl_metadata(url):
    what = "metadata" #currently the only option
    #what = "nothing" #for testing
    response = requests.get(f"{api_url}/{what}",auth=HTTPBasicAuth(username,password))
    as_pd = pd.json_normalize(response.json())
    return(as_pd)

def get_coding_ssm(url,projection,seq_type):
    what = "coding_ssm" #currently the only option
    #what = "nothing" #for testing
    #test_url = f"{api_url}/{what}?projection={projection}&seq_type={seq_type}"
    #print(test_url)
    #response = requests.get(f"{api_url}/{what}",auth=HTTPBasicAuth(username,password))
    response = requests.get(f"{api_url}/{what}?projection={projection}&seq_type={seq_type}",auth=HTTPBasicAuth(username,password))
    as_pd = pd.json_normalize(response.json())
    return(as_pd)


print("TESTING get_coding_ssm")
print("hg38, capture")
df = get_coding_ssm(api_url,"hg38","capture")
print(df)

print("grch37, genome")
df = get_coding_ssm(api_url,"grch37","genome")
print(df)

