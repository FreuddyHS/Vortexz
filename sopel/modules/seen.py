# coding=utf8

from __future__ import unicode_literals

import datetime
import json
import time
from sopel.tools import Ddict, get_timezone, format_time
from sopel.module import commands, rule, priority, unblockable

seen_dict = "seen_dict.json"

@commands('seen')
def seen(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'fr':
            bot.say(u"J'ai vu par derniere fois a \x02%s\x02 quand meme a \x02%s\x02, disant \x1D%s\x0F" % (trigger.nick, trigger.sender, trigger.group(0)))
        elif bot.config.lang == 'es':
			bot.say(u"He visto por ultima vez a \x02%s\x02 ahora mismo en \x02%s\x02, diciendo \x1D%s\x0F" % (trigger.nick, trigger.sender, trigger.group(0)))
        else:
            bot.say(u"The last time I saw \x02%s\x02 was right now on \x02%s\x02, saying \x1D%s\x0F" % (trigger.nick, trigger.sender, trigger.group(0)))
        return
	name = str(trigger.group(2))
	if ' ' in name:
		name = name.split()[0]
	with open(seen_dict, "r") as f:
		data = json.load(f)
    if name in data:
        timestamp = seen_dict[nick]['timestamp']
        channel = seen_dict[nick]['channel']
        message = seen_dict[nick]['message']

        tz = get_timezone(bot.db, bot.config, None, trigger.nick,
                          trigger.sender)
        saw = datetime.datetime.utcfromtimestamp(timestamp)
        timestamp = format_time(bot.db, bot.config, tz, trigger.nick,
                                trigger.sender, saw)
        if bot.config.lang == 'fr':
            msg = u"J'ai vu a \x02%s\x02 par derniere fois le jour \x02%s\x02 dans le canal \x02%s\x02, disant: \x1D%s\x0F" % (name, timestamp, channel, message)
        elif bot.config.lang == 'es':
            msg = u"He visto a \x02%s\x02 por ultima vez el dia \x02%s\x02 en el canal \x02%s\x02, diciendo: \x1D%s\x0F" % (name, timestamp, channel, message)
        else:                                
            msg = u"The last time I saw \x02%s\x02 was at \x02%s\x02 in the channel \x02%s\x02, saying \x1D%s\x0F" % (name, timestamp, channel, message)
        bot.say(str(trigger.nick) + ': ' + msg)
    else:
        if bot.config.lang == 'fr':
            bot.say(u"Je ne me souviens pas avoir vu a \x02%s\x02." % name)
        elif bot.config.lang == 'es':
            bot.say(u"No recuerdo haber visto a \x02%s\x02." % name)
        else:
            bot.say("Sorry, I haven't seen \x02%s\x02 around." % name)


@rule('(.*)')
@priority('low')
@unblockable # Also tracks ignored users
def note(bot, trigger):
    if trigger.sender.startswith("#"): # Only sees users that speak on public channels
        name = trigger.nick
        try:
            with open(seen_dict, "r+") as f:
                data = json.load(f)
                data[name] = {}
                data[name]['timestamp'] = time.time()
                data[name]['channel'] = trigger.sender
                data[name]['message'] = trigger
                f.seek(0)  # rewind
                f.write(json.dumps(data))
                f.truncate()                    
        except IOError:
            with open(seen_dict, "w+") as f:
                emptydict = {}
                f.seek(0)
                f.write(json.dumps(emptydict))
                f.truncate()        
        except ValueError:
            with open(seen_dict, "w+") as f:
                emptydict = {}
                f.seek(0)
                f.write(json.dumps(emptydict))
                f.truncate()        
