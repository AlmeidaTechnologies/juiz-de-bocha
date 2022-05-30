# from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import register_coco_instances

classes = ["sports ball"]


def juiz_de_bocha():
    register_coco_instances(
        name="juiz_de_bocha_train",
        metadata=dict(thing_classes=classes),
        json_file='datasets/coco/annotations/juiz_de_bocha_train.json',
        image_root='datasets/coco/train2017',
    )

    register_coco_instances(
        name="juiz_de_bocha_val",
        metadata=dict(thing_classes=classes),
        json_file='datasets/coco/annotations/juiz_de_bocha_val.json',
        image_root='datasets/coco/val2017',
    )
    # DatasetCatalog.register("juiz_de_bocha_train", juiz_de_bocha)
    # MetadataCatalog.get("juiz_de_bocha_train").thing_classes = classes
