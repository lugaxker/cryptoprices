#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
#
# Par lugaxker

# -----------------------------------------------------------------------------
# Fonction colorize
# Exemple : print(colorize('warning', 'red', True) + ' message')

import os
 
colors = {'grey': 30, 'red': 31, 'green': 32, 'yellow': 33,
          'blue': 34, 'magenta': 35, 'cyan': 36, 'white': 37}

def colorize(s, color, bold=False):
    if os.getenv('ANSI_COLORS_DISABLED') is None and color in colors:
        if bold:
            return '\033[1m\033[%dm%s\033[0m' % (colors[color], s)
        else:
            return '\033[%dm%s\033[0m' % (colors[color], s)
    else:
        return s
    
# -----------------------------------------------------------------------------
# Début du script

print('')
print('--- JETONS CRYPTOGRAPHIQUES ---')


# Affichage de l'horodatage
import datetime
utc = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S UTC")
print('')
print('Date' + '  {}'.format(utc))

# Lecture du fichier des cryptojetons
currencies_id = []
currencies_q = []
currencies_fiat = []

assetsfile = open("cryptotokens.dat", "r")

assetdata = assetsfile.read()
assetdata = assetdata.split('\n')
for s in assetdata:
    s = s.split(' ')
    currencies_id += [ s[0] ]
    currencies_q += [float(s[1])]
    currencies_fiat += [float(s[2])]
    
assetsfile.close()

# Récupération des données du marché
import urllib.request as urll
marketurl = 'https://api.coinmarketcap.com/v1/ticker/?convert=EUR&limit=150'
marketfilename = 'coinmarketcap_150_eur.json'
urll.urlretrieve(marketurl, marketfilename)

import json
f = open(marketfilename)
marketdata = json.load(f)
f.close()
 
with urll.urlopen("https://api.coinmarketcap.com/v1/global/") as u:
    globaldata = json.loads(u.read().decode())

glmarketcap = int( globaldata["total_market_cap_usd"] )
gmc = '{:,}'.format(glmarketcap).replace(',',' ')
btcdominance = float( globaldata["bitcoin_percentage_of_market_cap"] )

# Affichage de la capitalisation boursière et du pourcentage de dominance de Bitcoin (BTC)
print('Capitalisation boursière totale des cryptojetons' + '  {} USD\t\t\t\tDominance de BTC : {} %'.format(gmc,btcdominance))

# Affichage des prix et des gains/pertes
ncurrencies = len(currencies_id)
print('')
print(colorize('Monnaie\t\tRang\t\tPrix (USD)\tPrix (EUR)\tPrix (BTC)\t24h-chg (%)\tQuantité\tValeur (EUR)\tApport (EUR)\tGain/perte (%)','yellow'))
totalvalue = 0.
totalinvestment = 0.

for n in range(ncurrencies):
    for i in range(0,150):
        if ( marketdata[i]["id"] == currencies_id[n] ):
            symb = marketdata[i]["symbol"]
            rank = marketdata[i]["rank"]
            #mcap = float( marketdata[i]["market_cap_usd"] ) / 1e9
            prd = marketdata[i]["price_usd"]
            pre = marketdata[i]["price_eur"]
            pbtc = float(marketdata[i]["price_btc"])
            perchange = float(marketdata[i]["percent_change_24h"])
            quantity = currencies_q[n]
            fiat_investment = currencies_fiat[n]
            value = quantity*float(pre)
            totalvalue += value
            totalinvestment += fiat_investment
            if fiat_investment != 0:
                profit = 100*(value - fiat_investment)/fiat_investment
            else:
                profit = 0.
            print(colorize('{}'.format(symb), 'yellow', True) + 
                  '\t\t{}\t\t{:.7}\t\t{:.7}\t\t{:9.8f}\t{:+.2f}\t\t{:.8f}\t{:=6.2f}\t\t{:=6.2f}\t\t{:+.2f}'.format(rank, prd, pre, pbtc, perchange, quantity, value, fiat_investment, profit))
            break

totalprofit = 100*(totalvalue - totalinvestment)/totalinvestment
print(colorize('\t\t\t\t\t\t\t\t\t\t\t\tTOTAL\t\t{:.2f}\t\t{:.2f}\t\t{:+.2f}'.format(totalvalue,totalinvestment,totalprofit), 'red', True))


# Affichage de la source (coinmarketcap.com)
print('')
print('Source : coinmarketcap.com')