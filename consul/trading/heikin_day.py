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
    print('Starting heikin ashi day module')

    HA()



def HA():
    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']
                # Current prices
                last = float(summary['Last'])  # last price
                bid = float(summary['Bid'])  # sell price
                ask = float(summary['Ask'])  # buy price

#######################
                daylastcandle = get_candles(market, 'day')['result'][-1:]
                daycurrentlow = float(daylastcandle[0]['L'])*100000
                daycurrenthigh = float(daylastcandle[0]['H'])*100000
                daycurrentopen = float(daylastcandle[0]['O'])*100000
                daycurrentclose = float(daylastcandle[0]['C'])*100000
                daypreviouscandle = get_candles(market, 'day')['result'][-2:]
                dayprevlow = float(daypreviouscandle[0]['L'])*100000
                dayprevhigh = float(daypreviouscandle[0]['H'])*100000
                dayprevopen = float(daypreviouscandle[0]['O'])*100000
                dayprevclose = float(daypreviouscandle[0]['C'])*100000
                daypreviouscandle2 = get_candles(market, 'day')['result'][-3:]
                dayprevlow2 = float(daypreviouscandle2[0]['L'])*100000
                dayprevhigh2 = float(daypreviouscandle2[0]['H'])*100000
                dayprevopen2 = float(daypreviouscandle2[0]['O'])*100000
                dayprevclose2 = float(daypreviouscandle2[0]['C'])*100000
###############
                HAD_PREV_Close2 = (dayprevopen2 + dayprevhigh2 + dayprevlow2 + dayprevclose2) / 4
                HAD_PREV_Open2 = (dayprevopen2 + dayprevclose2) / 2
                HAD_PREV_Low2 = dayprevlow2
                HAD_PREV_High2 = dayprevhigh2

                HAD_PREV_Close = (dayprevopen + dayprevhigh + dayprevlow + dayprevclose) / 4
                HAD_PREV_Open = (HAD_PREV_Open2 + HAD_PREV_Close2) / 2
                elements1 = numpy.array([dayprevhigh, dayprevlow, HAD_PREV_Open, HAD_PREV_Close])
                HAD_PREV_High = elements1.max(0)
                HAD_PREV_Low = elements1.min(0)

                HAD_Close = (daycurrentopen + daycurrenthigh + daycurrentlow + daycurrentclose) / 4
                HAD_Open = (HAD_PREV_Open + HAD_PREV_Close) / 2
                elements0 = numpy.array([daycurrenthigh, daycurrentlow, HAD_Open, HAD_Close])
                HAD_High = elements0.max(0)
                HAD_Low = elements0.min(0)
#############
                HAD_trend = "NONE"
