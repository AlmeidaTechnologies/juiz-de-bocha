import io

import cv2
import numpy as np
import torch
from PIL import Image
import exifread
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.structures import Instances, Boxes
from detectron2.utils.visualizer import Visualizer
from detectron2.engine.defaults import DefaultPredictor


class Recognizer:
    def __init__(
            self,
            config_file: str,
            weights_file: str,
            confidence_threshold: float = 0.5,
            gpu_id=None,
    ):
        cfg = get_cfg()
        cfg.merge_from_file(config_file)
        cfg.MODEL.WEIGHTS = weights_file
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = confidence_threshold
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = confidence_threshold
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = confidence_threshold
        cfg.MODEL.DEVICE = 'cpu' if gpu_id is None else f'cuda:{gpu_id}'
        self.__predictor = DefaultPredictor(cfg)
        self.__cpu_device = torch.device("cpu")
        self._metadata = MetadataCatalog.get(
            cfg.DATASETS.TEST[0] if len(cfg.DATASETS.TEST) else "__unused"
        )
        self._class_names = self._metadata.get("thing_classes") or ['sports ball']

    @staticmethod
    def __read_img_and_correct_exif_orientation(file) -> Image:
        """
        Copiado de https://pypi.org/project/ExifRead/
        :param file
        :return: Image
        """
        im = Image.open(file)
        if isinstance(file, io.BytesIO):
            tags = exifread.process_file(file, details=False)
        else:
            with open(file, 'rb') as f:
                tags = exifread.process_file(f, details=False)
        if "Image Orientation" in tags.keys():
            orientation = tags["Image Orientation"]
            val = orientation.values
            if 2 in val:
                val += [4, 3]
            if 5 in val:
                val += [4, 6]
            if 7 in val:
                val += [4, 8]
            if 3 in val:
                im = im.transpose(Image.ROTATE_180)
            if 4 in val:
                im = im.transpose(Image.FLIP_TOP_BOTTOM)
            if 6 in val:
                im = im.transpose(Image.ROTATE_270)
            if 8 in val:
                im = im.transpose(Image.ROTATE_90)
        return im

    @staticmethod
    def read_file(file):
        im = Recognizer.__read_img_and_correct_exif_orientation(file)
        im = im.convert('RGB')
        im = np.array(im)
        return im

    def predict_data(self, img: np.ndarray):
        prediction: Instances = self.predict_instances(img)
        pred_boxes: Boxes = prediction.get('pred_boxes')
        centers = pred_boxes.get_centers().numpy()
        boxes = pred_boxes.tensor.numpy()
        scores = prediction.get('scores')
        classes = prediction.get('pred_classes')
        masks = prediction.get('pred_masks')
        instances = []
        for i in range(len(prediction)):
            mask = masks[i].numpy()
            area = mask.sum()
            instances.append({
                'center': {
                    'x': centers[i][0],
                    'y': centers[i][1],
                },
                'box': {
                    'x1': boxes[i][0],
                    'y1': boxes[i][1],
                    'x2': boxes[i][2],
                    'y2': boxes[i][3],
                },
                'mask': mask,
                'class': self._class_names[classes[i].item()],
                'score': scores[i].item(),
                'area': area,
            })
        return instances

    def predict_instances(self, img: np.ndarray):
        """
        Process an image and returns object instances
        :rtype: Instances
            predicted instances
        :param img: (np.ndarray)
            RGB image with shape (H, W, C)
        """
        # RGB to BGR
        img = img[:, :, ::-1]
        instances: Instances = self.__predictor(img)["instances"].to(self.__cpu_device)
        return instances

    def predict_img(self, img):
        instances = self.predict_instances(img)
        visualizer = Visualizer(img)
        vis_output = visualizer.draw_instance_predictions(predictions=instances)
        return instances, vis_output

    def test(self, img):
        """
        Process an image and show window
        :param img: numpy BGR image
        """
        instances, visualized_output = self.predict_img(img)
        print(f"detected {len(instances)} instances")
        cv2.namedWindow("prediction", cv2.WINDOW_NORMAL)
        cv2.imshow("prediction", visualized_output.get_image()[:, :, ::-1])
        while cv2.waitKey(0) != 27: # esc to quit
            pass
