from sopel.module import commands, NOLIMIT
import datetime


@commands('countdown', 'comptearebours', 'cuentaatras')
def generic_countdown(bot, trigger):
    text = trigger.group(2)
    if not text:
        if bot.config.lang == 'fr':
            bot.reply(u"Utilisez le format correct: countdown 2018 12 19")
        elif bot.config.lang == 'es':
            bot.say(u"Utiliza el formato correcto: cuentaatras 2018 12 19")
        else:
            bot.say("Please use correct format: countdown 2018 12 19")
        return NOLIMIT
    text = trigger.group(2).split()
    if text and (text[2].isdigit() and text[1].isdigit() and text[0].isdigit()
            and len(text) == 3):
        diff = (datetime.datetime(int(text[2]), int(text[1]), int(text[0]))
                - datetime.datetime.today())
        if bot.config.lang == 'fr':
            bot.say(str(diff.days) + " jours, " + str(diff.seconds / 60 / 60)
                       + " heures et "
                       + str(diff.seconds / 60 - diff.seconds / 60 / 60 * 60)
                       + " minutes pour "
                       + text[0] + " " + text[1] + " " + text[2])
        elif bot.config.lang == 'es':
            bot.say(str(diff.days) + " dias, " + str(diff.seconds / 60 / 60)
                       + " horas y "
                       + str(diff.seconds / 60 - diff.seconds / 60 / 60 * 60)
                       + " minutos para el "
                       + text[0] + "-" + text[1] + "-" + text[2])
        else:
            bot.say(str(diff.days) + " days, " + str(diff.seconds / 60 / 60)
                       + " hours and "
                       + str(diff.seconds / 60 - diff.seconds / 60 / 60 * 60)
                       + " minutes for "
                       + text[0] + " " + text[1] + " " + text[2])
    else:
        if bot.config.lang == 'fr':
            bot.reply(u"Utilisez le format correct: countdown 2018 12 19")
        elif bot.config.lang == 'es':
            bot.say(u"Utiliza el formato correcto: countdown 2018 12 19")
        else:
            bot.say("Please use correct format: countdown 2018 12 19")
        return NOLIMIT
