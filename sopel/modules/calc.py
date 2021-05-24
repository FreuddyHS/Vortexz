# coding=utf-8

import re
from sopel import web
from sopel.module import commands, example
from sopel.tools import eval_equation
from socket import timeout
import string
import HTMLParser


@commands('=', 'calcula', 'calculate', 'calc', 'calcule', 'calculer', 'calcular')
def c(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'fr':
            return bot.reply("Rien à calculer.")
        elif bot.config.lang == 'es':
            return bot.reply(u"Nada que calcular.")
        else:
            return bot.reply("Nothing to calculate.")
    try:
        result = str(eval_equation(trigger.group(2)))
    except ZeroDivisionError:
        if bot.config.lang == 'fr':
            result = u"La division entre zéro n'est pas supporté dans ce monde."
        elif bot.config.lang == 'es':
            result = u"¿Eres parguela o finges serlo? ¡La division entre cero no esta soportada en este mundo!"
        else:
            result = "Division by zero is not supported in this universe."
    except Exception:
        if bot.config.lang == 'fr':
            result = ("Désolé, mais je ne peux pas comprendre cela avec cette commande. "
                  "Peut-être que j'ai une autre qui peut faire.")
        if bot.config.lang == 'es':
            result = ("Lo siento, pero no puedo calcular eso con ese comando. "
                  "Quizás tengo otro que sí puede.")
        else:
            result = ("Sorry, I can't calculate that with this command. "
                      "I might have another one that can do it.")
    bot.reply(result)

@commands('wa', 'wolfram')
def wa(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'fr':
            return bot.reply("Rien à trouver. Syntaxe: .wa <mot|phrase|opération|...>.")
        elif bot.config.lang == 'es':
            return bot.reply("Nada para buscar. Sintaxis: .wa <palabra|frase|operación|...>.")
        else:
           return bot.reply("Nothing to search. Syntax: .wa <word|sentence|operation|...>.")     
    query = trigger.group(2)
    uri = 'http://tumbolia.appspot.com/wa/'
    try:
        answer = web.get(uri + web.quote(query.replace('+', '%2B')), 45)
    except timeout as e:
        if bot.config.lang == 'fr':
            return bot.say('[WOLFRAM ERROR] Délai d\'expiration dépassée.')
        elif bot.config.lang == 'es':
            return bot.say('[WOLFRAM ERROR] Tiempo de espera excedido.')
        else:
            return bot.say('[WOLFRAM ERROR] Request timed out')
    if answer:
        answer = answer.decode('string_escape')
        answer = HTMLParser.HTMLParser().unescape(answer)
        # This might not work if there are more than one instance of escaped
        # unicode chars But so far I haven't seen any examples of such output
        # examples from Wolfram Alpha
        match = re.search('\\\:([0-9A-Fa-f]{4})', answer)
        if match is not None:
            char_code = match.group(1)
            char = unichr(int(char_code, 16))
            answer = answer.replace('\:' + char_code, char)
        waOutputArray = string.split(answer, ";")
        if(len(waOutputArray) < 2):
            if(answer.strip() == "Couldn't grab results from json stringified precioussss."):
                # Answer isn't given in an IRC-able format, just link to it.
                if bot.config.lang == 'fr':
                    bot.say('[WOLFRAM] Il n\'y a pas n\'aucune réposte disponible. Tenter amb http://www.wolframalpha.com/input/?i=' + query.replace(' ', '+'))
                elif bot.config.lang == 'es':
                    bot.say('[WOLFRAM] No hay ninguna respusta disponible. Prueba con http://www.wolframalpha.com/input/?i=' + query.replace(' ', '+'))
                else:
                    bot.say('[WOLFRAM] Couldn\'t display any answer. Please try http://www.wolframalpha.com/input/?i=' + query.replace(' ', '+'))
            else:
                bot.say('[WOLFRAM ERROR]' + answer)
        else:

            bot.say('[WOLFRAM] ' + waOutputArray[0] + " = "
                    + waOutputArray[1])
        waOutputArray = []
    else:
        if bot.config.lang == 'fr':
            bot.reply(u"Sans résultats.")
        elif bot.config.lang == 'es':
            bot.repy(u"Sin resultados.")
        else:
            bot.reply('No results.')


if __name__ == "__main__":
    from sopel.test_tools import run_example_tests
    run_example_tests(__file__)
