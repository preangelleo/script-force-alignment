import os, time, requests
from typing import Tuple, List, Dict, Any
from dotenv import load_dotenv
load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in environment variables, add ELEVENLABS_API_KEY to .env file")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables, add GEMINI_API_KEY to .env file")

GEMINI_MODEL = 'gemini-2.0-flash'

def elevenlabs_force_alignment_to_srt(
    audio_file: str,
    input_text: str, 
    output_filepath: str,
    api_key: str = None,
    max_chars_per_line: int = 20,  # Changed default for Chinese
    language: str = 'chinese',  # 保持兼容性参数
    use_semantic_segmentation: bool = True,  # New parameter for AI semantic segmentation
    model: str = None  # Gemini model to use, defaults to GEMINI_MODEL
) -> Tuple[bool, str]:
    """
    使用ElevenLabs Force Alignment API生成SRT字幕文件
    作为火山引擎字幕生成的替代方案，支持多语言和更稳定的API
    
    Enhanced features:
    - 使用Gemini AI进行语义切割
    - 自动生成双语字幕（中文->英文）
    - 智能断句，保持语义完整性
    - 中英文混合文本自动加空格
    
    Args:
        audio_file (str): 音频文件路径
        input_text (str): 要对齐的文本内容
        output_filepath (str): 输出SRT文件路径
        api_key (str, optional): ElevenLabs API密钥，默认使用全局配置
        max_chars_per_line (int): 每行最大字符数（双语模式会自动减半）
        language (str): 语言类型，保持兼容性
        use_semantic_segmentation (bool): 是否使用AI语义切割（默认启用）
    
    Returns:
        Tuple[bool, str]: (成功状态, 结果路径或错误信息)
    
    Features:
        - 使用ElevenLabs Forced Alignment API进行高精度时间对齐
        - 支持99种语言，包括中文和英文
        - 提供单词级和字符级时间戳
        - 智能语义分段和双语SRT格式转换
        - 与火山引擎接口兼容，可直接替换
    """
    
    try:
        # 检查输入文件
        if not os.path.exists(audio_file):
            return False, f"Audio file does not exist: {audio_file}"
        
        # 如果输出文件已存在，直接返回
        if os.path.isfile(output_filepath):
            return True, output_filepath
        
        # 获取API密钥
        if not api_key:
            api_key = ELEVENLABS_API_KEY
        
        if not api_key:
            return False, "ElevenLabs API key not found. Please set ELEVENLABS_API_KEY in environment variables."
        
        # 检查文件大小（ElevenLabs限制1GB）
        file_size = os.path.getsize(audio_file)
        if file_size > 1024 * 1024 * 1024:  # 1GB
            return False, f"Audio file too large: {file_size} bytes (max 1GB)"
        
        if not input_text or input_text.strip() == "":
            return False, "Input text cannot be empty"
        
        print(f"📝 ElevenLabs Force Alignment: {os.path.basename(audio_file)} ({file_size} bytes)")
        print(f"   Text: {input_text[:50]}{'...' if len(input_text) > 50 else ''}")
        
        # 准备API请求
        url = "https://api.elevenlabs.io/v1/forced-alignment"
        headers = {"xi-api-key": api_key}
        
        # 发送请求
        with open(audio_file, 'rb') as audio_filehandle:
            files = {
                'file': (os.path.basename(audio_file), audio_filehandle, 'audio/mpeg')
            }
            data = {'text': input_text}
            
            print(f"🚀 Calling ElevenLabs Force Alignment API...")
            start_time = time.time()
            
            response = requests.post(url, headers=headers, files=files, data=data, timeout=120)
            elapsed_time = time.time() - start_time
            
            print(f"📡 API response received in {elapsed_time:.1f}s")
        
        # 检查响应
        if response.status_code != 200:
            error_msg = f"ElevenLabs API error: {response.status_code} - {response.text}"
            print(f"❌ {error_msg}")
            return False, error_msg
        
        # 解析响应数据
        alignment_data = response.json()
        
        if 'words' not in alignment_data:
            return False, f"Invalid API response: missing 'words' field. Response: {alignment_data}"
        
        words = alignment_data['words']
        if not words:
            return False, "No word alignment data received from API"
        
        print(f"✅ Force alignment successful: {len(words)} words aligned")
        
        # Use semantic segmentation or simple segmentation
        if use_semantic_segmentation:
            # Use new Gemini semantic segmentation
            srt_success, srt_result = _elevenlabs_semantic_srt_with_gemini(
                words, output_filepath, input_text, max_chars_per_line, language, model
            )
        else:
            # Use original simple segmentation
            srt_success, srt_result = _elevenlabs_words_to_srt(
                words, output_filepath, input_text, max_chars_per_line
            )
        
        if srt_success:
            print(f"✅ SRT file created: {output_filepath}")
            return True, output_filepath
        else:
            return False, f"SRT conversion failed: {srt_result}"
            
    except requests.exceptions.Timeout:
        return False, "ElevenLabs API timeout: request took too long to respond"
    except requests.exceptions.RequestException as e:
        return False, f"Network error calling ElevenLabs API: {str(e)}"
    except Exception as e:
        import traceback
        error_info = f"ElevenLabs Force Alignment error: {str(e)}\n{traceback.format_exc()}"
        print(error_info)
        return False, error_info


