# -*- coding: utf-8 -*-

from sopel.module import commands
import random

@commands('reverse', 'inverse', 'reves', 'inverser')
def reversetext(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis.")
        else:
            bot.reply("Syntax error.")
        return
    text = trigger.group(2)
    bot.say(text[::-1])

@commands('rainbow', 'arcoiris', 'colores', 'colors', 'couleurs', 'arcenciel')
def rainbow(bot, trigger):
    text = trigger.group(2)
    if not text:
        if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis.")
        else:
            bot.reply("Syntax error.")
        return
    colorlist = ["\x034","\x037","\x038","\x039","\x0311","\x0312","\x0313","\x036","\x034"]
    rainbowed = ""
    for letter in text:
        rainbowed += random.choice(colorlist) + letter
    bot.say(rainbowed.encode("utf8", "replace"))

@commands('cipher', 'chiffre', 'cifra', 'rot13')
def encrypt(bot, trigger):
    text = trigger.group(2)
    if not text:
        if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis.")
        else:
            bot.reply("Syntax error.")
        return
    bot.say(text.encode('rot13'))
    
@commands('numchar')
def c_numchar(bot, trigger):
    text = trigger.group(2)
    if len(text) > 1:
        if bot.config.lang == 'fr':
            bot.say(u"J'accepte seulement une letre pour ce argument.")
        elif bot.config.lang == 'es':
            bot.say("Sólo acepto una sola letra para ese argumento.")
        else:
            bot.say("I only accept one letter for this argument.")
        return
    numchar = lambda z: '0'*(3-len(str(z)))+str(z)
    if not text:
        if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis.")
        else:
            bot.reply("Syntax error.")
        return
    bot.say(numchar(ord(text)))

@commands('tonum')
def c_tonum(bot, trigger):
    toNum = lambda z: ''.join(numchar(ord(z[i])) for i in range(len(z)))
    text = trigger.group(2)
    if text.isdigit() == True:
        if bot.config.lang == 'fr':
            bot.say(u"Je seulement accept texte pour cette commande.")
        elif bot.config.lang == 'es':
            bot.say(u"Sólo acepto texto para este comando.")
        else:
            bot.say("I only accept text for this command.")
        return      
    if not text:
        if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis.")
        else:
            bot.reply("Syntax error.")
        return
    bot.say(toNum(text))

@commands('totext')
def c_totext(bot, trigger):
    toText = lambda z: ''.join(chr(int(z[i:i+3])) for i in range(0, len(z), 3))
    text = trigger.group(2)
    if not text:
        if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis")
        else:
            bot.reply("Syntax error.")
        return
    try:
        bot.say(toText(text).decode('cp1252').encode("utf-8"))
    except ValueError:
        if bot.config.lang == 'fr':
            bot.say(u"J'accept seulement numéros jusqu'à 256 pour cette commande.")
        elif bot.config.lang == 'es':
            bot.say(u"Sólo acepto números menores a 256 para ese comando.")
        else:
            bot.say("I only accept numbers smaller than 256 for this command.")
        return
