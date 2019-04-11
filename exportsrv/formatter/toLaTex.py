# -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from exportsrv.formatter.latexencode import utf8tolatex

# this module contains methods to encode for latex output

REGEX_LATEX = OrderedDict([
            (re.compile(r"(\d+)<SUP>(\d+)</SUP>"),  r"{}\1$^{\2}$"),              # convert something like '10<SUP>5</SUP>' to '{}10$^{5}$' and
            (re.compile(r"(\d+)<SUB>(\d+)</SUB>"),  r"{}\1$_{\2}$"),
            (re.compile(r"<SUP>(.+?)</SUP>"),       r"$^{\1}$"),                  # translate <SUP>foo</SUP> and <SUB>bar</SUB> sequences into
            (re.compile(r"<SUB>(.+?)</SUB>"),       r"$_{\1}$"),                  # the proper latex equivalent of $^{foo}$ and $_{bar}$
            (re.compile(r"''(.*?)''"),              r"``\1''")                    # straight double quotes to curly quotes
])
REGEX_LATEX_AUTHOR = dict([
        (re.compile(r"([A-Z]\.)\s(?=([A-Z]\.))"), r"\1~")   # replace something like 'Tendulkar, S. P.' with 'Tendulkar, S.~P.'
                                                            # also can replace 'Miller, S. N. A.' with 'Miller, S.~N.~A.'
    ])
REGEX_HTML_TAG = dict([
    (re.compile(r"<i>(.*)</i>"), r"{\it \1}"),  # we get italic and bold tags from CSL and we need to modify them
    (re.compile(r"<b>(.*)</b>"), r"{\\bf \1}"),
    (re.compile(r"(&amp;)"), r"&"),
    (re.compile(r"(,?\s*\{\\&\}amp;)"), r" \&")
])

def encode_laTex(text):
    """

    :param text:
    :return:
    """
    if (len(text) > 1):
        # character subtitution
        text = utf8tolatex(text, ascii_no_brackets=True)
        for key in REGEX_LATEX:
            text = key.sub(REGEX_LATEX[key], text)
    return text

def encode_laTex_author(text):
    """

    :param text:
    :return:
    """
    if (len(text) > 1):
        # character subtitution
        text = utf8tolatex(text, ascii_no_brackets=True)
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