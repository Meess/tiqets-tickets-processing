# Tiqets Tickets Processing

A small python script created for the assignment described in Tiqets Programming Assignment - CSV files.pdf. This framework reads csv files and allows for easy transformation and manipulation of the datasets, e.g. removing rows with empty column values, detecting, extracting and removing of duplicates.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

python 3.4 or higher

### Installing

Create a virtual environment, one way to do to do this is:

```
python3 -m venv ./venv-name
```

This will create a virutalenv in the current folder named venv-name, you can give it any name you prefer. Activate the virtualenv:

```
. venv-name/bin/activate
```
 
Install the requirements from the requirements.txt file. 

```
pip install -r requirements.txt
```

See the Example paragraph for execution of the assignment

### Assignment

To execute the assignment we need an output file, barcodes.csv and orders.csv file.

```
python main.py ./output.txt ./data/barcodes.csv ./data/orders.csv
```

As specified in the assignment the valid orders are written to the output.txt file, errors are logged to stderr and the customers who bought the most valid tickets are written to stdout.

stdout and stderr are ofter written to the terminal without visual difference. The following command makes it more explicit by writing the stdout output to stdout.log and stderr output to stderr.log. 

```
python main-pandas.py ./output.txt ./data/barcodes.csv ./data/orders.csv > >(tee -a stdout.log) 2> >(tee -a stderr.log >&2)
```

An example of the results, for this assignment, is stored in the results directory.

### SQL mockup
Considering a one-to-many relation for customer to order and from order to barcode, the following sql flow derived:
![SQL flow chart]
(https://raw.githubusercontent.com/Meess/tiqets-tickets-processing/master/images/sql.jpg?raw=true)

## Authors

* **Mees Kalf**
