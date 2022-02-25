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

def start(update, context):
    update.message.reply_text("Hello! Starting the bot! trend / list / pred")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    load_dotenv()
    
    token = os.getenv('TELEGRAM_TOKEN')
    print(token)
    updater = telegram.ext.Updater(token, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(telegram.ext.CommandHandler("start",start))
    disp.add_handler(telegram.ext.CommandHandler("list", list))

    updater.start_polling()
    updater.idle()
