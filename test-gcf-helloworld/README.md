
###### deploy:
```bash
BUCKET="gs://juizdebocha"
gcloud functions deploy test_process_image \
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
  test_process_image
```
