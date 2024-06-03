import os
import sys
import logging
from pytube import YouTube, Playlist, Channel
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable, RegexMatchError, PytubeError
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_xml_to_srt(xml_captions):
    """Converts YouTube's XML caption format to SRT format using lxml."""
    soup = BeautifulSoup(xml_captions, 'xml')  # Parse using lxml
    srt_captions = ""
    i = 1
    for p in soup.find_all('p'):
        start_seconds = int(float(p['t']) / 1000)
        end_seconds = start_seconds + int(float(p['d']) / 1000)
        start_time = '{:02}:{:02}:{:02},000'.format(start_seconds // 3600, (start_seconds % 3600) // 60, start_seconds % 60)
        end_time = '{:02}:{:02}:{:02},000'.format(end_seconds // 3600, (end_seconds % 3600) // 60, end_seconds % 60)
        text = p.text.strip()
        srt_captions += f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
        i += 1
    return srt_captions

def download_video(url, output_path):
    try:
        # Create YouTube object
        yt = YouTube(url, on_progress_callback=on_progress)

        # Get the highest resolution video stream
        stream = yt.streams.get_highest_resolution()

        # Get additional video info
        title = yt.title
        desc = yt.description
        views = yt.views
        length = yt.length
        thumb_url = yt.thumbnail_url

        logging.info(f"Downloading: {title}")
        logging.info(f"Description: {desc}")
        logging.info(f"Views: {views}")
        logging.info(f"Length: {length} seconds")
        logging.info(f"Thumbnail URL: {thumb_url}")

        # Download the video
        stream.download(output_path)
        logging.info("Video download completed successfully.")

        # Download English caption track if available
        try:
            caption = yt.captions['en']  # Access captions like a dictionary
            if caption:
                logging.info(f"Downloading English caption track: {caption.name}")

                try:
                    # Attempt to use generate_srt_captions() first
                    srt_captions = caption.generate_srt_captions()
                except KeyError:
                    # If KeyError occurs, it's likely the pytube bug @ https://github.com/pytube/pytube/issues/1867
                    logging.warning("pytube KeyError encountered. Using XML workaround.")

                    # Download the XML caption data
                    xml_captions = caption.xml_captions

                    # Convert XML captions to SRT using lxml
                    srt_captions = convert_xml_to_srt(xml_captions)

                srt_file_path = os.path.join(output_path, f"{title}_en.srt")
                with open(srt_file_path, "w", encoding="utf-8") as text_file:
                    text_file.write(srt_captions)
                logging.info("English caption track downloaded.")
            else:
                logging.info("No English caption track found.")

        except (KeyError, AttributeError) as e:
            logging.warning(f"Failed to download English caption track. Error: {str(e)}")

    except VideoUnavailable as e:
        logging.error(f"Video {url} is unavailable. Skipping. Error: {str(e)}")

    except RegexMatchError as e:
        logging.error(f"Error matching regex pattern. Error: {str(e)}")

    except PytubeError as e:
        logging.error(f"An error occurred: {str(e)}")

def download_playlist(url, output_path):
    try:
        # Create Playlist object
        playlist = Playlist(url)

        logging.info(f"Downloading playlist: {playlist.title}")

        # Download each video in the playlist
        for video_url in playlist.video_urls:
            download_video(video_url, output_path)

        logging.info("Playlist download completed.")

    except PytubeError as e:
        logging.error(f"An error occurred: {str(e)}")

def download_channel(url, output_path):
    try:
        # Create Channel object
        channel = Channel(url)

        logging.info(f"Downloading videos from channel: {channel.channel_name}")

        # Download each video in the channel
        for video in channel.videos:
            download_video(video.watch_url, output_path)

        logging.info("Channel download completed.")

    except PytubeError as e:
        logging.error(f"An error occurred: {str(e)}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <video_url>|<playlist_url>|<channel_url>")
        sys.exit(1)

    url = sys.argv[1]

    # Create "Videos" folder if it doesn't exist
    output_path = "Videos"
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if "youtube.com/watch" in url:
        logging.info("Single video detected.")
        download_video(url, output_path)
    elif "youtube.com/playlist" in url:
        logging.info("Playlist detected.")
        download_playlist(url, output_path)
    elif "youtube.com/channel" in url or "youtube.com/c/" in url or "youtube.com/user/" in url:
        logging.info("Channel detected.")
        download_channel(url, output_path)
    else:
        logging.error("Invalid URL. Please provide a valid YouTube video, playlist, or channel URL.")
        sys.exit(1)

if __name__ == "__main__":
    main()