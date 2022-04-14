import os
import random

from flask import Flask, request, send_file, jsonify
from PIL import Image
import numpy as np
import math
import io
from datetime import datetime
from google.cloud import storage
from recognizer import Recognizer
from uuid import uuid4

app = Flask(__name__)
rec = Recognizer(
    config_file='models/model/config.yaml',
    weights_file='models/model/weights.pkl',
)
__project = 'juizdebocha'
__storage_client = storage.Client(project=__project)
__raw_bucket: storage.Bucket = __storage_client.bucket('juizdebocha-raw')
__generated_bucket: storage.Bucket = __storage_client.bucket('juizdebocha')


def _two_centers_distance(ca, cb):
    return math.sqrt(
        math.pow(cb['x'] - ca['x'], 2) +
        math.pow(cb['y'] - ca['y'], 2)
    )


def _process_image(img_bytes):
    img = rec.read_file(img_bytes)
    instances = rec.predict_data(img)
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
            img[ball['mask']] = np.array(color, dtype=np.uint8)
    return _to_bytes(img)


__counter = random.randint(1, 10000)


def _create_filepath():
    global __counter
    __counter += 1
    return f"{datetime.now().timestamp()}.{__counter}.jpg"


def _to_bytes(im):
    img = Image.fromarray(im)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='jpeg')
    return io.BytesIO(img_bytes.getvalue())


def _upload_image(filepath, img_bytes, bucket, with_public_url=False):
    file = bucket.blob(filepath)
    token = None
    if with_public_url:
        token = uuid4()
        file.metadata = {
            'firebaseStorageDownloadTokens': token
        }
    file.upload_from_file(img_bytes, content_type='image/jpeg')
    if with_public_url:
        return f"https://firebasestorage.googleapis.com/v0/b/{__project}" \
               f"/o/{filepath}" \
               f"?alt=media" \
               f"&token={token}"


@app.route('/image', methods=['POST', 'GET'])
def process_image_return_image():

    img_bytes = request.stream.read()
    filepath = _create_filepath()
    _upload_image(filepath, img_bytes, __raw_bucket)
    img_bytes = _process_image(img_bytes)

    return send_file(
        img_bytes,
        download_name='response.jpeg',
        mimetype='image/jpeg',
        as_attachment=True,
    )


@app.route('/url', methods=['POST', 'GET'])
def process_image_return_url():

    img_bytes = request.stream.read()
    filepath = _create_filepath()
    _upload_image(filepath, img_bytes, __raw_bucket)
    img_bytes = _process_image(img_bytes)
    url = _upload_image(filepath, img_bytes, __generated_bucket, with_public_url=True)

    return url


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
