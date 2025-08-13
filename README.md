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
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey)) - Optional for semantic segmentation

### Installation

#### Option 1: Install from PyPI (Recommended)
```bash
pip install elevenlabs-srt-generator
```

#### Option 2: Install from Source
```bash
git clone https://github.com/preangelleo/script-force-alignment.git
cd script-force-alignment
pip install -r requirements.txt
```

## 📖 Usage

### Method 1: Using the SRTGenerator Class (Recommended)

The new class-based approach allows you to pass API keys directly without managing environment files:

```python
from main import SRTGenerator

# Initialize the generator with API keys
generator = SRTGenerator(
    elevenlabs_api_key="your_elevenlabs_key",
    gemini_api_key="your_gemini_key"  # Optional for semantic segmentation
)

# Generate subtitles
success, result = generator.generate(
    audio_file="path/to/audio.mp3",
    text="Your transcript text here",
    output_file="output/subtitles.srt",
    max_chars_per_line=20,
    language='chinese',
    use_semantic_segmentation=True,
    model='gemini-2.0-flash'  # Optional: specify Gemini model
)

if success:
    print(f"Subtitles saved to: {result}")
```

### Method 2: Command Line Interface

After installing from PyPI, you can use the CLI directly:

```bash
# Basic usage
elevenlabs-srt audio.mp3 "Your transcript text" -o output.srt

# With options
elevenlabs-srt audio.mp3 transcript.txt \
  --output subtitles.srt \
  --max-chars 30 \
  --language chinese \
  --no-semantic  # Disable AI segmentation
  --system-prompt custom_prompt.txt  # Use custom system prompt
```

### Method 3: Legacy Function Interface

For backward compatibility, you can still use the original function with environment variables:

```python
# Requires ELEVENLABS_API_KEY and GEMINI_API_KEY in .env file
from main import elevenlabs_force_alignment_to_srt

success, result = elevenlabs_force_alignment_to_srt(
    audio_file="path/to/audio.mp3",
    input_text="Your transcript text here",
    output_filepath="output/subtitles.srt"
)
```

### Using the Example Script

Edit `example_usage.py` with your API keys and parameters:

```python
# API Keys (required)
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"  # Optional

# Audio and text configuration
AUDIO_FILE = "./samples/your_audio.mp3"
TEXT_CONTENT = "Your transcript here..."
OUTPUT_FILE = "./output/subtitles.srt"
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

## 🎨 Custom System Prompt

The tool uses an AI system prompt to guide subtitle generation. You can customize this in three ways:

### 1. Modify the Default Prompt File
Edit `system_prompt.txt` to change the default behavior globally.

### 2. Pass Custom Prompt to SRTGenerator
```python
# Load custom prompt from file
with open('my_custom_prompt.txt', 'r') as f:
    custom_prompt = f.read()

generator = SRTGenerator(
    elevenlabs_api_key="key",
    gemini_api_key="key",
    system_prompt=custom_prompt  # Use custom prompt
)
```

### 3. Override Per Generation Call
```python
generator.generate(
    audio_file="audio.mp3",
    text="transcript",
    output_file="output.srt",
    system_prompt="Your custom prompt with {max_chars_per_line} and {words_json}"
)
```

### System Prompt Placeholders
Your custom prompt must include these placeholders:
- `{max_chars_per_line}` - Will be replaced with the character limit
- `{words_json}` - Will be replaced with the word timing data

## 🔧 API Configuration

### Option 1: Pass API Keys Directly (Recommended)
```python
generator = SRTGenerator(
    elevenlabs_api_key="your_key",
    gemini_api_key="your_key"
)
```

### Option 2: Use Environment Variables
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

### SRTGenerator Class

```python
class SRTGenerator:
    def __init__(
        elevenlabs_api_key: str,
        gemini_api_key: Optional[str] = None,
        default_model: str = 'gemini-2.0-flash',
        system_prompt: Optional[str] = None
    )
```

#### Constructor Parameters
- **elevenlabs_api_key**: ElevenLabs API key (required)
- **gemini_api_key**: Gemini API key (optional, needed for semantic segmentation)
- **default_model**: Default Gemini model to use
- **system_prompt**: Custom system prompt for AI segmentation

#### Generate Method

```python
def generate(
    audio_file: str,
    text: str,
    output_file: str,
    max_chars_per_line: int = 20,
    language: str = 'chinese',
    use_semantic_segmentation: bool = True,
    model: Optional[str] = None,
    system_prompt: Optional[str] = None
) -> Tuple[bool, str]
```

### Legacy Function

```python
elevenlabs_force_alignment_to_srt(
    audio_file: str,
    input_text: str,
    output_filepath: str,
    api_key: str = None,
    max_chars_per_line: int = 20,
    language: str = 'chinese',
    use_semantic_segmentation: bool = True,
    model: str = None,
    system_prompt: str = None
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
- **model**: Gemini model to use (default: 'gemini-2.0-flash'). Options:
  - `'gemini-2.0-flash'`: Fast and efficient (default)
  - `'gemini-2.0-flash-exp'`: Experimental features
  - `'gemini-1.5-pro'`: Higher quality output
  - `'gemini-2.0-flash-thinking'`: Complex reasoning

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