"""Routes for the stocks graph page."""

from flask import Blueprint, request, render_template
import telebot
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import os 

sched = BlockingScheduler()
bot = telebot.TeleBot("5619495208:AAEcLoGTvqc4tgaJC2rKplnavHqUgg6Js0I")


notifications = Blueprint('notifications', __name__, url_prefix='/notifications')

@notifications.route('/', methods=['GET'])
def render():
    default = 'TSLA'
    if request.args.get('stock') == None:
        stock=default
    else:
        args = request.args
        stock = args.get('stock')

    return render_template('notifications.html')

# ticker = 'TSLA'


def getStockData(stock):
    base_url = "https://financialmodelingprep.com/api/v3/quote/"
    key = os.environ.get('NOTIFICATION_KEY')
    full_url = base_url + stock + "?apikey=" + key
    r = requests.get(full_url)
    stock_data = r.json()
    return stock_data


def generateMessage(data):
    symbol = data[0]['symbol']
    price = data[0]["price"]
    changesPercent = data[0]["changesPercentage"]
    timestamp = data[0]['timestamp']

    current = datetime.fromtimestamp(timestamp)
    message = str(current)
    message += "\n Symbol: " + symbol
    message += "\n Current price: $" + str(price)
    message += "\n Price percentage change: " + str(changesPercent)

    return message


def my_interval_job():
    stock_data = getStockData('AMZN')
    text_message = generateMessage(stock_data)
    # returns data to the group with id -916932468
    bot.send_message(-916932468, text_message)


def add_notification():
    sched.add_job(my_interval_job, 'interval', seconds=10, id='job_id')
    sched.start()


def remove_notification():
    sched.remove_job('job_id')
    sched.shutdown()

