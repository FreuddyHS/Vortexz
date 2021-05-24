# -*- coding: utf-8 -*-

import re
from sopel import web
from sopel.module import commands, example
import json
import time


def formatnumber(n):
    """Format a number with beautiful commas."""
    parts = list(str(n))
    for i in range((len(parts) - 3), 0, -3):
        parts.insert(i, ',')
    return ''.join(parts)
	

r_bing = re.compile(r'<h3><a href="([^"]+)"')


def bing_search(query, lang='en-GB'):
    query = web.quote(query)
    base = 'http://www.bing.com/search?mkt=%s&q=' % lang
    bytes = web.get(base + query)
    m = r_bing.search(bytes)
    if m:
        return m.group(1)

r_duck = re.compile(r'nofollow" class="[^"]+" href="(.*?)">')


def duck_search(query):
    query = query.replace('!', '')
    query = web.quote(query)
    uri = 'http://duckduckgo.com/html/?q=%s&kl=uk-en' % query
    bytes = web.get(uri)
    m = r_duck.search(bytes)
    if m:
        return web.decode(m.group(1))


def duck_api(query):
    if '!bang' in query.lower():
        return 'https://duckduckgo.com/bang.html'

    uri = web.quote(query)
    uri = 'http://api.duckduckgo.com/?q=%s&format=json&no_html=1&no_redirect=1' % query
    results = json.loads(web.get(uri))
    print results
    if results['Redirect']:
        return results['Redirect']
    else:
        return None


@commands('duck', 'ddg')
def duck(bot, trigger):
    query = trigger.group(2)
    if not query:
        if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis.")
        else:
            bot.reply("Syntax error.")
        return
    
    #If the API gives us something, say it and stop
    result = duck_api(query)
    if result:
        bot.reply(result)
        return

    #Otherwise, look it up on the HTMl version
    uri = duck_search(query)

    if uri:
        bot.reply(uri)
        bot.memory['last_seen_url'][trigger.sender] = uri
    else:
        if bot.config.lang == 'fr':
            bot.reply("Je ne trouve résultats pour '%s'." % query)
        elif bot.config.lang == 'es':
            bot.reply("No se han encontrado resultados para '%s'." % query)
        else:
            bot.reply("No results found for '%s'." % query)
        return


@commands('search', 'cherche', 'busca', 'rechercher', 'recherche', 'chercher', 'buscar')
def search(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
        elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis.")
        else:
            bot.reply("Syntax error.")
        return
    
    query = trigger.group(2)
    gu = google_search(query) or '-'
    bu = bing_search(query) or '-'
    du = duck_search(query) or '-'

    if (gu == bu) and (bu == du):
        result = '%s (g, b, d)' % gu
    elif (gu == bu):
        result = '%s (g, b), %s (d)' % (gu, du)
    elif (bu == du):
        result = '%s (b, d), %s (g)' % (bu, gu)
    elif (gu == du):
        result = '%s (g, d), %s (b)' % (gu, bu)
    else:
        if len(gu) > 250:
            gu = '(extremely long link)'
        if len(bu) > 150:
            bu = '(extremely long link)'
        if len(du) > 150:
            du = '(extremely long link)'
        result = '%s (g), %s (b), %s (d)' % (gu, bu, du)

    bot.reply(result)

@commands('suggest', 'suggerer', 'sugiere')
def suggest(bot, trigger):
    if not trigger.group(2):
	if bot.config.lang == 'fr':
            bot.reply("Erreur de syntaxe.")
	elif bot.config.lang == 'es':
            bot.reply("Error de sintaxis.")
	else:
            bot.reply("Syntax error.")
	return
    query = trigger.group(2)
    uri = 'http://websitedev.de/temp-bin/suggest.pl?q='
    answer = web.get(uri + web.quote(query).replace('+', '%2B'))
    if answer:
    	bot.say(answer)
    else:
    	if bot.config.lang == 'fr':
    	    bot.reply("N'aucun résultat.")
    	elif bot.config.lang == 'es':
            bot.reply("No hay resultados")
    	else:
            bot.reply('Sorry, no result.')
