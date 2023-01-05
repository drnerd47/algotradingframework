import os, datetime, time
import redis,telegram
workers_count=2
lots_per_order_freeze_BN=36; qty_per_lot_BN=25

telegram_user = {'token':'',
                'chat_id_notification_1':''}
# bot = telegram.Bot(token=telegram_user['token'])

nse_calendar = {datetime.date(2023, 1, 26): 'Republic Day',
                datetime.date(2023, 3, 7): 'Holi',
                datetime.date(2023, 3, 30): 'Ram Navami',
                datetime.date(2023, 4, 4): 'Mahavir Jayanti',
                datetime.date(2023, 4, 7):  'Good Friday',
                datetime.date(2023, 4, 14):  'Dr.Baba Saheb Ambedkar Jayanti',
                datetime.date(2023, 5, 1): 'Maharashtra Day',
                datetime.date(2023, 6, 28): 'Bakri Id',
                datetime.date(2023, 8, 15): 'Independence Day',
                datetime.date(2023, 9, 19): 'Ganesh Chaturthi',
                datetime.date(2023, 10, 2): 'Mahatma Gandhi Jayanti',
                datetime.date(2023, 10, 24): 'Dussehra',
                datetime.date(2023, 11, 14): 'Diwali-Balipratipada',
                datetime.date(2023, 11, 27): 'Gurunanak Jayanti',
                datetime.date(2023, 12, 25): 'Christmas' }
                

def market_hours(open_time = datetime.time(9, 0, 0)):
    date_today = datetime.datetime.today().date()
    day_today = time.strftime("%A", time.localtime())
    if date_today in nse_calendar or day_today in ['Saturday', 'Sunday']:
        return 60*60*8

    
    close_time = datetime.time(15, 29, 59)
    market_time_open1 = datetime.datetime.today().time() > open_time
    market_time_open2 = datetime.datetime.today().time() < close_time
    if market_time_open1 and market_time_open2:
        return 'OPEN'

    current = datetime.datetime.time(datetime.datetime.now())
    diff = datetime.datetime.combine(datetime.date.today(), open_time) - datetime.datetime.combine(datetime.date.today(), current)
    sleep_secs = diff.seconds + 5
    get_up_time=datetime.datetime.fromtimestamp(sleep_secs+time.time()).strftime('%Y-%m-%d %H:%M:%S %A')
    print('System at sleep :), will wake up again @ ',get_up_time)
    return sleep_secs
    
def wake_up_time(wakeup_at = datetime.time(9, 15, 0)):
    current = datetime.datetime.time(datetime.datetime.now())
    diff = datetime.datetime.combine(datetime.date.today(), wakeup_at) - datetime.datetime.combine(datetime.date.today(), current)
    sleep_secs = diff.seconds + .51
    get_up_time=datetime.datetime.fromtimestamp(sleep_secs+time.time()).strftime('%Y-%m-%d %H:%M:%S %A')
    print('System at sleep :), will wake up again @ ',get_up_time)
    return sleep_secs

def telegram_msg(msg):
    return
    tried=0
    while tried<2:
        try:
            bot.sendMessage(chat_id=telegram_user['chat_id_notification_1'], text=msg)
            break
        except:
            tried+=1; time.sleep(1)

def time_now():return datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')