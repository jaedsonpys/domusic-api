import io

import pytube
import requests
import youtubesearchpython as ytsearch
from mutagen import mp4

from .exceptions import InvalidVideoIDError


class DoMusic:
    def _get_best_audio_quality(self, all_videos: pytube.StreamQuery) -> pytube.Stream:
        max_filesize = 0
        best_video = None

        for video in all_videos:
            if video.filesize > max_filesize:
                max_filesize = video.filesize
                best_video = video

        return best_video

    def get_video_info(self, url: str) -> dict:
        try:
            yt = pytube.YouTube(url)
        except pytube.exceptions.RegexMatchError:
            raise InvalidVideoIDError('Invalid video ID')

        all_videos = yt.streams.filter(file_extension='mp4', only_audio=True)

        best_audio = self._get_best_audio_quality(all_videos)

        author = yt.author
        views = yt.views
        thumbnail_url = yt.thumbnail_url

        video_info = {
            'author': author,
            'views': views,
            'thumbnail_url': thumbnail_url,
            'title': best_audio.title,
            'minutes': yt.length,
            'url': yt.watch_url
        }

        return video_info

    def search_video(self, query: str) -> dict:
        search = ytsearch.VideosSearch(query)
        result = search.result()
        all_videos = []

        for video in result['result']:
            all_videos.append({
                'author': video['channel']['name'],
                'views': video['viewCount']['short'],
                'thumbnail_url': video['thumbnails'][0]['url'],
                'title': video['title'],
                'minutes': video['duration'],
                'url': video['link']
            })

        return all_videos

    def get_video_thumbnail(self, thumbnail_url: str) -> bytes:
        req = requests.get(thumbnail_url)
        return req.content

    def download_audio(self, url: str) -> io.BytesIO:
        try:
            yt = pytube.YouTube(url)
        except pytube.exceptions.RegexMatchError:
            raise InvalidVideoIDError('Invalid video ID')

        buffer = io.BytesIO()

        all_videos = yt.streams.filter(file_extension='mp4', only_audio=True)
        best_audio = self._get_best_audio_quality(all_videos)
        thumbnail = self.get_video_thumbnail(yt.thumbnail_url)
        best_audio.stream_to_buffer(buffer)

        audio_file = mp4.MP4(fileobj=buffer)
        audio_file.add_tags()

        audio_file['\xa9ART'] = yt.author
        audio_file['\xa9nam'] = yt.title
        audio_file["covr"] = [
            mp4.MP4Cover(thumbnail, imageformat=mp4.MP4Cover.FORMAT_JPEG)
        ]

        audio_file.save(buffer)
        return buffer
