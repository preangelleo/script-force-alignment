#!/usr/bin/env python3
"""
Example usage of ElevenLabs Force Alignment SRT Generator

This file demonstrates how to use the SRTGenerator class for production use.
"""

from main import SRTGenerator

# ============================================================================
# CONFIGURATION
# ============================================================================

# API Keys (required)
ELEVENLABS_API_KEY = "your_elevenlabs_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"  # Optional, for semantic segmentation

# Audio and text configuration
AUDIO_FILE = "./samples/your_audio.mp3"
TEXT_CONTENT = """
将您的音频转录文本放在这里。
这个文本应该与音频中说的内容完全匹配。
支持多种语言，包括中文、英文、日文、韩文等。
For English content, simply put your English text here.
The tool supports 99+ languages.
"""

# Output configuration
OUTPUT_FILE = "./output/subtitles.srt"

# Subtitle formatting
MAX_CHARS_PER_LINE = 20  # Maximum characters per subtitle line
LANGUAGE = 'chinese'  # Options: 'chinese', 'english', 'spanish', 'french', etc.

# Semantic segmentation (requires Gemini API key)
USE_SEMANTIC_SEGMENTATION = True  # True: AI segmentation, False: simple segmentation

# Gemini model (optional)
GEMINI_MODEL = None  # Use default (gemini-2.0-flash)
# GEMINI_MODEL = "gemini-2.0-flash-exp"  # For experimental features
# GEMINI_MODEL = "gemini-1.5-pro"  # For higher quality
# GEMINI_MODEL = "gemini-2.0-flash-thinking"  # For complex reasoning

