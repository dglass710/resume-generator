#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to calculate checksum of a file
get_checksum() {
    local file=$1
    if [ -f "$file" ]; then
        shasum -a 256 "$file" | awk '{print $1}'
    else
        echo ""
    fi
}

# Files to check
FILES=("ResumeBuilder.exe" "ResumeBuilder.zip")
MATCHES=0
TOTAL=${#FILES[@]}

# Print header
echo "🔍 Verifying file checksums between Executable/ and Downloads/"
echo ""

# Check each file
for file in "${FILES[@]}"; do
    src_file="Executable/$file"
    dest_file="$HOME/Downloads/$file"
    
    # Get checksums
    src_checksum=$(get_checksum "$src_file")
    dest_checksum=$(get_checksum "$dest_file")
    
    # Print file info
    echo "📄 File: $file"
    echo "   Source: $src_file"
    echo "   Dest:   $dest_file"
    
    # Compare checksums
    if [ -z "$src_checksum" ] || [ -z "$dest_checksum" ]; then
        if [ -z "$src_checksum" ]; then
            echo "   ${RED}❌ Source file not found${NC}"
        fi
        if [ -z "$dest_checksum" ]; then
            echo "   ${RED}❌ Downloaded file not found${NC}"
        fi
    elif [ "$src_checksum" = "$dest_checksum" ]; then
        echo "   ${GREEN}✅ Checksums match${NC}"
        ((MATCHES++))
    else
        echo "   ${RED}❌ Checksums don't match${NC}"
        echo "   Source checksum: $src_checksum"
        echo "   Dest checksum:  $dest_checksum"
    fi
    echo ""
done

# Print summary
echo "📊 Summary:"
if [ $MATCHES -eq $TOTAL ]; then
    echo "${GREEN}✅ All files match! ($MATCHES/$TOTAL)${NC}"
elif [ $MATCHES -gt 0 ]; then
    echo "${RED}⚠️  Some files don't match! ($MATCHES/$TOTAL)${NC}"
else
    echo "${RED}❌ No matching files found!${NC}"
fi

exit 0
