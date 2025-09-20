import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
import subprocess
import time
from urllib.parse import urlparse
import json

# Set appearance mode
ctk.set_appearance_mode("system")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

class YouTubeDownloader:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Arijit's YT Video Downloader")
        self.root.geometry("900x750")  # Made taller to ensure all elements are visible
        self.root.minsize(800, 700)    # Set minimum size to prevent cutting off
        self.root.resizable(True, True)
        
        # Variables
        self.download_path = tk.StringVar()
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp4")
        self.quality_var = tk.StringVar(value="720p")
        self.is_playlist = tk.BooleanVar()
        self.is_audio_only = tk.BooleanVar()
        
        # Progress variables
        self.current_progress = tk.DoubleVar()
        self.total_videos = tk.IntVar()
        self.current_video = tk.IntVar()
        
        # Download state
        self.is_downloading = False
        self.download_thread = None
        
        self.setup_ui()
        self.check_dependencies()
        
    def check_dependencies(self):
        """Check if yt-dlp is installed"""
        try:
            subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            messagebox.showwarning(
                "Missing Dependency", 
                "yt-dlp is not installed. Please install it using:\npip install yt-dlp"
            )
    
    def setup_ui(self):
        # Create scrollable main frame to ensure all content is accessible
        main_container = ctk.CTkScrollableFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_container, 
            text="🎥 Arijit's YT Video Downloader", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(0, 30))
        
        # URL Input Section
        url_frame = ctk.CTkFrame(main_container)
        url_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(url_frame, text="YouTube URL:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.url_entry = ctk.CTkEntry(
            url_frame, 
            textvariable=self.url_var,
            placeholder_text="Enter YouTube video or playlist URL here...",
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.url_entry.pack(fill="x", padx=20, pady=(0, 15))
        
        # Options Section
        options_frame = ctk.CTkFrame(main_container)
        options_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(options_frame, text="Download Options:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        # Format and Quality Selection
        format_frame = ctk.CTkFrame(options_frame)
        format_frame.pack(fill="x", padx=20, pady=10)
        
        # Audio Only Checkbox
        self.audio_checkbox = ctk.CTkCheckBox(
            format_frame, 
            text="Audio Only (MP3)", 
            variable=self.is_audio_only,
            command=self.toggle_audio_mode,
            font=ctk.CTkFont(size=14)
        )
        self.audio_checkbox.pack(side="left", padx=20, pady=15)
        
        # Playlist Checkbox
        self.playlist_checkbox = ctk.CTkCheckBox(
            format_frame, 
            text="Playlist Mode", 
            variable=self.is_playlist,
            font=ctk.CTkFont(size=14)
        )
        self.playlist_checkbox.pack(side="left", padx=30, pady=15)
        
        # Quality Selection
        quality_frame = ctk.CTkFrame(options_frame)
        quality_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(quality_frame, text="Quality:", font=ctk.CTkFont(size=14)).pack(side="left", padx=20, pady=15)
        
        self.quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            variable=self.quality_var,
            values=["2160p (4K)", "1440p (2K)", "1080p (Full HD)", "720p (HD)", "480p", "360p", "240p", "best", "worst"],
            font=ctk.CTkFont(size=12),
            width=150
        )
        self.quality_menu.pack(side="left", padx=15, pady=15)
        
        # Download Path Section
        path_frame = ctk.CTkFrame(main_container)
        path_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(path_frame, text="Download Location:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        path_input_frame = ctk.CTkFrame(path_frame)
        path_input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.path_entry = ctk.CTkEntry(
            path_input_frame,
            textvariable=self.download_path,
            placeholder_text="Select download folder...",
            height=40,
            font=ctk.CTkFont(size=12)
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(15, 10), pady=12)
        
        browse_btn = ctk.CTkButton(
            path_input_frame,
            text="📁 Browse",
            width=100,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.browse_folder
        )
        browse_btn.pack(side="right", padx=(5, 15), pady=12)
        
        # Progress Section
        progress_frame = ctk.CTkFrame(main_container)
        progress_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(progress_frame, text="Download Progress:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=25)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 10))
        self.progress_bar.set(0)
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="Ready to download", font=ctk.CTkFont(size=14))
        self.progress_label.pack(padx=20, pady=(0, 15))
        
        # Status Text Area
        status_frame = ctk.CTkFrame(main_container)
        status_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(status_frame, text="Status Log:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.status_text = ctk.CTkTextbox(status_frame, height=140, font=ctk.CTkFont(size=11))
        self.status_text.pack(fill="x", padx=20, pady=(0, 15))
        
        # CONTROL BUTTONS SECTION - MOST IMPORTANT
        button_frame = ctk.CTkFrame(main_container)
        button_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(button_frame, text="Controls:", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Create a centered container for buttons
        buttons_container = ctk.CTkFrame(button_frame)
        buttons_container.pack(pady=(0, 20))
        
        # Make buttons large and prominent
        self.download_btn = ctk.CTkButton(
            buttons_container,
            text="📥 START DOWNLOAD",
            height=55,
            width=220,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#28a745",  # Green color
            hover_color="#218838",
            command=self.start_download
        )
        self.download_btn.pack(side="left", padx=20, pady=15)
        
        self.stop_btn = ctk.CTkButton(
            buttons_container,
            text="⏹️ STOP",
            height=55,
            width=120,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#dc3545",  # Red color
            hover_color="#c82333",
            command=self.stop_download,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=15, pady=15)
        
        self.clear_btn = ctk.CTkButton(
            buttons_container,
            text="🗑️ CLEAR",
            height=55,
            width=120,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#6c757d",  # Gray color
            hover_color="#5a6268",
            command=self.clear_all
        )
        self.clear_btn.pack(side="left", padx=15, pady=15)
        
        # Add extra space at bottom to ensure buttons are always visible
        ctk.CTkLabel(main_container, text="", height=30).pack()
        
        # Set default download path
        self.download_path.set(os.path.join(os.path.expanduser("~"), "Downloads"))
    
    def toggle_audio_mode(self):
        """Toggle between audio and video mode"""
        if self.is_audio_only.get():
            self.quality_var.set("best")
            self.quality_menu.configure(state="disabled")
        else:
            self.quality_menu.configure(state="normal")
    
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
    
    def log_message(self, message):
        """Add message to status text area"""
        timestamp = time.strftime('%H:%M:%S')
        self.status_text.insert("end", f"[{timestamp}] {message}\n")
        self.status_text.see("end")
        self.root.update_idletasks()
    
    def update_progress(self, percent, message=""):
        """Update progress bar and label"""
        self.progress_bar.set(percent / 100)
        if message:
            self.progress_label.configure(text=message)
        self.root.update_idletasks()
    
    def validate_url(self, url):
        """Validate YouTube URL"""
        youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
        try:
            parsed = urlparse(url)
            return any(domain in parsed.netloc for domain in youtube_domains)
        except:
            return False
    
    def get_video_info(self, url):
        """Get video information using yt-dlp"""
        try:
            cmd = ['yt-dlp', '--dump-json', '--no-download', url]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Handle playlist
            if '\n' in result.stdout:
                # Multiple videos (playlist)
                videos = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        videos.append(json.loads(line))
                return videos
            else:
                # Single video
                return [json.loads(result.stdout)]
        except subprocess.CalledProcessError as e:
            self.log_message(f"Error getting video info: {e}")
            return None
    
    def download_video(self):
        """Download video in separate thread"""
        url = self.url_var.get().strip()
        download_path = self.download_path.get()
        
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not download_path or not os.path.exists(download_path):
            messagebox.showerror("Error", "Please select a valid download folder")
            return
        
        if not self.validate_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return
        
        try:
            self.log_message("🔍 Getting video information...")
            self.update_progress(5, "Fetching video details...")
            
            # Get video info
            videos = self.get_video_info(url)
            if not videos:
                return
            
            self.total_videos.set(len(videos))
            self.log_message(f"📊 Found {len(videos)} video(s) to download")
            
            # Prepare download command
            cmd = ['yt-dlp']
            
            # Output template
            if self.is_playlist.get() and len(videos) > 1:
                cmd.extend(['-o', f'{download_path}/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'])
            else:
                cmd.extend(['-o', f'{download_path}/%(title)s.%(ext)s'])
            
            # Format selection
            if self.is_audio_only.get():
                cmd.extend(['--extract-audio', '--audio-format', 'mp3', '--audio-quality', '0'])
                self.log_message("🎵 Audio-only mode selected")
            else:
                quality = self.quality_var.get()
                if quality in ['best', 'worst']:
                    cmd.extend(['-f', quality])
                else:
                    # Extract number from quality (e.g., "720p (HD)" -> "720")
                    quality_num = quality.split('p')[0]
                    cmd.extend(['-f', f'best[height<={quality_num}]'])
                self.log_message(f"📺 Video quality: {quality}")
            
            # Add progress hook for better progress tracking
            cmd.extend(['--newline'])
            
            # Add URL
            cmd.append(url)
            
            self.log_message(f"🚀 Starting download...")
            self.log_message(f"📂 Destination: {download_path}")
            self.update_progress(10, "Starting download...")
            
            # Start download process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor progress
            while process.poll() is None and self.is_downloading:
                output = process.stdout.readline()
                if output:
                    self.parse_progress(output.strip())
            
            # Check if process completed successfully
            if process.poll() == 0 and self.is_downloading:
                self.update_progress(100, "Download completed successfully!")
                self.log_message("✅ Download completed successfully!")
                messagebox.showinfo("Success", "Download completed successfully!")
            elif not self.is_downloading:
                self.log_message("⏹️ Download stopped by user")
            else:
                self.log_message("❌ Download failed or was interrupted")
                messagebox.showerror("Error", "Download failed. Check the status log for details.")
            
        except Exception as e:
            self.log_message(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            self.download_finished()
    
    def parse_progress(self, output):
        """Parse yt-dlp output for progress information"""
        try:
            if '[download]' in output:
                if '%' in output and 'of' in output:
                    # Extract percentage
                    parts = output.split()
                    for i, part in enumerate(parts):
                        if part.endswith('%'):
                            try:
                                percent = float(part.replace('%', ''))
                                # Get file info if available
                                if i + 1 < len(parts) and 'of' in parts[i+1:i+3]:
                                    file_info = ' '.join(parts[i+1:i+4])
                                    self.update_progress(percent, f"Downloading... {percent:.1f}% {file_info}")
                                else:
                                    self.update_progress(percent, f"Downloading... {percent:.1f}%")
                                break
                            except ValueError:
                                continue
                elif 'Destination:' in output:
                    filename = output.split('Destination: ')[-1]
                    self.log_message(f"📁 Saving: {os.path.basename(filename)}")
                elif 'has already been downloaded' in output:
                    self.log_message("⚠️ File already exists, skipping...")
                elif 'Downloading' in output and 'playlist' in output:
                    self.log_message(f"📋 {output}")
            
            # Log important messages
            if any(keyword in output.lower() for keyword in ['error', 'warning', 'failed']):
                self.log_message(f"⚠️ {output}")
            elif '[info]' in output and ('Available formats' not in output):
                self.log_message(f"ℹ️ {output}")
            elif 'Extracting URL' in output or 'Downloading webpage' in output:
                self.log_message(f"🔄 {output}")
                
        except Exception as e:
            # If parsing fails, just log the raw output if it's meaningful
            if output.strip() and len(output.strip()) > 10:
                self.log_message(output.strip())
    
    def start_download(self):
        """Start download process"""
        if self.is_downloading:
            return
        
        # Check dependencies first
        try:
            subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        except FileNotFoundError:
            messagebox.showerror("Error", "yt-dlp is not installed.\n\nPlease install it using:\npip install yt-dlp")
            return
        
        self.is_downloading = True
        self.download_btn.configure(state="disabled", text="⏳ DOWNLOADING...")
        self.stop_btn.configure(state="normal")
        
        # Clear previous status
        self.status_text.delete("1.0", "end")
        self.update_progress(0, "Initializing download...")
        
        # Start download thread
        self.download_thread = threading.Thread(target=self.download_video, daemon=True)
        self.download_thread.start()
    
    def stop_download(self):
        """Stop download process"""
        if not self.is_downloading:
            return
        
        self.is_downloading = False
        self.log_message("🛑 Stopping download...")
        self.update_progress(0, "Download stopped")
        
        # Try to terminate any running yt-dlp processes
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(['taskkill', '/f', '/im', 'yt-dlp.exe'], 
                             capture_output=True, check=False)
            else:  # Unix/Linux/Mac
                subprocess.run(['pkill', '-f', 'yt-dlp'], 
                             capture_output=True, check=False)
        except:
            pass
        
        self.download_finished()
    
    def download_finished(self):
        """Reset UI after download completion"""
        self.is_downloading = False
        self.download_btn.configure(state="normal", text="📥 START DOWNLOAD")
        self.stop_btn.configure(state="disabled")
    
    def clear_all(self):
        """Clear all inputs and status"""
        if self.is_downloading:
            if messagebox.askyesno("Confirm", "Download is in progress. Stop and clear?"):
                self.stop_download()
            else:
                return
        
        self.url_var.set("")
        self.status_text.delete("1.0", "end")
        self.update_progress(0, "Ready to download")
        self.is_playlist.set(False)
        self.is_audio_only.set(False)
        self.quality_var.set("720p (HD)")
        self.toggle_audio_mode()
        self.log_message("🔄 Interface cleared and ready for new download")
    
    def run(self):
        """Start the application"""
        # Add a welcome message
        self.log_message("🎉 Welcome to YouTube Downloader Pro!")
        self.log_message("📝 Enter a YouTube URL and click 'START DOWNLOAD' to begin")
        self.log_message("💡 Tip: Enable 'Playlist Mode' for downloading entire playlists")
        
        self.root.mainloop()

# Installation requirements checker
def check_and_install_requirements():
    """Check and install required packages"""
    requirements = {
        'customtkinter': 'customtkinter',
        'yt-dlp': 'yt-dlp'
    }
    
    missing_packages = []
    
    for package, pip_name in requirements.items():
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(pip_name)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n⚠️ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    print("🎉 All requirements satisfied!")
    return True

if __name__ == "__main__":
    print("🎥 Arijit's YT Video Downloader")
    print("=" * 40)
    
    if check_and_install_requirements():
        try:
            app = YouTubeDownloader()
            app.run()
        except Exception as e:
            print(f"❌ Error starting application: {e}")
            print("\n💡 Try running the simple version if this doesn't work:")
            print("python simple_youtube_downloader.py")
    else:
        print("\n🛠️ Please install the required packages and try again.")
        input("Press Enter to exit...")