# Custom system prompt (optional)
CUSTOM_SYSTEM_PROMPT = None  # Use default from system_prompt.txt
# To use a custom prompt, you can either:
# 1. Set a string directly:
# CUSTOM_SYSTEM_PROMPT = "Your custom prompt here with {max_chars_per_line} and {words_json} placeholders"
# 2. Load from a file:
# with open('my_custom_prompt.txt', 'r', encoding='utf-8') as f:
#     CUSTOM_SYSTEM_PROMPT = f.read()

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def generate_subtitles():
    """Generate SRT subtitles using the SRTGenerator class."""
    
    print("🎬 ElevenLabs Force Alignment SRT Generator")
    print("=" * 60)
    
    try:
        # Initialize the generator with API keys
        generator = SRTGenerator(
            elevenlabs_api_key=ELEVENLABS_API_KEY,
            gemini_api_key=GEMINI_API_KEY,  # Optional
            system_prompt=CUSTOM_SYSTEM_PROMPT  # Optional custom prompt
        )
        
        print("✅ Generator initialized successfully")
        
        # Display configuration
        print("\n📋 Configuration:")
        print(f"   Audio: {AUDIO_FILE}")
        print(f"   Output: {OUTPUT_FILE}")
        print(f"   Language: {LANGUAGE}")
        print(f"   Max chars/line: {MAX_CHARS_PER_LINE}")
        print(f"   Semantic AI: {'Enabled' if USE_SEMANTIC_SEGMENTATION and GEMINI_API_KEY else 'Disabled'}")
        if GEMINI_MODEL:
            print(f"   Gemini Model: {GEMINI_MODEL}")
        print()
        
        # Generate subtitles
        print("🚀 Starting subtitle generation...")
        
        success, result = generator.generate(
            audio_file=AUDIO_FILE,
            text=TEXT_CONTENT.strip(),
            output_file=OUTPUT_FILE,
            max_chars_per_line=MAX_CHARS_PER_LINE,
            language=LANGUAGE,
            use_semantic_segmentation=USE_SEMANTIC_SEGMENTATION,
            model=GEMINI_MODEL,
            system_prompt=CUSTOM_SYSTEM_PROMPT  # Can also override per-call
        )
        
        # Report results
        print()
        if success:
            print("✅ SUCCESS! Subtitles generated successfully")
            print(f"📄 Output file: {result}")
            
            # Display file info
            import os
            if os.path.exists(result):
                file_size = os.path.getsize(result)
                with open(result, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    subtitle_count = len([l for l in lines if l.strip() and '-->' in l])
                
                print(f"\n📊 Statistics:")
                print(f"   File size: {file_size:,} bytes")
                print(f"   Subtitles: {subtitle_count} segments")
                print(f"   Total lines: {len(lines)}")
            
            return True
        else:
            print(f"❌ FAILED: {result}")
            print("\n🔍 Troubleshooting tips:")
            print("1. Check your API keys are valid")
            print("2. Ensure the audio file exists and is accessible")
            print("3. Verify the text matches the audio content")
            print("4. Check your internet connection")
            
            return False
            
    except ValueError as e:
        print(f"❌ Configuration error: {str(e)}")
        print("\nPlease check your API keys configuration.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

# ============================================================================
# ADDITIONAL EXAMPLES
# ============================================================================

def example_without_gemini():
    """Example using only ElevenLabs (no semantic segmentation)."""
    
    # Create generator with only ElevenLabs key
    generator = SRTGenerator(
        elevenlabs_api_key=ELEVENLABS_API_KEY,
        gemini_api_key=None  # No Gemini key = simple segmentation
    )
    
    success, result = generator.generate(
        audio_file=AUDIO_FILE,
        text=TEXT_CONTENT,
        output_file="simple_subtitles.srt",
        use_semantic_segmentation=False  # Will use simple segmentation
    )
    
    return success, result


def example_with_custom_model():
    """Example using a specific Gemini model."""
    
    generator = SRTGenerator(
        elevenlabs_api_key=ELEVENLABS_API_KEY,
        gemini_api_key=GEMINI_API_KEY
    )
    
    success, result = generator.generate(
        audio_file=AUDIO_FILE,
        text=TEXT_CONTENT,
        output_file="custom_model_subtitles.srt",
        model="gemini-2.0-flash-exp"  # Use experimental model
    )
    
    return success, result


def example_with_custom_prompt():
    """
    Example using a custom system prompt for subtitle generation.
    """
    
    # Define a custom prompt (simplified for demonstration)
    custom_prompt = """
    You are a subtitle creator. Create SRT subtitles from the word timing data.
    
    Requirements:
    - Maximum {max_chars_per_line} characters per line
    - Remove all punctuation marks
    - Create bilingual subtitles (original + English translation)
    
    Word data:
    {words_json}
    
    Return a JSON array with format:
    [{"index": 1, "start": 0.0, "end": 2.0, "original": "text", "translation": "English"}]
    """
    
    generator = SRTGenerator(
        elevenlabs_api_key=ELEVENLABS_API_KEY,
        gemini_api_key=GEMINI_API_KEY,
        system_prompt=custom_prompt  # Use custom prompt for this instance
    )
    
    success, result = generator.generate(
        audio_file=AUDIO_FILE,
        text=TEXT_CONTENT,
        output_file="custom_prompt_subtitles.srt"
    )
    
    return success, result


def batch_process_files(file_list):
    """
    Process multiple audio files in batch.
    
    Args:
        file_list: List of tuples (audio_path, text_content, output_path)
    """
    
    print(f"🔄 Batch processing {len(file_list)} files...")
    
    # Initialize generator once
    generator = SRTGenerator(
        elevenlabs_api_key=ELEVENLABS_API_KEY,
        gemini_api_key=GEMINI_API_KEY
    )
    
    results = []
    for i, (audio_path, text, output_path) in enumerate(file_list, 1):
        print(f"\n[{i}/{len(file_list)}] Processing: {audio_path}")
        
        success, result = generator.generate(
            audio_file=audio_path,
            text=text,
            output_file=output_path,
            max_chars_per_line=MAX_CHARS_PER_LINE,
            language=LANGUAGE,
            use_semantic_segmentation=USE_SEMANTIC_SEGMENTATION
        )
        
        results.append({
            'audio': audio_path,
            'success': success,
            'result': result
        })
    
    # Summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n📊 Batch Results: {successful}/{len(file_list)} successful")
    
    return results

# ============================================================================
# LEGACY FUNCTION USAGE (for backward compatibility)
# ============================================================================

def example_legacy_function():
    """Example using the legacy function interface with .env file."""
    
    # This requires ELEVENLABS_API_KEY and GEMINI_API_KEY in .env file
    from main import elevenlabs_force_alignment_to_srt
    
    success, result = elevenlabs_force_alignment_to_srt(
        audio_file=AUDIO_FILE,
        input_text=TEXT_CONTENT,
        output_filepath="legacy_output.srt",
        max_chars_per_line=MAX_CHARS_PER_LINE,
        language=LANGUAGE,
        use_semantic_segmentation=True
    )
    
    return success, result

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # Run the main subtitle generation
    success = generate_subtitles()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)