from mathiz import Mathiz
from mathiz import request

from .domusic import DoMusic

app = Mathiz()
domusic = DoMusic()


@app.route('/video/info/<url>')
def get_video_info():
    url = request.parameters.get('url')
    domusic.get_video_info(url)
    return domusic


if __name__ == '__main__':
    app.run(host='0.0.0.0')