def _elevenlabs_words_to_srt(
    words: List[Dict[str, Any]], 
    output_path: str, 
    original_text: str,
    max_chars_per_line: int = 40
) -> Tuple[bool, str]:
    """
    将ElevenLabs单词级时间戳转换为SRT字幕文件（内部函数）
    
    Args:
        words: ElevenLabs API返回的单词列表
        output_path: 输出SRT文件路径
        original_text: 原始文本（用于上下文）
        max_chars_per_line: 每行最大字符数
    
    Returns:
        Tuple[bool, str]: (成功状态, 结果信息)
    """
    
    try:
        # 将单词分组为字幕段
        subtitle_segments = _group_words_into_segments(words, max_chars_per_line)
        
        if not subtitle_segments:
            return False, "No subtitle segments created from word data"
        
        # 生成SRT内容
        srt_content = []
        
        for i, segment in enumerate(subtitle_segments, 1):
            # 格式化时间戳
            start_time = _seconds_to_srt_time(segment['start'])
            end_time = _seconds_to_srt_time(segment['end'])
            
            # 添加SRT条目
            srt_content.append(str(i))
            srt_content.append(f"{start_time} --> {end_time}")
            srt_content.append(segment['text'])
            srt_content.append("")  # 空行分隔
        
        # 写入文件
        srt_text = '\n'.join(srt_content)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(srt_text)
        
        # 验证生成的文件
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"📄 SRT file created: {len(subtitle_segments)} segments, {file_size} bytes")
            return True, f"SRT file created successfully with {len(subtitle_segments)} segments"
        else:
            return False, "SRT file was not created"
            
    except Exception as e:
        return False, f"SRT conversion error: {str(e)}"


