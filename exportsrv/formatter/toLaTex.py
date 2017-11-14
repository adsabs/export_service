#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from flask import current_app

# this module contains methods to encode for latex output

REGEX_LATEX_MATH = OrderedDict([
            (re.compile(r"(\d+)\^(\d+)"),           r"{}\1\\^{}\2"),              # convert something like '10^5' to '{}10\^{}5' and
            (re.compile(r"(\d+)\^\\\{(\d+)\\\}"),   r"{}\1\\^{}$\\{$\2$\\}$")     # something like '10^\{51\}' to '{}10\^{}$\{$51$\}$'
        ])
REGEX_LATEX_AUTHOR = dict([
        (re.compile(r"([A-Z]\.)\s(?=([A-Z]\.))"), r"\1~")   # replace something like 'Tendulkar, S. P.' with 'Tendulkar, S.~P.'
                                                            # also can replace 'Miller, S. N. A.' with 'Miller, S.~N.~A.'
    ])
REGEX_HTML_TAG = dict([
    (re.compile(r"<i>(.*)</i>"), r"{\it \1}"),  # we get italic and bold tags from CSL and we need to modify them
    (re.compile(r"<b>(.*)</b>"), r"{\\bf \1}"),
    (re.compile(r"(&amp;)"), r"\&")
])


def encode_laTex(text):
    """

    :param text:
    :return:
    """
    # make sure the input has unicode type
    if (isinstance(text, str)):
        text = unicode(text)
    # character subtitution
    if (len(text) > 1):
        latex_accents = current_app.config['EXPORT_SERVICE_LATEX_ACCENT']
        translation_table = dict([(ord(k), unicode(v)) for k, v in latex_accents])
        text = text.translate(translation_table)
        for key in REGEX_LATEX_MATH:
            text = key.sub(REGEX_LATEX_MATH[key], text)
    return text


def encode_laTex_author(text):
    """

    :param text:
    :return:
    """
    for key in REGEX_LATEX_AUTHOR:
        text = key.sub(REGEX_LATEX_AUTHOR[key], text)
    return text


def html_to_laTex(text):
    """

    :param text:
    :return:
    """
    for key in REGEX_HTML_TAG:
        text = key.sub(REGEX_HTML_TAG[key], text)
    return text