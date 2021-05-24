# -*- coding: utf-8 -*-

import sys
import os.path
import time
import imp
from sopel.module import nickname_commands, commands, priority, thread, NOLIMIT
import subprocess

@nickname_commands("reload")
@commands("reload")
@priority("low")
@thread(False)
def f_reload(bot, trigger):
    if not trigger.admin:
        if bot.config.lang == 'fr':
            bot.reply(u'Tu n\'es pas un administrateur')
        elif bot.config.lang == 'es':
            bot.reply(u"No tienes permisos de administrador")
        else:
            bot.reply(u"You aren't an admin")
        return

    name = trigger.group(2)

    if (not name) or (name == '*') or (name.upper() == 'ALL THE THINGS'):
        bot.callables = None
        bot.commands = None
        bot.setup()
        return bot.reply('Hecho')

    if not name in sys.modules:
        if bot.config.lang == 'fr':
            bot.reply(u"N'aucun module " + name)
        elif bot.config.lang == 'es':
            bot.reply(u"No hay ningún módulo nombrado " + name)
        else:
            bot.reply(name + ": no such module!")
        return NOLIMIT

    old_module = sys.modules[name]

    old_callables = {}
    for obj_name, obj in vars(old_module).iteritems():
        if bot.is_callable(obj) or bot.is_shutdown(obj):
            old_callables[obj_name] = obj

    bot.unregister(old_callables)
    # Also remove all references to sopel callables from top level of the
    # module, so that they will not get loaded again if reloading the
    # module does not override them.
    for obj_name in old_callables.keys():
        delattr(old_module, obj_name)
    
    # Also delete the setup function
    if hasattr(old_module, "setup"):
        delattr(old_module, "setup")

    # Thanks to moot for prodding me on this
    path = old_module.__file__
    if path.endswith('.pyc') or path.endswith('.pyo'):
        path = path[:-1]
    if not os.path.isfile(path):
        return bot.reply('Found %s, but not the source file' % name)

    module = imp.load_source(name, path)
    sys.modules[name] = module
    if hasattr(module, 'setup'):
        module.setup(bot)

    mtime = os.path.getmtime(module.__file__)
    modified = time.strftime(u'%Y-%m-%d, %H:%M:%S', time.gmtime(mtime))

    bot.register(vars(module))
    bot.bind_commands()

    bot.reply(u'%r (version: %s) reloaded' % (module, modified))
    return NOLIMIT

@nickname_commands("load")
@commands("load")
@priority("low")
@thread(False)
def f_load(bot, trigger):
    """Loads a module, for use by admins only."""
    if not trigger.admin:
        return

    module_name = trigger.group(2)
    path = ''

    if module_name in sys.modules:
        return bot.reply('Module already loaded, use reload. If you unloaded thos module use "reload" instead.')

    mods = bot.config.enumerate_modules()
    for name in mods:
        if name == trigger.group(2):
            path = mods[name]
    if not os.path.isfile(path):
        bot.reply('Module %s not found' % module_name)
        return NOLIMIT

    module = imp.load_source(module_name, path)
    mtime = os.path.getmtime(module.__file__)
    modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))
    if hasattr(module, 'setup'):
        module.setup(bot)
    bot.register(vars(module))
    bot.bind_commands()

    bot.reply(u'%r (version: %s) loaded. Use "unload" to unload it.' % (module, modified))
    return NOLIMIT
    
@nickname_commands("unload")
@commands("unload")
@priority("low")
@thread(False)
def f_unload(bot, trigger):
    if not trigger.admin:
        if bot.config.lang == 'fr':
            bot.reply(u'Tu n\'es pas un administrateur')
        elif bot.config.lang == 'es':
            bot.reply(u"No tienes permisos de administrador")
        else:
            bot.reply(u"You aren't an admin")
        return

    name = trigger.group(2)

    if not name in sys.modules:
        if bot.config.lang == 'fr':
            bot.reply(u"N'aucun module " + name)
        elif bot.config.lang == 'es':
            bot.reply(u"No hay ningún module nombrado " + name)
        else:
            bot.reply(name + ": no such module!")
        return NOLIMIT

    old_module = sys.modules[name]

    old_callables = {}
    for obj_name, obj in vars(old_module).iteritems():
        if bot.is_callable(obj) or bot.is_shutdown(obj):
            old_callables[obj_name] = obj

    bot.unregister(old_callables)
    # Also remove all references to sopel callables from top level of the
    # module, so that they will not get loaded again if reloading the
    # module does not override them.
    for obj_name in old_callables.keys():
        delattr(old_module, obj_name)
    
    # Also delete the setup function
    if hasattr(old_module, "setup"):
        delattr(old_module, "setup")

    # Thanks to moot for prodding me on this
    path = old_module.__file__
    if path.endswith('.pyc') or path.endswith('.pyo'):
        path = path[:-1]
    if not os.path.isfile(path):
        return bot.reply('Found %s, but not the source file' % name)    
    module = imp.load_source(name, path)
    mtime = os.path.getmtime(module.__file__)
    modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))

    bot.reply(u'%r (version: %s) unloaded. Use "reload" to load it again.' % (module, modified))
    return NOLIMIT

@nickname_commands('update')
@commands("update")
def f_update(bot, trigger):
    if not trigger.admin:
        return
    
    bot.reply("Updating and reloading...")
    """Pulls the latest versions of all modules from Git"""
    proc = subprocess.Popen('/usr/bin/git pull',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True)
    msg = proc.communicate()[0]
    bot.say(msg)
    if msg.startswith("Already"): # ...up-to-date.
        return # Not necessary to reload
    else:
        f_reload(bot, trigger)
    
if __name__ == '__main__':
    print __doc__.strip()