def _group_words_into_segments(words: List[Dict[str, Any]], max_chars_per_line: int) -> List[Dict[str, Any]]:
    """
    将单词列表分组为合适的字幕段（内部函数）
    
    Args:
        words: 单词列表，每个包含text, start, end
        max_chars_per_line: 每行最大字符数
    
    Returns:
        List[Dict]: 字幕段列表，每个包含text, start, end
    """
    
    segments = []
    current_segment = {
        'words': [],
        'start': None,
        'end': None,
        'char_count': 0
    }
    
    max_words_per_subtitle = 8  # 每个字幕段最大单词数
    
    for word in words:
        word_text = word['text'].strip()
        word_start = word['start']
        word_end = word['end']
        
        # 检查是否需要开始新段落
        should_start_new = False
        
        if not current_segment['words']:
            # 第一个单词
            should_start_new = False
        elif len(current_segment['words']) >= max_words_per_subtitle:
            # 单词数量超限
            should_start_new = True
        elif current_segment['char_count'] + len(word_text) + 1 > max_chars_per_line:
            # 字符数超限
            should_start_new = True
        elif word_text in ['。', '！', '？', '.', '!', '?'] and len(current_segment['words']) > 3:
            # 遇到句号且已有足够单词
            current_segment['words'].append(word_text)
            current_segment['char_count'] += len(word_text)
            current_segment['end'] = word_end
            should_start_new = True
        
        if should_start_new and current_segment['words']:
            # 完成当前段落
            segment_text = ''.join(current_segment['words'])
            segments.append({
                'text': segment_text.strip(),
                'start': current_segment['start'],
                'end': current_segment['end']
            })
            
            # 开始新段落
            current_segment = {
                'words': [word_text],
                'start': word_start,
                'end': word_end,
                'char_count': len(word_text)
            }
        else:
            # 添加到当前段落
            if current_segment['start'] is None:
                current_segment['start'] = word_start
            
            current_segment['words'].append(word_text)
            current_segment['end'] = word_end
            current_segment['char_count'] += len(word_text)
    
    # 添加最后一个段落
    if current_segment['words']:
        segment_text = ''.join(current_segment['words'])
        segments.append({
            'text': segment_text.strip(),
            'start': current_segment['start'],
            'end': current_segment['end']
        })
    
    return segments



def _create_elevenlabs_semantic_prompt(
    words_data: List[Dict[str, Any]], 
    max_chars_per_line: int = 20
) -> str:
    """
    Create semantic segmentation prompt for Gemini AI
    
    Args:
        words_data: ElevenLabs word-level timing data
        max_chars_per_line: Maximum characters per subtitle line
    
    Returns:
        str: Gemini prompt
    """
    
    import json
    
    # Convert words to JSON for prompt
    words_json = json.dumps(words_data, ensure_ascii=False, indent=2)
    
    prompt = f"""You are an expert subtitle creator specializing in semantic segmentation and bilingual subtitles.

## YOUR TASK:
Transform the following word-level timing data into properly segmented SRT subtitles with these requirements:

1. **Semantic Segmentation**: 
   - Group words into meaningful phrases and sentences
   - Each subtitle line should be a complete thought or phrase
   - **LENGTH RULES**: 
     * Try to use as much of the {max_chars_per_line} character limit as possible
     * ONLY break into new subtitle when exceeding {max_chars_per_line} characters
     * DO NOT break short sentences that fit within the limit
     * Example: If limit is 30, "这就构成了我们今天真正要去解开的核心谜题" (20 chars) should be ONE line, not broken
   - When breaking is necessary, break at natural pause points (commas, conjunctions, etc.)
   - Never break in the middle of a phrase or compound word like "一百八十度"

2. **Bilingual Format**:
   - If the original text is Chinese/Japanese/Korean/etc., create bilingual subtitles
   - Format: Original language on first line, English translation on second line
   - If original is English, keep single language
   - **IMPORTANT**: English translation must ALWAYS be on ONE SINGLE LINE, never break it

3. **CRITICAL PUNCTUATION AND SPACING RULES**:
   - **ABSOLUTELY MUST REMOVE ALL QUOTATION MARKS**: Remove "" '' "" '' 「」 『』 and replace with spaces
   - REMOVE ALL Chinese punctuation marks: ，。！？；：（）【】〈〉《》
   - REMOVE ALL English punctuation at beginning and end of lines
   - NO punctuation at the start or end of any subtitle line
   - **IMPORTANT**: Quotation marks MUST be removed, not kept!
   - **Mixed Chinese-English**: Add spaces around English words in Chinese text
   - Examples of quote removal:
     * "混合政体" → 混合政体
     * "中道" → 中道  
     * 最好的政体是"混合政体" → 最好的政体是 混合政体
     * 追求"中道"，避免极端 → 追求 中道 避免极端
     * "认识世界" → 认识世界
     * "改造世界" → 改造世界
   - Other examples:
     * "因此，铭记历史，" → "因此 铭记历史"
     * "Hello, world!" → "Hello world"
     * "今天学习Python编程" → "今天学习 Python 编程"
     * "使用API接口" → "使用 API 接口"

4. **Timing Rules**:
   - Use the first word's start time as subtitle start
   - Use the last word's end time as subtitle end
   - Each subtitle should be 1-4 seconds long ideally
   - Never exceed 7 seconds for a single subtitle

5. **Output Format**:
   Return a JSON array with this structure:
   ```json
   [
     {{
       "index": 1,
       "start": 0.123,
       "end": 2.456,
       "original": "原文内容没有标点",
       "translation": "Complete English translation on one line without breaks"
     }},
     ...
   ]
   ```

## WORD-LEVEL DATA:
{words_json}

## IMPORTANT:
- Focus on natural reading flow and comprehension
- **MINIMIZE LINE BREAKS**: Only break when text exceeds {max_chars_per_line} characters
- **BAD EXAMPLE** (too many breaks):
  "这就构成了" (6 chars) → Break → "我们" (2 chars) ❌ WRONG - should be one line
- **GOOD EXAMPLE**:
  "这就构成了我们今天真正要去解开的核心谜题" (20 chars) → One subtitle ✅ CORRECT
- Never split compound words or numbers like "一百八十度", "API接口", etc.
- **VALIDATION**: Check your output - it should NOT contain any quotes "" '' "" '' 「」 『』
- MUST remove ALL punctuation marks as specified above, especially quotation marks
- English translation MUST NEVER be broken into multiple lines
- Return ONLY the JSON array, no explanations"""

    return prompt


