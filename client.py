#!/usr/bin/env python
import requests
import yaml
import argparse
import pandas as pd
from requests.auth import HTTPBasicAuth

# load actual users and scopes from locked config
with open('gambl_access.yml', 'r') as file:
    user_config = yaml.safe_load(file)

#load any project-specific scopes from user-editable config
with open('gambl_projects.yml', 'r') as file:
    proj_config = yaml.safe_load(file)

api_url = "http://localhost:5678/GAMBL/api/v0.1"


#these arguments aren't all used yet. See hard-coded section at the end

def get_gambl_metadata(url,username,password):
    what = "get_gambl_metadata" #currently the only option
    response = requests.get(f"{api_url}/{what}",auth=HTTPBasicAuth(username,password))
    as_pd = pd.json_normalize(response.json())
    return(as_pd)

def get_coding_ssm(url,username,password,projection,seq_type):
    what = "get_coding_ssm" # this tells the API what GAMBLR function to call
    response = requests.get(f"{api_url}/{what}?projection={projection}&seq_type={seq_type}",auth=HTTPBasicAuth(username,password))
    as_pd = pd.json_normalize(response.json())
    return(as_pd)

def get_combined_sv(url,username,password,projection,seq_type):
    what = "get_combined_sv" # this tells the API what GAMBLR function to call
    response = requests.get(f"{api_url}/{what}?projection={projection}&seq_type={seq_type}",auth=HTTPBasicAuth(username,password))
    as_pd = pd.json_normalize(response.json())
    return(as_pd)

def get_manta_sv(url,username,password,projection):
    what = "get_manta_sv" # this tells the API what GAMBLR function to call
    response = requests.get(f"{api_url}/{what}?projection={projection}",auth=HTTPBasicAuth(username,password))
    as_pd = pd.json_normalize(response.json())
    return(as_pd)

to_test = "manta_sv"
#to_test = "combined_sv"
to_test = "coding_ssm"

for username in user_config['user'].keys():
    print("==================")
    print(f"USER: {username}")
    print(">>>>>>>>>>>>>>>>>>")
    print(username,user_config['user'][username]['password'])
    for project in proj_config['project'].keys():
        if project == "default":
            continue
        print(f"PROJECT: {project}")
        if "projection" in proj_config['project'][project]:
            projection = proj_config['project'][project]["projection"]
        else:
            projection = proj_config['project']['default']["projection"]
        if "seq_type" in proj_config['project'][project]:
            print("seq_type key exists")
            seq_type = proj_config['project'][project]["seq_type"]
        else:
            print('seq_type key not exists')
            print(proj_config['project'][project])
            seq_type = proj_config['project']['default']["seq_type"]
        if to_test == "coding_ssm":
            print(f"TESTING get_coding_ssm with {project}. projection: {projection}, seq_type: {seq_type}")
        
            # TODO: need to eventually elegantly handle functions that allow only a single seq_type at a time!
            if isinstance(seq_type, list):
                for a_seq_type in seq_type:
                    print(f"{projection}, {a_seq_type}")
                    df = get_coding_ssm(api_url,username,user_config['user'][username]['password'],projection,a_seq_type)
                    print(df)
            else:
                print(f"{projection}, {seq_type}")
                df = get_coding_ssm(api_url,username,user_config['user'][username]['password'],projection,seq_type)
                print(df)
        elif to_test == "combined_sv":
            if not "genome" in seq_type:
                continue
                #skip any projects where sv data will not exist
            seq_type = "genome"
            print(f"TESTING get_combined_sv with {project}. projection: {projection}, seq_type: {seq_type}")
            print(f"{projection}, {seq_type}")
            df = get_combined_sv(api_url,username,user_config['user'][username]['password'],project,projection,seq_type)
            print(df)
        elif to_test == "manta_sv":
            if not "genome" in seq_type:
                continue
                #skip any projects where sv data will not exist
            seq_type = "genome"
            print(f"TESTING get_manta_sv with {project}. projection: {projection}")
            df = get_manta_sv(api_url,username,user_config['user'][username]['password'],projection)
            print(df)
        else:
            print("Don't know what to do")