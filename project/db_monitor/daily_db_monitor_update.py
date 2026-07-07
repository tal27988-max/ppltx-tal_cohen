#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
-----------
The job will extract the info on all the tables in the projects datasets
this script load data from my ppltx project
on the netxt step i wil load data from public big qurery

Reference
---------
in the readme file

Execution
---------

python ./project/db_monitor/daily_db_monitor_update.py

"""

from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta
import sys
import argparse
import uuid
import os
import platform



from google.cloud import bigquery



# Construct a BigQuery client object.
client = bigquery.Client()


# List of all dataset objects
datasets = list(client.list_datasets())  # Make an API request.

# Get project name
project = client.project

tables_info_list = []

if datasets:
    print("Datasets in project {}:".format(project))
    for dataset in datasets[:2]:
        print("\t{}".format(dataset.dataset_id))
        dataset_id = dataset.dataset_id

        # get table from dataset
        tables = client.list_tables(dataset_id)  # Make an API request.

        # iterate over all tables
        for table_var in tables:
            table_id = ("{}.{}.{}".format(table_var.project, table_var.dataset_id, table_var.table_id))
            print(table_id)
            table = client.get_table(table_id) # Make ana API request
            table_info = {
                # "run_time": run_time,
                # "uid" : uid,
                "project_id": table.project,
                "dataset_id": table.dataset_id,
                "table_id": table.table_id,
                "num_rows": table.num_rows,
                "created": table.created,
                "modified": table.modified,
                "num_bytes": table.num_bytes,
            }
            tables_info_list.append(table_info)
            # print(table_info)


else:
    print("{} project does not contain any datasets.".format(project))

print('end')




# drafy
"""


# View table properties
print(
    "Got table '{}.{}.{}'.".format(table.project, table.dataset_id, table.table_id)
)

print("Table has {} table_id".format(table.table_id))
print("Table has {} dataset_id".format(table.dataset_id))
print("Table has {} rows".format(table.num_rows))
print("Table created on{}".format(table.created))
print("Table modified on {}".format(table.modified))
print("Table has {} bytes".format(table.num_bytes))

"""