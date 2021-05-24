# -*- coding: utf-8 -*-

from sopel.module import commands
from random import choice, randint
from re import search
import sched
import time

allcolors = ['Red', 'Yellow', 'Blue', 'White', 'Black', 'Green', 'Purple', 'Brown', 'Orange', 'Pink', 'Rouge', 'Jaune', 'Bleu', 'Blanc', 'Noir', 'Vert', 'Violet', 'Brun', 'Orange', 'Rosé', 'Rojo', 'Amarillo', 'Azul', 'Blanco', 'Negro', 'Verde', 'Morado', 'Marrón', 'Naranja', 'Rosado'] 
colors_en = ['Red', 'Yellow', 'Blue', 'White', 'Black', 'Green', 'Purple', 'Brown', 'Orange', 'Pink'] 
colors_fr = ['Rouge', 'Jaune', 'Bleu', 'Blanc', 'Noir', 'Vert', 'Violet', 'Brun', 'Orange', 'Rosé']
colors_es = ['Rojo', 'Amarillo', 'Azul', 'Blanco', 'Negro', 'Verde', 'Morado', 'Marrón', 'Naranja', 'Rosado']
sch = sched.scheduler(time.time, time.sleep)
fuse = 120  # seconds
bombs = dict()


@commands('bomb', 'bombe', 'bomba')
def start(bot, trigger):
    if not trigger.group(2):
        return

    if not trigger.sender.startswith('#'):
        return
    global bombs
    global sch
    target = trigger.group(2).split(' ')[0]
    if target == bot.nick or target == bot.config.owner or target == bot.config.admins:
        if trigger.group(1) == 'bomb':
            bot.say(u"Error: You can't throw bombs to the bot owner, the bot admins or the bot.")
            return
        else:
            if bot.config.lang == 'fr':
                bot.say(u"Erreur: Tu ne peux pas mettre des bombes au propriétaire, aux administrateurs ni au bot.")
            else:
                bot.say(u"Error: No puedes tirarle bombas ni al dueño, ni a los administradores ni al propio bot.")
            return
    if target in bombs:
        if trigger.group(1) == 'bomb':
            bot.say(u"I can't put another bomb to " + target + "!")
            return
        else:
            if bot.config.lang == 'fr':
                bot.say(u'Je ne peux pas mettre une autre bombe à ' + target + '!')
            else:
                bot.say(u"¡No le puedo otra bomba a " + target + "!")
            return
    if trigger.group(1) == 'bomb':
        message = ('Hey, ' + target + u'! Somebody has given you a bomb! You have \x022 minutes\x02 and \x0210 wires\x02: Red, Yellow, Blue, White, Black, Green, Purple, Brown, Orange and Pink. What wire should I cut? Don\'t worry, I know what I\'m doing ! (answer with "%scutwire color")' % bot.config.prefix.replace("\\", ""))
        bot.say(message)
        color = choice(colors_en)
        #bot.msg(trigger.nick,
        #           u"Hey, don't tell it to %s, but is the %s one! "
        #           u"But shh! Don't tell it to anybody!" % (target, color))
        code = sch.enter(fuse, 1, explode_en, (bot, trigger))
        bombs[target.lower()] = (color, code)
        sch.run()
    else:
        if bot.config.lang == 'fr':
            message = ('Hey, ' + target + u'! Ça me semble qu\'il y a aucun qui t\'a mis une bombe... Tu as de \x022 minutes\x02 et \x0210 câbles\x02: Rouge, Jaune, Bleu, Blanc, Noir, Vert, Violet, Brun, Orange et Rosé. Quel câble dois-je couper? Ne t\'inquiétes pas, je sais ce que je fais! (répondez avec "%scouper couleur")' % bot.config.prefix.replace("\\", ""))
            bot.say(message)
            color = choice(colors_fr)
            #bot.msg(trigger.nick,
            #           u"Hey, ne dites pas à %s, mais c'est le câble %s! "
            #           u"Mais shh! Ne le dis à personne!" % (target, color))
            code = sch.enter(fuse, 1, explode_fr, (bot, trigger))
            bombs[target.lower()] = (color, code)
            sch.run()
        else:
            message = ('¡Hey, ' + target + u'! Parece que alguien te ha puesto una bomba... Tienes \x022 minutos\x02 y \x0210 cables\x02: Rojo, Amarillo, Azul, Blanco, Negro, Verde, Morado, Marrón, Naranja y Rosado. ¿Qué cable tengo que cortar? ¡No te preocupes, yo sé lo que hago! (responde con "%scorta color")' % bot.config.prefix.replace("\\", ""))
            bot.say(message)
            color = choice(colors_es)
            #bot.msg(trigger.nick,
            #           u"¡Hey, no se lo digas a %s, pero es el cable %s! "
            #           u"¡Pero shh! No se lo digas a nadie xD" % (target, color))
            code = sch.enter(fuse, 1, explode_es, (bot, trigger))
            bombs[target.lower()] = (color, code)
            sch.run()

