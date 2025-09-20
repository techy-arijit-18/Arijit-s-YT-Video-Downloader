# 🎥 Arijit's YT Video Downloader

@techy-arijit-18

A comprehensive Python application with modern GUI for downloading YouTube videos and playlists with support for multiple resolutions, audio-only downloads, and real-time progress tracking.

## ✨ Features

### 🎯 Core Features
- **Modern GUI Interface** - Beautiful, user-friendly interface using CustomTkinter
- **Video & Audio Downloads** - Support for both video (MP4) and audio-only (MP3) downloads
- **Playlist Support** - Download entire YouTube playlists with organized folder structure
- **Resolution Selection** - Choose from 240p to 2160p (4K) or select "best" quality
- **Real-time Progress Tracking** - Visual progress bar with download status updates
- **Threading Support** - Non-blocking downloads that keep the GUI responsive

### 🛠️ Technical Features  
- **Multi-threaded Architecture** - Separate threads for GUI and download operations
- **Error Handling** - Comprehensive error handling with user-friendly messages
- **Download Management** - Start, stop, and monitor download progress
- **Path Selection** - Custom download folder selection
- **Status Logging** - Real-time status updates and download information
- **URL Validation** - Automatic validation of YouTube URLs

## 📋 Requirements

- **Python 3.7+**
- **yt-dlp** - Modern YouTube downloader backend
- **customtkinter** - Modern GUI framework (for Pro version)
- **tkinter** - Standard GUI framework (built-in with Python)

### How to Use

1. **Enter YouTube URL**
   - Paste any YouTube video or playlist URL
   - The app will automatically detect if it's a playlist

2. **Select Download Options**
   - Choose between video download or audio-only (MP3)
   - Select video quality (240p to 2160p)
   - Enable playlist mode if downloading multiple videos

3. **Choose Download Location**
   - Use the Browse button to select your download folder
   - Default location is your Downloads folder

4. **Start Download**
   - Click "Start Download" to begin
   - Monitor progress in real-time
   - View detailed status in the log area

5. **Download Management**
   - Use "Stop" to cancel ongoing downloads
   - Use "Clear" to reset all fields

## 🎮 User Interface Guide

### Main Application (youtube_downloader_pro.py)
- **Modern Design** - Dark/Light theme support with CustomTkinter
- **Intuitive Layout** - All controls organized in logical sections
- **Real-time Feedback** - Progress bars and status updates
- **Responsive Design** - Resizable window with proper scaling

### Simple Version (simple_youtube_downloader.py)
- **Standard Look** - Uses default system theme
- **Same Functionality** - All core features available
- **Lighter Requirements** - Only needs yt-dlp package
- **Cross-platform** - Works on all systems with Python

## 🔧 Configuration Options

### Video Quality Options
- **2160p** - 4K Ultra HD
- **1440p** - 2K Quad HD  
- **1080p** - Full HD
- **720p** - HD (Default)
- **480p** - Standard Definition
- **360p** - Low Quality
- **240p** - Minimal Quality
- **best** - Highest available quality
- **worst** - Lowest available quality

### Audio Options
- **Format**: MP3
- **Quality**: High quality (320kbps equivalent)
- **Auto-extraction**: Automatic audio extraction from video

### Playlist Options
- **Auto-detection**: Automatically detects playlist URLs
- **Organized Downloads**: Creates playlist folders
- **Sequential Downloads**: Downloads videos one by one
- **Progress Tracking**: Individual progress for each video

## 📄 License
This project is open source and available.

## ⚠️ Disclaimer
This tool is for personal use only. Please respect YouTube's Terms of Service and copyright laws. Only download content you have permission to download.

## 🎉 Acknowledgments
- **yt-dlp** - Powerful YouTube downloader backend
- **CustomTkinter** - Modern GUI framework
- **Python Community** - For excellent documentation and support

---

*Enjoy downloading your favorite YouTube content responsibly!* 🎬