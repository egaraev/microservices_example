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
    print('Starting heikin ashi module')

    HA()



def HA():

    market_summ = c.get_market_summaries().json()['result']
    for summary in market_summ: #Loop trough the market summary
        try:
            if available_market_list(summary['MarketName']):
                market = summary['MarketName']

                last = float(summary['Last'])  # last price
                bought_quantity_sql = float(status_orders(market, 2))
                HAD_trend = heikin_ashi(market, 18)
                ha_old_time=heikin_ashi(market, 23)
                print "Gather hour HA candle info for ", market

                hlastcandle = get_candles(market, 'hour')['result'][-1:]
                hcurrentlow = float(hlastcandle[0]['L'])*100000
                hcurrenthigh = float(hlastcandle[0]['H'])*100000
                hcurrentopen = float(hlastcandle[0]['O'])*100000
                hcurrentclose = float(hlastcandle[0]['C'])*100000
                hpreviouscandle = get_candles(market, 'hour')['result'][-2:]
                hprevlow = float(hpreviouscandle[0]['L'])*100000
                hprevhigh = float(hpreviouscandle[0]['H'])*100000
                hprevopen = float(hpreviouscandle[0]['O'])*100000
                hprevclose = float(hpreviouscandle[0]['C'])*100000
                hpreviouscandle2 = get_candles(market, 'hour')['result'][-3:]
                hprevlow2 = float(hpreviouscandle2[0]['L'])*100000
                hprevhigh2 = float(hpreviouscandle2[0]['H'])*100000
                hprevopen2 = float(hpreviouscandle2[0]['O'])*100000
                hprevclose2 = float(hpreviouscandle2[0]['C'])*100000

                print "Gather 5hour HA candle info for ", market

                hourlastcandle = get_candles(market, 'hour')['result'][-1:]
                hourcurrentlow = float(hourlastcandle[0]['L'])*100000
                hourcurrenthigh = float(hourlastcandle[0]['H'])*100000
                hourcurrentopen = float(hourlastcandle[0]['O'])*100000
                hourcurrentclose = float(hourlastcandle[0]['C'])*100000
                hourpreviouscandle = get_candles(market, 'hour')['result'][-2:]
                hourprevlow = float(hourpreviouscandle[0]['L'])*100000
                hourprevhigh = float(hourpreviouscandle[0]['H'])*100000
                hourprevopen = float(hourpreviouscandle[0]['O'])*100000
                hourprevclose = float(hourpreviouscandle[0]['C'])*100000
                hourpreviouscandle2 = get_candles(market, 'hour')['result'][-3:]
                hourprevlow2 = float(hourpreviouscandle2[0]['L'])*100000
                hourprevhigh2 = float(hourpreviouscandle2[0]['H'])*100000
                hourprevopen2 = float(hourpreviouscandle2[0]['O'])*100000
                hourprevclose2 = float(hourpreviouscandle2[0]['C'])*100000
                hourpreviouscandle3 = get_candles(market, 'hour')['result'][-4:]
                hourprevlow3 = float(hourpreviouscandle3[0]['L'])*100000
                hourprevhigh3 = float(hourpreviouscandle3[0]['H'])*100000
                #hourprevopen3 = float(hourpreviouscandle3[0]['O'])*100000
                #hourprevclose3 = float(hourpreviouscandle3[0]['C'])*100000
                hourpreviouscandle4 = get_candles(market, 'hour')['result'][-5:]
                hourprevlow4 = float(hourpreviouscandle4[0]['L'])*100000
                hourprevhigh4 = float(hourpreviouscandle4[0]['H'])*100000
                hourprevopen4 = float(hourpreviouscandle4[0]['O'])*100000
                #hourprevclose4 = float(hourpreviouscandle4[0]['C'])*100000
                hourpreviouscandle5 = get_candles(market, 'hour')['result'][-6:]
                hourprevlow5 = float(hourpreviouscandle5[0]['L'])*100000
                hourprevhigh5 = float(hourpreviouscandle5[0]['H'])*100000
                #hourprevopen5 = float(hourpreviouscandle5[0]['O'])*100000
                hourprevclose5 = float(hourpreviouscandle5[0]['C'])*100000
                hourpreviouscandle6 = get_candles(market, 'hour')['result'][-7:]
                hourprevlow6 = float(hourpreviouscandle6[0]['L'])*100000
                hourprevhigh6 = float(hourpreviouscandle6[0]['H'])*100000
                #hourprevopen6 = float(hourpreviouscandle6[0]['O'])*100000
                #hourprevclose6 = float(hourpreviouscandle6[0]['C'])*100000
                hourpreviouscandle7 = get_candles(market, 'hour')['result'][-8:]
                hourprevlow7 = float(hourpreviouscandle7[0]['L'])*100000
                hourprevhigh7 = float(hourpreviouscandle7[0]['H'])*100000
                #hourprevopen7 = float(hourpreviouscandle7[0]['O'])*100000
                #hourprevclose7 = float(hourpreviouscandle7[0]['C'])*100000
                hourpreviouscandle8 = get_candles(market, 'hour')['result'][-9:]
                hourprevlow8 = float(hourpreviouscandle8[0]['L'])*100000
                hourprevhigh8 = float(hourpreviouscandle8[0]['H'])*100000
                #hourprevopen8 = float(hourpreviouscandle8[0]['O'])*100000
                #hourprevclose8 = float(hourpreviouscandle8[0]['C'])*100000
                hourpreviouscandle9 = get_candles(market, 'hour')['result'][-10:]
                hourprevlow9 = float(hourpreviouscandle9[0]['L'])*100000
                hourprevhigh9 = float(hourpreviouscandle9[0]['H'])*100000
                hourprevopen9 = float(hourpreviouscandle9[0]['O'])*100000
                #hourprevclose9 = float(hourpreviouscandle9[0]['C'])*100000
                hourpreviouscandle10 = get_candles(market, 'hour')['result'][-11:]
                hourprevlow10 = float(hourpreviouscandle10[0]['L'])*100000
                hourprevhigh10 = float(hourpreviouscandle10[0]['H'])*100000
                #hourprevopen10 = float(hourpreviouscandle10[0]['O'])*100000
                hourprevclose10 = float(hourpreviouscandle10[0]['C'])*100000
                hourpreviouscandle11 = get_candles(market, 'hour')['result'][-12:]
                hourprevlow11 = float(hourpreviouscandle11[0]['L'])*100000
                hourprevhigh11 = float(hourpreviouscandle11[0]['H'])*100000
                #hourprevopen11 = float(hourpreviouscandle11[0]['O'])*100000
                #hourprevclose11 = float(hourpreviouscandle11[0]['C'])*100000
                hourpreviouscandle12 = get_candles(market, 'hour')['result'][-13:]
                hourprevlow12 = float(hourpreviouscandle12[0]['L'])*100000
                hourprevhigh12 = float(hourpreviouscandle12[0]['H'])*100000
                #hourprevopen12 = float(hourpreviouscandle12[0]['O'])*100000
                #hourprevclose12 = float(hourpreviouscandle12[0]['C'])*100000
                hourpreviouscandle13 = get_candles(market, 'hour')['result'][-14:]
                hourprevlow13 = float(hourpreviouscandle13[0]['L'])*100000
                hourprevhigh13 = float(hourpreviouscandle13[0]['H'])*100000
                #hourprevopen13 = float(hourpreviouscandle13[0]['O'])*100000
                #hourprevclose13 = float(hourpreviouscandle13[0]['C'])*100000
                hourpreviouscandle14 = get_candles(market, 'hour')['result'][-15:]
                hourprevlow14 = float(hourpreviouscandle14[0]['L'])*100000
                hourprevhigh14 = float(hourpreviouscandle14[0]['H'])*100000
                hourprevopen14 = float(hourpreviouscandle14[0]['O'])*100000
                #hourprevclose14 = float(hourpreviouscandle14[0]['C'])*100000
                hourpreviouscandle15 = get_candles(market, 'hour')['result'][-16:]
                hourprevlow15 = float(hourpreviouscandle15[0]['L'])*100000
                hourprevhigh15 = float(hourpreviouscandle15[0]['H'])*100000
                #hourprevopen15 = float(hourpreviouscandle15[0]['O'])*100000
                hourprevclose15 = float(hourpreviouscandle15[0]['C'])*100000
                hourpreviouscandle16 = get_candles(market, 'hour')['result'][-17:]
                hourprevlow16 = float(hourpreviouscandle16[0]['L'])*100000
                hourprevhigh16 = float(hourpreviouscandle16[0]['H'])*100000
                #hourprevopen16 = float(hourpreviouscandle16[0]['O'])*100000
                #hourprevclose16 = float(hourpreviouscandle16[0]['C'])*100000
                hourpreviouscandle17 = get_candles(market, 'hour')['result'][-18:]
                hourprevlow17 = float(hourpreviouscandle17[0]['L'])*100000
                hourprevhigh17 = float(hourpreviouscandle17[0]['H'])*100000
                #hourprevopen17 = float(hourpreviouscandle17[0]['O'])*100000
                #hourprevclose17 = float(hourpreviouscandle17[0]['C'])*100000
                hourpreviouscandle18 = get_candles(market, 'hour')['result'][-19:]
                hourprevlow18 = float(hourpreviouscandle18[0]['L'])*100000
                hourprevhigh18 = float(hourpreviouscandle18[0]['H'])*100000
                #hourprevopen18 = float(hourpreviouscandle18[0]['O'])*100000
                #hourprevclose18 = float(hourpreviouscandle18[0]['C'])*100000
                hourpreviouscandle19 = get_candles(market, 'hour')['result'][-20:]
                hourprevlow19 = float(hourpreviouscandle19[0]['L'])*100000
                hourprevhigh19 = float(hourpreviouscandle19[0]['H'])*100000
                hourprevopen19 = float(hourpreviouscandle19[0]['O'])*100000
                #hourprevclose19 = float(hourpreviouscandle19[0]['C'])*100000
                hourpreviouscandle20 = get_candles(market, 'hour')['result'][-21:]
                hourprevlow20 = float(hourpreviouscandle20[0]['L'])*100000
                hourprevhigh20 = float(hourpreviouscandle20[0]['H'])*100000
                #hourprevopen20 = float(hourpreviouscandle20[0]['O'])*100000
                hourprevclose20 = float(hourpreviouscandle20[0]['C'])*100000
                hourpreviouscandle21 = get_candles(market, 'hour')['result'][-22:]
                hourprevlow21 = float(hourpreviouscandle21[0]['L'])*100000
                hourprevhigh21 = float(hourpreviouscandle21[0]['H'])*100000
                #hourprevopen21 = float(hourpreviouscandle21[0]['O'])*100000
                #hourprevclose21 = float(hourpreviouscandle21[0]['C'])*100000
                hourpreviouscandle22 = get_candles(market, 'hour')['result'][-23:]
                hourprevlow22 = float(hourpreviouscandle22[0]['L'])*100000
                hourprevhigh22 = float(hourpreviouscandle22[0]['H'])*100000
                #hourprevopen22 = float(hourpreviouscandle22[0]['O'])*100000
                #hourprevclose22 = float(hourpreviouscandle22[0]['C'])*100000
                hourpreviouscandle23 = get_candles(market, 'hour')['result'][-24:]
                hourprevlow23 = float(hourpreviouscandle23[0]['L'])*100000
                hourprevhigh23 = float(hourpreviouscandle23[0]['H'])*100000
                #hourprevopen23 = float(hourpreviouscandle23[0]['O'])*100000
                #hourprevclose23 = float(hourpreviouscandle23[0]['C'])*100000
                hourpreviouscandle24 = get_candles(market, 'hour')['result'][-25:]
                hourprevlow24 = float(hourpreviouscandle24[0]['L'])*100000
                hourprevhigh24 = float(hourpreviouscandle24[0]['H'])*100000
                hourprevopen24 = float(hourpreviouscandle24[0]['O'])*100000
                #hourprevclose24 = float(hourpreviouscandle24[0]['C'])*100000






                fivehourcurrentlow = min(hourcurrentlow, hourprevlow, hourprevlow2, hourprevlow3, hourprevlow4)
                fivehourcurrenthigh = max(hourcurrenthigh, hourprevhigh, hourprevhigh2, hourprevhigh3, hourprevhigh4)
                fivehourcurrentopen = hourprevopen4
                fivehourcurrentclose = hourcurrentclose


                fivehourprevlow = min(hourprevlow5, hourprevlow6, hourprevlow7, hourprevlow8, hourprevlow9)
                fivehourprevhigh = max(hourprevhigh5,hourprevhigh6, hourprevhigh7, hourprevhigh8, hourprevhigh9)
                fivehourprevopen = hourprevopen9
                fivehourprevclose = hourprevclose5


                fivehourprevlow2 = min(hourprevlow10, hourprevlow11, hourprevlow12, hourprevlow13, hourprevlow14)
                fivehourprevhigh2 = max(hourprevhigh10,hourprevhigh11, hourprevhigh12, hourprevhigh13, hourprevhigh14)
                fivehourprevopen2 = hourprevopen14
                fivehourprevclose2 = hourprevclose10


                fivehourprevlow3 = min(hourprevlow15, hourprevlow16, hourprevlow17, hourprevlow18, hourprevlow19)
                fivehourprevhigh3 = max(hourprevhigh15,hourprevhigh16, hourprevhigh17, hourprevhigh18, hourprevhigh19)
                fivehourprevopen3 = hourprevopen19
                fivehourprevclose3 = hourprevclose15


                fivehourprevlow4 = min(hourprevlow20, hourprevlow21, hourprevlow22, hourprevlow23, hourprevlow24)
                fivehourprevhigh4 = max(hourprevhigh20,hourprevhigh21, hourprevhigh22, hourprevhigh23, hourprevhigh24)
                fivehourprevopen4 = hourprevopen24
                fivehourprevclose4 = hourprevclose20

                print "Computing HA candles for ", market

                HA_PREV_Close4 = (fivehourprevopen4 + fivehourprevhigh4 + fivehourprevlow4 + fivehourprevclose4) / 4
                HA_PREV_Open4 = (fivehourprevopen4 + fivehourprevclose4) / 2
                HA_PREV_Low4 = fivehourprevlow4
                HA_PREV_High4 = fivehourprevhigh4


                HA_PREV_Close3 = (fivehourprevopen3 + fivehourprevhigh3 + fivehourprevlow3 + fivehourprevclose3) / 4
                HA_PREV_Open3 = (HA_PREV_Open4 + HA_PREV_Close4) / 2
                elements3 = numpy.array([fivehourprevhigh3, fivehourprevlow3, HA_PREV_Open4, HA_PREV_Close4])
                HA_PREV_High3 = elements3.max(0)
                HA_PREV_Low3 = elements3.min(0)

                HA_PREV_Close2 = (fivehourprevopen2 + fivehourprevhigh2 + fivehourprevlow2 + fivehourprevclose2) / 4
                HA_PREV_Open2 = (HA_PREV_Open3 + HA_PREV_Close3) / 2
                elements2 = numpy.array([fivehourprevhigh2, fivehourprevlow2, HA_PREV_Open3, HA_PREV_Close3])
                HA_PREV_High2 = elements2.max(0)
                HA_PREV_Low2 = elements2.min(0)

                HA_PREV_Close = (fivehourprevopen + fivehourprevhigh + fivehourprevlow + fivehourprevclose) / 4
                HA_PREV_Open = (HA_PREV_Open2 + HA_PREV_Close2) / 2
                elements1 = numpy.array([fivehourprevhigh, fivehourprevlow, HA_PREV_Open, HA_PREV_Close])
                HA_PREV_High = elements1.max(0)
                HA_PREV_Low = elements1.min(0)

                HA_Close = (fivehourcurrentopen + fivehourcurrenthigh + fivehourcurrentlow + fivehourcurrentclose) / 4
                HA_Open = (HA_PREV_Open + HA_PREV_Close) / 2
                elements0 = numpy.array([fivehourcurrenthigh, fivehourcurrentlow, HA_Open, HA_Close])
                HA_High = elements0.max(0)
                HA_Low = elements0.min(0)






                HAH_PREV_Close2 = (hprevopen2 + hprevhigh2 + hprevlow2 + hprevclose2) / 4
                HAH_PREV_Open2 = (hprevopen2 + hprevclose2) / 2
                HAH_PREV_Low2 = hprevlow2
                HAH_PREV_High2 = hprevhigh2

                HAH_PREV_Close = (hprevopen + hprevhigh + hprevlow + hprevclose) / 4
                HAH_PREV_Open = (HAH_PREV_Open2 + HAH_PREV_Close2) / 2
                elements1 = numpy.array([hprevhigh, hprevlow, HAH_PREV_Open, HAH_PREV_Close])
                HAH_PREV_High = elements1.max(0)
                HAH_PREV_Low = elements1.min(0)

                HAH_Close = (hcurrentopen + hcurrenthigh + hcurrentlow + hcurrentclose) / 4
                HAH_Open = (HAH_PREV_Open + HAH_PREV_Close) / 2
                elements0 = numpy.array([hcurrenthigh, hcurrentlow, HAH_Open, HAH_Close])
                HAH_High = elements0.max(0)
                HAH_Low = elements0.min(0)




                try:
                    db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
                    cursor = db.cursor()
                    cursor.execute("update markets set ha_close = %s, ha_open =%s, ha_low =%s, ha_high =%s, ha_time =%s, ha_time_second=%s  where market = %s",(HA_Close, HA_Open, HA_Low, HA_High, currenttime, currtime, market))
                    db.commit()
                except MySQLdb.Error, e:
                    print "Error %d: %s" % (e.args[0], e.args[1])
                    sys.exit(1)
                finally:
                    db.close()

                HA_trend = "NONE"

                HAH_trend = "NONE"

                print "Generting direction info for ", market

                ha_direction_down_short0 =((HA_High - HA_Low) / (HA_Open - HA_Close) >= 2)  and (HA_Open - HA_Close !=0)
                ha_direction_down_short1 = ((HA_PREV_High - HA_PREV_Low) / (HA_PREV_Open - HA_PREV_Close) >= 2) and (HA_PREV_Open - HA_PREV_Close !=0)
                ha_direction_down_short2 = ((HA_PREV_High2 - HA_PREV_Low2) / (HA_PREV_Open2 - HA_PREV_Close2) >= 2) and (HA_PREV_Open2 - HA_PREV_Close2 !=0)
                ha_direction_down_shorter0 =((HA_High - HA_Low) / (HA_Open - HA_Close) >= 4)  and (HA_Open - HA_Close !=0)
                ha_direction_down_shorter1 = ((HA_PREV_High - HA_PREV_Low) / (HA_PREV_Open - HA_PREV_Close) >= 4) and (HA_PREV_Open - HA_PREV_Close !=0)
                ha_direction_down_shorter2 = ((HA_PREV_High2 - HA_PREV_Low2) / (HA_PREV_Open2 - HA_PREV_Close2) >= 4) and (HA_PREV_Open2 - HA_PREV_Close2 !=0)
                ha_direction_down0 = (HA_Close < HA_Open)
                ha_direction_down1 = (HA_PREV_Close < HA_PREV_Open)
                ha_direction_down2 = (HA_PREV_Close2 < HA_PREV_Open2)
                ha_direction_down_long_0 = (HA_Open == HA_High and HA_Close < HA_Open)
                ha_direction_down_long_1 = (HA_PREV_Open == HA_PREV_High and HA_PREV_Close < HA_PREV_Open)
                ha_direction_down_long_2 = (HA_PREV_Open2 == HA_PREV_High2 and HA_PREV_Close2 < HA_PREV_Open2)
                ha_direction_down_longer = (numpy.abs(HA_Open - HA_Close) > numpy.abs(HA_PREV_Open - HA_PREV_Close) and ha_direction_down0 and ha_direction_down1)
                ha_direction_down_longermax = (numpy.abs(HA_Open - HA_Close) > numpy.abs(HA_PREV_Open - HA_PREV_Close) and numpy.abs(HA_PREV_Open - HA_PREV_Close) > numpy.abs(HA_PREV_Open2 - HA_PREV_Close2 ) and ha_direction_down0 and ha_direction_down1 and ha_direction_down2)
                ha_direction_down_smaller = (numpy.abs(HA_Open - HA_Close) < numpy.abs(HA_PREV_Open - HA_PREV_Close) and ha_direction_down0 and ha_direction_down1)
                ha_direction_down_smaller1 = (numpy.abs(HA_PREV_Open - HA_PREV_Close) < numpy.abs(HA_PREV_Open2 - HA_PREV_Close2) and ha_direction_down1 and ha_direction_down2)
                ha_direction_down_smallermax = (numpy.abs(HA_Open - HA_Close) < numpy.abs(HA_PREV_Open - HA_PREV_Close) and numpy.abs(HA_PREV_Open - HA_PREV_Close) < numpy.abs(HA_PREV_Open2 - HA_PREV_Close2) and ha_direction_down0 and ha_direction_down1 and ha_direction_down2)

                ha_direction_spin0 = (HA_Open == HA_Close)
                ha_direction_spin1 = (HA_PREV_Open == HA_PREV_Close)
                ha_direction_spin2 = (HA_PREV_Open2 == HA_PREV_Close2)

                ha_direction_up_short0 = ((HA_High - HA_Low) / (HA_Close - HA_Open) >= 2) and (HA_Close - HA_Open !=0)
                ha_direction_up_short1 = ((HA_PREV_High - HA_PREV_Low) / (HA_PREV_Close - HA_PREV_Open) >= 2) and (HA_PREV_Close - HA_PREV_Open !=0)
                ha_direction_up_short2 = ((HA_PREV_High2 - HA_PREV_Low2) / (HA_PREV_Close2 - HA_PREV_Open2) >= 2) and (HA_PREV_Close2 - HA_PREV_Open2 !=0)
                ha_direction_up_shorter0 = ((HA_High - HA_Low) / (HA_Close - HA_Open) >= 4) and (HA_Close - HA_Open !=0)
                ha_direction_up_shorter1 = ((HA_PREV_High - HA_PREV_Low) / (HA_PREV_Close - HA_PREV_Open) >= 4) and (HA_PREV_Close - HA_PREV_Open !=0)
                ha_direction_up_shorter2 = ((HA_PREV_High2 - HA_PREV_Low2) / (HA_PREV_Close2 - HA_PREV_Open2) >= 4) and (HA_PREV_Close2 - HA_PREV_Open2 !=0)
                ha_direction_up0 = (HA_Close > HA_Open)
                ha_direction_up1 = (HA_PREV_Close > HA_PREV_Open)
                ha_direction_up2 = (HA_PREV_Close2 > HA_PREV_Open2)
                ha_direction_up_long_0 = (HA_Open == HA_Low and HA_Close > HA_Open)
                ha_direction_up_long_1 = (HA_PREV_Open == HA_PREV_Low and HA_PREV_Close > HA_PREV_Open)
                ha_direction_up_long_2 = (HA_PREV_Open2 == HA_PREV_Low2 and HA_PREV_Close2 > HA_PREV_Open2)
                ha_direction_up_longer = (numpy.abs(HA_Close - HA_Open) > numpy.abs(HA_PREV_Close - HA_PREV_Open) and ha_direction_up0 and ha_direction_up1)
                ha_direction_up_longermax = (numpy.abs(HA_Close - HA_Open) > numpy.abs(HA_PREV_Close - HA_PREV_Open) and numpy.abs(HA_PREV_Close - HA_PREV_Open) > numpy.abs(HA_PREV_Close2 - HA_PREV_Open2) and ha_direction_up0 and ha_direction_up1 and ha_direction_up2)
                ha_direction_up_smaller = (numpy.abs(HA_Close - HA_Open) < numpy.abs(HA_PREV_Close - HA_PREV_Open) and ha_direction_up0 and ha_direction_up1)
                ha_direction_up_smaller1 = (numpy.abs(HA_PREV_Close - HA_PREV_Open) < numpy.abs(HA_PREV_Close2 - HA_PREV_Open2) and ha_direction_up1 and ha_direction_up2)
                ha_direction_up_smallermax = (numpy.abs(HA_Close - HA_Open) < numpy.abs(HA_PREV_Close - HA_PREV_Open) and numpy.abs(HA_PREV_Close - HA_PREV_Open) < numpy.abs(HA_PREV_Close2 - HA_PREV_Open2) and ha_direction_up0 and ha_direction_up1 and ha_direction_up2)




                hah_direction_down_short0 =((HAH_High - HAH_Low) / (HAH_Open - HAH_Close) >= 2)  and (HAH_Open - HAH_Close !=0)
                hah_direction_down_short1 = ((HAH_PREV_High - HAH_PREV_Low) / (HAH_PREV_Open - HAH_PREV_Close) >= 2) and (HAH_PREV_Open - HAH_PREV_Close !=0)
                hah_direction_down_short2 = ((HAH_PREV_High2 - HAH_PREV_Low2) / (HAH_PREV_Open2 - HAH_PREV_Close2) >= 2) and (HAH_PREV_Open2 - HAH_PREV_Close2 !=0)
                hah_direction_down_shorter0 =((HAH_High - HAH_Low) / (HAH_Open - HAH_Close) >= 4)  and (HAH_Open - HAH_Close !=0)
                hah_direction_down_shorter1 = ((HAH_PREV_High - HAH_PREV_Low) / (HAH_PREV_Open - HAH_PREV_Close) >= 4) and (HAH_PREV_Open - HAH_PREV_Close !=0)
                hah_direction_down_shorter2 = ((HAH_PREV_High2 - HAH_PREV_Low2) / (HAH_PREV_Open2 - HAH_PREV_Close2) >= 4) and (HAH_PREV_Open2 - HAH_PREV_Close2 !=0)
                hah_direction_down0 = (HAH_Close < HAH_Open)
                hah_direction_down1 = (HAH_PREV_Close < HAH_PREV_Open)
                hah_direction_down2 = (HAH_PREV_Close2 < HAH_PREV_Open2)
                hah_direction_down_long_0 = (HAH_Open == HAH_High and HAH_Close < HAH_Open)
                hah_direction_down_long_1 = (HAH_PREV_Open == HAH_PREV_High and HAH_PREV_Close < HAH_PREV_Open)
                hah_direction_down_long_2 = (HAH_PREV_Open2 == HAH_PREV_High2 and HAH_PREV_Close2 < HAH_PREV_Open2)
                hah_direction_down_longer = (numpy.abs(HAH_Open - HAH_Close) > numpy.abs(HAH_PREV_Open - HAH_PREV_Close) and hah_direction_down0 and hah_direction_down1)
                hah_direction_down_longermax = (numpy.abs(HAH_Open - HAH_Close) > numpy.abs(HAH_PREV_Open - HAH_PREV_Close) and numpy.abs(HAH_PREV_Open - HAH_PREV_Close) > numpy.abs(HAH_PREV_Open2 - HAH_PREV_Close2 ) and hah_direction_down0 and hah_direction_down1 and hah_direction_down2)
                hah_direction_down_smaller = (numpy.abs(HAH_Open - HAH_Close) < numpy.abs(HAH_PREV_Open - HAH_PREV_Close) and hah_direction_down0 and hah_direction_down1)
                hah_direction_down_smaller1 = (numpy.abs(HAH_PREV_Open - HAH_PREV_Close) < numpy.abs(HAH_PREV_Open2 - HAH_PREV_Close2) and hah_direction_down1 and hah_direction_down2)
                hah_direction_down_smallermax = (numpy.abs(HAH_Open - HAH_Close) < numpy.abs(HAH_PREV_Open - HAH_PREV_Close) and numpy.abs(HAH_PREV_Open - HAH_PREV_Close) < numpy.abs(HAH_PREV_Open2 - HAH_PREV_Close2) and hah_direction_down0 and hah_direction_down1 and hah_direction_down2)

                hah_direction_spin0 = (HAH_Open == HAH_Close)
                hah_direction_spin1 = (HAH_PREV_Open == HAH_PREV_Close)
                hah_direction_spin2 = (HAH_PREV_Open2 == HAH_PREV_Close2)

                hah_direction_up_short0 = ((HAH_High - HAH_Low) / (HAH_Close - HAH_Open) >= 2) and (HAH_Close - HAH_Open !=0)
                hah_direction_up_short1 = ((HAH_PREV_High - HAH_PREV_Low) / (HAH_PREV_Close - HAH_PREV_Open) >= 2) and (HAH_PREV_Close - HAH_PREV_Open !=0)
                hah_direction_up_short2 = ((HAH_PREV_High2 - HAH_PREV_Low2) / (HAH_PREV_Close2 - HAH_PREV_Open2) >= 2) and (HAH_PREV_Close2 - HAH_PREV_Open2 !=0)
                hah_direction_up_shorter0 = ((HAH_High - HAH_Low) / (HAH_Close - HAH_Open) >= 4) and (HAH_Close - HAH_Open !=0)
                hah_direction_up_shorter1 = ((HAH_PREV_High - HAH_PREV_Low) / (HAH_PREV_Close - HAH_PREV_Open) >= 4) and (HAH_PREV_Close - HAH_PREV_Open !=0)
                hah_direction_up_shorter2 = ((HAH_PREV_High2 - HAH_PREV_Low2) / (HAH_PREV_Close2 - HAH_PREV_Open2) >= 4) and (HAH_PREV_Close2 - HAH_PREV_Open2 !=0)
                hah_direction_up0 = (HAH_Close > HAH_Open)
                hah_direction_up1 = (HAH_PREV_Close > HAH_PREV_Open)
                hah_direction_up2 = (HAH_PREV_Close2 > HAH_PREV_Open2)
                hah_direction_up_long_0 = (HAH_Open == HAH_Low and HAH_Close > HAH_Open)
                hah_direction_up_long_1 = (HAH_PREV_Open == HAH_PREV_Low and HAH_PREV_Close > HAH_PREV_Open)
                hah_direction_up_long_2 = (HAH_PREV_Open2 == HAH_PREV_Low2 and HAH_PREV_Close2 > HAH_PREV_Open2)
                hah_direction_up_longer = (numpy.abs(HAH_Close - HAH_Open) > numpy.abs(HAH_PREV_Close - HAH_PREV_Open) and hah_direction_up0 and hah_direction_up1)
                hah_direction_up_longermax = (numpy.abs(HAH_Close - HAH_Open) > numpy.abs(HAH_PREV_Close - HAH_PREV_Open) and numpy.abs(HAH_PREV_Close - HAH_PREV_Open) > numpy.abs(HAH_PREV_Close2 - HAH_PREV_Open2) and hah_direction_up0 and hah_direction_up1 and hah_direction_up2)
                hah_direction_up_smaller = (numpy.abs(HAH_Close - HAH_Open) < numpy.abs(HAH_PREV_Close - HAH_PREV_Open) and hah_direction_up0 and hah_direction_up1)
                hah_direction_up_smaller1 = (numpy.abs(HAH_PREV_Close - HAH_PREV_Open) < numpy.abs(HAH_PREV_Close2 - HAH_PREV_Open2) and hah_direction_up1 and hah_direction_up2)
                hah_direction_up_smallermax = (numpy.abs(HAH_Close - HAH_Open) < numpy.abs(HAH_PREV_Close - HAH_PREV_Open) and numpy.abs(HAH_PREV_Close - HAH_PREV_Open) < numpy.abs(HAH_PREV_Close2 - HAH_PREV_Open2) and hah_direction_up0 and hah_direction_up1 and hah_direction_up2)



                if (((ha_direction_down_long_0 and ha_direction_down0) or (ha_direction_down_long_0 and ha_direction_down_long_1 and ha_direction_down0) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longer) or (ha_direction_down_long_0 or ha_direction_down_long_1 and ha_direction_down_longermax and ha_direction_down_longer) and ha_direction_down0) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down2)):
                    HA_trend = "DOWN"


                if (((ha_direction_up_long_0 and ha_direction_up0) or (ha_direction_up_long_0 and ha_direction_up_long_1 and ha_direction_up0) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer) or (ha_direction_up_long_0 or ha_direction_up_long_1 and ha_direction_up_longer and ha_direction_up_longermax) and ha_direction_up0) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up2)):
                    HA_trend = "UP"


                if ((ha_direction_up_short2 and ha_direction_spin1 and ha_direction_up0) or (ha_direction_down_short2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_down_short1 and ha_direction_spin0) or (ha_direction_down_long_2 and ha_direction_down_short1 and ha_direction_up_long_0) or (ha_direction_down_long_2 and ha_direction_up_short1 and ha_direction_up_long_0) or (ha_direction_down2 and ha_direction_up_long_0 and ha_direction_up1 and ha_direction_up_longer) or (ha_direction_down_long_2 and ha_direction_down_smaller1 and ha_direction_up0) or (ha_direction_down_long_2 and ha_direction_down_short1 and  ha_direction_up_long_0) or (ha_direction_down_longermax and ha_direction_up_short0) and ha_direction_down1 and ha_direction_down2) and ha_direction_down1 and ha_direction_down2:
                    HA_trend = "Revers-UP"


                if ((ha_direction_down_short2 and ha_direction_spin1 and ha_direction_down0) or (ha_direction_up_short2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_up_short1 and ha_direction_spin0) or (ha_direction_up_long_2 and ha_direction_up_short1 and ha_direction_down_long_0) or (ha_direction_up_long_2 and ha_direction_down_short1 and ha_direction_down_long_0) or (ha_direction_up2 and ha_direction_down_long_0 and ha_direction_down1 and ha_direction_down_longer) or (ha_direction_up_long_2 and ha_direction_up_smaller1 and ha_direction_down0) or (ha_direction_up_long_2 and ha_direction_up_short1 and  ha_direction_down_long_0) or (ha_direction_up_longermax and ha_direction_down_short0) and ha_direction_up1 and ha_direction_up2) and ha_direction_up1 and ha_direction_up2:
                    HA_trend = "Revers-DOWN"


                if  HA_trend != "Revers-DOWN" and   HA_trend != "Revers-UP" and  HA_trend != "DOWN" and HA_trend != "UP":
                    HA_trend = "STABLE"





                if (((hah_direction_down_long_0 and hah_direction_down0) or (hah_direction_down_long_0 and hah_direction_down_long_1 and hah_direction_down0) or (hah_direction_down_long_0 or hah_direction_down_long_1 and hah_direction_down_longer) or (hah_direction_down_long_0 or hah_direction_down_long_1 and hah_direction_down_longermax and hah_direction_down_longer) and hah_direction_down0) or (hah_direction_down0 and hah_direction_down1 and hah_direction_down2)):
                    HAH_trend = "DOWN"

                if (((hah_direction_up_long_0 and hah_direction_up0) or (hah_direction_up_long_0 and hah_direction_up_long_1 and hah_direction_up0) or (hah_direction_up_long_0 or hah_direction_up_long_1 and hah_direction_up_longer) or (hah_direction_up_long_0 or hah_direction_up_long_1 and hah_direction_up_longer and hah_direction_up_longermax) and hah_direction_up0) or (hah_direction_up0 and hah_direction_up1 and hah_direction_up2)):
                    HAH_trend = "UP"

                if ((hah_direction_up_short2 and hah_direction_spin1 and hah_direction_up0) or (hah_direction_down_short2 and hah_direction_up_short1 and hah_direction_up_long_0) or (hah_direction_down2 and hah_direction_down_short1 and hah_direction_spin0) or (hah_direction_down_long_2 and hah_direction_down_short1 and hah_direction_up_long_0) or (hah_direction_down_long_2 and hah_direction_up_short1 and hah_direction_up_long_0) or (hah_direction_down2 and hah_direction_up_long_0 and hah_direction_up1 and hah_direction_up_longer) or (hah_direction_down_long_2 and hah_direction_down_smaller1 and hah_direction_up0) or (hah_direction_down_long_2 and hah_direction_down_short1 and  hah_direction_up_long_0) or (hah_direction_down_longermax and hah_direction_up_short0) and hah_direction_down1 and hah_direction_down2):
                    HAH_trend = "Revers-UP"

                if ((hah_direction_down_short2 and hah_direction_spin1 and hah_direction_down0) or (hah_direction_up_short2 and hah_direction_down_short1 and hah_direction_down_long_0) or (hah_direction_up2 and hah_direction_up_short1 and hah_direction_spin0) or (hah_direction_up_long_2 and hah_direction_up_short1 and hah_direction_down_long_0) or (hah_direction_up_long_2 and hah_direction_down_short1 and hah_direction_down_long_0) or (hah_direction_up2 and hah_direction_down_long_0 and hah_direction_down1 and hah_direction_down_longer) or (hah_direction_up_long_2 and hah_direction_up_smaller1 and hah_direction_down0) or (hah_direction_up_long_2 and hah_direction_up_short1 and  hah_direction_down_long_0) or (hah_direction_up_longermax and hah_direction_down_short0) and hah_direction_up1 and hah_direction_up2):
                    HAH_trend = "Revers-DOWN"

                if  HAH_trend != "Revers-DOWN" and   HAH_trend != "Revers-UP" and  HAH_trend != "DOWN" and HAH_trend != "UP":
                    HAH_trend = "STABLE"

                print market, HA_trend, HAH_trend

                print "Generate HA signls for ", market
                if ((ha_direction_down0 and ha_direction_down1  and ha_direction_down_long_0) or (ha_direction_down0 and ha_direction_down1  and ha_direction_down_long_0 and ha_direction_down_long_1) or (ha_direction_down0 and ha_direction_down1 and ha_direction_down_longer)) and bought_quantity_sql > 0 and HAD_trend!='UP' and (hah_direction_down_long_0 or hah_direction_down0):

                    try:
                        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      '+ market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 1 where active=1 and market =("%s")' % market)
                        #if bought_quantity_sql>0:
                        #    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()

                lastcandlesize= fivehourcurrenthigh-fivehourcurrentlow
                prevcandlesize= fivehourprevhigh-fivehourprevlow
                lastcandlebodysize = numpy.abs(fivehourcurrentopen - last)
                prevcandlebodysize = numpy.abs(fivehourprevopen - fivehourprevclose)

                if ((lastcandlesize>prevcandlesize or lastcandlebodysize>prevcandlebodysize) and fivehourcurrentopen>last and fivehourprevopen<fivehourprevclose and HAH_trend!="UP" and bought_quantity_sql > 0):
                    try:
                        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      ' + market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 2 where active=1 and market =("%s")' % market)
                        # if bought_quantity_sql>0:
                        #    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()



                if ((ha_direction_up0 and ha_direction_up1 and ha_direction_up_long_0) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up_long_0 and ha_direction_up_long_1) or (ha_direction_up0 and ha_direction_up1 and ha_direction_up_longer) and bought_quantity_sql > 0):

                    try:
                        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                        printed = ('      '+ market + '   Received HA sell signal  ' + '  ' + HA_trend)
                        cursor.execute('update orders set sell = 0 where active=1 and market =("%s")' % market)
                        #if bought_quantity_sql>0:
                        #    cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()


