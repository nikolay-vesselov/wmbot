from __future__ import print_function
import asyncio
import sys
from binance import AsyncClient, BinanceSocketManager, ThreadedWebsocketManager
from binance.enums import *
from binance.client import Client
import time


async def main():
    

    bm = BinanceSocketManager(client)

    pair1 = 0
    pair2 = 0
    pair3 = 0
    pair4 = 0
    pair5 = 0
    pair6 = 0

    coin1 = 'BTC'
    coin2 = 'ETH'
    coin3 = sys.argv[1]
    stable = 'USDT'
    uchet_sum = float(1000)
    sum_per = float(sys.argv[2])

    print(f" Parameters: {sys.argv[1]} - {sys.argv[2]}")

    pairtext1 = coin1 + stable  # BTCUSDT
    pairtext2 = coin2 + stable  # ETHUSDT
    pairtext3 = coin2 + coin1  # ETHBTC
    pairtext4 = coin3 + coin2  # SOLETH
    pairtext5 = coin3 + coin1  # SOLBTC
    pairtext6 = coin3 + stable  # SOLUSDT

    print(f'  USDT-BTC-ETH-USDT      |     BTC-ETH-{coin3}-BTC      |     USDT-BTC-{coin3}-USDT      |     USDT-{coin3}-BTC-USDT      |     ETH-{coin3}-BTC-ETH   ')

    ms = bm.multiplex_socket([pairtext1.lower()+'@aggTrade', pairtext2.lower()+'@aggTrade', pairtext3.lower()+'@aggTrade', pairtext4.lower()+'@aggTrade', pairtext5.lower()+'@aggTrade', pairtext6.lower()+'@aggTrade'])

    async with ms as tscm:
        while True:
            res = await tscm.recv()
            #print(res)
            #print('.', end=' ')



            if res['data']['s'] == pairtext1:                   #BTCUSDT
                pair1 = float(res['data']['p'])
            elif res['data']['s'] == pairtext2:             #ETHUSDT
                pair2 = float(res['data']['p'])
            elif res['data']['s'] == pairtext3:              #ETHBTC
                pair3 = float(res['data']['p'])
            elif res['data']['s'] == pairtext4:              #SOLETH
                pair4 = float(res['data']['p'])
            elif res['data']['s'] == pairtext5:              #SOLBTC
                pair5 = float(res['data']['p'])
            elif res['data']['s'] == pairtext6:             #SOLUSDT
                pair6 = float(res['data']['p'])

            #pair1 != 0 and pair2 != 0 and pair3 != 0 and pair4 != 0 and pair5 != 0 and pair6 != 0:

            if pair1 != 0 and pair2 != 0 and pair3 != 0 and pair4 != 0 and pair5 != 0 and pair6 != 0:
                #print(pairtext1, f': {pair1}      |  ',pairtext2, f': {pair2}      |  ', pairtext3, f': {pair3}      |  ', pairtext4, f': {pair4}      |  ', pairtext5, f': {pair5}      |  ', pairtext6, f': {pair6}  |  ')
                #it1 = ((pair2 / (pair1 * pair3)) - 1) * 100
                it1 = (((((1000 / pair1) / pair3) * pair2) / 1000) - 1) * 100
                #it2 = ((pair5 / (pair3 * pair4)) - 1) * 100
                it2 = (((((0.1 / pair3) / pair4) * pair5) / 0.1) - 1) * 100
                #it3 = ((pair6 / (pair1 * pair5)) - 1) * 100
                it3 = (((((1000 / pair1) / pair5) * pair6) / 1000) - 1) * 100
                #it4 = ((pair1 / (pair6 * pair5)) - 1) * 100
                it4 = (((((1000 / pair6) * pair5) * pair1) / 1000) - 1) * 100
                it5 = (((((1 / pair4) * pair5) / pair3) / 1) - 1) * 100
                #it5 = ((pair3 / (pair4 * pair5)) - 1) * 100
                #it1 = (((uchet_sum / pair1) / pair3) / pair4) * pair6
                #it2 = ((uchet_sum / pair6) * pair5) * pair1
                #it3 = (((uchet_sum / pair6) * pair4) * pair3) * pair1
                #it4 = ((uchet_sum / pair2) * pair3) * pair1
                #it5 = (((uchet_sum / pair2) * pair3) / pair5) * pair6
                if it1 > sum_per or it2 > sum_per or it3 > sum_per or it4 > sum_per or it5 > sum_per:
                    print(f'{it1}  |   {it2}  |   {it3}  |   {it4}  |   {it5}')
                    if it2 > sum_per: #BTC-ETH-{coin3}-BTC
                        summ1 = round(0.01 / pair3, 4)
                        res1 = client2.order_market_buy(symbol='ETHBTC', quantity=summ1)
                        time.sleep(0.2)
                        summeth = float(res1['executedQty'])
                        symbol2 = coin3+'ETH'
                        summ2 = round(summeth / pair4, 0)
                        res2 = client2.order_market_buy(symbol=symbol2, quantity=summ2)
                        time.sleep(0.2)
                        summcoin = round(float(res2['executedQty']), 0)
                        symbol3 = coin3+'BTC'
                        res3 = client2.order_market_sell(symbol=symbol3, quantity=summcoin)
                        time.sleep(0.2)
                        summbtc = res3['cummulativeQuoteQty']
                        print('==================================================================================')
                        print(f'SELL 0.01 BTC -> BUY {summeth} ETH -> BUY {summcoin} {coin3} -> BUY {summbtc} BTC')
                        print('==================================================================================')
                        if float(summbtc) < 0.01000750:
                            exit()

                    if it3 > sum_per: #USDT-BTC-{coin3}-USDT
                        summ1 = round(250 / pair1, 6)
                        res1 = client2.order_market_buy(symbol='BTCUSDT', quantity=summ1)
                        time.sleep(0.2)
                        summbtc = float(res1['executedQty'])
                        symbol2 = coin3+'BTC'
                        summ2 = round(summbtc / pair5, 0)
                        res2 = client2.order_market_buy(symbol=symbol2, quantity=summ2)
                        time.sleep(0.2)
                        summcoin = round(float(res2['executedQty']), 0)
                        symbol3 = coin3+'USDT'
                        res3 = client2.order_market_sell(symbol=symbol3, quantity=summcoin)
                        time.sleep(0.2)
                        summusdt = res3['cummulativeQuoteQty']
                        print('==================================================================================')
                        print(f'SELL 250 USDT -> BUY {summbtc} BTC -> BUY {summcoin} {coin3} -> BUY {summusdt} USDT')
                        print('==================================================================================')
                        if float(summusdt) < 250.19:
                            exit()

                    if it4 > sum_per: #USDT-{coin3}-BTC-USDT
                        summ1 = round(250 / pair6, 0)
                        symbol1 = coin3+'USDT'
                        res1 = client2.order_market_buy(symbol=symbol1, quantity=summ1)
                        time.sleep(0.2)
                        summcoin = float(res1['executedQty'])
                        symbol2 = coin3+'BTC'
                        #summ2 = round(summcoin * pair5, 0)
                        res2 = client2.order_market_sell(symbol=symbol2, quantity=summcoin)
                        time.sleep(0.2)
                        summbtc = round(float(res2['cummulativeQuoteQty']), 6)
                        symbol3 = 'BTCUSDT'
                        res3 = client2.order_market_sell(symbol=symbol3, quantity=summbtc)
                        time.sleep(0.2)
                        summusdt = res3['cummulativeQuoteQty']
                        print('==================================================================================')
                        print(f'SELL 250 USDT -> BUY {summ1} {coin3} -> BUY {summbtc} BTC -> BUY {summusdt} USDT')
                        print('==================================================================================')
                        if float(summusdt) < 250.19:
                            exit()

                    if it5 > sum_per: #ETH-{coin3}-BTC-ETH
                        summ1 = round(0.17 / pair4, 0)
                        symbol1 = coin3+'ETH'
                        res1 = client2.order_market_buy(symbol=symbol1, quantity=summ1)
                        time.sleep(0.2)
                        summcoin = float(res1['executedQty'])
                        symbol2 = coin3+'BTC'
                        #summ2 = round(summcoin * pair5, 0)
                        res2 = client2.order_market_sell(symbol=symbol2, quantity=summcoin)
                        time.sleep(0.2)
                        summbtc = round(float(res2['cummulativeQuoteQty']), 6)
                        symbol3 = 'ETHBTC'
                        summ2 = summbtc*pair3
                        res3 = client2.order_market_buy(symbol=symbol3, quantity=summ2)
                        time.sleep(0.2)
                        summ3 = res3['executedQty']
                        print('==================================================================================')
                        print(f'SELL 0.17 ETH -> BUY {summ1} {coin3} -> BUY {summbtc} BTC -> BUY {summ3} ETH')
                        print('==================================================================================')
                        if float(summusdt) < 0.17013:
                            exit()

    await client.close_connection()



if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
