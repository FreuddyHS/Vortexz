# -*- coding: cp1252 -*-

from sopel import web, tools
from sopel.module import commands, example
from HTMLParser import HTMLParser

@commands('drae')
def drae(bot, trigger):
    if trigger.group(2):
        bot.reply('http://lema.rae.es/drae/?val=%s' % (trigger.group(2)))
    if trigger.group(2) == None:
        if bot.config.lang == 'fr':
            bot.reply(u"Dites-moi ce que tu veux rechercher!")
        elif bot.config.lang == 'es':
            bot.reply(u"¡dime que quieres buscar!")
        else:
            bot.reply(u"But tell me what I have to search!")
        return

@commands('wordreference', 'define')
def wordreference(bot, trigger):
    if trigger.group(2):
        bot.reply('http://www.wordreference.com/definition/%s' % (trigger.group(2)))
    if trigger.group(2) == None:
        if bot.config.lang == 'fr':
            bot.reply(u"Dites-moi ce que tu veux rechercher!")
        elif bot.config.lang == 'es':
            bot.reply(u"¡dime que quieres buscar!")
        else:
            bot.reply(u"But tell me what I have to search!")
        return