#                print market, last, HA_trend, HAH_trend



                if currtime-ha_old_time>7200:
                    try:
                        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()

                        printed = ('      '+ market + '   The HA_hour is  ' + HA_trend + '  and HAH is ' + HAH_trend)
                        cursor.execute("update markets set current_price = %s, ha_direction =%s,  ha_direction_hour=%s  where market = %s and active =1",(last, HA_trend,  HAH_trend, market))
                        if status_orders(market, 4) == 1:
                            cursor.execute('insert into orderlogs(market, signals, time) values("%s", "%s", "%s")' % (market, str(currenttime)+' HA: ' + str(HA_trend) + ' HAH: ' + str(HAH_trend), currtime))
                        else:
                            pass
                        #cursor.execute('insert into ha_logs (date, market, HA_hour, log ) values ("%s", "%s", "%s", "%s")' % (currenttime, market, HA_trend, printed))
                        #cursor.execute('insert into logs(date, log_entry) values("%s", "%s")' % (currenttime, printed))
                        db.commit()
                    except MySQLdb.Error, e:
                        print "Error %d: %s" % (e.args[0], e.args[1])
                        sys.exit(1)
                    finally:
                        db.close()





                lastcandlesize = (hourcurrenthigh-hourcurrentlow)*1000
                previouscandlesize = (hourprevhigh-hourprevlow)*1000
                previouscandlesize2 = (hourprevhigh2-hourprevlow2)*1000
                previouscandlesize3 = (hourprevhigh3-hourprevlow3)*1000
                previouscandlesize4 = (hourprevhigh4-hourprevlow4)*1000
                previouscandlesize5 = (hourprevhigh5-hourprevlow5)*1000
                previouscandlesize6 = (hourprevhigh6- hourprevlow6)*1000

                averagecandlesize=(previouscandlesize6+previouscandlesize5+previouscandlesize4)/3
                #print market, averagecandlesize, lastcandlesize, previouscandlesize, previouscandlesize2, previouscandlesize3


                if (lastcandlesize/averagecandlesize>3 and last*1000>hourcurrentopen) or (previouscandlesize2/averagecandlesize>3 and hourprevclose*1000>hourprevopen*1000) or (previouscandlesize3/averagecandlesize>3 and hourprevclose2*1000>hourprevopen2*1000) and last*1000> hourprevhigh6*1000:
                    print market, "We have peak situation, lets wait"
                    printed1=("We have peak situation, lets wait")



                    try:
                        db = MySQLdb.connect("mysqldb", "cryptouser", "123456", "cryptodb")
                        cursor = db.cursor()
                       #cursor.execute("update markets set strike_date=%s, strike_info=%s  where market = %s",(currenttime, printed1, market))
                        cursor.execute(
                            "update markets set strike_date=%s, strike_time2=%s, strike_info=%s  where market = %s",
                            (currenttime, currtime, printed1, market))
                        if status_orders(market, 4) == 1:
                            cursor.execute(
                                'insert into orderlogs(market, signals, time) values("%s", "%s", "%s")' % (
                                market, printed1, currtime))
                        else:
                            pass
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
    cursor.execute("SELECT * FROM markets WHERE active =1 and market = '%s'" % market)
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
    cursor.execute("SELECT * FROM markets WHERE market = '%s'" % market)
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
    r = cursor.fetchall()
    for row in r:
        if row[1] == marketname:
            return row[value]

    return 0




def format_float(f):
    return "%.7f" % f


if __name__ == "__main__":
    main()
