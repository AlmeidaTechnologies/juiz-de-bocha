# from detectron2.structures import BoxMode
import json

_folder = 'datasets/coco/annotations'


def generate_data(phase):
    with open(f'{_folder}/instances_{phase}2017.json') as file:
        coco = json.load(file)
    coco_images = coco['images']
    coco_annotations = coco['annotations']
    coco_categories = coco['categories']
    ball_id = None
    categories = None
    for cat in coco_categories:
        if cat['name'] == "sports ball":
            ball_id = cat['id']
            cat['id'] = 1
            categories = [cat]
            break
    print("categories:", categories)
    assert ball_id is not None
    images_annotation_count = {
        image['id']: 0
        for image in coco_images
    }
    # coco_images = {
    #     image['id']: {
    #         **image,
    #         'file_name': f"datasets/coco/{phase}2017/{image['file_name']}",
    #         'annotations': [],
    #     }
    #     for image in coco_images
    # }
    annotations = []
    for annotation in coco_annotations:
        if annotation['category_id'] == ball_id:
            annotation['category_id'] = 1
            annotations.append(annotation)
            images_annotation_count[annotation['image_id']] += 1
            # annotation['bbox_mode'] = BoxMode.XYWHA_ABS
            # coco_images[annotation['image_id']]['annotations'].append(annotation)
    if phase != 'train':  # remove images without balls
        i = 0
        while i < len(coco_images):
            count = images_annotation_count[coco_images[i]['id']]
            if count == 0:
                del coco_images[i]
            else:
                i += 1
    # samples = coco_images.values()
    return dict(
        images=coco_images,
        annotations=annotations,
        categories=categories,
    )

    ## non-coco json format:
    # return [
    #     dict(
    #         file_name="",
    #         # height=200,
    #         # width=100,
    #         # image_id=0,
    #         annotations=[
    #             dict(
    #                 bbox=[0.0, 0.0, 0.0, 0.0],
    #                 bbox_mode=BoxMode.XYXY_ABS,
    #                 category_id=0,
    #                 segmentation=[
    #                     [0.],
    #                 ]
    #             ),
    #         ],
    #         sem_seg_file_name="",
    #
    #     )
    # ]


if __name__ == '__main__':
    for phase in ['train', 'val']:
        data = generate_data(phase)
        with open(f'{_folder}/juiz_de_bocha_{phase}.json', 'w') as f:
            json.dump(data, f)
