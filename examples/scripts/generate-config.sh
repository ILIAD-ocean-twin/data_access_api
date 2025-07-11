#!/bin/bash

# Usage: ./concat_files.sh output.txt file1.txt file2.txt ...

# Check if at least two arguments are provided (output file + at least one input file)
if [ "$#" -lt 2 ]; then
  echo "Usage: $0 output_file input_file1 [input_file2 ...]"
  exit 1
fi

# Extract the output file name
output_file="$1"
shift

# Concatenate all input files into the output file
cat "$@" > "$output_file"

echo "Files concatenated into $output_file"
