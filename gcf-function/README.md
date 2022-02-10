###### link files
```bash
ln -s ../recognizer.py .
mkdir model
cp '../models/mask_rcnn_X_101_32x8d_FPN_3x/mask_rcnn_X_101_32x8d_FPN_3x.yaml' model/config.yaml
cp '../models/mask_rcnn_X_101_32x8d_FPN_3x/model_final_2d9806.pkl' model/weights.pkl
```


###### deploy:
```bash
virtualenv -p python3 venv
source venv/bin/activate

python -m pip install detectron2 \
  -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html \
  --target detectron2
mv venv/lib/python3.8/site-packages/detectron2 ./detectron2



pip3 install \
  torch==1.10.2+cpu torchvision==0.11.3+cpu \
  -f https://download.pytorch.org/whl/cpu/torch_stable.html
mv venv/lib/python3.8/site-packages/torch ./torch
mv venv/lib/python3.8/site-packages/torchvision ./torchvision


BUCKET="gs://juizdebocha.appspot.com"
gcloud functions deploy process_game_image \
  --verbosity debug \
  --project juizdebocha \
  --region southamerica-east1 \
  --stage-bucket gs://juizdebocha-recognizer \
  --runtime python39 \
  --trigger-resource $BUCKET \
  --trigger-event google.storage.object.finalize
```

###### read logs:
```bash
gcloud functions logs read --limit 50 --project juizdebocha
gcloud functions logs read --limit 30 \
  --project juizdebocha \
  --region southamerica-east1 \
  process_game_image
```
