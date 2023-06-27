# pyGAMBL
## A (nascent) RESTful Python API serving up GAMBL results

This repository currently contains two Python scripts. The `api.py` script will launch a Flask server on the specified port (5678). Only one instance of `api.py` can be run on a server and attempting to run it while the port is in use will result in an error. 

### Quick start (assumes you are on a gphost)

`git clone git@github.com:morinlab/pyGAMBL.git`

`cd pyGAMBL`

`conda activate /projects/rmorin_scratch/for_kostia/pygambl`

`./client.py`
