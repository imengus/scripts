#!/bin/bash

# Create a CSV file with the given name
touch "$1.csv"

for file in ~/Documents/notes/medicine/"$1"/0*; do
    # Extract the filename from the full path
    filename="${file##*/}"
    echo "$filename"

    # Run the file2fc.sh script on the current file and append the output to the CSV file
    ./file2fc.sh "$file" "$1.csv"
done

# Remove lines from the CSV file that do not contain a comma
sed -i '/","/!d' "$1.csv"