@commands('cutwire', 'couper', 'corta', 'cortar')
def cutwire(bot, trigger):
    global bombs, colors_fr, colors_en, colors_es, allcolors
    target = trigger.nick
    if target.lower() != bot.nick.lower() and target.lower() not in bombs:
        return
    color, code = bombs.pop(target.lower())  # remove target from bomb list
    wirecut = trigger.group(2).rstrip(' ')
    if wirecut.lower() in ('all', 'all!', 'tout', 'tout!', 'tous', 'tous!', 'todo', 'todos', 'todo!', 'todos!', '¡todos!', '¡todo!'):
        sch.cancel(code)  # defuse timer, execute premature detonation
        if trigger.group(1) == 'cutwire':
            kmsg = (u'KICK %s %s:Cutting ALL the wires! *BOOM!!!* (You should cut the %s one.)'
                    % (trigger.sender, target, color))
        elif trigger.group(1) == 'couper':
            kmsg = (u'KICK %s %s:Coupant TOUS les câbles! *BOOM!!!* (tu avais dû de couper le câble %s.)'
                    % (trigger.sender, target, color))
        else:
            kmsg = (u'KICK %s %s:¡Cortando TODOS los cables! *BOOM!!!* (debiste haber cortado el cable %s.)'
                    % (trigger.sender, target, color))
        bot.write([kmsg])
    elif wirecut.capitalize() not in allcolors:
        if trigger.group(1) == 'cutwire':
            bot.say(u'I don\'t see that wire, ' + target + u'! That wire doesn\'t exist!')
        elif trigger.group(1) == 'couper':
            bot.say(u'Je ne peux pas trouver ce câble, ' + target + u'! Ce câble n\'existe pas!')
        else:
            bot.say(u'¡No encuentro ese cable, ' + target + u'! ¡Ese cable no existe!')
        bombs[target.lower()] = (color, code)  # Add the target back onto the bomb list,
    elif wirecut.capitalize() == color:
        if trigger.group(1) == 'cutwire':
            bot.say(u'Well done, ' + target + u'! You have defused the bomb before exploding! Well done!!')
        elif trigger.group(1) == 'couper':
            bot.say(u'Très bien, ' + target + u'! Tu as désamorcé la bombe avant qu\'elle explose! Bon travail!!')
        else:
            bot.say(u"¡Muy bien, " + target + u"! ¡Has conseguido desactivar la bomba antes de que explotara! ¡¡Buen trabajo!!")
        sch.cancel(code)  # defuse bomb
    else:
        sch.cancel(code)  # defuse timer, execute premature detonation
        if trigger.group(1) == 'cutwire':
            kmsg = 'KICK ' + trigger.sender + ' ' + target + \
                   u' :No! No, that was the bad one and you have killed yourself... sorry (you should choose the ' + color + ' wire)'
        elif trigger.group(1) == 'couper':
            kmsg = 'KICK ' + trigger.sender + ' ' + target + \
                   u' :Non!, Tu t\'as trompé de câble et t\'as assassiné a toi-même... désolé (tu avais dû de couper le câble ' + color + ')'
        else:
            kmsg = 'KICK ' + trigger.sender + ' ' + target + \
                   u' :¡No! Te equivocaste de cable y te mataste a ti mismo... lo siento (debiste haber cortado el cable de color ' + color + ')'
        bot.write([kmsg])

def explode_fr(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           u' :Tu n\'as pas coupé le câble à temps! Maintenant tu es mort. D:'
    bot.write([kmsg])

def explode_en(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           u' :You didn\'t cut the wire on time! Now you\'re dead. D:'
    bot.write([kmsg])

def explode_es(bot, trigger):
    target = trigger.group(2)
    kmsg = 'KICK ' + trigger.sender + ' ' + target + \
           u' :¡No cortaste el cable a tiempo! Ahora estás muerto. D:'
    bot.write([kmsg])