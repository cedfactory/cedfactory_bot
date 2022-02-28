
# Telegram bot

### Deploy

```sh
gcloud functions deploy <function> --set-env-vars "TELEGRAM_TOKEN=<TELEGRAM_TOKEN>" --runtime python38 --trigger-http --project=<project_name>
```


then

```sh
curl "https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook?url=https://europe-west1-<PROJECT-NAME>.cloudfunctions.net/webhook"
```
