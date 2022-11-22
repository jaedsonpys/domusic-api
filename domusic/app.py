from mathiz import Mathiz
from mathiz import request

from .domusic import DoMusic

app = Mathiz()
domusic = DoMusic()


@app.route('/video/info/<video_id>')
def get_video_info():
    video_id = request.parameters.get('video_id')
    url = f'https://www.youtube.com/watch?v={video_id}'
    video_info = domusic.get_video_info(url)

    return video_info


if __name__ == '__main__':
    app.run(host='0.0.0.0')
