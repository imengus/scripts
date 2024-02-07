#!/bin/bash

# Extract flashcards between the headings of List-like and Personal interest
flashcards="$(awk '/## List-like/,/## Personal interest/ { if (!/## List-like|## Personal interest/) print }' "$1")"

# Untick flashcards, replace double tabs with HTML line breaks, and put quotes around questions and answers
flashcards="$(
    awk '{ gsub(/- \[x\]/, "- [ ]") }1' <<< "$flashcards" |
    awk '{ gsub(/\t\t- \[ \] /, " <br>\&nbsp - "); gsub(/\t- \[ \] /, "\"NEWLINE\"") }1' |
    awk '/NEWLINE/ { sub(/\?/, "?\",\"") } END {print "\""} 1'
)"

# Remove first 8 characters to get rid of extra NEWLINE, then remove all newlines and replace NEWLINE with line breaks
# Each question and answer pair is on a single line delimited by a comma
formatted_flashcards="$(
    echo "${flashcards:8}" |
    tr -d '\n' |
    sed "s/NEWLINE/\n/g"
)"

# Append formatted flashcards to the specified output file
if [[ "${formatted_flashcards:0:2}" != "\"\"" ]]; then
    echo "$formatted_flashcards" >> "$2"
fi
