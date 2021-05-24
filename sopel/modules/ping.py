# -*- coding: utf-8 -*-
from sopel import module
from sopel.module import commands
import random
import re

@commands("ping")
def normal_ping(bot, trigger):
    bot.say("Pong!")
    
@commands("pong")
def normal_pong(bot, trigger):
    bot.say("Ping!")

@commands("linel")
def normal_linel(bot, trigger):
    bot.say("Ese men es mi brother <3 by Xenial")

@commands("status")
def normal_status(bot, trigger):
    bot.say("Estado del bot: Operativo")

@commands("xenial")
def normal_status(bot, trigger):
    bot.say("Un Español que desarrollo XeniBot")

@commands("estado")
def normal_estado(bot, trigger):
    bot.say("Estado del bot: Operativo")

@commands("about")
def normal_about(bot, trigger):
    bot.say("Soy Vortexz V-XeniBot, un bot desarrollado por Xenial, Reeditado por Freuddy.")
