from mathiz import Mathiz
from mathiz import request

from .domusic import DoMusic
from .exceptions import InvalidVideoIDError

app = Mathiz()
domusic = DoMusic()


@app.route('/video/info/<video_id>')
def get_video_info():
    video_id = request.parameters.get('video_id')
    url = f'https://www.youtube.com/watch?v={video_id}'
    
    try:
        video_info = domusic.get_video_info(url)
    except InvalidVideoIDError:
        return {'status': 'error', 'error': 'invalid_video_id'}, 400

    return video_info


if __name__ == '__main__':
    app.run(host='0.0.0.0')
