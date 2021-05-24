# -*- coding: utf-8 -*-
from sopel.module import commands, rule, example, priority
import sopel.config as config
import json


@rule('$nick' '(?i)(help|doc) +([A-Za-z]+)(?:\?+)?$')
@commands('help', 'aide', 'ayuda')
@priority('low')
def help(bot, trigger):
    if not trigger.group(2):
    	if bot.config.lang == 'fr':
    	    bot.reply(u'Tapez "{0}commandes" pour voir une liste des commandes, ou {0}aide <commande> pour avoir aide d\'une commande specifiée.'.format(bot.config.prefix.replace("\\", "")))
    	elif bot.config.lang == 'es':
    	    bot.reply(u'Para Ayuda. Teclea "{0}comandos" para ver una lista de los comandos creados por el mesías de xenial, o {0}ayuda <comando> para obtener ayuda de un comando en concreto. Si sigues sin enterarte es que eres retrasado de serie. Debes acudir al médico para revisartelo'.format(bot.config.prefix.replace("\\", "")))
    	else:
    	    bot.reply(u'Type "{0}commands" for a list of my commands, or {0}help <command> to get help of a specific command.'.format(bot.config.prefix.replace("\\", "")))
    
    else:
        name = trigger.group(2).lower()
        l = bot.config.lang
        f = 'doc/alias.json'
        aliasfile = open(f, 'r')
        datalias = json.load(aliasfile)
        aliasfile.close()
        command = ""
        for i in datalias:
            if name in datalias[i]["alias"]:
                command = datalias[i]["alias"][0].lower()
        ff = 'doc/commands.json'
        helpfile = open(ff, 'r')
        data = json.load(helpfile)
        helpfile.close()
        if not command in list(data):
            if bot.config.lang == "fr":
            	doc = u"Désolé, mais cette commande n'existe pas ou il n'y a pas de documentation encore."
            elif bot.config.lang == "es":
            	doc = u"No tengo tal comando"
            else:
            	doc = "Sorry, but this command doesn't exist or doesn't have documentation yet."
        else:
            doc = "\x02%s\x02: %s | \x02Example\x02: %s | \x02Alias\x02 (or in other languages): %s" % (command, data[command][l]["help"], bot.config.prefix.replace("\\", "") + data[command][l]["example"], ", ".join(datalias[command]["alias"]))
        bot.say(doc)
        
@commands('commands', 'commandes', 'ordres', 'comandos', 'ordenes')
@priority('low')
def commands(bot, trigger):
    f = open('doc/alias.json', 'r')
    data = json.load(f)
    f.close()
    names = ', '.join(sorted(list(data)))
    listnames = names.split()
    num = len(listnames)
    if bot.config.lang == 'fr':
        bot.msg(trigger.sender, '\x02' + str(num) + ' commandes disponibles:\x02 ' + names + '.', max_messages=10)
        bot.reply("Pour obtenir aide sur une commande spécifique, tapez {0}aide <commande>".format(bot.config.prefix.replace("\\", "")))
        return
    elif bot.config.lang == 'es':
    	bot.msg(trigger.sender, '\x02' + str(num) + ' comandos disponibles:\x02 ' + names + '.', max_messages=10)
    	bot.reply("Para obtener ayuda sobre un comando en concreto, escribe {0}ayuda <comando>".format(bot.config.prefix.replace("\\", "")))
    	return
    else:
	bot.msg(trigger.sender, '\x02' + str(num) + ' available commands:\x02 ' + names + '.', max_messages=10)
	bot.reply("For help on a specific command, type {0}help <command>".format(bot.config.prefix.replace("\\", "")))
	return

@rule('$nick' r'(?i)(aide|ayuda|help)(?:[?!]+)?$')
@priority('low')
def help2(bot, trigger):
    if bot.config.lang == 'fr':
    	response = (
    		'Tapez "{0}commandes" pour voir une liste des commandes, ou {0}aide <commande> pour avoir aide d\'une commande specifiée.'.format(bot.config.prefix.replace("\\", ""))
	    )
    elif bot.config.lang == 'es':
    	response = (
	        'Escribe "{0}comandos" para ver una lista de mis comandos, o {0}ayuda <comando> para obtener ayuda de un comando en específico.'.format(bot.config.prefix.replace("\\", ""))
	    )
    else:
    	response = (
	        'Type "{0}commands" for a list of my commands, or {0}help <command> to get help for a specific command.'.format(bot.config.prefix.replace("\\", ""))
	    )
	   
    bot.reply(response)

if __name__ == '__main__':
    print __doc__.strip()
