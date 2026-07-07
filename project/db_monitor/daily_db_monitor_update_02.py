#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
-----------
The job will extract the info on all the tables in the projects datasets
on the next script i will add a var(argg pars) that chose about witch project i want to work (flag) took from basic 10
and add logs


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
run_time = datetime.now()
uid = str(uuid.uuid4())[:8]

if datasets:
    print("Datasets in project {}:".format(project))
    for dataset in datasets:
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
                "run_time": run_time,
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


# load tables data into a table
dst_table ="my-project-ppltx-sql.bi_final_project.tables_in_project"
dataframe = pd.DataFrame(tables_info_list)


job = client.load_table_from_dataframe(
    dataframe, dst_table #, job_config=job_config
)  # Make an API request.
job.result()  # Wait for the job to complete.

table = client.get_table(dst_table)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), dst_table
    )
)



print('end')



