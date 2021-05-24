# -*- coding: utf-8 -*-
import random
import re

import sopel.module
from sopel.tools import eval_equation


class DicePouch:
    def __init__(self, num_of_die, type_of_die, addition):
        """Initialize dice pouch and roll the dice.

        Args:
            num_of_die: number of dice in the pouch.
            type_of_die: how many faces the dice have.
            addition: how much is added to the result of the dice.
        """
        self.num = num_of_die
        self.type = type_of_die
        self.addition = addition

        self.dice = {}
        self.dropped = {}

        self.roll_dice()

    def roll_dice(self):
        """Roll all the dice in the pouch."""
        self.dice = {}
        self.dropped = {}
        for __ in xrange(self.num):
            number = random.randint(1, self.type)
            count = self.dice.setdefault(number, 0)
            self.dice[number] = count + 1

    def drop_lowest(self, n):
        """Drop n lowest dice from the result.

        Args:
            n: the number of dice to drop.
        """
        for i, count in self.dice.iteritems():
            count = self.dice[i]
            if n == 0:
                break
            elif n < count:
                self.dice[i] = count - n
                self.dropped[i] = n
                break
            else:
                self.dice[i] = 0
                self.dropped[i] = count
                n = n - count

        for i, count in self.dropped.iteritems():
            if self.dice[i] == 0:
                del self.dice[i]

    def get_simple_string(self):
        """Return the values of the dice like (2+2+2[+1+1])+1."""
        dice = self.dice.iteritems()
        faces = ("+".join([str(face)] * times) for face, times in dice)
        dice_str = "+".join(faces)

        dropped_str = ""
        if self.dropped:
            dropped = self.dropped.iteritems()
            dfaces = ("+".join([str(face)] * times) for face, times in dropped)
            dropped_str = "[+%s]" % ("+".join(dfaces),)

        plus_str = ""
        if self.addition:
            plus_str = "{:+d}".format(self.addition)

        return "(%s%s)%s" % (dice_str, dropped_str, plus_str)

    def get_compressed_string(self):
        """Return the values of the dice like (3x2[+2x1])+1."""
        dice = self.dice.iteritems()
        faces = ("%dx%d" % (times, face) for face, times in dice)
        dice_str = "+".join(faces)

        dropped_str = ""
        if self.dropped:
            dropped = self.dropped.iteritems()
            dfaces = ("%dx%d" % (times, face) for face, times in dropped)
            dropped_str = "[+%s]" % ("+".join(dfaces),)

        plus_str = ""
        if self.addition:
            plus_str = "{:+d}".format(self.addition)

        return "(%s%s)%s" % (dice_str, dropped_str, plus_str)

    def get_sum(self):
        """Get the sum of non-dropped dice and the addition."""
        result = self.addition
        for face, times in self.dice.iteritems():
            result += face * times
        return result

    def get_number_of_faces(self):
        """Returns sum of different faces for dropped and not dropped dice

        This can be used to estimate, whether the result can be shown in
        compressed form in a reasonable amount of space.
        """
        return len(self.dice) + len(self.dropped)


def _roll_dice(dice_expression):
    result = re.search(r"""
            (?P<dice_num>\d*)
            d
            (?P<dice_type>\d+)
            (v(?P<drop_lowest>\d+))?
            $""",
            dice_expression,
            re.IGNORECASE | re.VERBOSE)

    dice_num = int(result.group('dice_num') or 1)
    dice_type = int(result.group('dice_type'))

    # Upper limit for dice should be at most a million. Creating a dict with
    # more than a million elements already takes a noticeable amount of time
    # on a fast computer and ~55kB of memory.
    if dice_num > 1000:
        return None

    dice = DicePouch(dice_num, dice_type, 0)

    if result.group('drop_lowest'):
        drop = int(result.group('drop_lowest'))
        dice.drop_lowest(drop)

    return dice


@sopel.module.commands("dice", 'de', 'dado', 'roll', 'd', 'dados', 'des')
@sopel.module.priority("medium")
def roll(bot, trigger):
    # This regexp is only allowed to have one captured group, because having
    # more would alter the output of re.findall.
    dice_regexp = r"\d*d\d+(?:v\d+)?"

    # Get a list of all dice expressions, evaluate them and then replace the
    # expressions in the original string with the results. Replacing is done
    # using string formatting, so %-characters must be escaped.
    if not trigger.group(2):
        if bot.config.lang == 'fr':
            bot.reply("Tu ne m'as donné n'aucun argument!")
        elif bot.config.lang == 'es':
            bot.reply("¡No me has dado ningún argumento!")
        else:
            bot.reply("You didn't give me any arguments!")
        return
    arg_str = trigger.group(2)
    dice_expressions = re.findall(dice_regexp, arg_str)
    arg_str = arg_str.replace("%", "%%")
    arg_str = re.sub(dice_regexp, "%s", arg_str)
    dice = map(_roll_dice, dice_expressions)
    if None in dice:
        if bot.config.lang == 'fr':
            bot.reply(u"J'ai seulement de 1000 dés.")
        elif bot.config.lang == 'es':
            bot.reply(u"Sólo tengo 1000 dados.")
        else:
            bot.reply(u"I only have 1000 dices.")
        return

    def _get_eval_str(dice):
        return "(%d)" % (dice.get_sum(),)

    def _get_pretty_str(dice):
        if dice.num <= 10:
            return dice.get_simple_string()
        elif dice.get_number_of_faces() <= 10:
            return dice.get_compressed_string()
        else:
            return "(...)"

    eval_str = arg_str % (tuple(map(_get_eval_str, dice)))
    pretty_str = arg_str % (tuple(map(_get_pretty_str, dice)))

    # Showing the actual error will hopefully give a better hint of what is
    # wrong with the syntax than a generic error message.
    try:
        result = eval_equation(eval_str)
    except Exception as e:
        bot.reply("SyntaxError, eval(%s), %s" % (eval_str, e))
        return

    bot.reply("Tú ruedas %s: %s = %d" % (
            trigger.group(2), pretty_str, result))


@sopel.module.commands("choice", 'escoge', 'escoger', 'choisir')
@sopel.module.priority("medium")
def choose(bot, trigger):
    if not trigger.group(2):
        if bot.config.lang == 'fr':
            return bot.reply(u"Tu ne m'as donné n'aucune option pour choisir!")
        elif bot.config.lang == 'es':
            return bot.reply(u"No me has dado ninguna opción para escoger!")
        else:
            return bot.reply('I\'d choose an option, but you didn\'t give me any.')
    choices = re.split('[\|\\\\\/]', trigger.group(2))
    pick = random.choice(choices)
    if bot.config.lang == 'fr':
        return bot.reply('Tes options: %s. Mon choix: %s' % (', '.join(choices), pick))
    elif bot.config.lang == 'es':
        return bot.reply(u"Tus opciones: %s. Mi elección: %s" % (', '.join(choices), pick))
    else:
        return bot.reply('Your options: %s. My choice: %s' % (', '.join(choices), pick))


if __name__ == "__main__":
    from sopel.test_tools import run_example_tests
    run_example_tests(__file__)
