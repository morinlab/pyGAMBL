#!/usr/bin/env python
from flask import Flask, jsonify, make_response, request
import pandas as pd
import os
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import yaml

verbose = True
#location = "remote"
location = "GSC"

# load and set paths from config
with open('config.yml', 'r') as file:
    config_all = yaml.safe_load(file)

if location == "remote":
    REPO_BASE = config_all['remote']['repo_base']
    GAMBL_BASE = config_all['remote']['project_base']
else:
    REPO_BASE = config_all['default']['repo_base']
    GAMBL_BASE = config_all['default']['project_base'] + "/results/"

gamblr_script = "./run_gamblr_function.R"
METADATA_FILE = f"{REPO_BASE}/data/metadata/gambl_samples_available.tsv"

auth = HTTPBasicAuth()

# load actual users and scopes from locked config
with open('gambl_access.yml', 'r') as file:
    user_config = yaml.safe_load(file)

users = {}
user_scope = {}
project_scope = {}
for user in user_config['user'].keys():
    users[user] = user_config['user'][user]['password']
    user_scope[user] = user_config['user'][user]['scope']

with open('gambl_projects.yml', 'r') as file:
    proj_config = yaml.safe_load(file)

for proj in proj_config['project'].keys():
    if 'scope' in proj_config['project'][proj]:
        project_scope[proj] = proj_config['project'][proj]['scope']

print("USERS:")
print(users)
print("SCOPES:")
print(user_scope)
print("PROJECTS:")
print(project_scope)
print("-------")
app = Flask(__name__)

print("LOADING METADATA")
metadata = pd.read_csv(METADATA_FILE,delimiter="\t")

if verbose:
    print(metadata)

@auth.verify_password
def verify_password(username, password):
    if username in users and password == users.get(username):
        return username

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/GAMBL/api/v0.1/get_gambl_metadata', methods=['GET'])
@auth.login_required
def get_gambl_metadata():
    some_metadata = subset_df(metadata,auth.current_user())
    print(f"USER: {auth.current_user()}")
    return some_metadata.to_json(orient="records") #return data frame in json format that is easily converted back to a data frame

@app.route('/GAMBL/api/v0.1/get_coding_ssm', methods=['GET'])
@auth.login_required
def get_coding_ssm():
    some_metadata = subset_df(metadata,auth.current_user())
    cmd = f"{gamblr_script} --function_name get_coding_ssm --args"
    for arg in request.args:
        cmd = cmd + f" {arg}={request.args[arg]}"
    coding_ssm_df = pd.read_csv(os.popen(cmd),delimiter="\t")
    #Important! All of these functions must drop rows this user is not allowed to see per the scope in the gambl_acces.yml file (stored in user_scope)
    coding_ssm_df = coding_ssm_df[coding_ssm_df["Tumor_Sample_Barcode"].isin(some_metadata["sample_id"])]
    
    print(coding_ssm_df)
    return coding_ssm_df.to_json(orient="records")

@app.route('/GAMBL/api/v0.1/get_combined_sv', methods=['GET'])
@auth.login_required
def get_combined_sv():
    if 'project' in request.args:
        project = request.args['project']
    else:
        project = "default"
    if 'projection' in request.args:
        print(f"PROJECTION:{request.args['projection']}")
        projection = request.args['projection']
    else:
        projection = proj_config['project'][project]['projection']
    
    if 'seq_type' in request.args:
        seq_type = request.args['seq_type']
    else:
        seq_type = proj_config['project'][project]['seq_type']
    
    some_metadata = subset_df(metadata,auth.current_user())
    print(some_metadata)
    this_df = pd.read_csv(os.popen(f"{gamblr_script} --function_name get_combined_sv --args projection={projection}"),delimiter="\t")
    this_df = this_df[this_df["tumour_sample_id"].isin(some_metadata["sample_id"])]
    #drop rows this user is not allowed to see
    print(this_df)
    return this_df.to_json(orient="records")

@app.route('/GAMBL/api/v0.1/get_manta_sv', methods=['GET'])
@auth.login_required
def get_manta_sv():
    some_metadata = subset_df(metadata,auth.current_user())
    print(some_metadata)
    cmd = f"{gamblr_script} --function_name get_manta_sv --args"
    for arg in request.args:
        cmd = cmd + f" {arg}={request.args[arg]}"
    print(cmd)
    this_df = pd.read_csv(os.popen(cmd),delimiter="\t")
    this_df = this_df[this_df["tumour_sample_id"].isin(some_metadata["sample_id"])]
    #drop rows this user is not allowed to see
    print(this_df)
    return this_df.to_json(orient="records")


def subset_df(df,username,project=""):
    this_scope = user_scope[username]
    print(this_scope)
    new_df = df
    for column in this_scope.keys():
        print(f"SCOPE {column} {this_scope[column]}")
        print(type(this_scope[column]))
        new_df = new_df[new_df[column].isin(this_scope[column])]
    if project == "":
        return(new_df)
    this_scope = project_scope[project]
    print(new_df)
    print(this_scope)
    for column in this_scope.keys():
        print(f"SCOPE {column} {this_scope[column]}")
        print(type(this_scope[column]))
        new_df = new_df[new_df[column].isin(this_scope[column])]
    print(new_df)
    return(new_df)



if __name__ == '__main__':
    app.run(debug=True,port=5678)
