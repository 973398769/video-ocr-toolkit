# Video OCR Toolkit

A powerful toolkit for extracting and annotating text from videos using OCR (Optical Character Recognition). Perfect for video captioning, subtitle generation, and visual text analysis.

## Features

- 🎯 **Precise Text Extraction**: Extract text with accurate timestamps (second-level precision)
- 🎨 **Visual Annotation**: Annotate detected text with red bounding boxes
- ⏱️ **Second-by-Second Analysis**: Split videos into frames by second
- 📊 **Multiple Output Formats**: Generate clean, organized text reports
- 🌍 **Multi-language Support**: Support for English, Chinese, and 80+ languages
- 🚀 **GPU Acceleration**: Fast processing with GPU support

## Installation

### Prerequisites

- Python 3.8 or higher
- CUDA-compatible GPU (optional, for faster processing)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Tools

### 1. Video OCR Extractor

Extract all visible text from videos with precise timestamps.

**Features:**
- Tracks text appearance and disappearance
- Second-level timestamp format: `[M:SS-M:SS]`
- Sorts text from top-to-bottom, left-to-right
- Individual timestamp for each text element

**Usage:**

```bash
# Basic usage
python video_ocr_extractor.py video.mp4

# Specify output file
python video_ocr_extractor.py video.mp4 -o output.txt

# English only (recommended for better accuracy)
python video_ocr_extractor.py video.mp4 -l en

# Adjust confidence threshold (0-1)
python video_ocr_extractor.py video.mp4 -c 0.5

# Set frame sampling interval (1 = every frame, higher = faster but less precise)
python video_ocr_extractor.py video.mp4 -i 1
```

**Output Format:**

```
[0:00-0:01]
Hello
[0:00-0:01]
World
[0:01-0:02]
Welcome
```

### 2. Video OCR by Second

Split video into frames by second and annotate with red boxes.

**Features:**
- One frame per second
- Red bounding boxes around detected text
- Confidence scores displayed
- Detailed report generation

**Usage:**

```bash
# Basic usage
python video_ocr_by_second.py video.mp4

# English only
python video_ocr_by_second.py video.mp4 -l en

# Custom output directory
python video_ocr_by_second.py video.mp4 -o output_folder

# Adjust confidence threshold
python video_ocr_by_second.py video.mp4 -c 0.5
```

**Output:**
- `second_000_0-00.jpg` - Frame at 0 seconds with annotations
- `second_001_0-01.jpg` - Frame at 1 second with annotations
- `by_second_report.txt` - Detailed report of detected text per second

### 3. Video OCR Visualizer

Create annotated video with all detected text highlighted.

**Features:**
- Frame-by-frame text detection
- Red bounding boxes with labels
- Generates both annotated video and individual frames
- Comprehensive report

**Usage:**

```bash
# Basic usage (generates video + frames)
python video_ocr_visualizer.py video.mp4

# Only save frames (no video)
python video_ocr_visualizer.py video.mp4 --no-video

# Custom output directory
python video_ocr_visualizer.py video.mp4 -o output_folder

# English only
python video_ocr_visualizer.py video.mp4 -l en
```

**Output:**
- `*_annotated.mp4` - Annotated video file
- `frame_00001.jpg`, `frame_00002.jpg`, ... - Individual annotated frames
- `annotation_report.txt` - Statistical report

### 4. Clean OCR Results

Clean and deduplicate OCR extraction results.

**Usage:**

```bash
python clean_ocr_results.py input.txt output.txt
```

## Examples

### Extract Text with Timestamps

```bash
python video_ocr_extractor.py my_video.mp4 -l en -i 1 -o results.txt
```

### Create Annotated Video

```bash
python video_ocr_visualizer.py my_video.mp4 -l en
```

### Split Video by Second

```bash
python video_ocr_by_second.py my_video.mp4 -l en
```

## Configuration Options

### Languages

Supported languages include:
- `en` - English
- `ch_sim` - Chinese Simplified
- `ch_tra` - Chinese Traditional
- `ja` - Japanese
- `ko` - Korean
- `fr` - French
- `de` - German
- `es` - Spanish
- And 70+ more...

Specify multiple languages:
```bash
python video_ocr_extractor.py video.mp4 -l en ch_sim ja
```

### Frame Interval

- `1` - Process every frame (most accurate, slowest)
- `2-5` - Balanced accuracy and speed
- `10+` - Fast processing, may miss brief text

### Confidence Threshold

- `0.3` - Default, good balance
- `0.5` - Higher precision, fewer false positives
- `0.7+` - Very strict, only high-confidence detections

## Technical Details

### OCR Engine

This toolkit uses [EasyOCR](https://github.com/JaidedAI/EasyOCR), a powerful OCR engine with:
- Deep learning-based text detection
- Support for 80+ languages
- GPU acceleration
- High accuracy for various fonts and styles

### Video Processing

- Uses OpenCV for video frame extraction
- Tracks text across frames to determine exact appearance/disappearance times
- Position-based sorting (Y-coordinate first, then X-coordinate)

### Timestamp Logic

- **Start timestamp**: When the first letter becomes readable
- **End timestamp**: Immediately after the last letter becomes fully unreadable

## Performance Tips

1. **Use GPU**: Ensure CUDA is installed for 10-50x faster processing
2. **Adjust frame interval**: Use `-i 2` or `-i 5` for faster processing if precise timestamps aren't critical
3. **Specify language**: Use `-l en` for English-only to reduce false positives
4. **Increase confidence**: Use `-c 0.5` to filter out uncertain detections

## Requirements

See [requirements.txt](requirements.txt) for full dependency list:
- opencv-python
- easyocr
- numpy
- torch
- torchvision
- Pillow

## License

MIT License - Feel free to use, modify, and distribute.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - OCR engine
- [OpenCV](https://opencv.org/) - Video processing

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
