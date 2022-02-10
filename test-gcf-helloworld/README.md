
###### deploy:
```bash
BUCKET="gs://juizdebocha.appspot.com"
gcloud functions deploy process_game_image \
  --verbosity debug \
  --project juizdebocha \
  --region southamerica-east1 \
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
