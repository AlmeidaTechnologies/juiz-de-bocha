from google.cloud.functions.context import Context
from google.cloud import storage
from PIL import Image
import numpy as np
import io


__project = 'juizdebocha'
__bucket = "juizdebocha.appspot.com"


def process_game_image(event: dict, context: Context):

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
    img = Image.open(io.BytesIO(img_bytes))
    img = img.convert('RGB')
    im = np.array(img)
    im = 255-im
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
    }, None)
