#!/bin/bash

# List all files recursively, extract full paths, shuffle, and pick 75
gsutil ls -lR gs://arxiv-dataset/arxiv/arxiv/pdf/2509/ \
  | awk '{print $NF}' \
  | shuf -n 75 > pick.txt

# Download only the selected files
gsutil -o "GSUtil:parallel_process_count=1" \
       -m cp -I ./raw/ < pick.txt

