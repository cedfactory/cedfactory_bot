import telegram.ext
import urllib
from urllib.request import urlopen
import json
import os
from dotenv import load_dotenv
import pandas as pd


def list(update, context):
    market = update.message.text.split(" ")[1]
    fdp_url = os.getenv('FPD_URL')
    url = fdp_url+"/list?markets="+market

    request = urllib.request.Request(url)
    request.add_header('User-Agent',"cheese")
    data = urllib.request.urlopen(request).read()
    data_json = json.loads(data)
    if data_json['status'] != "ok" or data_json['result'][market]['status'] != "ok":
        update.message.reply_text("no data received")
        return

    dataframe_market = data_json["result"][market]['dataframe']
    df = pd.read_json(dataframe_market)
    print(df["name"].tolist())
    update.message.reply_text(df["name"].tolist())

def echo(update, context):
    response = update.message.text.split(' ', 1)[1]
    update.message.reply_text(response)


load_dotenv()
token = os.getenv('TELEGRAM_TOKEN')
if token == "":
    token=os.environ["TELEGRAM_TOKEN"]

bot = telegram.Bot(token)
updater = telegram.ext.Updater(token)
disp = updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler("list", list))
disp.add_handler(telegram.ext.CommandHandler("echo", echo))

def webhook(request):
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        #chat_id = update.message.chat.id
        # Reply with the same message
        #bot.sendMessage(chat_id=chat_id, text=update.message.text)
        disp.process_update(update)
    return "ok"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    updater.start_polling()
    updater.idle()
