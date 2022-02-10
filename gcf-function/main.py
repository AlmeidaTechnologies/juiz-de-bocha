from google.cloud import storage
from PIL import Image
import numpy as np
import math
import io
from recognizer import Recognizer

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


def process_game_image(event: dict, context=None):

    filepath: str = event['name']

    extension = filepath.split('.')[-1].lower()
    if extension not in ['png', 'jpg', 'jpeg']:
        return

    filename = filepath.split('.')[-2]
    if filename.lower().endswith('generated'):
        return

    print("Reading uploaded image", filepath)
    client = storage.Client(project=__project)
    bucket: storage.Bucket = client.bucket(__bucket)
    blob: storage.Blob = bucket.get_blob(filepath)
    img_bytes: bytes = blob.download_as_bytes()

    print("Processing image")
    im = rec.read_file(io.BytesIO(img_bytes))
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
            print(color)
            im[ball['mask']] = np.array(color, dtype=np.uint8)
    img = Image.fromarray(im)

    new_filepath = filename + '-generated.jpg'
    print("Uploading new image", new_filepath)
    bytes_io: io.BytesIO = io.BytesIO()
    img.save(bytes_io, format='jpeg')
    blob = bucket.blob(new_filepath)
    blob.upload_from_string(bytes_io.getvalue(), content_type='image/jpeg')


if __name__ == '__main__':
    process_game_image({
        'name': "Screenshot from 2022-01-10 13-47-12.png",
    })