def _elevenlabs_semantic_srt_with_gemini(
    words: List[Dict[str, Any]],
    output_filepath: str,
    original_text: str,
    max_chars_per_line: int = 20,
    language: str = 'chinese',
    model: str = None
) -> Tuple[bool, str]:
    """
    Use Gemini AI for semantic segmentation and bilingual SRT generation
    
    Args:
        words: ElevenLabs API word list
        output_filepath: Output SRT file path
        original_text: Original text for context
        max_chars_per_line: Max characters per line
        language: Language type
    
    Returns:
        Tuple[bool, str]: (success status, result path or error message)
    """
    
    try:
        import json
        import google.generativeai as genai
        
        # Configure Gemini
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Check if bilingual mode
        is_bilingual = language.lower() != 'english'
        
        if is_bilingual:
            print(f"🌐 Bilingual mode detected (language: {language})")
        
        # Use the user's specified max_chars directly - they know what they want
        adjusted_max_chars = max_chars_per_line
        
        print(f"🧠 Using Gemini for semantic segmentation...")
        print(f"   Words: {len(words)}, Max chars/line: {adjusted_max_chars}")
        
        # Create prompt with adjusted character limit
        prompt = _create_elevenlabs_semantic_prompt(words, adjusted_max_chars)
        
        # Call Gemini
        # Use provided model or default to GEMINI_MODEL
        model_name = model if model else GEMINI_MODEL
        model = genai.GenerativeModel(model_name)
        
        print("🚀 Calling Gemini for semantic segmentation...")
        start_time = time.time()
        
        response = model.generate_content(prompt)
        
        elapsed = time.time() - start_time
        print(f"✅ Gemini responded in {elapsed:.1f}s")
        
        # Parse response
        response_text = response.text.strip()
        
        # Clean up response - remove markdown code blocks if present
        if response_text.startswith('```json'):
            response_text = response_text[7:]
        if response_text.startswith('```'):
            response_text = response_text[3:]
        if response_text.endswith('```'):
            response_text = response_text[:-3]
        
        # Parse JSON
        try:
            segments = json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse Gemini response as JSON: {e}")
            # Fallback to simple segmentation
            print("⚠️ Falling back to simple character-based segmentation")
            return _elevenlabs_words_to_srt(words, output_filepath, original_text, max_chars_per_line)
        
        if not isinstance(segments, list):
            print("⚠️ Invalid response format, falling back to simple segmentation")
            return _elevenlabs_words_to_srt(words, output_filepath, original_text, max_chars_per_line)
        
        print(f"📝 Created {len(segments)} subtitle segments")
        
        # Convert segments to SRT format
        srt_lines = []
        
        for seg in segments:
            # Format timestamps
            start_time = _seconds_to_srt_time(seg['start'])
            end_time = _seconds_to_srt_time(seg['end'])
            
            # Build subtitle entry
            srt_lines.append(str(seg['index']))
            srt_lines.append(f"{start_time} --> {end_time}")
            
            # Add original text
            srt_lines.append(seg['original'])
            
            # Add translation if exists (ensure it's on single line)
            if 'translation' in seg and seg['translation']:
                # Remove any line breaks from translation and clean it up
                translation = seg['translation'].replace('\n', ' ').replace('  ', ' ').strip()
                srt_lines.append(translation)
            
            srt_lines.append("")  # Empty line between entries
        
        # Write to file
        srt_content = '\n'.join(srt_lines)
        
        os.makedirs(os.path.dirname(output_filepath) if os.path.dirname(output_filepath) else '.', exist_ok=True)
        
        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(srt_content)
        
        file_size = os.path.getsize(output_filepath)
        print(f"✅ Semantic SRT file created: {output_filepath} ({file_size} bytes)")
        
        return True, output_filepath
        
    except Exception as e:
        error_msg = f"Semantic SRT generation error: {str(e)}"
        print(f"❌ {error_msg}")
        print("⚠️ Falling back to simple character-based segmentation")
        # Fallback to original simple segmentation
        return _elevenlabs_words_to_srt(words, output_filepath, original_text, max_chars_per_line)


