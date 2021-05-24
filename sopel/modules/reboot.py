# -*- coding: cp1252 -*-

from sopel.module import commands, example
import os, time

@commands('reboot')
def reboot(bot, trigger):
    if trigger.owner or trigger.admin:
        bot.callables = None
        bot.commands = None
        bot.setup()
        if bot.config.lang == 'fr':
            bot.reply(u"Bot redemarre avec succes.")
        elif bot.config.lang == 'es':
            bot.reply(u"Bot reiniciado correctamente.")
        else:
            bot.reply(u"Bot successfully rebooted.")
        return
    else:
        return bot.reply(u"You aren't my owner. - No eres mi owner. - Tu n'es pas mon proprietaire.")

@commands('apagar')
def restart(bot, trigger):
    if trigger.owner:
        if not trigger.group(2):
            quit_msg = "Apagando"
        else:
            quit_msg = trigger.group(2)
        bot.quit("%s [por %s]" % (quit_msg, trigger.nick))
        time.sleep(3) # Avoid restarting vortexz when it's still running
        os.system("python Vortexz.py")
