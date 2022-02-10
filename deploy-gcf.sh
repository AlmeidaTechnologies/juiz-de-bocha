gcloud functions deploy process_image \
  --project juiz-de-bocha-teste-gcf \
  --stage-bucket imgs-juiz-de-bocha \
  --region southamerica-east1 \
  --memory 8192MB \
  --trigger-http \
  --allow-unauthenticated \
  --runtime python38 \
  --max-instances=5 \
  --verbosity debug
