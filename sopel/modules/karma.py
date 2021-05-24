# -*- coding: utf-8 -*-
import sopel
import json
import os
import re
import shutil
import time

homedir = "config"

karmare = re.compile(r"^([a-zA-Z0-9\[\]\{\}\\\|\-\_\`^]*)(:?,? ?)?(\+\+|\-\-)")
    
try:
    from config.karma import karmas
except:
    karmas = {}
    
try:
    karmafilev = open(homedir + "/karma.py", "w")
    try:
        karmafilev.truncate()
    except:
        pass
    karmafilev.write("karmas = " + str(dict(karmas)))
    karmafilev.close()
except:
    pass
try:
    karmafilew = open(homedir + "/karma.py", "w")
except:
    raise Exception("I can't load karma file!")

@sopel.module.commands('karma')
def karma(bot, trigger):
    if trigger.group(2):
        user = trigger.group(2).lower().replace(" ", "")
    else:
        user = trigger.nick.lower()
    if trigger.group(2):
        oriuser = trigger.group(2)
    else:
        oriuser = trigger.nick
    try: 
        karmas[user]
    except:
        if bot.config.lang == 'fr':
            return bot.reply(oriuser + " Il n'a pas reçu n'aucun karma!")
        elif bot.config.lang == 'es':
            return bot.reply(oriuser + u" no ha recibido ningún karma!")
        else:
            return bot.reply(oriuser + " never have been karmed!")
    if bot.config.lang == 'fr':
        bot.reply(oriuser + u" a de " + str(karmas[user]) + " points de karma.")
    elif bot.config.lang == 'es':
        bot.reply(oriuser + u" tiene " + str(karmas[user]) + " puntos de karma.")
    else:
        bot.reply(oriuser + u" has " + str(karmas[user]) + " points of karma.")
       
@sopel.module.rule(r".*")
def karmaman(bot, trigger):
    k = karmare.match(trigger.group(0))
    if k != None:
        if k.group(1).lower() == trigger.nick.lower():
            if bot.config.lang == 'fr':
                return bot.notice(trigger.nick, "Tu ne te peux pas donner karma à toi-même.")
            elif bot.config.lang == 'es':
                return bot.notice(trigger.nick, "No puedes darte karma a ti mismo.")
            else:
                return bot.notice(trigger.nick, "You can't karma yourself.")

        try:
            karmas[k.group(1).lower()]
        except:
            karmas[k.group(1).lower()] = 0
        if k.group(3) == "++":
            karmas[k.group(1).lower()] += 1
            if bot.config.lang == 'fr':
                bot.notice(trigger.nick, "T'as donné un point de karma à " + k.group(1) + ".")
            elif bot.config.lang == 'es':
                bot.notice(trigger.nick, "Has dado un punto de karma a " + k.group(1) + ".")
            else:
                bot.notice(trigger.nick, "You have karmed up " + k.group(1) + ".")
        else:
            karmas[k.group(1).lower()] -= 1
            if bot.config.lang == 'fr':
                bot.notice(trigger.nick, "T'as déjà quitté un point de karma à " + k.group(1) + ".")
            elif bot.config.lang == 'es':
                bot.notice(trigger.nick, "Has quitado un punto de karma a " + k.group(1) + ".")
            else:
                bot.notice(trigger.nick, "You have karmed down " + k.group(1) + ".")
        try:
            karmafilew.truncate()
        except:
            pass
        karmafilew.write("karmas = " + str(dict(karmas)))
