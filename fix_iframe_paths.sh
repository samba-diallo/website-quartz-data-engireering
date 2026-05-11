#!/bin/bash

# Fix iframe paths in all markdown files
# Converts absolute paths to relative paths that work from each markdown location

cd "/home/sable/Documents/E4FD/S4/Data Engineering"

echo "Fixing iframe paths in all markdown files..."
count=0

# Find all markdown files with iframes
find content -name "*.md" -type f | while read md_file; do
    if grep -q "iframe" "$md_file"; then
        # Get the relative depth of the file to calculate relative path to root
        # Count how many directories deep it is from content/
        depth=$(echo "$md_file" | sed 's|[^/]||g' | wc -c)
        
        # Calculate how many ../ we need
        # depth includes content/, Data-Engineering-X/, and the folder, so:
        # - 1 content/
        # - 1 or 2 intermediate folders (Data Engineering 1/2, etc)
        # - the actual folder
        # We want to go up to project root where static/ is
        
        # Simple approach: always go up 3 levels (content -> up to root)
        relative_path="../../.."
        
        # Replace /static/nb/... with the relative path
        # Pattern: src="/static/nb/...(stuff).html"
        # Replace with: src="../../.../static/nb/...(stuff).html"
        
        sed -i 's|src="/static/nb/\([^"]*\).html"|src="'"${relative_path}"'/static/nb/\1.html"|g' "$md_file"
        
        if grep -q "${relative_path}/static/nb/" "$md_file"; then
            count=$((count + 1))
            echo "Fixed: $md_file"
        fi
    fi
done

echo "Completed! Fixed $count files."
