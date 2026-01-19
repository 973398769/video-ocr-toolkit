# Demo Examples

This directory contains demonstration videos and results showing the capabilities of Video OCR Toolkit.

## Demo Video

**`demo_text_video.mp4`** (1.9 MB, 10 seconds)
- Created specifically to showcase OCR capabilities
- Contains clear text at different timestamps
- Includes multilingual references
- Resolution: 1280x720, 30 FPS

### Text Content by Timeline:

- **0-3 seconds**: "VIDEO OCR TOOLKIT" + "Demo Video"
- **3-6 seconds**: "Text Detection" + "Multi-language Support" + "English • 中文 • 日本語"
- **6-9 seconds**: "Timestamp: 6-9 seconds" + "Precise Frame Analysis" + "GPU Accelerated OCR"
- **9-10 seconds**: "GitHub: video-ocr-toolkit" + "Open Source • MIT License"

## Demo Results

### `demo_results.txt`
Complete text extraction with timestamps in `[M:SS-M:SS]` format.

### `demo_by_seconds/`
Visual annotations showing detected text with red bounding boxes for each second of the video.

## Recreate Demo

To recreate the demo video:

```bash
cd examples
python3 create_demo_video.py
```

To run the toolkit on the demo:

```bash
# Extract text
python3 ../video_ocr_extractor.py demo_text_video.mp4 -l en -i 1

# Create visual annotations by second
python3 ../video_ocr_by_second.py demo_text_video.mp4 -l en

# Create annotated video
python3 ../video_ocr_visualizer.py demo_text_video.mp4 -l en
```

## Try Your Own Video

Replace `demo_text_video.mp4` with your own video file:

```bash
python3 ../video_ocr_extractor.py your_video.mp4 -l en -i 1 -o your_results.txt
```

## Notes

- The demo video is synthetically generated and contains no copyrighted content
- Text is rendered in standard fonts for optimal OCR recognition
- Background gradient and grid pattern show the toolkit works in various conditions
