import os
import yt_dlp

def extract_m3u8_link(file_path):
    """Extracts the first valid M3U8 link from a text file."""
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if '.m3u8' in line:
                # Ensure we extract only the URL part if there's extra text
                m3u8_url = line.split()[-1]  # Extract the last part as the URL
                if m3u8_url.startswith("http"):
                    return m3u8_url  # Return the cleaned M3U8 link
    return None  # Return None if no valid M3U8 link is found

def format_mp4_filename(txt_filename):
    """Formats the .txt filename to the desired .mp4 format."""
    base_filename = os.path.splitext(txt_filename)[0]  # Remove .txt extension
    formatted_filename = base_filename.replace("__", " ").replace("_", " ") + ".mp4"  # Remove underscores and replace with spaces
    return formatted_filename

def download_m3u8_from_file(file_path):
    # Extract the M3U8 link from the file
    m3u8_url = extract_m3u8_link(file_path)
    
    if not m3u8_url:
        print(f"No valid M3U8 link found in {file_path}. Skipping file.")
        return

    # Format the output filename for the MP4
    txt_filename = os.path.basename(file_path)
    output_filename = format_mp4_filename(txt_filename)

    # Check if the file already exists to prevent duplicate downloads
    if os.path.exists(output_filename):
        print(f"{output_filename} already exists. Skipping download.")
        return

    # Define yt-dlp options to download best available quality
    ydl_opts = {
        'format': 'best',  # Download the best available quality
        'noplaylist': True,  # Do not download playlists
        'outtmpl': output_filename  # Output path for the downloaded file
    }

    # Use yt-dlp to fetch available formats and check for 720p
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(m3u8_url, download=False)  # Fetch info without downloading
            # Check if a 720p format is available
            target_format = next((f for f in info_dict['formats'] if f.get('height') == 720), None)
            
            if target_format:
                print(f"720p format found. Downloading {output_filename} in 720p...")
                ydl_opts['format'] = target_format['format_id']  # Download 720p
            else:
                print(f"No 720p format available for {output_filename}. Downloading best available format...")
            
            # Download the video
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([m3u8_url])

    except yt_dlp.utils.DownloadError as e:
        print(f"Error downloading {m3u8_url}: {e}")

if __name__ == "__main__":
    # Get the current directory where the script is located
    current_directory = os.getcwd()
    
    # Loop through all .txt files in the directory
    for filename in os.listdir(current_directory):
        if filename.endswith(".txt"):
            txt_file_path = os.path.join(current_directory, filename)
            print(f"Processing {txt_file_path}...")
            download_m3u8_from_file(txt_file_path)
            
