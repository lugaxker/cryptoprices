#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
#
# Cryptoprices : gestion d'investissement en cryptojetons
# (C) 2018 lugaxker

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

print()
print('--- JETONS CRYPTOGRAPHIQUES ---')
print()

# Affichage de l'horodatage
import datetime
utc = datetime.datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S")
print('Date' + '  {} UTC'.format(utc))

# Lecture du fichier des cryptojetons
assetsfile = open("assets.dat", "r")
assetdata = assetsfile.read()
assetdata = assetdata.split('\n')
for i in range( len(assetdata) ):
    assetdata[i] = assetdata[i].split(" ")
assetsfile.close()

# Récupération des données du marché
import urllib.request as urll
marketurl = 'https://api.coinmarketcap.com/v1/ticker/?convert=EUR&limit=0'
marketfilename = 'coinmarketcap_eur.json'
urll.urlretrieve(marketurl, marketfilename)

import json
f = open(marketfilename)
marketdata = json.load(f)
f.close()

with urll.urlopen("https://api.coinmarketcap.com/v1/global/") as u:
    globaldata = json.loads(u.read().decode())

# Affichage de la capitalisation boursière et du pourcentage de dominance de Bitcoin (BTC)
glmarketcap = int( globaldata["total_market_cap_usd"] )
gmc = '{:,}'.format(glmarketcap).replace(',',' ')
btcdominance = float( globaldata["bitcoin_percentage_of_market_cap"] )

print('Capitalisation boursière totale des cryptojetons' + '  {} USD\t\t\t\tDominance de BTC : {} %'.format(gmc,btcdominance))
print()

# Affichage des prix et des gains/pertes
print(colorize('Jeton\t\tRang\t\tPrix (USD)\tPrix (EUR)\tPrix (BTC)\t24h-chg (%)\tQuantité\tValeur (EUR)\tApport (EUR)\tGain/perte (%)','yellow'))
totalvalue = 0.
totalinvestment = 0.

for asset in assetdata:
    assetid = asset[0]
    for token in marketdata:
        
        if ( token["id"] == assetid ):
            symb = token["symbol"]
            rank = token["rank"]
            #mcap = float( token["market_cap_usd"] ) / 1e9
            prd = token["price_usd"]
            pre = token["price_eur"]
            pbtc = float(token["price_btc"])
            perchange = float(token["percent_change_24h"])
            quantity = float( asset[1] )
            fiat_investment = float( asset[2] )
            value = quantity*float(pre)
            totalvalue += value
            totalinvestment += fiat_investment
            if fiat_investment != 0:
                profit = 100*(value - fiat_investment)/fiat_investment
            else:
                profit = 0.
            
            row = colorize("{}".format(symb), "yellow", True)
            row += "\t\t{}\t\t{:.7}\t\t{:.7}\t\t{:9.8f}\t{:+.2f}\t\t".format(rank, prd, pre, pbtc, perchange)
            if assetid in ["ethereum", "omisego"]:
                row += "{:.9f}\t".format(quantity)
            elif assetid == "iota":
                row += "{:.6f}\t".format(quantity)
            elif assetid == "neo":
                row += "{:.0f}\t\t".format(quantity)
            else:
                row += "{:.8f}\t".format(quantity)
            row += "{:=6.2f}\t\t{:=6.2f}\t\t{:+.2f}".format(value, fiat_investment, profit)
            print(row)
            
            break

totalprofit = 100*(totalvalue - totalinvestment)/totalinvestment
print(colorize('\t\t\t\t\t\t\t\t\t\t\t\tTOTAL\t\t{:.2f}\t\t{:.2f}\t\t{:+.2f}'.format(totalvalue,totalinvestment,totalprofit), 'red', True))
print()

# Affichage de la source (coinmarketcap.com)
print('Source : coinmarketcap.com')