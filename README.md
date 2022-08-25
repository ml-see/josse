

# Introduction
Using the JIRA user interface for a couple of open-source projects, it was possible to collect many issues that are software development tasks annotated with description, actual cost, and expert estimates. The data points were gathered in one database named JIRA Open Source Software Effort (JOSSE) dataset. To replicate the dataset from its raw files (.csv files downloaded from JIRA), you can use the python file `csv_2_sqlite.py` inside `dataset_replication`.


## Content

- `JOSSE_18092020.sqlite3`: this is the dataset in form of SQLite. It can be read by and SQLite reader.

- `JOSSE PAPER.pdf`: this is a short paper explaining how the dataset was collected and its rationale. It describes how the data were collected and details six data quality refinement procedures of the data points.

- `dataset_replication`: this folder contains a python script (`csv_2_sqlite.py`) that reads `.csv` files and creates the SQLite database. It also contains a folder (`raw_data`) with all raw data files in `.csv` files as downloaded from their origins, which is explained in the short paper (`JOSSE PAPER.pdf`).


# How to Obtain the JOSSE dataset
The dataset is publicly accessible using its public Github repository. The Github repository URL is: 
https://github.com/ml-see/josse

You also can get an archived version of the replication pack that is stored in Zenodo using it DOI: 10.5281/zenodo.7022735


# How to Replicate the dataset

First, you need to have Python 3 installed. You can follow the instructions from Python official website here [BeginnersGuide/Download - Python Wiki](https://wiki.python.org/moin/BeginnersGuide/Download). 

After installing Python, you can run the conversion python script `csv_2_sqlite.py` to create the dataset SQLite database from raw `.csv` files with this command:

`> python csv_2_sqlite.py`