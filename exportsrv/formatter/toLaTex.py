# -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from exportsrv.formatter.latexencode import utf8tolatex
from lxml import etree

# this module contains methods to encode for latex output

REGEX_LATEX = OrderedDict([
            (re.compile(r"(\d+)<SUP>(\d+)</SUP>"),          r"{}\1$^{\2}$"),                        # convert something like '10<SUP>5</SUP>' to '{}10$^{5}$' and
            (re.compile(r"(\d+)<SUB>(\d+)</SUB>"),          r"{}\1$_{\2}$"),
            (re.compile(r"<SUP>(.+?)</SUP>"),               r"$^{\1}$"),                            # translate <SUP>foo</SUP> and <SUB>bar</SUB> sequences into
            (re.compile(r"<SUB>(.+?)</SUB>"),               r"$_{\1}$"),                            # the proper latex equivalent of $^{foo}$ and $_{bar}$
            (re.compile(r"''(.*?)''"),                      r"``\1''"),                             # straight double quotes to curly quotes
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
GREEK_ALPHABET = "Alpha|Beta|Gamma|Delta|Epsilon|Zeta|Eta|Theta|Iota|Kappa|Lambda|Mu|Nu|Xi|Omicron|Pi|Rho|Sigma|Tau|Upsilon|Phi|Chi|Psi|Omega"
REGEX_LATEX_GREEK_LETTER = re.compile(r"\\(%s)+\\"%GREEK_ALPHABET, re.IGNORECASE    )
def encode_laTex(text):
    """

    :param text:
    :return:
    """
    if (len(text) > 1):
        # first remove/convert any mathML markup
        text = mathml_to_latex(text)

        # if any greek letter macro map it here
        # convert something like \\Sigma\\ to \textbackslash{}Sigma\textbackslash{}
        # however needs to go through utf8tolatex so add placeholder to be replaced afterward
        text = REGEX_LATEX_GREEK_LETTER.sub(r'PLACEHOLDER\1PLACEHOLDER', text)

        # make sure we want to break on $...$ (In-line math) where we are not applying latex substitution
        # however, it could be dollar sign representation as in the following record's title
        # "bibcode":"1979AstQ....3..143M",
        # "title":["The Gemini Syndrome: Star Wars of the Oldest Kind. Roger Culver and Philip Ianna The Astronomy
        # Quarterly Library Volume 1 Pachart Publishing House $11.95"],
        if text.count('$') % 2 == 0:
            chunks = re.split(r'(\$)', text)
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
                chunks[i] = utf8tolatex(chunks[i], ascii_no_brackets=True).replace('PLACEHOLDER', r'\textbackslash{}')
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


def convert_mathml_element(el):
    if not isinstance(el, etree._Element):
        return ""

    tag = etree.QName(el).localname

    if tag == "msup":
        base = convert_mathml_element(el[0]).strip() or "{}"
        exp = convert_mathml_element(el[1]).strip()
        return f"{base}$^{{{exp}}}$"

    if tag == "msub":
        base = convert_mathml_element(el[0]).strip() or "{}"
        sub = convert_mathml_element(el[1]).strip()
        return f"{base}$_{{{sub}}}$"

    if tag == "mn" or tag == "mi":
        return "".join(el.itertext()).strip()

    if tag == "mrow":
        return "".join([convert_mathml_element(child) for child in el])

    # fallback
    return "".join(el.itertext()).strip()

def mathml_to_latex(text):
    # Regex to find <inline-formula>...</inline-formula> blocks
    pattern = re.compile(r"<inline-formula.*?</inline-formula>", re.DOTALL)

    def replace_mathml(match):
        chunk = match.group(0)
        # Clean the chunk so it's parseable
        cleaned = (
            chunk
            # have to squish the mathML markup into an XML format for lxml to work
            .replace("<inline-formula", "<div xmlns:mml=\"http://www.w3.org/1998/Math/MathML\"")
            .replace("</inline-formula>", "</div>")
            .replace("``", "\"").replace("''", "\"")
        )

        parser = etree.XMLParser(recover=True)
        try:
            root = etree.fromstring(cleaned.encode(), parser=parser)
            mml_math = root.xpath(".//*[local-name()='math']")  # this will return an array
            if mml_math:
                return convert_mathml_element(mml_math[0])
            else:
                return "[MATHML]"
        except Exception as e:
            return "[MATHML_ERROR]"

    # Substitute all MathML chunks with LaTeX equivalents
    return pattern.sub(replace_mathml, text)
