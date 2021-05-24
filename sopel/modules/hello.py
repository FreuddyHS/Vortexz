import sopel

@sopel.module.commands('saluda', 'hello', 'hola', 'salut', 'saluter')
def helloworld(bot, trigger):
    if bot.config.lang == 'fr':
        hi = "Salut "
        if trigger.group(2):
            nick = trigger.group(2) + "!"
        else:
            nick = "a tous!"
    elif bot.config.lang == 'es':
        hi = " Hola "
        if trigger.group(2):
            nick = trigger.group(2) + "!"
        else:
            nick = "Hola Disfruten den canal :)!"
    else:
        hi = "Hello "
        if trigger.group(2):
            nick = trigger.group(2) + "!"
        else:
            nick = "everybody!"
    bot.say(hi + nick)
    return
