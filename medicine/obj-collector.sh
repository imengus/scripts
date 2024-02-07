touch "objectives-${1}.md"
for file in ~/Documents/notes/medicine/$1/0*; do
    filename="${file##*/}"
    echo "$(awk '/## Objectives/,/## Quick/ { if (!/## Objectives|## Quick/) print }' "$file")" >> "objectives-${1}.md"
done
sed -i '/-/!d' "objectives-${1}.md"
sed -i 's/-/- \[ \]/g' "objectives-${1}.md"
