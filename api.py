#!/usr/bin/env python
from flask import Flask, jsonify, make_response
import pandas as pd
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
auth = HTTPBasicAuth()

users = {
    "GAMBLR": "letmein",
    "undergrad": "opensesame"
}

#how data will be subset per user/group
user_scope = {
    "undergrad": {"unix_group":["gambl"]},
    "GAMBLR": {"unix_group":["gambl","icgc_dart"]}
}

GAMBL_BASE = "/projects/rmorin/projects/gambl-repos/gambl-kdreval/"
METADATA_FILE = f"{GAMBL_BASE}/data/metadata/gambl_samples_available.tsv"

app = Flask(__name__)

print("LOADING METADATA")
metadata = pd.read_csv(METADATA_FILE,delimiter="\t")

print(metadata)

@auth.verify_password
def verify_password(username, password):
    if username in users and password == users.get(username):
        return username

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.route('/GAMBL/api/v0.1/metadata', methods=['GET'])
@auth.login_required
def get_gambl_metadata():
    some_metadata = subset_df(metadata,auth.current_user())
    print(f"USER: {auth.current_user()}")
    return some_metadata.to_json(orient="records") #return data frame in json format that is easily converted back to a data frame

def subset_df(df,username):
    this_scope = user_scope[username]
    new_df = df
    for column in this_scope.keys():
        print(f"SCOPE {column} {this_scope[column]}")
        new_df = new_df[new_df[column].isin(this_scope[column])]
    return(new_df)



if __name__ == '__main__':
    app.run(debug=True,port=5678)