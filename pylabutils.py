# For defining intervals in real numbers line
# (n, m); [a, b]; (x, y]

import re

class Interval:
    def __init__(self, interval):
        if isinstance(interval, Interval):
            self.begin, self.end = interval.begin, interval.end
            self.begin_included = interval.begin_included
            self.end_included = interval.end_included
            return
        number_re = '-?[0-9]+(?:.[0-9]+)?'
        interval_re = ('^\s*'
                       +'(\[|\()'  #  opening bracket
                       + '\s*'
                       + '(' + number_re + ')'  #  beginning of the interval
                       + '\s*,\s*'
                       + '(' + number_re + ')'  #  end of the interval
                       + '\s*'
                       + '(\]|\))'  #  closing bracket
                       + '\s*$'
                      )
        match = re.search(interval_re, interval)
        if match is None:
            raise ValueError('Got an incorrect string representation of an interval: {!r}'. format(interval))
        opening_bracket, begin, end, closing_bracket = match.groups()
        self.begin, self.end = float(begin), float(end)
        if self.begin >= self.end:
            raise ValueError("Interval's begin shoud be smaller than it's end")
        self.begin_included = opening_bracket == '['
        self.end_included = closing_bracket == ']'
        #  It might have been better to use number_re = '.*' and catch exceptions, float() raises instead

    def __repr__(self):
        return 'Interval({!r})'.format(str(self))

    def __str__(self):
        opening_bracket = '[' if self.begin_included else '('
        closing_bracket = ']' if self.end_included else ')'
        return '{}{}, {}{}'.format(opening_bracket, self.begin, self.end, closing_bracket)

    def __contains__(self, number):
        if self.begin < number < self.end:
            return True
        if number == self.begin:
            return self.begin_included
        if number == self.end:
            return self.end_included




# Sorting various functions to a criteria that only one of them follows
# 'dalt' is almost useless
# >>>multisort(guide, data, criteria)

import copy

def multisort(*args):

    def asc(item):
        myitem = [[x, item.index(x)] for x in item]
        myitem.sort()
        return myitem

    def desc(item):
        myitem = [[x, item.index(x)] for x in item]
        myitem.sort(reverse = True)
        return myitem

    def dalt(item):
        temp = [[x, item.index(x)] for x in item]
        myitem = []
        while temp:
            try:
                myitem.append(temp[temp.index(max(temp))])
                del temp[temp.index(max(temp))]
            except(Exception):
                pass
            try:
                myitem.append(temp[temp.index(min(temp))])
                del temp[temp.index(min(temp))]
            except(Exception):
                pass
        return myitem

    sortings = (asc, desc, dalt)

    if len(args) == 3:
        guide, data, criteria = args
        if type(criteria) == str:
            criteria = eval(criteria)
    elif len(args) == 2 and type(args[1]) not in ['function', 'string']:
        guide, data = args
        criteria = asc
    elif not args:
        return sortings
    else:
        raise(ValueError('introduced arguments are invalid'))
        return

    mydict = dict([tuple(x) for x in criteria(guide)])
    findices = list(mydict.values())

    for i in data:
        temp_list = copy.deepcopy(i)
        for j in range(len(i)):
            i[j] = temp_list[findices[j]]

    return data

asc, desc, dalt = multisort()




# For adjusting (x, y) data to a given curve
# with unknown parameter values

import re
import copy
import numpy as np
import scipy.optimize as so

# Function has to be introduced as a string
# Variables have to be x and y, with y = f(x)
# y has to be left alone in the first term of the equation
# Parameters go in CAPS (unfortunately they cannot have numbers
# in their names, like A1, A2. You have to choose different letters, like
# AA, AB, etc.), number constants go between square brackets.
# For example, y = np.exp(TA / x + TB / x) + CP * [np.e]
# here TA, TB and CP are parameters and np.e is obviously a constant.

