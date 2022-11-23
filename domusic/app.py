import json
import base64

from mathiz import Mathiz
from mathiz import request

from .domusic import DoMusic
from .exceptions import InvalidVideoIDError

app = Mathiz()
domusic = DoMusic()


@app.route('/audio/info')
def get_audio_info():
    body = request.body

    if not body:
        return {'status': 'error', 'msg': 'no_body_content'}, 400
    else:
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return {'status': 'error', 'msg': 'invalid_json_data'}, 400

    url = data.get('url')
    query = data.get('query')

    if not url or not query:
        return {'status': 'error', 'msg': 'url_or_query_expected'}, 400
    
    try:
        if url:
            audio_info = domusic.get_video_info(url)
        elif query:
            audio_info = domusic.search_video(query)
    except InvalidVideoIDError:
        return {'status': 'error', 'msg': 'invalid_video_id'}, 400

    return audio_info


@app.route('/audio/download')
def download_audio():
    body = request.body

    if not body:
        return {'status': 'error', 'msg': 'no_body_content'}, 400
    else:
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return {'status': 'error', 'msg': 'invalid_json_data'}, 400

    url = data.get('url')

    if not url:
        return {'status': 'error', 'msg': 'url_expected'}, 400
    
    try:
        audio = domusic.download_audio(url)
    except InvalidVideoIDError:
        return {'status': 'error', 'msg': 'invalid_video_id'}, 400

    b64_audio = base64.b64encode(audio.getbuffer()).decode()
    return b64_audio, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
