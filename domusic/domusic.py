import pytube


class DoMusic:
    def get_video_info(self, url: str) -> dict:
        yt = pytube.YouTube(url)
        all_videos = yt.streams.filter(file_extension='mp4', only_audio=True)

        max_filesize = 0
        best_video_audio: pytube.Stream = None

        for video in all_videos:
            if video.filesize > max_filesize:
                max_filesize = video.filesize
                best_video_audio = video

        video_info = {
            'title': best_video_audio.title,
            'size': best_video_audio.filesize
        }

        return video_info
