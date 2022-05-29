import os
import random
from flask import Flask, request, send_file
from PIL import Image
import numpy as np
from scipy import ndimage
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
    confidence_threshold=0.1,
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


def gaussian_kernel(l=5, sig=1.):
    """\
    creates gaussian kernel with side length `l` and a sigma of `sig`
    """
    ax = np.linspace(-(l - 1) / 2., (l - 1) / 2., l)
    gauss = np.exp(-0.5 * np.square(ax) / np.square(sig))
    kernel = np.outer(gauss, gauss)
    return kernel / np.sum(kernel)


def _process_image(img_bytes):
    img = rec.read_file(io.BytesIO(img_bytes))
    img_winner = img.copy()
    instances = rec.predict_data(img)
    instances = list(filter(lambda i: i['class'] == 'sports ball', instances))
    if len(instances) >= 2:
        instances.sort(key=lambda i: i['area'])
        smallest = instances[0]
        balls = instances[1:]
        for i in range(len(balls)):
            balls[i]['distance'] = _two_centers_distance(smallest['center'], balls[i]['center'])
        balls.sort(key=lambda b: b['distance'])
        # grid
        # if smallest:
        #     width = int(smallest['box']['x2'] - smallest['box']['x1']) +1
        #     height = int(smallest['box']['y2'] - smallest['box']['y1']) +1
        #     grid_color = np.array([80, 80, 80], dtype=np.uint8)
        #     for direction in [-1, 1]:
        #         x = int(smallest['box']['x1'])
        #         while 0 < x < img.shape[1]:
        #             img[:, x-1:x] = grid_color
        #             x += direction * width
        #         y = int(smallest['box']['y1'])
        #         while 0 < y < img.shape[0]:
        #             img[y-1:y, :] = grid_color
        #             y += direction * height
        #         # y = int(smallest['box']['y1'])
        #     # i, j = 0, 0
        # smaller
        if smallest:
            img[smallest.get('mask')] = np.array([255, 255, 255], dtype=np.uint8)
        # balls border
        for i in reversed(range(len(balls))):
            colors = img[balls[i].get('mask')]
            avg_color = colors.mean(axis=0)
            img[balls[i].get('mask')] = np.array(avg_color, dtype=np.uint8)
        # winner
        winner = balls[0]
        img_winner = img.copy()
        if winner:
            img[winner.get('mask')] = np.array([50, 230, 50], dtype=np.uint8)
            # border = winner.get('mask')
            # dilated = ndimage.binary_dilation(border, gaussian_kernel(10))
            # eroded = ndimage.binary_erosion(border, gaussian_kernel(5))
            # border = dilated ^ eroded
            # border = ndimage.binary_dilation(border, gaussian_kernel(5, 0.5))
            # img[border] = np.array([100, 220, 100], dtype=np.uint8)
    return img, img_winner


__counter = random.randint(1, 10000)


def _create_filename():
    global __counter
    __counter += 1
    return f"{datetime.now().timestamp()}.{__counter}"


def _to_gif_bytes(images):
    gif_bytes = io.BytesIO()
    # fade in
    base, winner = images
    frames = []
    p = 0.0
    for step in [0.1, -0.1]:
        for i in range(10):
            frame = np.array(base * (1-p) + winner * p, dtype=np.uint8)
            frame = Image.fromarray(frame)
            frames.append(frame)
            p += step
    frames[0].save(
        gif_bytes,
        format='gif',
        append_images=frames[1:],
        save_all=True,
        duration=50,
        optimize=True,
        loop=0,
    )
    return gif_bytes.getvalue()


def _to_bytes(im, format='jpeg'):
    img = Image.fromarray(im)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format)
    return img_bytes.getvalue()


def _upload_image(filepath, img_bytes, bucket, metadata, with_public_url=False):
    file = bucket.blob(filepath)
    token = None
    if with_public_url:
        token = uuid4()
        file.metadata = {
            'firebaseStorageDownloadTokens': token,
            **metadata,
        }
    if not isinstance(img_bytes, io.BytesIO):
        img_bytes = io.BytesIO(img_bytes)
    file.upload_from_file(img_bytes, content_type='image/jpeg')
    if with_public_url:
        return f"https://firebasestorage.googleapis.com/v0/b/{__project}" \
               f"/o/{filepath}" \
               f"?alt=media" \
               f"&token={token}"


@app.route('/image', methods=['POST'])
def process_image_return_image():
    img_bytes = request.stream.read()
    filename = _create_filename()
    _upload_image(
        filename + '.jpg',
        img_bytes,
        __raw_bucket,
        metadata=request.args,
    )
    result = _process_image(img_bytes)
    result_bytes = _to_gif_bytes(result)

    return send_file(
        io.BytesIO(result_bytes),
        download_name='response.gif',
        mimetype='image/gif',
        as_attachment=True,
    )


@app.route('/url', methods=['POST'])
def process_image_return_url():
    img_bytes = request.stream.read()
    filename = _create_filename()
    _upload_image(
        filename + '.jpg',
        img_bytes,
        __raw_bucket,
        metadata=request.args,
    )
    img = _process_image(img_bytes)
    url = _upload_image(
        filename + '.gif',
        _to_gif_bytes(img),
        __generated_bucket,
        metadata=request.args,
        with_public_url=True
    )

    return url


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
