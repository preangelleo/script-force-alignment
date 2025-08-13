#!/usr/bin/env python3
"""
Test script for ElevenLabs semantic SRT generation feature
Testing with scene 15 from web_1755001064534_tlv280s7z
"""

from main import *

def test():
    print("🧪 Testing ElevenLabs Semantic SRT Generation Feature")
    print("=" * 60)
    
    # Scene 15 data
    scene_15_data = {
        "scene_number": 30,
        "scene_name": "第三环的转向",
        "scene_audio_script": "这不仅仅是简单的知识传授，这是一个巨大的思想实验室。亚里士多德在塑造一个未来帝王心智的同时，也在大规模地验证和完善着自己的政治理论。他告诉亚历山大，最好的政体是融合了各方优点的“混合政体”，并且要时时刻刻追求“中道”，避免任何形式的极端。这是我们的第二条线索：理论与权力的第一次亲密接触。这段宝贵的经历让亚里士多德深刻地认识到，知识的最终目的，不仅仅是“认识世界”，更重要的是“改造世界”。"
    }
    
    # File paths
    base_dir = "/Users/lgg/coding/sumatman/Temps/web_1755001064534_tlv280s7z"
    audio_file = os.path.join(base_dir, "audio", "scene_019_chinese.mp3")
    
    # Output paths for comparison
    semantic_output = os.path.join("/Users/lgg/coding/sumatman/Temps/", "scene_30_semantic_test.srt")
    simple_output = os.path.join("/Users/lgg/coding/sumatman/Temps/", "scene_030_simple_test.srt")
    
    # Verify audio file exists
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return
    
    file_size = os.path.getsize(audio_file)
    print(f"📁 Audio file: {os.path.basename(audio_file)} ({file_size:,} bytes)")
    print(f"📝 Scene: {scene_15_data['scene_name']}")
    print(f"✏️  Script: {scene_15_data['scene_audio_script'][:50]}...")
    print()
    
    # Test 1: With semantic segmentation (default)
    print("🧠 TEST 1: With Semantic Segmentation (Gemini AI)")
    print("-" * 40)
    
    # Clean up previous test files
    if os.path.exists(semantic_output):
        os.remove(semantic_output)
    
    start_time = time.time()
    success1, result1 = elevenlabs_force_alignment_to_srt(
        audio_file=audio_file,
        input_text=scene_15_data['scene_audio_script'],
        output_filepath=semantic_output,
        max_chars_per_line=30,  # Will be halved to 10 for bilingual
        language='chinese',
        use_semantic_segmentation=True
    )
    elapsed1 = time.time() - start_time
    
    print(f"⏱️  Time taken: {elapsed1:.1f}s")
    print(f"✅ Result: {success1}")
    if success1:
        print(f"📄 Output: {result1}")
    else:
        print(f"❌ Error: {result1}")
    print()
    
    # Test 2: Without semantic segmentation (simple character-based)
    print("📏 TEST 2: Without Semantic Segmentation (Simple)")
    print("-" * 40)
    
    # Clean up previous test files
    if os.path.exists(simple_output):
        os.remove(simple_output)
    
    start_time = time.time()
    success2, result2 = elevenlabs_force_alignment_to_srt(
        audio_file=audio_file,
        input_text=scene_15_data['scene_audio_script'],
        output_filepath=simple_output,
        max_chars_per_line=20,
        language='chinese',
        use_semantic_segmentation=False
    )
    elapsed2 = time.time() - start_time
    
    print(f"⏱️  Time taken: {elapsed2:.1f}s")
    print(f"✅ Result: {success2}")
    if success2:
        print(f"📄 Output: {result2}")
    else:
        print(f"❌ Error: {result2}")
    print()
    
    # Compare results
    print("🔍 COMPARISON AND ANALYSIS")
    print("=" * 60)
    
    if success1 and success2:
        # Read and compare both SRT files
        with open(semantic_output, 'r', encoding='utf-8') as f:
            semantic_content = f.read()
        
        with open(simple_output, 'r', encoding='utf-8') as f:
            simple_content = f.read()
        
        print("📊 File Size Comparison:")
        print(f"   Semantic SRT: {len(semantic_content):,} characters")
        print(f"   Simple SRT:   {len(simple_content):,} characters")
        print()
        
        print("📝 Content Preview - Semantic SRT (first 10 lines):")
        semantic_lines = semantic_content.split('\n')[:10]
        for i, line in enumerate(semantic_lines, 1):
            print(f"   {i:2d}: {line}")
        print()
        
        print("📝 Content Preview - Simple SRT (first 10 lines):")
        simple_lines = simple_content.split('\n')[:10]
        for i, line in enumerate(simple_lines, 1):
            print(f"   {i:2d}: {line}")
        print()
        
        # Verify key features
        print("✅ FEATURE VERIFICATION:")
        print("-" * 30)
        
        # Check for bilingual content
        has_bilingual = any('translation' in line.lower() or 
                           any(ord(c) < 256 and c.isalpha() for c in line) 
                           for line in semantic_lines if line.strip())
        print(f"🌐 Bilingual content detected: {'Yes' if has_bilingual else 'No'}")
        
        # Check for punctuation removal
        chinese_punctuation = "，。！？；：""''「」『』（）【】"
        has_chinese_punct = any(p in semantic_content for p in chinese_punctuation)
        print(f"🔣 Chinese punctuation removed: {'Yes' if not has_chinese_punct else 'No'}")
        
        # Check line lengths
        content_lines = [line for line in semantic_lines if line.strip() and not line.strip().isdigit() and '-->' not in line]
        max_line_length = max(len(line) for line in content_lines) if content_lines else 0
        print(f"📏 Max line length: {max_line_length} characters")
        
        # Character limit compliance (should be around 10 for bilingual)
        over_limit = [line for line in content_lines if len(line) > 15]
        print(f"⚠️  Lines over 15 chars: {len(over_limit)}")
        
        if over_limit:
            print("   Sample long lines:")
            for line in over_limit[:3]:
                print(f"     '{line}' ({len(line)} chars)")
        
            print()
            print("🎯 SUMMARY:")
            print(f"   Semantic segmentation: {'✅ SUCCESS' if success1 else '❌ FAILED'}")
            print(f"   Simple segmentation:   {'✅ SUCCESS' if success2 else '❌ FAILED'}")
            if success1 and success2:
                elapsed1 = results["semantic"]["time"]
                elapsed2 = results["simple"]["time"]
                print(f"   Processing time difference: {elapsed1 - elapsed2:.1f}s")
                print(f"   Content quality improvement: {'Yes' if len(semantic_content) > len(simple_content) else 'No'}")
        else:
            print("❌ Could not compare results due to failures")
    
    print("\n✨ Test completed!")
    return True, results