def curvefit(func, x, y, dev, *guess):

    parms = re.findall('[A-Z]+', func)
    nums = re.findall('\['+'[^\]]+'+'\]', func)

    if not guess:
        guess = [1] * len(parms)

    def curve(x, *values):

        tempcurve = copy.copy(func)

        for i in range(len(parms)):
            tempcurve = re.sub(parms[i], str(values[i]), tempcurve)
        for i in range(len(nums)):
            tempcurve = re.sub('\\' + nums[i][:-1] + '\\]', nums[i][1:-1], tempcurve)

        if '= ' in tempcurve:
            y = eval(tempcurve[tempcurve.find('=')+1:])
        else:
            y = eval(tempcurve[tempcurve.find('='):])
        return y

    sols = so.curve_fit(curve, x, y, p0 = guess, sigma = dev, absolute_sigma = True)
    return [sols[0], np.sqrt(np.diag(sols[1]))]


# To do:
# Allow more freedom at naming variables and parameters
# and at writing equations
# Introduce graphical representation




# Do a series of things with a given path
# Typically used for importing/exporting data
# that's not saved in the same place as our program,
# letting you not have to change wdir back
# >>>wdir([path_you_want_to_work_in])
# sets a path for your current project,
# >>>with wdir([path]) [do_something]
# otherwise

from contextlib import contextmanager
import os

@contextmanager
def wdir(path):
    current_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(current_dir)




# Generate a simple Latex table

from IPython.display import display, Latex

# data, data_titles and precision should all
# be tuples and have the same item order
# shape = 'hor'|'ver', box = 'hor'|'ver'|'full'|'none'
# precision values should be strings, like
# '3.5f'; '.3i'; '.2f'; '.f'

def table(data, data_titles, precision, shape = 'ver', box = 'ver'):

    shape_values = ('ver', 'hor')
    box_values = ('full', 'none', 'ver', 'hor')
    if shape not in shape_values:
        raise(ValueError('shape value is incorrect'))
        return
    if box not in box_values:
        raise(ValueError('box value is incorrect'))
        return
    else:
        if len(data) != len(precision) or len(data) != len(data_titles):
            raise(ValueError('data\'s, data titles\' and precision\'s sizes don\'t match'))
            return
        else:
            for i in range(len(data)):
                if len(data[i]) != len(data[i-1]):
                    raise(ValueError('data\'s sizes don\'t match'))
                    return
                else:
                    pass

    cadena  = '\\begin{table}[H]\n\\begin{tabular}'

    disp = ''
    tt = ''

    if shape == 'ver':
        if box == 'none' or box == 'hor':
            disp += '{' + 'c' * len(data) + '}'
        else:
            disp += '{' + '|c' * len(data) + '|}'
        cadena += disp
        tt += '\n\\hline\n'
        for i in range(len(data_titles)):
            tt += data_titles[i]
            if i != len(data_titles) - 1:
                tt += ' & '
            else:
                tt +=  '\\\\\n\\hline\n'
        cadena += tt
        for i in range(len(data[0])):
            dt = '('
            pt = ''
            for j in range(len(data)):
                dt += 'data[' + str(j) + '][' + str(i) + ']'
                pt += '%' + precision[j]
                if j != len(data) - 1:
                    dt += ', '
                    pt += ' & '
                else:
                    dt += ')'
                    if box == 'none' or box == 'ver':
                        pt += ' \\\\\n'
                    else:
                        pt += ' \\\\\n\\hline\n'
            cadena += pt % eval(dt)

    elif shape == 'hor':
        if box == 'none' or box == 'hor':
            disp += '{|c|' + 'c' * len(data) + '|}'
        else:
            disp += '{|c' + '|c' * len(data) + '|}'
        cadena += disp + '\n\\hline\n'
        for i in range(len(data)):
            dt = '('
            pt = data_titles[i] + ' & '
            for j in range(len(data[0])):
                dt += 'data[' + str(i) + '][' + str(j) + ']'
                pt += '%' + precision[i]
                if j != len(data[0]) - 1:
                    dt += ', '
                    pt += ' & '
                else:
                    dt += ')'
                    if box == 'none' or box == 'ver':
                        pt += ' \\\\\n'
                    else:
                        pt += ' \\\\\n\\hline\n'
            cadena += pt % eval(dt)

    if box == 'hor' or box == 'full':
        cadena += '\\end{tabular}\n\\end{table}\n'
    else:
        cadena += '\\hline\n\\end{tabular}\n\\end{table}\n'

    display(Latex(cadena))

    return
