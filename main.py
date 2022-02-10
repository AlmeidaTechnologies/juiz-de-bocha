import functions_framework
from recognizer import Recognizer

rec = Recognizer(
    config_file='models/mask_rcnn_X_101_32x8d_FPN_3x/mask_rcnn_X_101_32x8d_FPN_3x.yaml',
    weights_file='models/mask_rcnn_X_101_32x8d_FPN_3x/model_final_2d9806.pkl',
)


@functions_framework.http
def process_image(request):
    if 'img' not in request.files:
        raise Exception("Missing 'img' file")

    img = rec.read_file(request.files['img'])

    instances = rec.predict_json(img)
    instances = list(filter(lambda i: i['class'] == 'sports ball', instances))
    instances.sort(key=lambda i: i['area'])
    instances[0]['smallest'] = True

    return instances
