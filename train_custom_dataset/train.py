from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2.evaluation import DatasetEvaluators, COCOEvaluator
import os
from . import register_datasets

register_datasets.juiz_de_bocha_custom()

model_dir = 'models/mask_rcnn_juiz_de_bocha_custom'

cfg = get_cfg()
cfg.merge_from_file(f'{model_dir}/mask_rcnn_juiz_de_bocha.yaml')

# cfg.DATASETS.TRAIN = ("coco_2017_train",)
# cfg.DATASETS.TEST = ("coco_2017_val",)

cfg.DATALOADER.NUM_WORKERS = 8
cfg.MODEL.WEIGHTS = f'{model_dir}/weights_first_train.pth'  # initialize from previous training
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.005
cfg.SOLVER.MAX_ITER = (
    200
)  # 300 iterations seems good enough, but you can certainly train longer
cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = (
    128
)  # faster, and good enough for this toy dataset
# cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3  # 3 classes (data, fig, hazelnut)

cfg.OUTPUT_DIR = './train_custom_dataset/training/'
os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)


class Trainer(DefaultTrainer):
    @classmethod
    def build_evaluator(cls, cfg, dataset_name, output_folder=None):
        return DatasetEvaluators([
            COCOEvaluator(dataset_name, output_dir=output_folder)
        ])


# trainer = DefaultTrainer(cfg)
trainer = Trainer(cfg)
trainer.resume_or_load(resume=True)
trainer.train()
