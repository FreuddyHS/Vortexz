# coding=utf-8

from sopel.module import commands, example, rule, priority
import platform, sys, time
import sopel
import sopel.config as config
import json

@commands('privs')
def privileges(bot, trigger):
    if trigger.group(2):
        try:
            bot.say(str(bot.privileges[trigger.group(2)]))
        except Exception:
            if bot.config.lang == 'fr':
                bot.reply("Canal inconnu.")
            elif bot.config.lang == 'es':
                bot.reply("Canal desconocido.")
            else:
                bot.reply("Channel not found.")
    else:
        bot.say(str(bot.privileges))
	
@commands('owner')
def owner(bot, trigger):
    if bot.config.lang == 'fr':
        say = "Mon propriétaire est \x02" + bot.config.core.owner + "\x02."
    elif bot.config.lang == 'es':
        say = "Mi propietario es \x02" + bot.config.core.owner + "\x02."
    else:
        say = "My owner is \x02" + bot.config.core.owner + "\x02."
    bot.say(say)
    return
	
@commands('admins')
def admins(bot, trigger):
    admins = bot.config.core.get_list('admins')
    if len(admins) == 0:
        if bot.config.lang == 'fr':
            bot.say("\x02Je n'ai pas d'administrateurs.\x02")
        elif bot.config.lang == 'es':
            bot.say("\x02No tengo administradores.\x02")
        else:
            bot.say("\x02I have no admins.\x02")
    else:
		if bot.config.lang == 'fr':
			bot.say("\x02Mes administrateurs sont:\x02 "+", ".join(admins))
		elif bot.config.lang == 'es':
			bot.say("\x02Mis administradores son:\x02 "+", ".join(admins))
		else:
			bot.say("\x02My admins are:\x02 "+", ".join(admins))
	
@commands('ignore', 'ignores')
def ignore(bot, trigger):
    ignorednicks = bot.config.core.get_list('nick_blocks')
    ignoredhosts = bot.config.core.get_list('host_blocks')
    if len(ignorednicks) == 0:
		if bot.config.lang == 'fr':
				bot.say("\x02Nicks ignorés:\x02 N'aucun nick ignoré. "+", ".join(ignorednicks)+"  \x02Hosts ignorés:\x02"+", ".join(ignorednicks))
		elif bot.config.lang == 'es':
				bot.say("\x02\x02Nicks ignorados:\x02 Ninguno. "+", ".join(ignorednicks)+"  \x02Hosts ignorados:\x02"+", ".join(ignorednicks))
                else:
			    bot.say("\x02Ignored nicks:\x02 No nick ignored. "+", ".join(ignorednicks)+"  \x02Ignored hosts:\x02"+", ".join(ignorednicks))
    elif len(ignoredhosts) == 0:
		if bot.config.lang == 'fr':
				bot.say("\x02Nicks ignorés:\x02 "+", ".join(ignorednicks)+"  \x02Hosts ignorés:\x02 N'aucun host ignoré.")
		elif bot.config.lang == 'es':
				bot.say("\x02Nicks ignorados:\x02 "+", ".join(ignorednicks)+"  \x02Hosts ignorados:\x02 Ninguno.")
                else:
			    bot.say("\x02Ignored nicks:\x02 "+", ".join(ignorednicks)+"  \x02Ignored hosts:\x02 No host ignored.")

    elif len(ignorednicks) == 0 and len(ignoredhosts) == 0:
        if bot.config.lang == 'fr':
            bot.say("\x02Ma liste d'utilisateurs ignorés est vide.\x02")
        elif bot.config.lang == 'es':
            bot.say("\x02Mi lista de ignorados está vacía.\x02")
        else:
            bot.say("\x02My ignore list is empty.\x02")
    else:
		if bot.config.lang == 'fr':
			bot.say("\x02Nicks ignorés:\x02 "+", ".join(ignorednicks)+"  \x02Hosts ignorés:\x02 "+", ".join(ignoredhosts))
		elif bot.config.lang == 'es':
			bot.say("\x02Nicks ignorados:\x02 "+", ".join(ignorednicks)+"  \x02Hosts ignorados:\x02 "+", ".join(ignoredhosts))
		else:
			bot.say("\x02Ignored nicks:\x02 "+", ".join(ignorednicks)+"  \x02Ignored hosts:\x02 "+", ".join(ignoredhosts))
	
@rule('$nick' r'(?i)(prefix|prefijo|prefixe)(?:[?!]+)?$')
@priority('low')
def prefix(bot, trigger):
    if bot.config.lang == 'fr':
    	response = (
    		"Mon prefixe est " + bot.config.core.prefix + " (sans le \).".format(bot.config.prefix.replace("\\", ""))
	    )
    elif bot.config.lang == 'es':
    	response = (
	        "Mi prefijo es: " + bot.config.core.prefix + "".format(bot.config.prefix.replace("\\", ""))
	    )
    else:
    	response = (
	        "My prefix is " + bot.config.core.prefix + " (without the \).".format(bot.config.prefix.replace("\\", ""))
	    )
	   
    bot.reply(response)

@commands('raiseException', 'causeProblems', 'giveError')
def cause_problems(bot, trigger):
    raise Exception("Problems were caused on command.")
