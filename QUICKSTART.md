# Quick Start Guide

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/video-ocr-toolkit.git
cd video-ocr-toolkit

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### 1. Extract Text with Timestamps

```bash
python video_ocr_extractor.py your_video.mp4 -l en -i 1 -o results.txt
```

**Output format:**
```
[0:00-0:01]
Hello
[0:00-0:01]
World
```

### 2. Create Annotated Frames by Second

```bash
python video_ocr_by_second.py your_video.mp4 -l en
```

This creates:
- `your_video_by_seconds/second_000_0-00.jpg`
- `your_video_by_seconds/second_001_0-01.jpg`
- `your_video_by_seconds/by_second_report.txt`

### 3. Create Annotated Video

```bash
python video_ocr_visualizer.py your_video.mp4 -l en
```

This creates:
- `your_video_annotated_frames/*_annotated.mp4`
- Individual frames with annotations
- Statistical report

## Common Parameters

- `-l en` - English only (recommended)
- `-i 1` - Process every frame (most accurate)
- `-c 0.3` - Confidence threshold (0.3 = default)
- `-o output.txt` - Specify output file

## Tips

1. **For best accuracy**: Use `-i 1` (every frame)
2. **For speed**: Use `-i 5` or `-i 10`
3. **Reduce false positives**: Use `-c 0.5` or higher
4. **English-only videos**: Use `-l en` instead of default multilingual

## Troubleshooting

### GPU Issues
If you encounter GPU-related errors, EasyOCR will automatically fall back to CPU processing.

### Memory Issues
For long videos, increase frame interval: `-i 10`

### Poor Recognition
- Try adjusting confidence: `-c 0.2` (lower) or `-c 0.5` (higher)
- Ensure video quality is good
- Use language-specific settings: `-l en`

## Example Workflow

```bash
# Step 1: Extract text with timestamps
python video_ocr_extractor.py video.mp4 -l en -i 1 -o extracted.txt

# Step 2: Clean results (remove duplicates)
python clean_ocr_results.py extracted.txt cleaned.txt

# Step 3: Create visual verification
python video_ocr_by_second.py video.mp4 -l en

# Step 4: Review second_XXX.jpg files to verify accuracy
```
