from detectron2.data import DatasetMapper, transforms, build_detection_train_loader
from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2.evaluation import DatasetEvaluators, COCOEvaluator
import os

from train_custom_dataset import register_datasets

register_datasets.juiz_de_bocha_custom()

model_dir = 'models/mask_rcnn_juiz_de_bocha_custom'

cfg = get_cfg()
cfg.merge_from_file(f'{model_dir}/mask_rcnn_juiz_de_bocha.yaml')

# cfg.DATASETS.TRAIN = ("coco_2017_train",)
# cfg.DATASETS.TEST = ("coco_2017_val",)

cfg.MODEL.WEIGHTS = f'{model_dir}/weights_first_train.pth'  # initialize from previous training

cfg.DATALOADER.NUM_WORKERS = 8
cfg.SOLVER.IMS_PER_BATCH = 3
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
cfg.SOLVER.BASE_LR = 0.0025
# cfg.SOLVER.MAX_ITER = 2000  # 614 * 10
# cfg.SOLVER.STEPS = ()
cfg.SOLVER.MAX_ITER = 5000
cfg.SOLVER.STEPS = (614,)

cfg.OUTPUT_DIR = './train_custom_dataset/training/'
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)


class Trainer(DefaultTrainer):
    @classmethod
    def build_train_loader(cls, cfg):
        return build_detection_train_loader(
            cfg,
            mapper=DatasetMapper(
                cfg,
                is_train=True,
                augmentations=[
                    transforms.RandomBrightness(0.5, 1.5),
                    transforms.RandomFlip(prob=0.5),
                    transforms.RandomCrop("absolute_range", (640, 640)),
                    transforms.RandomRotation(angle=[-90, 90], expand=True,),
                    transforms.RandomContrast(intensity_min=0.2, intensity_max=1.8),
                    transforms.RandomLighting(scale=1.0),
                    transforms.RandomSaturation(intensity_min=0.2, intensity_max=1.8),
                ],
            ),
        )

    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        return DatasetEvaluators([
            COCOEvaluator(dataset_name, output_dir=output_folder)
        ])


trainer = Trainer(cfg)
trainer.resume_or_load(resume=False)
trainer.train()
