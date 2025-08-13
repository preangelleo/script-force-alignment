#!/usr/bin/env python3
"""
Setup and validation script for ElevenLabs Force Alignment SRT Generator
Ensures environment is properly configured before running the main application.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_environment():
    """
    Check if the environment is properly configured with required API keys.
    
    Returns:
        bool: True if environment is valid, False otherwise
    """
    
    print("🔧 ElevenLabs Force Alignment Setup Validator")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    env_example_file = Path(".env.example")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("\n📝 Instructions to create .env file:")
        
        if env_example_file.exists():
            print("1. Copy the example file: cp .env.example .env")
            print("2. Edit .env and add your API keys")
        else:
            print("1. Create a new .env file")
            print("2. Add the following lines:")
            print("   ELEVENLABS_API_KEY=your_elevenlabs_api_key_here")
            print("   GEMINI_API_KEY=your_gemini_api_key_here")
        
        return False
    
    # Load environment variables
    load_dotenv()
    
    # Check for required API keys
    errors = []
    warnings = []
    
    # Check ElevenLabs API key
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    if not elevenlabs_key:
        errors.append("ELEVENLABS_API_KEY is not set in .env file")
    elif elevenlabs_key == "your_elevenlabs_api_key_here":
        errors.append("ELEVENLABS_API_KEY still has the placeholder value")
    else:
        print("✅ ELEVENLABS_API_KEY found")
    
    # Check Gemini API key
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        errors.append("GEMINI_API_KEY is not set in .env file")
    elif gemini_key == "your_gemini_api_key_here":
        errors.append("GEMINI_API_KEY still has the placeholder value")
    else:
        print("✅ GEMINI_API_KEY found")
    
    # Report errors
    if errors:
        print("\n❌ Configuration Errors:")
        for error in errors:
            print(f"   - {error}")
        
        print("\n📝 How to get API keys:")
        print("   ElevenLabs: https://elevenlabs.io/")
        print("   Google Gemini: https://makersuite.google.com/app/apikey")
        
        return False
    
    print("\n✅ All required API keys are configured!")
    return True

def check_dependencies():
    """
    Check if all required Python packages are installed.
    
    Returns:
        bool: True if all dependencies are installed, False otherwise
    """
    
    print("\n📦 Checking Python dependencies...")
    
    missing_packages = []
    
    # Check required packages
    required_packages = {
        'requests': 'requests',
        'dotenv': 'python-dotenv',
        'google.generativeai': 'google-generativeai'
    }
    
    for module_name, package_name in required_packages.items():
        try:
            if module_name == 'google.generativeai':
                # Special handling for google.generativeai
                import google.generativeai
            elif '.' in module_name:
                # Handle other submodules
                __import__(module_name)
            else:
                __import__(module_name)
            print(f"   ✅ {package_name} is installed")
        except (ImportError, AttributeError):
            missing_packages.append(package_name)
            print(f"   ❌ {package_name} is NOT installed")
    
    if missing_packages:
        print("\n❌ Missing packages detected!")
        print("Install them with:")
        print(f"   pip install {' '.join(missing_packages)}")
        print("\nOr install all dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def create_sample_files():
    """
    Create sample directories and inform user about sample files.
    """
    
    print("\n📁 Setting up sample directories...")
    
    # Create samples directory
    samples_dir = Path("samples")
    samples_dir.mkdir(exist_ok=True)
    print(f"   ✅ Created {samples_dir} directory")
    
    # Create test_output directory
    test_output_dir = Path("test_output")
    test_output_dir.mkdir(exist_ok=True)
    print(f"   ✅ Created {test_output_dir} directory")
    
    print("\n📝 Next steps:")
    print("1. Place your audio file in the 'samples' directory")
    print("2. Update the parameters in test.py or example_usage.py")
    print("3. Run the test: python test.py")

def main():
    """
    Main setup validation function.
    """
    
    print("🚀 ElevenLabs Force Alignment Setup")
    print("=" * 50)
    
    # Check environment
    env_valid = check_environment()
    
    # Check dependencies
    deps_valid = check_dependencies()
    
    # Create sample directories
    if env_valid and deps_valid:
        create_sample_files()
        
        print("\n✨ Setup validation completed successfully!")
        print("You can now run the force alignment tool.")
        print("\nQuick start:")
        print("   python test.py        # Run tests")
        print("   python example_usage.py   # Run example")
        
        return 0
    else:
        print("\n❌ Setup validation failed!")
        print("Please fix the issues above and run setup.py again.")
        return 1

if __name__ == "__main__":
    sys.exit(main())