#!/usr/bin/env python3
"""
Example usage of ElevenLabs Force Alignment SRT Generator

This file demonstrates how to use the force alignment tool in production.
Users can copy this file and modify the parameters for their specific use case.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path to import main module
sys.path.insert(0, str(Path(__file__).parent))
from main import elevenlabs_force_alignment_to_srt

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION PARAMETERS - MODIFY THESE FOR YOUR USE CASE
# ============================================================================

# Audio file configuration
AUDIO_FILE_PATH = "/Users/lgg/coding/sumatman/Temps/web_1755001064534_tlv280s7z/audio/scene_033_chinese.mp3"  # Path to your audio file
# Supported formats: MP3, WAV, M4A, OGG, FLAC, AAC, OPUS, MP4

# Text content that corresponds to the audio
# This should be the exact transcript of what's spoken in the audio
TEXT_CONTENT = """
亚里士多德和他的学生们，在这里进行着一项前无古人、也可能后无来者的庞大工程：那就是系统性地收集、整理、研究当时人类已知的一切知识。想象一下吕克昂的日常：清晨，亚里士多德可能在和学生讨论悲剧的本质，深入剖析索福克勒斯的《俄狄浦斯王》，并从中总结出“净化”和“突转”等经典的戏剧理论。他的研究范围无所不包，充满了对万事万物的好奇心。
"""

# Output configuration
OUTPUT_FILE_PATH = "temps/subtitles_33.srt"  # Where to save the SRT file

# Subtitle formatting configuration
MAX_CHARS_PER_LINE = 36  # Maximum characters per subtitle line
# Note: For bilingual subtitles, this will be automatically adjusted

# Language configuration
LANGUAGE = 'chinese'  # Options: 'chinese', 'english', 'spanish', 'french', etc.
# This helps the tool optimize for specific language characteristics

# Semantic segmentation configuration
USE_SEMANTIC_SEGMENTATION = True  # True: Use AI for smart segmentation
# - True: Uses Gemini AI to create natural, meaningful subtitle segments
# - False: Uses simple character-based segmentation

# Advanced configuration (optional)
API_KEY_OVERRIDE = None  # Set to override the .env file API key
# Example: API_KEY_OVERRIDE = "xi-abc123..."

# Gemini model configuration (optional)
GEMINI_MODEL = 'gemini-2.0-flash'  # Use default model (gemini-2.0-flash)
# Example: GEMINI_MODEL = "gemini-2.0-flash-exp"  # For experimental features
# Example: GEMINI_MODEL = "gemini-1.5-pro"  # For higher quality
# Example: GEMINI_MODEL = "gemini-2.0-flash-thinking"  # For complex reasoning


# ============================================================================
# MAIN FUNCTION - Usually you don't need to modify this
# ============================================================================

def generate_subtitles():
    """
    Generate SRT subtitles for the configured audio file.
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print("🎬 ElevenLabs Force Alignment SRT Generator")
    print("=" * 60)
    
    # Validate environment
    if not os.getenv("ELEVENLABS_API_KEY") and not API_KEY_OVERRIDE:
        print("❌ ERROR: ELEVENLABS_API_KEY not found")
        print("Please set up your .env file or provide API_KEY_OVERRIDE")
        print("See .env.example for reference")
        return False
    
    if USE_SEMANTIC_SEGMENTATION and not os.getenv("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY not found (required for semantic segmentation)")
        print("Please set up your .env file or set USE_SEMANTIC_SEGMENTATION = False")
        return False
    
    # Validate input file
    if not os.path.exists(AUDIO_FILE_PATH):
        print(f"❌ ERROR: Audio file not found: {AUDIO_FILE_PATH}")
        print("Please check the file path and try again")
        return False
    
    # Create output directory if needed
    output_dir = os.path.dirname(OUTPUT_FILE_PATH)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Display configuration
    print("📋 Configuration:")
    print(f"   Audio: {AUDIO_FILE_PATH}")
    print(f"   Output: {OUTPUT_FILE_PATH}")
    print(f"   Language: {LANGUAGE}")
    print(f"   Max chars/line: {MAX_CHARS_PER_LINE}")
    print(f"   Semantic AI: {'Enabled' if USE_SEMANTIC_SEGMENTATION else 'Disabled'}")
    if GEMINI_MODEL:
        print(f"   Gemini Model: {GEMINI_MODEL}")
    print()
    
    # Generate subtitles
    print("🚀 Starting force alignment...")
    
    success, result = elevenlabs_force_alignment_to_srt(
        audio_file=AUDIO_FILE_PATH,
        input_text=TEXT_CONTENT.strip(),
        output_filepath=OUTPUT_FILE_PATH,
        api_key=API_KEY_OVERRIDE,
        max_chars_per_line=MAX_CHARS_PER_LINE,
        language=LANGUAGE,
        use_semantic_segmentation=USE_SEMANTIC_SEGMENTATION,
        model=GEMINI_MODEL
    )
    
    # Report results
    print()
    if success:
        print("✅ SUCCESS! Subtitles generated successfully")
        print(f"📄 Output file: {result}")
        
        # Display file info
        if os.path.exists(result):
            file_size = os.path.getsize(result)
            with open(result, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                subtitle_count = len([l for l in lines if l.strip() and '-->' in l])
            
            print(f"📊 Statistics:")
            print(f"   File size: {file_size:,} bytes")
            print(f"   Subtitles: {subtitle_count} segments")
            print(f"   Total lines: {len(lines)}")
        
        return True
    else:
        print(f"❌ FAILED: {result}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Check your API keys are valid")
        print("2. Ensure the audio file is accessible")
        print("3. Verify the text matches the audio content")
        print("4. Check your internet connection")
        
        return False

# ============================================================================
# ADDITIONAL HELPER FUNCTIONS (Optional)
# ============================================================================

def batch_process_files(file_list):
    """
    Process multiple audio files in batch.
    
    Args:
        file_list: List of tuples (audio_path, text_content, output_path)
    
    Example:
        files = [
            ("audio1.mp3", "Text 1", "output1.srt"),
            ("audio2.mp3", "Text 2", "output2.srt"),
        ]
        batch_process_files(files)
    """
    
    print(f"🔄 Batch processing {len(file_list)} files...")
    
    results = []
    for i, (audio_path, text, output_path) in enumerate(file_list, 1):
        print(f"\n[{i}/{len(file_list)}] Processing: {audio_path}")
        
        success, result = elevenlabs_force_alignment_to_srt(
            audio_file=audio_path,
            input_text=text,
            output_filepath=output_path,
            max_chars_per_line=MAX_CHARS_PER_LINE,
            language=LANGUAGE,
            use_semantic_segmentation=USE_SEMANTIC_SEGMENTATION,
            model=GEMINI_MODEL
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

def validate_alignment(srt_file, original_text):
    """
    Validate that the SRT file contains all the original text.
    
    Args:
        srt_file: Path to the SRT file
        original_text: Original text content
    
    Returns:
        bool: True if validation passes
    """
    
    if not os.path.exists(srt_file):
        return False
    
    with open(srt_file, 'r', encoding='utf-8') as f:
        srt_content = f.read()
    
    # Extract only subtitle text (skip timecodes and numbers)
    lines = srt_content.split('\n')
    subtitle_text = []
    
    for line in lines:
        line = line.strip()
        if line and not line.isdigit() and '-->' not in line:
            subtitle_text.append(line)
    
    combined_text = ' '.join(subtitle_text)
    
    # Basic validation: check if most words are present
    original_words = set(original_text.lower().split())
    subtitle_words = set(combined_text.lower().split())
    
    coverage = len(original_words & subtitle_words) / len(original_words) if original_words else 0
    
    return coverage > 0.8  # 80% word coverage threshold

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    # Run the subtitle generation
    success = generate_subtitles()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)