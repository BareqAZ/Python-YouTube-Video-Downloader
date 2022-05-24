# requirements: pytube, pytube3
# author: blu
from pytube import YouTube as Video
from pytube import Playlist
from pytube import Channel
from pytube import Search


def create_video_audio_path(video):
    path = video.title
    return path


def create_channel_path(channel):
    path = channel.channel_name
    return path


def create_playlist_path(playlist):
    path = playlist.title
    return path


def search_video(search_input):
    video_num = 1
    results = Search(search_input)
    print(f"\nWe found {len(results.results)} results\n")
    for result in results.results:
        print(f"{video_num} - {result.title}")
        video_num += 1
    try:
        selected_video = int(input("\nSelect a video to download: "))
    except Exception:
        not_found("video")
    video_to_download = results.results[selected_video - 1]
    print(f"\nSelected video: {video_to_download.title}")
    video_id = str(video_to_download)
    video_id = video_id.replace(
        "<pytube.__main__.YouTube object: videoId=", "")
    video_id = video_id.replace(">", "")
    video_link = f"https://www.youtube.com/watch?v={video_id}"
    return video_link


def on_complete(stream, file_path):
    print(f"\n\nSuccesfully downloaded {file_path}")


def playlist_video_on_complete(stream, downloaded_playlist_video_title):
    print(f"\nDownloaded {downloaded_playlist_video_title}")


def view_download_progress(stream, chunk, bytes_remaining):
    percent = (1 - bytes_remaining / stream.filesize) * 100
    print(f"\r{percent:.2f}%", end="")


def not_found(type):
    if(type == "video"):
        print("\nVideo was not found")
    elif(type == "playlist"):
        print("\nPlaylist was not found")
    elif(type == "channel"):
        print("\nChannel was not found")
    else:
        print("\nVideo, channel or playlist was not found")
    exit()


mode = input(
    "\nSelect the mode:\nVideo(v) | Playlist/Playlist video(p) | Channel(c) | Search video(s)\nchoice: ")


if mode == "v":
    link = input("\nEnter the link of the video: ")
elif mode == "p":
    link = input("\nEnter the link of the playlist: ")
elif mode == "c":
    link = input("\nEnter the link of the channel: ")
elif mode == "s":
    search = input("\nEnter the search: ")
    link = search_video(search)
else:
    print("\nInvalid mode")
    exit()

if mode == "v" or mode == "s":
    try:
        video_to_download = Video(
            link, on_complete_callback=on_complete, on_progress_callback=view_download_progress, use_oauth=False, allow_oauth_cache=True)
    except Exception:
        not_found("video")
elif mode == "p":
    try:
        playlist_to_download = Playlist(link)
    except Exception:
        not_found("playlist")
elif mode == "c":
    try:
        channel_to_download = Channel(link)
    except Exception:
        not_found("channel")

if mode == "v" or mode == "s":
    print(f"\nTitle: {video_to_download.title}")
    print(f"Thumbnail: {video_to_download.thumbnail_url}")
    print(f"Views: {video_to_download.views}")
    print(f"Duration: {round(video_to_download.length / 60,2)}")
elif mode == "p":
    print(f"\nPlaylist title: {playlist_to_download.title}")
    print(f"Playlist views: {playlist_to_download.views}")
    print(f"{len(playlist_to_download.videos)} videos on playlist to download")
elif mode == "c":
    print(
        f"\nChannel to download all videos: {channel_to_download.channel_name}")


to_download = input("\nOptions available:\nVideo(v) | Audio(a)\nchoice: ")


