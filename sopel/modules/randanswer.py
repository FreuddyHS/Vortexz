# -*- coding: utf-8 -*-
import sopel
import random
@sopel.module.commands('answer', 'repond', 'responde', 'respuesta', 'repondez')
def ball(bot, trigger):
    if bot.config.lang == 'fr':
        messages = [u"Certainement vrai.",u"Oui monsieur!",u"Sans doute!",u"Oui, certainement",u"D'accord!",u"Je crois que oui",u"Sûrement...",u"Je ne trouve n'aucun problème...",u"Oui",u"Il me semble que oui",u"Oups! Tenter à plus.",u"Maintenant mieux non...",u"Ouff, j'ai la boule magique sale.",u"Je crois que non",u"Negativament negatiu."]
    elif bot.config.lang == 'es':
        messages = [u"Ciertamente cierto.", u"¡Sí señor!", u"¡Sin duda!", u"Sí, definitivamente.", u"¡Totalmente de acuerdo!", u"Yo creo que sí...", u"Seguramente...", "No veo ningún problema...", u"Sí.", u"Parece que sí.", "Uy, intenta más tarde.", "Mejor no te lo digo ahora.", u"Uy, tengo la bola mágica sucia.", "Me has cogido por sorpresa, espera que me concentre... Intenta otra vez", "No cuentes con ello", "Yo creo que no...", "Yo no lo haría...", "Dudo que sea cierto..", "No parece muy bueno...", "Négativament négatif"]
    else:
        messages = ["It is certain"," It is decidedly so","Without a doubt","Yes definitely","You may rely on it","As I see it yes","Most likely","Outlook good","Yes","Signs point to yes","Reply hazy try again","Ask again later","Better not tell you now","Cannot predict now","Concentrate and ask again","Don't count on it","My reply is no","God says no","Very doubtful","Outlook not so good"]
    answer = random.randint(0,len(messages) - 1)
    bot.say(messages[answer]);
