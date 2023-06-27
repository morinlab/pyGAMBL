#!/usr/bin/env python
from flask import Flask, jsonify, make_response
import pandas as pd
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth = HTTPBasicAuth()

# a few phoney accounts for debugging authentication
# TODO: update this to read user account details from a local file readable only by the person who will run this server
users = {
    "GAMBLR": "letmein",
    "undergrad": "opensesame"
}

#how data will be subset per user/group.
# TODO: the scope of user accesss will also be determined by the user file mentioned above. 
# Notably, scope can also be limited to include/exclude any specific cohort(s) with some minor changes to this code
user_scope = {
    "undergrad": {"unix_group":["gambl"]},
    "GAMBLR": {"unix_group":["gambl","icgc_dart"]}
}

GAMBL_BASE = "/projects/rmorin/projects/gambl-repos/gambl-kdreval/"
METADATA_FILE = f"{GAMBL_BASE}/data/metadata/gambl_samples_available.tsv"

app = Flask(__name__)

print("LOADING METADATA")
metadata = pd.read_csv(METADATA_FILE,delimiter="\t")

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

@app.route('/GAMBL/api/v0.1/coding_ssm', methods=['GET'])
@auth.login_required
def get_coding_ssm(projection="grch37",seq_type="genome"):
    some_metadata = subset_df(metadata,auth.current_user())
    some_metadata = some_metadata[some_metadata["seq_type"]==seq_type]
    CODING_SSM_FILE = f"{GAMBL_BASE}/results/all_the_things/slms_3-1.0_vcf2maf-1.3/{seq_type}--projection/deblacklisted/augmented_maf/all_slms-3--{projection}.CDS.maf"
    # temporary code for debugging and benchmarking
    print(f"loading {CODING_SSM_FILE}")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Start Time =", current_time)
    coding_maf = pd.read_csv(CODING_SSM_FILE,delimiter="\t")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Completion Time =", current_time)
    #TODO: Subset the mAF based on the sample_id in some_metadata
    return coding_maf.to_json(orient="records")

def subset_df(df,username):
    this_scope = user_scope[username]
    new_df = df
    for column in this_scope.keys():
        print(f"SCOPE {column} {this_scope[column]}")
        new_df = new_df[new_df[column].isin(this_scope[column])]
    return(new_df)



if __name__ == '__main__':
    app.run(debug=True,port=5678)
