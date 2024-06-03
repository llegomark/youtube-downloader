# YouTube Video Downloader

A Python script to download YouTube videos and playlists with the highest resolution and caption tracks.

## Features

- Download single YouTube videos, entire playlists, or all videos from a channel.
- Automatically download the highest resolution video stream available.
- Download available caption tracks in SRT format.
- Save downloaded videos and caption files to a "Videos" folder.
- Command-line interface for easy usage.
- Robust error handling for unavailable videos and other exceptions.

## Requirements

- Python 3.12 or higher
- `pytube` library
- `beautifulsoup4` library
- `lxml` library 

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/llegomark/youtube-downloader.git
   ```

2. Navigate to the project directory:
   ```bash
   cd youtube-downloader
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To download a YouTube video, playlist, or channel content, run the script from the command line with the URL as an argument:

```bash
python downloader.py <video_url>|<playlist_url>|<channel_url>
```

Replace:
- `<video_url>` with the URL of a single YouTube video.
- `<playlist_url>` with the URL of a YouTube playlist.
- `<channel_url>` with the URL of a YouTube channel.

**Examples:**

- Download a single video:
  ```bash
  python downloader.py https://www.youtube.com/watch?v=GwpivzSzHps 
  ```

- Download a playlist:
  ```bash
  python downloader.py https://www.youtube.com/playlist?list=PLxIGRNqt1BBiGyB_BFDa8CcgapLivAcGe 
  ```
The script will automatically detect the type of URL provided and download accordingly.

Downloaded videos and caption files will be saved in a "Videos" folder created in the same directory as the script.

## Folder Structure

```
youtube-video-downloader/
├── downloader.py
├── requirements.txt
├── README.md
└── Videos/
    ├── video1.mp4
    ├── video1_en.srt
    ├── video2.mp4
    └── video2_en.srt
```

- `downloader.py`: The main Python script for downloading.
- `requirements.txt`: The list of required Python libraries.
- `README.md`: This file.
- `Videos/`: The folder where downloads are saved.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

[MIT License](LICENSE)

## Acknowledgements

- [pytube](https://github.com/pytube/pytube) library
- The open-source community

## Disclaimer

Downloading YouTube videos may be subject to YouTube's terms of service. Use this script responsibly and respect intellectual property rights.
