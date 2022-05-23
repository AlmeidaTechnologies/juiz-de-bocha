
DIR=models/mask_rcnn_X_101_32x8d_FPN_3x

python detectron2-test/demo.py \
  --config-file $DIR/mask_rcnn_X_101_32x8d_FPN_3x.yaml \
  --input "datasets/Jogos de bocha/IMG-20220108-WA0044.jpg" \
  --opts MODEL.WEIGHTS $DIR/model_final_2d9806.pkl
#  --webcam \

