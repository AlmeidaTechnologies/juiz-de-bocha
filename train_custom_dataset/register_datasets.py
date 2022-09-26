# from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import register_coco_instances

dataset_dir = 'datasets/juizdebocha-raw/dataset'
classes = ["sports ball"]


def juiz_de_bocha_custom():
    register_coco_instances(
        name="juiz_de_bocha_train",
        metadata=dict(thing_classes=classes),
        json_file=f'{dataset_dir}/juiz_de_bocha_train.json',
        image_root=f'{dataset_dir}/data',
    )

    register_coco_instances(
        name="juiz_de_bocha_val",
        metadata=dict(thing_classes=classes),
        json_file=f'{dataset_dir}/juiz_de_bocha_val.json',
        image_root=f'{dataset_dir}/data',
    )
    # DatasetCatalog.register("juiz_de_bocha_train", juiz_de_bocha)
    # MetadataCatalog.get("juiz_de_bocha_train").thing_classes = classes
