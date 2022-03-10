import os
from flask import Flask, request, send_file
from PIL import Image
import numpy as np
import math
import io
from datetime import datetime
from google.cloud import storage
from recognizer import Recognizer

app = Flask(__name__)

rec = Recognizer(
    config_file='models/model/config.yaml',
    weights_file='models/model/weights.pkl',
)

__project = 'juizdebocha'
__bucket = "juizdebocha.appspot.com"


def _two_centers_distance(ca, cb):
    return math.sqrt(
        math.pow(cb['x'] - ca['x'], 2) +
        math.pow(cb['y'] - ca['y'], 2)
    )


def _to_bytes(im):
    img = Image.fromarray(im)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='jpeg')
    return img_bytes.getvalue()


@app.route("/", methods=['POST', 'GET'])
def process_game_image():
    im = rec.read_file(request.stream)

    client = storage.Client(project=__project)
    bucket: storage.Bucket = client.bucket(__bucket)

    blob = bucket.blob(f"{datetime.now().timestamp()}.jpg")
    blob.upload_from_string(_to_bytes(im), content_type='image/jpeg')

    instances = rec.predict_data(im)
    instances = list(filter(lambda i: i['class'] == 'sports ball', instances))
    if len(instances) >= 2:
        instances.sort(key=lambda i: i['area'])
        smallest = instances[0]
        balls = instances[1:]
        for i in range(len(balls)):
            balls[i]['distance'] = _two_centers_distance(smallest['center'], balls[i]['center'])
        balls.sort(key=lambda b: b['distance'])
        for i, ball in enumerate([smallest, *balls]):
            if i == 0:
                color = [255, 255, 255]
            elif i == 1:
                color = [100, 200, 100]
            else:
                color = [200, 100, 100]
            im[ball['mask']] = np.array(color, dtype=np.uint8)

    return send_file(
        io.BytesIO(_to_bytes(im)),
        download_name='response.jpeg',
        mimetype='image/jpeg',
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
