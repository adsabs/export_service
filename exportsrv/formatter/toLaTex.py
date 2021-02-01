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
            (re.compile(r"''(.*?)''"),              r"``\1''"),                   # straight double quotes to curly quotes
])
REGEX_LATEX_AUTHOR = dict([
        (re.compile(r"([A-Z]\.)\s(?=([A-Z]\.))"), r"\1~")   # replace something like 'Tendulkar, S. P.' with 'Tendulkar, S.~P.'
                                                            # also can replace 'Miller, S. N. A.' with 'Miller, S.~N.~A.'
    ])
REGEX_HTML_TAG = OrderedDict([
    (re.compile(r"<i>(.*)</i>"), r"{\\it \1}"),             # we get italic and bold tags from CSL and we need to modify them
    (re.compile(r"<b>(.*)</b>"), r"{\\bf \1}"),
    (re.compile(r"(\\?&amp;)"), r"\\&"),
    (re.compile(r"(\\&lt;)"), r"$\\lt$"),                   # html entity less-than
    (re.compile(r"(\\&gt;)"), r"$\\gt$"),                   # html entity greater-than
    (re.compile(r"(,?\s*\{\\&\}amp;)"), r" \&"),
])

def encode_laTex(text):
    """

    :param text:
    :return:
    """
    if (len(text) > 1):
        # make sure we want to break on $...$ (In-line math) where we are not applying latex substitution
        # however, it could be dollar sign representation as in the following record's title
        # "bibcode":"1979AstQ....3..143M",
        # "title":["The Gemini Syndrome: Star Wars of the Oldest Kind. Roger Culver and Philip Ianna The Astronomy
        # Quarterly Library Volume 1 Pachart Publishing House $11.95"],
        if text.count('$') % 2 == 0:
            chunks = re.split('(\$)', text)
        else:
            chunks = [text]
        latex = []
        i = 0
        while i < len(chunks):
            # no substitution in the math mode
            if chunks[i] == '$':
                for j in range(3):
                    latex.append(chunks[i+j])
                i = i + 3
            else:
                # character substitution
                chunks[i] = utf8tolatex(chunks[i], ascii_no_brackets=True)
                for key in REGEX_LATEX:
                    chunks[i] = key.sub(REGEX_LATEX[key], chunks[i])
                latex.append(html_to_laTex(chunks[i]))
                i = i + 1
        return ''.join(latex)
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


def encode_latex_doi(text):
    """
    :param text: plain text
    :return: escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    if (len(text) > 1):
        regex = re.compile('|'.join(re.escape(str(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
        return regex.sub(lambda match: conv[match.group()], text)
    return text


def html_to_laTex(text):
    """

    :param text:
    :return:
    """
    for key in REGEX_HTML_TAG.keys():
        text = key.sub(REGEX_HTML_TAG[key], text)
    return text