#############
                had_direction_down_short0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 2)  and (HAD_Open - HAD_Close !=0)
                had_direction_down_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 2) and (HAD_PREV_Open - HAD_PREV_Close !=0)
                had_direction_down_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 2) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
                had_direction_down_shorter0 =((HAD_High - HAD_Low) / (HAD_Open - HAD_Close) >= 4)  and (HAD_Open - HAD_Close !=0)
                had_direction_down_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Open - HAD_PREV_Close) >= 4) and (HAD_PREV_Open - HAD_PREV_Close !=0)
                had_direction_down_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Open2 - HAD_PREV_Close2) >= 4) and (HAD_PREV_Open2 - HAD_PREV_Close2 !=0)
                had_direction_down0 = (HAD_Close < HAD_Open)
                had_direction_down1 = (HAD_PREV_Close < HAD_PREV_Open)
                had_direction_down2 = (HAD_PREV_Close2 < HAD_PREV_Open2)
                had_direction_down_long_0 = (HAD_Open == HAD_High and HAD_Close < HAD_Open)
                had_direction_down_long_1 = (HAD_PREV_Open == HAD_PREV_High and HAD_PREV_Close < HAD_PREV_Open)
                had_direction_down_long_2 = (HAD_PREV_Open2 == HAD_PREV_High2 and HAD_PREV_Close2 < HAD_PREV_Open2)
                had_direction_down_longer = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
                had_direction_down_longermax = (numpy.abs(HAD_Open - HAD_Close) > numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) > numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2 ) and had_direction_down0 and had_direction_down1 and had_direction_down2)
                had_direction_down_smaller = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and had_direction_down0 and had_direction_down1)
                had_direction_down_smaller1 = (numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down1 and had_direction_down2)
                had_direction_down_smallermax = (numpy.abs(HAD_Open - HAD_Close) < numpy.abs(HAD_PREV_Open - HAD_PREV_Close) and numpy.abs(HAD_PREV_Open - HAD_PREV_Close) < numpy.abs(HAD_PREV_Open2 - HAD_PREV_Close2) and had_direction_down0 and had_direction_down1 and had_direction_down2)

                had_direction_spin0 = (HAD_Open == HAD_Close)
                had_direction_spin1 = (HAD_PREV_Open == HAD_PREV_Close)
                had_direction_spin2 = (HAD_PREV_Open2 == HAD_PREV_Close2)

                had_direction_up_short0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 2) and (HAD_Close - HAD_Open !=0)
                had_direction_up_short1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 2) and (HAD_PREV_Close - HAD_PREV_Open !=0)
                had_direction_up_short2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 2) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
                had_direction_up_shorter0 = ((HAD_High - HAD_Low) / (HAD_Close - HAD_Open) >= 4) and (HAD_Close - HAD_Open !=0)
                had_direction_up_shorter1 = ((HAD_PREV_High - HAD_PREV_Low) / (HAD_PREV_Close - HAD_PREV_Open) >= 4) and (HAD_PREV_Close - HAD_PREV_Open !=0)
                had_direction_up_shorter2 = ((HAD_PREV_High2 - HAD_PREV_Low2) / (HAD_PREV_Close2 - HAD_PREV_Open2) >= 4) and (HAD_PREV_Close2 - HAD_PREV_Open2 !=0)
                had_direction_up0 = (HAD_Close > HAD_Open)
                had_direction_up1 = (HAD_PREV_Close > HAD_PREV_Open)
                had_direction_up2 = (HAD_PREV_Close2 > HAD_PREV_Open2)
                had_direction_up_long_0 = (HAD_Open == HAD_Low and HAD_Close > HAD_Open)
                had_direction_up_long_1 = (HAD_PREV_Open == HAD_PREV_Low and HAD_PREV_Close > HAD_PREV_Open)
                had_direction_up_long_2 = (HAD_PREV_Open2 == HAD_PREV_Low2 and HAD_PREV_Close2 > HAD_PREV_Open2)
                had_direction_up_longer = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
                had_direction_up_longermax = (numpy.abs(HAD_Close - HAD_Open) > numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) > numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)
                had_direction_up_smaller = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and had_direction_up0 and had_direction_up1)
                had_direction_up_smaller1 = (numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up1 and had_direction_up2)
                had_direction_up_smallermax = (numpy.abs(HAD_Close - HAD_Open) < numpy.abs(HAD_PREV_Close - HAD_PREV_Open) and numpy.abs(HAD_PREV_Close - HAD_PREV_Open) < numpy.abs(HAD_PREV_Close2 - HAD_PREV_Open2) and had_direction_up0 and had_direction_up1 and had_direction_up2)



                if (((had_direction_down_long_0 and had_direction_down0) or (had_direction_down_long_0 and had_direction_down_long_1 and had_direction_down0) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longer) or (had_direction_down_long_0 or had_direction_down_long_1 and had_direction_down_longermax and had_direction_down_longer) and had_direction_down0) or (had_direction_down0 and had_direction_down1 and had_direction_down2)):
                    HAD_trend = "DOWN"
                if (((had_direction_up_long_0 and had_direction_up0) or (had_direction_up_long_0 and had_direction_up_long_1 and had_direction_up0) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer) or (had_direction_up_long_0 or had_direction_up_long_1 and had_direction_up_longer and had_direction_up_longermax) and had_direction_up0) or (had_direction_up0 and had_direction_up1 and had_direction_up2)):
                    HAD_trend = "UP"
                if ((had_direction_up_short2 and had_direction_spin1 and had_direction_up0) or (had_direction_down_short2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_down_short1 and had_direction_spin0) or (had_direction_down_long_2 and had_direction_down_short1 and had_direction_up_long_0) or (had_direction_down_long_2 and had_direction_up_short1 and had_direction_up_long_0) or (had_direction_down2 and had_direction_up_long_0 and had_direction_up1 and had_direction_up_longer) or (had_direction_down_long_2 and had_direction_down_smaller1 and had_direction_up0) or (had_direction_down_long_2 and had_direction_down_short1 and  had_direction_up_long_0) or (had_direction_down_longermax and had_direction_up_short0) and had_direction_down1 and had_direction_down2):
                    HAD_trend = "Revers-UP"
                if ((had_direction_down_short2 and had_direction_spin1 and had_direction_down0) or (had_direction_up_short2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_up_short1 and had_direction_spin0) or (had_direction_up_long_2 and had_direction_up_short1 and had_direction_down_long_0) or (had_direction_up_long_2 and had_direction_down_short1 and had_direction_down_long_0) or (had_direction_up2 and had_direction_down_long_0 and had_direction_down1 and had_direction_down_longer) or (had_direction_up_long_2 and had_direction_up_smaller1 and had_direction_down0) or (had_direction_up_long_2 and had_direction_up_short1 and  had_direction_down_long_0) or (had_direction_up_longermax and had_direction_down_short0) and had_direction_up1 and had_direction_up2):
                    HAD_trend = "Revers-DOWN"
                if  HAD_trend != "Revers-DOWN" and   HAD_trend != "Revers-UP" and  HAD_trend != "DOWN" and HAD_trend != "UP":
                    HAD_trend = "STABLE"


                print market, HAD_trend
                try:
                    db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set current_price = %s, ha_direction_daily=%s  where market = %s",(last,  HAD_trend,  market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()

        except:
            continue


def available_market_list(marketname):
    db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
    cursor.execute("SELECT * FROM `markets` where `percent_chg`>0 and enabled=1 and market = '%s'" % market)

    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return True

    return False

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


def heikin_ashi(marketname, value):
    db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market = marketname
#    cursor.execute(
#        "SELECT * FROM `markets` where `percent_chg`>(SELECT AVG(`percent_chg`)/1.5 FROM `markets` where `percent_chg`>1) and market = '%s'" % market)
    cursor.execute("SELECT * FROM `markets` where `percent_chg`>0  and market = '%s'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return False

def status_orders(marketname, value):
    db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
    cursor = db.cursor()
    market=marketname
    cursor.execute("SELECT * FROM orders WHERE active = 1 and market = '%s'" % market)
    #cursor.execute("SELECT o.*, m.market FROM orders o, markets m WHERE o.active = 1 and o.market_id = m.id and m.market like '%%'" % market)
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0


if __name__ == "__main__":
    main()
