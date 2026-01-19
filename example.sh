#!/bin/bash
# Example usage script for Video OCR Toolkit

echo "Video OCR Toolkit - Example Usage"
echo "=================================="
echo ""

# Check if video file is provided
if [ -z "$1" ]; then
    echo "Usage: ./example.sh <video_file>"
    echo ""
    echo "Examples:"
    echo "  ./example.sh my_video.mp4"
    echo ""
    exit 1
fi

VIDEO_FILE="$1"

if [ ! -f "$VIDEO_FILE" ]; then
    echo "Error: Video file '$VIDEO_FILE' not found!"
    exit 1
fi

echo "Processing video: $VIDEO_FILE"
echo ""

# Extract base name
BASE_NAME=$(basename "$VIDEO_FILE" | sed 's/\.[^.]*$//')

echo "Step 1: Extracting text with timestamps..."
python video_ocr_extractor.py "$VIDEO_FILE" -l en -i 1 -o "${BASE_NAME}_extracted.txt"
echo "✓ Results saved to: ${BASE_NAME}_extracted.txt"
echo ""

echo "Step 2: Cleaning results..."
python clean_ocr_results.py "${BASE_NAME}_extracted.txt" "${BASE_NAME}_cleaned.txt"
echo "✓ Cleaned results saved to: ${BASE_NAME}_cleaned.txt"
echo ""

echo "Step 3: Creating visual annotations (by second)..."
python video_ocr_by_second.py "$VIDEO_FILE" -l en
echo "✓ Visual frames saved to: ${BASE_NAME}_by_seconds/"
echo ""

echo "=================================="
echo "Processing complete!"
echo ""
echo "Output files:"
echo "  - ${BASE_NAME}_extracted.txt (raw OCR results)"
echo "  - ${BASE_NAME}_cleaned.txt (cleaned results)"
echo "  - ${BASE_NAME}_by_seconds/ (visual frames)"
echo ""
