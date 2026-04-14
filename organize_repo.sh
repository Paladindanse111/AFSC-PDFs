#!/bin/bash

# Create the folders
mkdir -p AFSC_files
mkdir -p BASE_files

# Move all AFSC html and jpg files (numbered codes like 10C, 11B, etc.)
for file in [0-9]*[A-Z].html [0-9]*[A-Z]_p*.jpg [0-9]*[A-Z0-9].html [0-9]*[A-Z0-9]_p*.jpg; do
  [ -e "$file" ] && mv "$file" AFSC_files/
done

# Move all BASE html files
for file in BASE_*.html; do
  [ -e "$file" ] && mv "$file" BASE_files/
done

echo "Done! Files organized into:"
echo "  AFSC_files/ - all AFSC .html and .jpg files"
echo "  BASE_files/ - all BASE .html files"
echo "  Root - README.md, afsc_navigator.html, USAF_Bases_Long_Format_v7.csv"
