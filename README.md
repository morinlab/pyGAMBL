# pyGAMBL
## A (nascent) RESTful Python API serving up GAMBL results

### The RESTful api server

This repository currently contains two Python scripts. The `api.py` script will launch a Flask server on the specified port (5678). Only one instance of `api.py` can be run on a server and attempting to run it while the port is in use will result in an error. If the server launches successfully, you should see something like this in your terminal:

```
 * Debugger is active!
 * Debugger PIN: 132-309-303
```

### The client

The `client.py` script provides a simple example demonstrating the functionality of the server. Run it by specifying the full name of the GAMBLR function you want to run. Because this code is in the early stages of development, currently only a few functions are supported.

Example:

To retrieve the metadata as a pandas dataframe:

`./client.py get_coding_ssm`

To retrieve the full coding ssm MAF file as a pandas dataframe (default grch37/genome):

`./client.py get_coding_ssm`


### Quick start (assumes you are on a gphost)

`git clone git@github.com:morinlab/pyGAMBL.git`

`cd pyGAMBL`

`conda activate /projects/rmorin_scratch/for_kostia/pygambl`

`./client.py`
