###### link files
```bash
ln -s ../recognizer.py .
mkdir model
cp '../models/mask_rcnn_X_101_32x8d_FPN_3x/mask_rcnn_X_101_32x8d_FPN_3x.yaml' model/config.yaml
cp '../models/mask_rcnn_X_101_32x8d_FPN_3x/model_final_2d9806.pkl' model/weights.pkl
cp ../recognizer.py recognizer.py
```


###### install locally
```bash
virtualenv -p python3 venv
source venv/bin/activate

pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cpu/torch1.10/index.html
pip install torch==1.10.2+cpu torchvision==0.11.3+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
pip install -r requirements.txt
```

###### start
```bash
python main.py
```

## Deploy;
```bash
gcloud run deploy recognizer \
  --region southamerica-east1 \
  --project juizdebocha \
  --source .

gcloud run deploy recognizer \
  --region southamerica-east1 \
  --project juizdebocha \
  --image southamerica-east1-docker.pkg.dev/juizdebocha/cloud-run-source-deploy/recognizer:latest
````

###### read logs:
```bash
gcloud functions logs read --limit 50 --project juizdebocha
gcloud functions logs read --limit 30 \
  --project juizdebocha \
  --region southamerica-east1 \
  process_game_image
```

