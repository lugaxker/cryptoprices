#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
#
# Cryptoprices : gestion d'investissement en cryptojetons
# (C) 2018 Ludovic Lars

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
with open("assets.dat", "r") as f:
    assetdata = f.read()
    assetdata = assetdata.split('\n')
    for i, a in enumerate(assetdata):
        assetdata[i] = a.split(" ")
        
# Récupération des données du marché        
import urllib.request as urll
import json
listingurl = "https://api.coinmarketcap.com/v2/listings/"
with urll.urlopen(listingurl, timeout=10) as u:
    listing = json.loads(u.read().decode())

for i, asset in enumerate(assetdata):
    for token in listing["data"]:
        if token["website_slug"] == asset[0]:
            assetdata[i][0] = token["id"]

# Récupération des données concernant les jetons
tokendata = []
for asset in assetdata:
    tokenurl = "https://api.coinmarketcap.com/v2/ticker/{:d}/?convert=EUR".format( asset[0] )
    with urll.urlopen(tokenurl, timeout=10) as u:
        t = json.loads(u.read().decode())
    token = {"symbol": t["data"]["symbol"], "rank": int(t["data"]["rank"]), 
             "price_usd": float(t["data"]["quotes"]["USD"]["price"]), 
             "percent_change_24h_usd": float(t["data"]["quotes"]["USD"]["percent_change_24h"]), 
             "price_eur": float(t["data"]["quotes"]["EUR"]["price"]),
             "quantity": float( asset[1] ), "investment_eur": float( asset[2] )}
    if asset[0] in [1027, 1808, 1765]: # ethereum tokens
        token["decimals"] = 9 # for now (max: 18)
    elif asset[0] in [1230, 1312]: # steem
        token["decimals"] = 3
    elif asset[0] == 1720: # iota
        token["decimals"] = 6
    elif asset[0] == 1376: # neo
        token["decimals"] = 0
    elif asset[0] == 512: # lumen
        token["decimals"] = 7
    elif asset[0] in [328, 2632, 2655]: # monero
        token["decimals"] = 8 # for now (max: 12)
    else:
        token["decimals"] = 8
    tokendata.append( token )

# Récupération des données globales    
with urll.urlopen("https://api.coinmarketcap.com/v2/global/") as u:
    gl = json.loads(u.read().decode())
glmarketcap = int( gl["data"]["quotes"]["USD"]["total_market_cap"] )
gmc = '{:,}'.format(glmarketcap).replace(',',' ')
btcdominance = float( gl["data"]["bitcoin_percentage_of_market_cap"] )

# Tri par rang
tokendata.sort(key = lambda t: t["rank"])

# Affichage de la capitalisation boursière et du pourcentage de dominance de Bitcoin (BTC)
print('Capitalisation boursière totale des cryptojetons' + '  {} USD\t\t\t\tDominance de BTC : {} %'.format(gmc,btcdominance))
print()

# Affichage des prix et des gains/pertes
print(colorize('Jeton\t\tRang\t\tPrix (USD)\tPrix (EUR)\t24h-chg (%)\tQuantité\tValeur (EUR)\tApport (EUR)\tGain/perte (%)','yellow'))
totalvalue = 0
totalinvestment = 0
rank101andabove = False
for token in tokendata:
    symb = token["symbol"]
    rank = token["rank"]
    prd = token["price_usd"]
    pre = token["price_eur"]
    perchange = token["percent_change_24h_usd"]
    quantity = token["quantity"]
    fiat_investment = token["investment_eur"] 
    value = quantity * pre
    totalvalue += value
    totalinvestment += fiat_investment
    if fiat_investment != 0:
        profit = 100*(value - fiat_investment)/fiat_investment
    else:
        profit = 0
    
    if not rank101andabove:
        if rank >= 100:
            print(colorize("------", "yellow", True))
            rank101andabove = True
            
    row = colorize("{}".format(symb), "yellow", True)
    row += "\t\t{:d}\t\t{:9.3f}\t{:9.3f}\t{:+.2f}\t\t".format(rank, prd, pre, perchange)
    row += "{:.{prec}f}\t". format(quantity, prec=str(token["decimals"]))
    if token["decimals"] <= 3:
        row += "\t"
    row += "{:=8.2f}\t{:=8.2f}\t\t{:+.2f}".format(value, fiat_investment, profit)
    print(row)

totalprofit = 100*(totalvalue - totalinvestment)/totalinvestment
print(colorize('\t\t\t\t\t\t\t\t\t\tTOTAL\t\t{:8.2f}\t{:8.2f}\t\t{:+.2f}'.format(totalvalue,totalinvestment,totalprofit), 'red', True))
print()

# Affichage de la source (coinmarketcap.com)
print('Source : coinmarketcap.com')