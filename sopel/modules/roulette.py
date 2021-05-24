# -*- coding:utf-8 -*-

from sopel.module import commands, priority
import random
from datetime import datetime, timedelta
random.seed()

# edit this setting for roulette counter. Larger, the number, the harder the game.
ROULETTE_SETTINGS = {
    # the bigger the MAX_RANGE, the harder/longer the game will be
    'MAX_RANGE': 5,

    # game timeout in minutes (default is 1 minute)
    'INACTIVE_TIMEOUT': 1,
}

## do not edit below this line unless you know what you're doing
ROULETTE_TMP = {
    'NUMBER': None,
    'TIMEOUT': timedelta(minutes=ROULETTE_SETTINGS['INACTIVE_TIMEOUT']),
    'LAST-ACTIVITY': None,
}


@commands('roulette', 'ruleta')
@priority('low')
def roulette(bot, trigger):
    global ROULETTE_SETTINGS, ROULETTE_TMP
    if bot.config.lang == 'fr':
        ROULETTE_STRINGS = {
            'TICK': '*tick*',
            'KICK_REASON': u'Oh, non! T\'as perdu et maintenant tu es mort D:',
            'GAME_END': 'Jeu arrêté.',
            'GAME_END_FAIL': "%s: S'il te plaît, attendez %s secondes pour arrêter le jeu.",
        }
    elif bot.config.lang == 'es':
        ROULETTE_STRINGS = {
            'TICK': '*tick*',
            'KICK_REASON': u'¡Oh, no! Has perdido y estás muerto D:',
            'GAME_END': 'Juego parado.',
            'GAME_END_FAIL': "%s: Por favor, espera %s segundos para parar el juego.",
        }
    else:
        ROULETTE_STRINGS = {
            'TICK': '*tick*',
            'KICK_REASON': u'Oh, no! You lose and you are dead D:',
            'GAME_END': 'Game stopped.',
            'GAME_END_FAIL': "%s: Please, wait %s seconds to stop the game.",
        }        
    if ROULETTE_TMP['NUMBER'] is None:
        ROULETTE_TMP['NUMBER'] = random.randint(0, ROULETTE_SETTINGS['MAX_RANGE'])
        bot.say(ROULETTE_STRINGS['TICK'])
        return
    if ROULETTE_TMP['NUMBER'] == random.randint(0, ROULETTE_SETTINGS['MAX_RANGE']):
        bot.write(['KICK', '%s %s :%s' % (trigger.sender, trigger.nick, ROULETTE_STRINGS['KICK_REASON'])])
        ROULETTE_TMP['LAST-PLAYER'] = None
        ROULETTE_TMP['NUMBER'] = None
        ROULETTE_TMP['LAST-ACTIVITY'] = None
    else:
        bot.say(ROULETTE_STRINGS['TICK'])

if __name__ == '__main__':
    print __doc__.strip()