def _seconds_to_srt_time(seconds: float) -> str:
    """
    将秒数转换为SRT时间格式 (HH:MM:SS,mmm)（内部函数）
    
    Args:
        seconds (float): 时间（秒）
    
    Returns:
        str: SRT格式的时间字符串
    """
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"


def cli():
    """Command-line interface for ElevenLabs SRT Generator"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Generate synchronized SRT subtitles using ElevenLabs Force Alignment API'
    )
    parser.add_argument('audio', help='Path to audio file')
    parser.add_argument('text', help='Text content or path to text file')
    parser.add_argument('-o', '--output', default='output.srt', help='Output SRT file path')
    parser.add_argument('-m', '--max-chars', type=int, default=20, help='Max characters per line')
    parser.add_argument('-l', '--language', default='chinese', help='Language code')
    parser.add_argument('--no-semantic', action='store_true', help='Disable semantic segmentation')
    parser.add_argument('--api-key', help='ElevenLabs API key (overrides .env)')
    parser.add_argument('--model', default=None, help=f'Gemini model to use (default: {GEMINI_MODEL})')
    
    args = parser.parse_args()
    
    # Read text from file if it's a path
    if os.path.exists(args.text):
        with open(args.text, 'r', encoding='utf-8') as f:
            text_content = f.read()
    else:
        text_content = args.text
    
    # Generate subtitles
    success, result = elevenlabs_force_alignment_to_srt(
        audio_file=args.audio,
        input_text=text_content,
        output_filepath=args.output,
        api_key=args.api_key,
        max_chars_per_line=args.max_chars,
        language=args.language,
        use_semantic_segmentation=not args.no_semantic,
        model=args.model
    )
    
    if success:
        print(f"✅ Subtitles saved to: {result}")
        return 0
    else:
        print(f"❌ Error: {result}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(cli())