def choose_video_quality():
    quality = input(
        "\nChoose the quality of video:\nBest(b) | Worst(w)\nchoice: ")
    if quality == "b":
        print("\nDownloading...")
        if mode == "v" or mode == "s":
            try:
                video_to_download.streams.get_by_itag(22).download(
                    create_video_audio_path(video_to_download))
            except Exception:
                video_to_download.streams.get_highest_resolution().download(
                    create_video_audio_path(video_to_download))
        elif mode == "p":
            for video_in_playlist in playlist_to_download.videos:
                video_in_playlist.register_on_complete_callback(
                    playlist_video_on_complete)
                try:
                    video_in_playlist.streams.get_by_itag(22).download(
                        create_playlist_path(playlist_to_download))
                except Exception:
                    video_in_playlist.streams.get_highest_resolution().download(
                        create_playlist_path(playlist_to_download))
        elif mode == "c":
            for video_in_channel in channel_to_download.videos:
                try:
                    video_in_channel.streams.get_by_itag(22).download(
                        create_channel_path(channel_to_download))
                except Exception:
                    video_in_channel.streams.get_highest_resolution().download(
                        create_channel_path(channel_to_download))
    elif quality == "w":
        print("\nDownloading...")
        if mode == "v" or mode == "s":
            video_to_download.streams.get_lowest_resolution().download(
                create_video_audio_path(video_to_download))
        elif mode == "p":
            for video_in_playlist in playlist_to_download.videos:
                video_in_playlist.register_on_complete_callback(
                    playlist_video_on_complete)
                video_in_playlist.streams.get_lowest_resolution().download(
                    create_playlist_path(playlist_to_download))
        elif mode == "c":
            for video_in_channel in channel_to_download.videos:
                video_in_channel.streams.get_lowest_resolution().download(
                    create_channel_path(channel_to_download))
    else:
        print("Invalid choice")


def choose_audio_quality():
    quality = input(
        "\nChoose the quality of audio:\nBest(b) | Worst(w)\nchoice: ")
    if quality == "b":
        print("\nDownloading...")
        if mode == "v" or mode == "s":
            try:
                video_to_download.streams.get_by_itag(251).download(
                    create_video_audio_path(video_to_download))
            except Exception:
                video_to_download.streams.get_audio_only().download(
                    create_video_audio_path(video_to_download))
        elif mode == "p":
            for video_in_playlist in playlist_to_download.videos:
                video_in_playlist.register_on_complete_callback(
                    playlist_video_on_complete)
                try:
                    video_in_playlist.streams.get_by_itag(251).download(
                        create_playlist_path(playlist_to_download))
                except Exception:
                    video_in_playlist.streams.get_audio_only().download(
                        create_playlist_path(playlist_to_download))
        elif mode == "c":
            for video_in_channel in channel_to_download.videos:
                try:
                    video_in_channel.streams.get_by_itag(251).download(
                        create_channel_path(channel_to_download))
                except Exception:
                    video_in_channel.streams.get_audio_only().download(
                        create_channel_path(channel_to_download))
    elif quality == "w":
        print("\nDownloading...")
        if mode == "v" or mode == "s":
            try:
                video_to_download.streams.get_by_itag(249).download(
                    create_video_audio_path(video_to_download))
            except Exception:
                video_to_download.streams.get_by_itag(250).download(
                    create_video_audio_path(video_to_download))
        elif mode == "p":
            for video_in_playlist in playlist_to_download.videos:
                video_in_playlist.register_on_complete_callback(
                    playlist_video_on_complete)
                try:
                    video_in_playlist.streams.get_by_itag(249).download(
                        create_playlist_path(playlist_to_download))
                except Exception:
                    video_in_playlist.streams.get_by_itag(250).download(
                        create_playlist_path(playlist_to_download))
        elif mode == "c":
            for video_in_channel in channel_to_download.videos:
                try:
                    video_in_channel.streams.get_by_itag(249).download(
                        create_channel_path(channel_to_download))
                except Exception:
                    video_in_channel.streams.get_by_itag(250).download(
                        create_channel_path(channel_to_download))


def download():
    if to_download == "v":
        choose_video_quality()
    elif to_download == "a":
        choose_audio_quality()
    else:
        print("Invalid choice")


download()
print("\nAll done")
