# ElevenLabs Force Alignment SRT Generator

🎬 A powerful Python tool for generating synchronized SRT subtitles using ElevenLabs Force Alignment API with optional AI-powered semantic segmentation.

## ✨ Features

- **High-Precision Alignment**: Uses ElevenLabs Force Alignment API for accurate word-level timing
- **AI Semantic Segmentation**: Leverages Google Gemini for intelligent subtitle breaking
- **Bilingual Support**: Automatically generates bilingual subtitles (original + translation)
- **Multi-Language**: Supports 99+ languages including Chinese, English, Japanese, Korean, etc.
- **Smart Formatting**: Removes punctuation and optimizes line breaks for readability
- **Flexible Output**: Configurable character limits and segmentation strategies

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- ElevenLabs API key ([Get one here](https://elevenlabs.io/))
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/script_force_alignment.git
cd script_force_alignment
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

4. Run setup validation:
```bash
python setup.py
```

## 📖 Usage

### Basic Example

```python
from main import elevenlabs_force_alignment_to_srt

# Generate subtitles
success, result = elevenlabs_force_alignment_to_srt(
    audio_file="path/to/audio.mp3",
    input_text="Your transcript text here",
    output_filepath="output/subtitles.srt",
    max_chars_per_line=20,
    language='chinese',
    use_semantic_segmentation=True  # Enable AI segmentation
)

if success:
    print(f"Subtitles saved to: {result}")
```

### Using the Example Script

Edit `example_usage.py` with your parameters:

```python
# Configuration
AUDIO_FILE_PATH = "./samples/your_audio.mp3"
TEXT_CONTENT = "Your transcript here..."
OUTPUT_FILE_PATH = "./output/subtitles.srt"
LANGUAGE = 'chinese'
MAX_CHARS_PER_LINE = 20
USE_SEMANTIC_SEGMENTATION = True
```

Then run:
```bash
python example_usage.py
```

### Running Tests

The test script allows you to compare semantic vs simple segmentation:

```bash
python test.py
```

## 🔧 API Configuration

### Required Environment Variables

Create a `.env` file with:

```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Getting API Keys

1. **ElevenLabs API Key**:
   - Sign up at [ElevenLabs](https://elevenlabs.io/)
   - Go to your profile settings
   - Copy your API key
   - **Important**: Enable the Force Alignment feature in your API settings (it's disabled by default)

2. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Enable the Gemini API

## 📝 API Reference

### Main Function

```python
elevenlabs_force_alignment_to_srt(
    audio_file: str,           # Path to audio file
    input_text: str,           # Transcript text
    output_filepath: str,      # Output SRT path
    api_key: str = None,       # Optional API key override
    max_chars_per_line: int = 20,  # Max characters per line
    language: str = 'chinese',     # Language code
    use_semantic_segmentation: bool = True  # Enable AI segmentation
) -> Tuple[bool, str]
```

### Parameters

- **audio_file**: Path to audio file (MP3, WAV, M4A, OGG, FLAC, etc.)
- **input_text**: Exact transcript of the audio content
- **output_filepath**: Where to save the SRT file
- **api_key**: Optional ElevenLabs API key (overrides .env)
- **max_chars_per_line**: Maximum characters per subtitle line
- **language**: Language of the content (e.g., 'chinese', 'english')
- **use_semantic_segmentation**: Enable AI-powered semantic breaking

### Returns

- **Tuple[bool, str]**: (Success status, Output path or error message)

## 🎯 Features Comparison

| Feature | Semantic Segmentation | Simple Segmentation |
|---------|----------------------|-------------------|
| Natural breaks | ✅ Yes | ❌ No |
| Bilingual support | ✅ Yes | ❌ No |
| AI-powered | ✅ Yes | ❌ No |
| Processing time | ~3-5s | ~1-2s |
| Quality | High | Basic |

## 🌍 Supported Languages

The tool supports 99+ languages including:
- Chinese (Simplified & Traditional)
- English
- Japanese
- Korean
- Spanish
- French
- German
- Russian
- Arabic
- Hindi
- And many more...

## 📊 Output Format

The tool generates standard SRT format:

```srt
1
00:00:00,123 --> 00:00:02,456
这是第一行字幕
This is the first subtitle

2
00:00:02,456 --> 00:00:05,789
这是第二行字幕
This is the second subtitle
```

## 🔍 Troubleshooting

### Common Issues

1. **API Key Errors**:
   - Ensure your API keys are valid
   - Check that .env file is in the correct location
   - Verify keys don't have extra spaces

2. **Audio File Issues**:
   - Maximum file size: 1GB
   - Supported formats: MP3, WAV, M4A, OGG, FLAC, AAC, OPUS, MP4
   - Ensure file path is correct

3. **Text Alignment Issues**:
   - Text must match audio content exactly
   - Remove extra spaces or formatting
   - Check language setting matches audio

### Debug Mode

Enable detailed logging by setting environment variable:
```bash
export DEBUG=true
python example_usage.py
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io/) for the Force Alignment API
- [Google Gemini](https://deepmind.google/technologies/gemini/) for AI semantic analysis
- Community contributors

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: your-email@example.com

## 🚦 Project Status

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![API](https://img.shields.io/badge/API-ElevenLabs-orange.svg)
![AI](https://img.shields.io/badge/AI-Gemini-purple.svg)

---

Made with ❤️ for the subtitle generation community