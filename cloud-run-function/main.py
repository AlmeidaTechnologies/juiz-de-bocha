import os
from flask import Flask, request, send_file, jsonify
from PIL import Image
import numpy as np
import math
import io
# from datetime import datetime
# from google.cloud import storage
from recognizer import Recognizer
# from uuid import uuid4

app = Flask(__name__)

rec = Recognizer(
    config_file='models/model/config.yaml',
    weights_file='models/model/weights.pkl',
)

__project = 'juizdebocha'


def _two_centers_distance(ca, cb):
    return math.sqrt(
        math.pow(cb['x'] - ca['x'], 2) +
        math.pow(cb['y'] - ca['y'], 2)
    )


def _to_bytes(im):
    img = Image.fromarray(im)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='jpeg')
    return io.BytesIO(img_bytes.getvalue())


@app.route("/", methods=['POST', 'GET'])
def process_game_image():
    img = rec.read_file(request.stream)

    """ create buckets """
    # client = storage.Client(project=__project)
    # raw_bucket: storage.Bucket = client.bucket('juizdebocha-raw')
    # generated_bucket: storage.Bucket = client.bucket('juizdebocha')

    """ store raw image """
    # img_path = f"{datetime.now().timestamp()}.jpg"
    # raw_img = raw_bucket.blob(img_path)
    # raw_img.upload_from_file(_to_bytes(img), content_type='image/jpeg')

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

    """ send to storage """
    # generated_img = generated_bucket.blob(img_path)
    # token = uuid4()
    # generated_img.metadata = {
    #     'firebaseStorageDownloadTokens': token
    # }
    # generated_img.upload_from_file(_to_bytes(img), content_type='image/jpeg')
    # return f"https://firebasestorage.googleapis.com/v0/b/{__project}" \
    #        f"/o/{img_path}" \
    #        f"?alt=media" \
    #        f"&token={token}"

    """ return processed image """
    return send_file(
        _to_bytes(img),
        download_name='response.jpeg',
        mimetype='image/jpeg',
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
