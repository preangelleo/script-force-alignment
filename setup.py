#!/usr/bin/env python3
"""
Setup script for ElevenLabs Force Alignment SRT Generator
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="elevenlabs-srt-generator",
    version="1.1.0",
    author="Script Force Alignment Contributors",
    author_email="",
    description="Generate synchronized SRT subtitles using ElevenLabs Force Alignment API with AI-powered semantic segmentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/preangelleo/script-force-alignment",
    project_urls={
        "Bug Tracker": "https://github.com/preangelleo/script-force-alignment/issues",
        "Documentation": "https://github.com/preangelleo/script-force-alignment#readme",
        "Source Code": "https://github.com/preangelleo/script-force-alignment",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Multimedia :: Video",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="subtitles srt elevenlabs force-alignment speech-to-text transcription ai gemini bilingual",
    py_modules=["main"],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "google-generativeai>=0.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "build>=0.10.0",
            "twine>=4.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "elevenlabs-srt=main:cli",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "LICENSE", ".env.example", "system_prompt.txt"],
    },
    zip_safe=False,
)