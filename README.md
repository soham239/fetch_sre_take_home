# FETCH SRE TAKE HOME

### Description

The given program in 'health_check.py' file runs health checks every 15 secs for a list of endpoints passed to it using YAML format and prints out the cumulative availability percentage values to the console.

### Pre-requisites to run

Make sure you have Python3 installed with 'pyyaml' and 'requests' packages. If using pip3 manager, simply run:

```Bash
pip3 install -r requirements.txt
```

### Command to run

Using python3, have your input config YAML file in the same folder and pass it as an argument to the command line like:

```Bash
python3 health_check.py <your_yaml_file>
```

An example would look like (using sample.yaml given in original prompt)

```Bash
python3 health_check.py sample.yaml
```

Press Ctrl+C to terminate the program

### Results Display in Command Line

Results are displayed as '<domain_name> has <availability_percentage_value> availability percentage'

For example:

```Bash
fetch.com has 67% availability percentage
www.fetchrewards.com has 100% availability percentage
```