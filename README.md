# Video OCR Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A powerful toolkit for extracting and annotating text from videos using OCR (Optical Character Recognition).

![Demo](https://via.placeholder.com/800x400.png?text=Video+OCR+Toolkit+Demo)

## ✨ Features

- 🎯 **Precise Text Extraction** - Extract text with accurate timestamps (second-level precision)
- 🎨 **Visual Annotation** - Annotate detected text with red bounding boxes
- ⏱️ **Second-by-Second Analysis** - Split videos into frames by second
- 📊 **Multiple Output Formats** - Generate clean, organized text reports
- 🌍 **Multi-language Support** - Support for English, Chinese, and 80+ languages
- 🚀 **GPU Acceleration** - Fast processing with GPU support

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/your-username/video-ocr-toolkit.git
cd video-ocr-toolkit
pip install -r requirements.txt
```

### Basic Usage

```bash
# Extract text with timestamps
python video_ocr_extractor.py video.mp4 -l en -i 1 -o results.txt

# Create annotated frames (one per second)
python video_ocr_by_second.py video.mp4 -l en

# Create annotated video
python video_ocr_visualizer.py video.mp4 -l en
```

## 📖 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started in 5 minutes
- [Examples & Demo](examples/README.md) - See the toolkit in action with demo video

## 🛠️ Tools Included

| Tool | Description | Output |
|------|-------------|--------|
| `video_ocr_extractor.py` | Extract text with timestamps | `.txt` file with `[M:SS-M:SS]` format |
| `video_ocr_by_second.py` | Split video by second + annotate | Annotated `.jpg` frames + report |
| `video_ocr_visualizer.py` | Frame-by-frame annotation | Annotated video + frames |
| `clean_ocr_results.py` | Clean & deduplicate results | Cleaned `.txt` file |

## 📋 Example Output

### Text Extraction (`video_ocr_extractor.py`)

```
[0:00-0:01]
Hello
[0:00-0:01]
World
[0:01-0:02]
Welcome to Video OCR
```

### Visual Annotation

Each detected text element is highlighted with:
- ✅ Red bounding box
- ✅ Text label with confidence score
- ✅ Individual timestamp

## 🎯 Use Cases

- 📺 Video subtitle generation
- 📊 Content analysis and indexing
- 🎓 Educational video annotation
- 🔍 Video search and discovery
- 📝 Automated video captioning

## ⚙️ Configuration

### Languages

```bash
# English only (recommended for best accuracy)
-l en

# Multiple languages
-l en ch_sim ja
```

### Frame Interval

```bash
-i 1   # Every frame (most accurate, slowest)
-i 5   # Every 5th frame (balanced)
-i 10  # Every 10th frame (fastest)
```

### Confidence Threshold

```bash
-c 0.3  # Default (balanced)
-c 0.5  # Higher precision
-c 0.7  # Very strict
```

## 📦 Requirements

- Python 3.8+
- OpenCV
- EasyOCR
- PyTorch
- NumPy

See [requirements.txt](requirements.txt) for full list.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - Powerful OCR engine
- [OpenCV](https://opencv.org/) - Computer vision library

## 📧 Support

For issues, questions, or suggestions, please [open an issue](https://github.com/your-username/video-ocr-toolkit/issues).

---

**Made with ❤️ for the open-source community**
