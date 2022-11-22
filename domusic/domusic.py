import pytube


class DoMusic:
    def get_video_info(self, url: str) -> dict:
        yt = pytube.YouTube(url)
        all_videos = yt.streams.filter(file_extension='mp4', only_audio=True)

        max_filesize = 0
        best_video: pytube.Stream = None

        for video in all_videos:
            if video.filesize > max_filesize:
                max_filesize = video.filesize
                best_video = video

        author = yt.author
        views = yt.views
        thumbnail_url = yt.thumbnail_url

        video_info = {
            'author': author,
            'views': views,
            'thumbnail_url': thumbnail_url,
            'title': best_video.title,
            'size': best_video.filesize
        }

        return video_info
