# -*- coding: utf8 -*-

import sopel
import time


@sopel.module.commands('annonce', 'announce', 'anuncio', 'anuncia', 'anunciar')
def announce(bot, trigger):
    if not trigger.owner:
        if bot.config.lang == 'fr':
            bot.reply(u'Tu n\'est pas mon propriétaire.')
        elif bot.config.lang == 'es':
            bot.reply(u"No eres mi owner.")
        else:
            bot.reply(u"You are not my owner.")
        return
    channels = bot.config.channels.split(',')
    for channel in channels:
        if bot.config.lang == 'fr':
            bot.msg(channel, '[ANNONCE GLOBAL] %s' % trigger.group(2))
        elif bot.config.lang == 'es':
            bot.msg(channel, '[ANUNCIO GLOBAL] %s' % trigger.group(2))
        else:
            bot.msg(channel, '[GLOBAL ANNOUNCE] %s' % trigger.group(2))
