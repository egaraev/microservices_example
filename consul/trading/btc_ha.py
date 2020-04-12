import time
import config
from pybittrex.client import Client
import MySQLdb
import sys
import requests
import hashlib
import hmac
import numpy
import datetime
c1 = Client(api_key=config.key, api_secret=config.secret)
c=Client(api_key='', api_secret='')

currtime = int(round(time.time()))
now = datetime.datetime.now()
currenttime = now.strftime("%Y-%m-%d %H:%M")





def main():
    print('Starting btc_ha module')

    HA()



def HA():

    BTC_price = c.get_ticker('USDT-BTC').json()['result']['Last']
    currtime = int(time.time())

    btclastcandle = get_candles('USDT-BTC', 'day')['result'][-1:]
    btccurrentlow = float(btclastcandle[0]['L'])
    btccurrentopen = float(btclastcandle[0]['O'])
    btccurrentclose = float(btclastcandle[0]['C'])
    btccurrenthigh = float(btclastcandle[0]['H'])
    btcprevcandle = get_candles('USDT-BTC', 'day')['result'][-2:]
    btcprevlow = float(btcprevcandle[0]['L'])
    btcprevopen = float(btcprevcandle[0]['O'])
    btcprevclose = float(btcprevcandle[0]['C'])
    btcprevhigh = float(btcprevcandle[0]['H'])
    btcprevcandle2 = get_candles('USDT-BTC', 'day')['result'][-3:]
    btcprevlow2 = float(btcprevcandle2[0]['L'])
    btcprevopen2 = float(btcprevcandle2[0]['O'])
    btcprevclose2 = float(btcprevcandle2[0]['C'])
    btcprevhigh2 = float(btcprevcandle2[0]['H'])
    btcprevcandle3 = get_candles('USDT-BTC', 'day')['result'][-4:]
    btcprevlow3 = float(btcprevcandle3[0]['L'])
    btcprevopen3 = float(btcprevcandle3[0]['O'])
    btcprevclose3 = float(btcprevcandle3[0]['C'])
    btcprevhigh3 = float(btcprevcandle3[0]['H'])




    btclastcandlehour = get_candles('USDT-BTC', 'hour')['result'][-1:]
    btccurrentlowhour = float(btclastcandlehour[0]['L'])
    btccurrentopenhour = float(btclastcandlehour[0]['O'])
    btccurrentclosehour = float(btclastcandlehour[0]['C'])
    btccurrenthighhour = float(btclastcandlehour[0]['H'])
    btcprevcandlehour = get_candles('USDT-BTC', 'hour')['result'][-2:]
    btcprevlowhour = float(btcprevcandlehour[0]['L'])
    btcprevopenhour = float(btcprevcandlehour[0]['O'])
    btcprevclosehour = float(btcprevcandlehour[0]['C'])
    btcprevhighhour = float(btcprevcandlehour[0]['H'])
    btcprevcandlehour2 = get_candles('USDT-BTC', 'hour')['result'][-3:]
    btcprevlowhour2 = float(btcprevcandlehour2[0]['L'])
    btcprevopenhour2 = float(btcprevcandlehour2[0]['O'])
    btcprevclosehour2 = float(btcprevcandlehour2[0]['C'])
    btcprevhighhour2 = float(btcprevcandlehour2[0]['H'])





    BTC_HA_PREV_Close3 = (btcprevopen3 + btcprevhigh3 + btcprevlow3 + btcprevclose3) / 4
    BTC_HA_PREV_Open3 = (btcprevopen3 + btcprevclose3) / 2
    BTC_HA_PREV_Low3 = btcprevlow3
    BTC_HA_PREV_High3 = btcprevhigh3

    BTC_HA_PREV_Close2 = (btcprevopen2 + btcprevhigh2 + btcprevlow2 + btcprevclose2) / 4
    BTC_HA_PREV_Open2 = (BTC_HA_PREV_Open3 + BTC_HA_PREV_Close3) / 2
    elements2 = numpy.array([btcprevhigh2, btcprevlow2, BTC_HA_PREV_Open2, BTC_HA_PREV_Close2])
    BTC_HA_PREV_Low2 = elements2.min(0)
    BTC_HA_PREV_High2 = elements2.max(0)


    BTC_HA_PREV_Close = (btcprevopen + btcprevhigh + btcprevlow + btcprevclose) / 4
    BTC_HA_PREV_Open = (BTC_HA_PREV_Open2 + BTC_HA_PREV_Close2) / 2
    elements0 = numpy.array([btcprevhigh, btcprevlow, BTC_HA_PREV_Open, BTC_HA_PREV_Close])
    BTC_HA_PREV_Low = elements0.min(0)
    BTC_HA_PREV_High = elements0.max(0)

    BTC_HA_Close = (btccurrentopen + btccurrenthigh + btccurrentlow + btccurrentclose) / 4
    BTC_HA_Open = (BTC_HA_PREV_Open + BTC_HA_PREV_Close) / 2
    elements1 = numpy.array([btccurrenthigh, btccurrentlow, BTC_HA_Open, BTC_HA_Close])
    BTC_HA_Low = elements1.min(0)
    BTC_HA_High = elements1.max(0)

    try:
        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
        cursor = db.cursor()
        cursor.execute(
            "update parameters set btc_ha_close_day = %s, btc_ha_open_day =%s, btc_ha_low_day =%s, btc_ha_high_day =%s, btc_ha_time_day =%s  where id = %s",
            (BTC_HA_Close, BTC_HA_Open, BTC_HA_Low, BTC_HA_High, currtime, 1))
        db.commit()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        db.close()

    BTC_HA_PREV_Close_hour2 = (btcprevopenhour2 + btcprevhighhour2 + btcprevlowhour2 + btcprevclosehour2) / 4
    BTC_HA_PREV_Open_hour2 = (btcprevopenhour2 + btcprevclosehour2) / 2
    BTC_HA_PREV_Low_hour2 = btcprevlowhour2
    BTC_HA_PREV_High_hour2 = btcprevhighhour2

    BTC_HA_PREV_Close_hour = (btcprevopenhour + btcprevhighhour + btcprevlowhour + btcprevclosehour) / 4
    BTC_HA_PREV_Open_hour = (BTC_HA_PREV_Open_hour2 + BTC_HA_PREV_Close_hour2) / 2
    elements3 = numpy.array([btccurrenthighhour, btccurrentlowhour, BTC_HA_PREV_Open_hour, BTC_HA_PREV_Close_hour])
    BTC_HA_PREV_High_hour = elements3.max(0)
    BTC_HA_PREV_Low_hour = elements3.min(0)

    BTC_HA_Close_hour = (btccurrentopenhour + btccurrenthighhour + btccurrentlowhour + btccurrentclosehour) / 4
    BTC_HA_Open_hour = (BTC_HA_PREV_Open_hour + BTC_HA_PREV_Close_hour) / 2
    elements2 = numpy.array([btccurrenthighhour, btccurrentlowhour, BTC_HA_Open_hour, BTC_HA_Close_hour])
    BTC_HA_High_hour = elements2.max(0)
    BTC_HA_Low_hour = elements2.min(0)

    try:
        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
        cursor = db.cursor()
        cursor.execute(
            "update parameters set btc_ha_close_hour = %s, btc_ha_open_hour =%s, btc_ha_low_hour =%s, btc_ha_high_hour =%s, btc_ha_time_hour =%s  where id = %s",
            (BTC_HA_Close_hour, BTC_HA_Open_hour, BTC_HA_Low_hour, BTC_HA_High_hour, currtime, 1))
        db.commit()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        db.close()

    btc_trend = "NONE"
    btc_trend_hour = "NONE"



    direction_down0 = (BTC_HA_Close < BTC_HA_Open)
    direction_down1 = (BTC_HA_PREV_Close < BTC_HA_PREV_Open)
    direction_down2 = (BTC_HA_PREV_Close2 < BTC_HA_PREV_Open2)
    direction_down_long_0 = (BTC_HA_Open == BTC_HA_High and BTC_HA_Close < BTC_HA_Open)
    direction_down_long_1 = (BTC_HA_PREV_Open == BTC_HA_PREV_High and BTC_HA_PREV_Close < BTC_HA_PREV_Open)
    direction_down_longer = (numpy.abs(BTC_HA_Close - BTC_HA_Open) > numpy.abs(
        BTC_HA_PREV_Close - BTC_HA_PREV_Open) and direction_down0 and direction_down1)
    direction_spin0 = (BTC_HA_Open == BTC_HA_Close)
    direction_spin1 = (BTC_HA_PREV_Open == BTC_HA_PREV_Close)

    hour_direction_down0 = (BTC_HA_Close_hour < BTC_HA_Open_hour)
    hour_direction_down1 = (BTC_HA_PREV_Close_hour < BTC_HA_PREV_Open_hour)
    hour_direction_down_long_0 = (BTC_HA_Open_hour == BTC_HA_High_hour and BTC_HA_Close_hour < BTC_HA_Open_hour)
    hour_direction_down_long_1 = (
    BTC_HA_PREV_Open_hour == BTC_HA_PREV_High_hour and BTC_HA_PREV_Close_hour < BTC_HA_PREV_Open_hour)
    hour_direction_down_longer = (numpy.abs(BTC_HA_Close_hour - BTC_HA_Open_hour) > numpy.abs(
        BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) and hour_direction_down0 and hour_direction_down1)
    hour_direction_spin0 = (BTC_HA_Open_hour == BTC_HA_Close_hour)
    hour_direction_spin1 = (BTC_HA_PREV_Open_hour == BTC_HA_PREV_Close_hour)

    direction_down_short0 = ((BTC_HA_High - BTC_HA_Low) / (BTC_HA_Open - BTC_HA_Close) >= 6) and (
    BTC_HA_Open - BTC_HA_Close != 0)
    direction_down_short1 = ((BTC_HA_PREV_High - BTC_HA_PREV_Low) / (BTC_HA_PREV_Open - BTC_HA_PREV_Close) >= 6) and (
    BTC_HA_PREV_Open - BTC_HA_PREV_Close != 0)
    direction_up_short0 = ((BTC_HA_High - BTC_HA_Low) / (BTC_HA_Close - BTC_HA_Open) >= 6) and (
    BTC_HA_Close - BTC_HA_Open != 0)
    direction_up_short1 = ((BTC_HA_PREV_High - BTC_HA_PREV_Low) / (BTC_HA_PREV_Close - BTC_HA_PREV_Open) >= 6) and (
    BTC_HA_PREV_Close - BTC_HA_PREV_Open != 0)

    hour_direction_down_short0 = ((BTC_HA_High_hour - BTC_HA_Low_hour) / (
    BTC_HA_Open_hour - BTC_HA_Close_hour) >= 6) and (BTC_HA_Open_hour - BTC_HA_Close_hour != 0)
    hour_direction_down_short1 = ((BTC_HA_PREV_High_hour - BTC_HA_PREV_Low_hour) / (
    BTC_HA_PREV_Open_hour - BTC_HA_PREV_Close_hour) >= 6) and (BTC_HA_PREV_Open_hour - BTC_HA_PREV_Close_hour != 0)
    hour_direction_up_short0 = (
                               (BTC_HA_High_hour - BTC_HA_Low_hour) / (BTC_HA_Close_hour - BTC_HA_Open_hour) >= 6) and (
                               BTC_HA_Close_hour - BTC_HA_Open_hour != 0)
    hour_direction_up_short1 = ((BTC_HA_PREV_High_hour - BTC_HA_PREV_Low_hour) / (
    BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) >= 6) and (BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour != 0)

    direction_up0 = (BTC_HA_Close > BTC_HA_Open)
    direction_up1 = (BTC_HA_PREV_Close > BTC_HA_PREV_Open)
    direction_up2 = (BTC_HA_PREV_Close2 > BTC_HA_PREV_Open2)
    direction_up_long_0 = (BTC_HA_Open == BTC_HA_Low and BTC_HA_Close_hour > BTC_HA_Open_hour)
    direction_up_long_1 = (BTC_HA_PREV_Open == BTC_HA_PREV_Low and BTC_HA_PREV_Close > BTC_HA_PREV_Open)
    direction_up_longer = (numpy.abs(BTC_HA_Close - BTC_HA_Open) > numpy.abs(
        BTC_HA_PREV_Close - BTC_HA_PREV_Open) and direction_up0 and direction_up1)

    hour_direction_up0 = (BTC_HA_Close_hour > BTC_HA_Open_hour)
    hour_direction_up1 = (BTC_HA_PREV_Close_hour > BTC_HA_PREV_Open_hour)
    hour_direction_up_long_0 = (BTC_HA_Open_hour == BTC_HA_Low_hour and BTC_HA_Close_hour > BTC_HA_Open_hour)
    hour_direction_up_long_1 = (
    BTC_HA_PREV_Open_hour == BTC_HA_PREV_Low_hour and BTC_HA_PREV_Close_hour > BTC_HA_PREV_Open_hour)
    hour_direction_up_longer = (numpy.abs(BTC_HA_Close_hour - BTC_HA_Open_hour) > numpy.abs(
        BTC_HA_PREV_Close_hour - BTC_HA_PREV_Open_hour) and hour_direction_up0 and hour_direction_up1)



    if (((hour_direction_down_long_0 and hour_direction_down0) or (
            hour_direction_down_long_0 and hour_direction_down_long_1 and hour_direction_down0) or (
        hour_direction_down_long_0 or hour_direction_down_long_1 and hour_direction_down_longer) and hour_direction_down0) or (
        hour_direction_down0 and hour_direction_down1)):
        btc_trend_hour = "DOWN"
    if (((hour_direction_up_long_0 and hour_direction_up0) or (
            hour_direction_up_long_0 and hour_direction_up_long_1 and hour_direction_up0) or (
        hour_direction_up_long_0 or hour_direction_up_long_1 and hour_direction_up_longer) and hour_direction_up0) or (
        hour_direction_up0 and hour_direction_up1)):
        btc_trend_hour = "UP"

    if btc_trend_hour != "DOWN" and btc_trend_hour != "UP":
        btc_trend_hour = "STABLE"


        # Daily HA
    if (((direction_down_long_0 and direction_down0) or (
            direction_down_long_0 and direction_down_long_1 and direction_down0) or (
        direction_down_long_0 or direction_down_long_1 and direction_down_longer) and direction_down0) or (
        direction_down0 and direction_down1 and direction_down2)):
        btc_trend = "DOWN"
    if (((direction_up_long_0 and direction_up0) or (
            direction_up_long_0 and direction_up_long_1 and direction_up0) or (
        direction_up_long_0 or direction_up_long_1 and direction_up_longer) and direction_up0) or (
        direction_up0 and direction_up1 and direction_up2)):
        btc_trend = "UP"

    if btc_trend != "DOWN" and btc_trend != "UP":
        btc_trend = "STABLE"



    if btc_trend == "DOWN" and btc_trend_hour == "DOWN":
        btc_trend = "DANGER"








    try:
        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
        cursor = db.cursor()
        cursor.execute("update parameters set usdt_btc_price = %s, btc_ha_direction_day =%s where id = %s",
                       (BTC_price, btc_trend, 1))
        db.commit()
    except MySQLdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    finally:
        db.close()



    print btc_trend




def get_candles(market, tick_interval):
    url = 'https://bittrex.com/api/v2.0/pub/market/GetTicks?apikey=' + config.key + '&MarketName=' + market +'&tickInterval=' + str(tick_interval)
    return signed_request(url)


def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(config.secret, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signed}
    r = requests.get(url, headers=headers)
    return r.json()

















if __name__ == "__main__":
    main()
