#!/bin/bash

# Initialize variables
max_size=0
total_size=0
total_ticked=0
content_sizes=()
file_names=()
file_contents=()
tick_counts=()
box_counts=()

# Iterate through files
for file_path in ~/Documents/notes/medicine/"$1"/0*; do
    # Extract file name without extension
    file_name="$(basename "$file_path")"
    file_name="${file_name%.*}"

    # Get file content between specified headings
    file_content="$(awk '/## Quick/,/## Terms/ { if (!/## Quick|## Terms/) print }' "$file_path")"

    # Count ticks and boxes in the content
    tick_count=$(echo "$file_content" | sed -n "s/\[x\]/&/gp" | wc -l)
    box_count=$(echo "$file_content" | sed -n "s/-\ \[/&/gp" | wc -l)

    total_ticked=$((tick_count + total_ticked))
    total_box=$((box_count + total_box))

    # Get content size
    content_size=$(echo "$file_content" | wc -m)

    # Store size, name, content, and counts in arrays
    content_sizes+=($((content_size + 1)))
    file_names+=("$file_name")
    file_contents+=("$file_content")
    tick_counts+=("$tick_count")
    box_counts+=("$box_count")

    # Calculate total size
    total_size=$((content_size + total_size))

    # Find maximum size
    if ((content_size > max_size)); then
        max_size=$((content_size))
    fi

    # Check if file is reviewed
    reviewed="${file_name:3:1}"
    if [[ $reviewed = "i" ]]; then
        total_rev=$((content_size + total_rev))
    fi
done

# Display bar chart
for index in "${!content_sizes[@]}"; do
    size="${content_sizes[index]}"
    name="${file_names[index]}"
    content="${file_contents[index]}"
    n_tick="${tick_counts[index]}"
    n_box="${box_counts[index]}"

    bar_size=50
    frac1=$(echo "scale=3; $size / ($max_size+0.01) * $bar_size" | bc)
    n_bars=$(printf "%.0f" "$frac1")
    remain=$((bar_size - n_bars))

    frac2=$(echo "scale=3; $n_tick / ($n_box+0.01) * $n_bars" | bc)
    n_solid=$(printf "%.0f" "$frac2")
    n_hash=$((n_bars - n_solid))

    # Display bars
    for ((i = 1; i <= remain; i++)); do
        echo -n "_"
    done
    for ((i = 1; i <= n_hash; i++)); do
        echo -n "▒"
    done
    for ((i = 1; i <= n_solid; i++)); do
        echo -n "▓"
    done

    # Display file name
    echo "|${name}"
done

# Display review and knowledge acquisition percentages
echo "$(printf "%.1f" "$(echo "scale=3; $total_rev / $total_size * 100" | bc)")% of files reviewed"
echo "$(printf "%.1f" "$(echo "scale=3; $total_ticked / $total_box * 100" | bc)") % of knowledge acquired"