if __name__ == "__main__":
    # Example usage with configurable parameters
    # Users should modify these parameters for their own testing
    
    # TEST CONFIGURATION - MODIFY THESE FOR YOUR USE CASE
    # ====================================================
    
    # Path to your audio file (MP3, WAV, or other supported formats)
    AUDIO_FILE = "./samples/sample_audio.mp3"
    
    # Text content that should be aligned with the audio
    TEXT_CONTENT = """这是一段示例文本，用于测试语音对齐功能。
    您可以将这里替换为您自己的文本内容。
    支持中文、英文和其他多种语言。"""
    
    # Output directory for generated SRT files
    OUTPUT_DIR = "./test_output"
    
    # Scene or content name (for display purposes)
    SCENE_NAME = "示例场景"
    
    # Maximum characters per subtitle line
    # For bilingual subtitles, this will be automatically adjusted
    MAX_CHARS_PER_LINE = 20
    
    # Language of the content ('chinese', 'english', 'spanish', etc.)
    LANGUAGE = 'chinese'
    
    # Whether to run both semantic and simple segmentation tests
    RUN_BOTH_TESTS = True
    
    # ====================================================
    # RUN THE TEST
    # ====================================================
    
    # Check if we have the required environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("❌ ERROR: ELEVENLABS_API_KEY not found in .env file")
        print("Please create a .env file with your API keys.")
        print("See .env.example for reference.")
        exit(1)
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("Please create a .env file with your API keys.")
        print("See .env.example for reference.")
        exit(1)
    
    # Run the test with your parameters
    success, results = test_force_alignment(
        audio_file=AUDIO_FILE,
        text_content=TEXT_CONTENT,
        output_dir=OUTPUT_DIR,
        scene_name=SCENE_NAME,
        max_chars_per_line=MAX_CHARS_PER_LINE,
        language=LANGUAGE,
        run_both_tests=RUN_BOTH_TESTS
    )
    
    if not success:
        print("\n❌ Test failed. Please check the error messages above.")
        exit(1)