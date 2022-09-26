import os
import json
import importlib
import random
from copy import deepcopy
from tqdm import tqdm
import numpy as np
from recognizer import Recognizer
from pycocotools import mask as mask_tool
from skimage import measure


rec = Recognizer(
    config_file='cloud-run-function/models/model/config.yaml',
    # weights_file='models/model/weights.pkl',
    weights_file='models/mask_rcnn_juiz_de_bocha_custom/weights_first_train.pth',
    # confidence_threshold=0.9,
    confidence_threshold=0.7,
    gpu_id=0,
)

base_dir = './datasets/juizdebocha-raw/dataset'
data_dir = f'{base_dir}/data'

base_labels = {
    'info': {
        'description': "Juiz de Bocha",
        'version': "1.0",
        'year': 2022,
        'contributor': "Almeida Technologies",
        'date_created': "2022/09/23"
    },
    'licenses': [],
    'categories': [
        {
            'id': 1,
            'name': 'sports ball',
            'supercategory': 'sports',
        },
    ],
    'images': [],
    'annotations': [],
}

samples = list(enumerate(os.listdir(data_dir)))
random.seed(2)
random.shuffle(samples)
split = int(0.8 * len(samples))

annotation_id = 1
for split, samples in [('train', samples[:split]), ('val', samples[split:])]:
    print("Preparing", split)
    labels: dict = deepcopy(base_labels)
    for i, filename in tqdm(samples):
        filepath = os.path.join(data_dir, filename)
        im: np.ndarray = rec.read_file(filepath)
        # add image
        labels['images'].append(dict(
            id=i,
            file_name=filename,
            height=im.shape[0],
            width=im.shape[1],
        ))
        # add annotations
        instances = rec.predict_instances(im)
        masks = instances.get('pred_masks')
        for mask in masks:
            mask = np.array(mask, dtype=np.uint8)
            fortran_ground_truth_binary_mask = np.asfortranarray(mask)
            encoded_ground_truth = mask_tool.encode(fortran_ground_truth_binary_mask)
            ground_truth_area = mask_tool.area(encoded_ground_truth)
            ground_truth_bounding_box = mask_tool.toBbox(encoded_ground_truth)
            contours = measure.find_contours(mask, level=0.5)
            labels['annotations'].append(dict(
                image_id=i,
                category_id=1,
                id=annotation_id,
                area=ground_truth_area.tolist(),
                bbox=ground_truth_bounding_box.tolist(),
                iscrowd=0,
                segmentation=[
                    np.flip(contours[0], axis=1).ravel().tolist()
                    for contour in contours
                ],
            ))
            annotation_id += 1

    with open(f'{base_dir}/juiz_de_bocha_{split}.json', 'w') as labels_file:
        json.dump(labels, labels_file)
