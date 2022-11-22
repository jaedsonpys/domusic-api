import io

import pytube


class DoMusic:
    def get_best_audio_quality(self, all_videos: pytube.StreamQuery) -> pytube.Stream:
        max_filesize = 0
        best_video = None

        for video in all_videos:
            if video.filesize > max_filesize:
                max_filesize = video.filesize
                best_video = video

        return best_video

    def get_video_info(self, url: str) -> dict:
        yt = pytube.YouTube(url)
        all_videos = yt.streams.filter(file_extension='mp4', only_audio=True)

        best_audio = self.get_best_audio_quality(all_videos)

        author = yt.author
        views = yt.views
        thumbnail_url = yt.thumbnail_url

        video_info = {
            'author': author,
            'views': views,
            'thumbnail_url': thumbnail_url,
            'title': best_audio.title,
            'size': best_audio.filesize,
            'url': yt.watch_url
        }

        return video_info

    def download_audio(self, url: str) -> io.BytesIO:
        yt = pytube.YouTube(url)
        buffer = io.BytesIO()

        all_videos = yt.streams.filter(file_extension='mp4', only_audio=True)
        best_audio = self.get_best_audio_quality(all_videos)
        best_audio.stream_to_buffer(buffer)
        return buffer
