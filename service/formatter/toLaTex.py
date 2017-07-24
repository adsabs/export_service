#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from flask import current_app

# this module contains methods to encode for latex outpu

def encodeLaTex(text):
    # make sure the input has unicode type
    if (isinstance(text, str)):
        text = unicode(text)
    # character subtitution
    if (len(text) > 1):
        latexAccents = current_app.config['EXPORT_SERVICE_LATEX_ACCENT']
        translationTable = dict([(ord(k), unicode(v)) for k, v in latexAccents])
        text = text.translate(translationTable)
        latexMath = OrderedDict([
            (r"(\d+)\^(\d+)",           r"{}\1\\^{}\2"),              # convert something like '10^5' to '{}10\^{}5' and
            (r"(\d+)\^\\\{(\d+)\\\}",   r"{}\1\\^{}$\\{$\2$\\}$")     # something like '10^\{51\}' to '{}10\^{}$\{$51$\}$'
        ])
        for key in latexMath:
            regex = re.compile(key)
            text = regex.sub(latexMath[key], text)
    return text

def encodeLaTexAuthor(text):
    latexAuthor = dict([
        (r"([A-Z]\.)\s(?=([A-Z]\.))", r"\1~")   # replace something like 'Tendulkar, S. P.' with 'Tendulkar, S.~P.'
                                                # also can replace 'Miller, S. N. A.' with 'Miller, S.~N.~A.'
    ])
    for key in latexAuthor:
        regex = re.compile(key)
        text = regex.sub(latexAuthor[key], text)
    return text

def htmlToLaTex(text):
    htmlTag = dict([
        (r"<i>(.*)</i>", r"{\it \1}"),          # we get italic and bold tags from CSL and we need to modify them
        (r"<b>(.*)</b>", r"{\\bf \1}"),
        (r"(&amp;)", r"\&")
    ])
    for key in htmlTag:
        regex = re.compile(key)
        text = regex.sub(htmlTag[key], text)
    return text