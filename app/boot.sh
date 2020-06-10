#!/usr/bin/env bash

python3 run_write_data_s3.py create_db
python3 run_write_data_s3.py ingest
python3 app.py