# -*- coding: cp1252 -*-
import sopel
import random
import time

@sopel.module.commands('moneda', 'coin', 'monnaie')
def moneda(bot, trigger):
    if bot.config.lang == 'fr':
    	moneda = ['face', 'cachet']
    elif bot.config.lang == 'es':
    	moneda = ['cara', 'sello']
    else:
    	moneda = ["heads", "tails"]
    if bot.config.lang == 'fr':
          bot.say('\x01ACTION lance une monnaie et donne... \x02%s\x02!\x01' % random.choice(moneda))
    elif bot.config.lang == 'es':
    	bot.say('\x01ACTION tira una moneda y sale... \x02%s\x02!\x01' % random.choice(moneda))
    else:
    	bot.say('\x01ACTION tosses a coin into the air that lands on... \x02%s\x02!\x01' % random.choice(moneda))
