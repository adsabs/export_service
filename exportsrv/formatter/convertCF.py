# -*- coding: utf-8 -*-

import re


def re_sub(pattern, replacement, string):
    def _r(m):
        # Now this is ugly.
        # Python has a "feature" where unmatched groups return None
        # then re.sub chokes on this.
        # see http://bugs.python.org/issue1519638

        # this works around and hooks into the internal of the re module...

        # the match object is replaced with a wrapper that
        # returns "" instead of None for unmatched groups

        class _m():
            def __init__(self, m):
                self.m = m
                self.string = m.string

            def group(self, n):
                return m.group(n) or ""

        return re._expand(pattern, _m(m), replacement)

    return re.sub(pattern, _r, string)

def convert(classicCF):
    """

    :param classicCF: classic's custom format
    :return: new custom format
    """
    # fix the encoding, remove the ones we no longer support
    currentCF = classicCF.replace('%Zencoding', '%ZEncoding').replace('%ZEncoding:TeX','%ZEncoding:latex').replace('%ZEncoding:ISO-8859-1', '').replace('%ZEncoding:ISO-8859-2', '')
    currentCF = currentCF.replace('%Zlinelength', '%ZLinelength')
    # remove any space between the % and the specifier if any
    currentCF = re_sub(r'%\s+(\\?\w)', r'%\1', currentCF)
    currentCF = currentCF.replace('%\\n', '%n')
    # move dash to before the specifier
    currentCF = re_sub(r'%-(\w)', r'-%\1', currentCF)
    # page range replacement, we have %pp for %p-%P
    currentCF = re_sub(r'%([\\>])?([\(\{\[\"])?(p)([\)\}\]\"])?\-?%\-?([\\])?([\(\{\[\"])?(P)([\)\}\]\"])?', r'%\1pp', currentCF)
    # move parentheses, curly brackets, and brackets around the specifier (ie, %{R} becomes {%R}
    currentCF = re_sub(r'%([\\>])?(\d*\.?\d*)?([\(\{\[\"\'])?(\w+)([\)\}\]\"\'])?', r'\3%\1\2\4\5', currentCF)
    # another variation: %{\1h} becomes {%\1h}
    currentCF = re_sub(r'%([\(\{\[\"\'])([\\])(\d*\.?\d*)?(\w+)([\)\}\]\"\'])', r'\1%\2\3\4\5', currentCF)
    # redundant specifiers has been eliminated, convert all the lower cases to upper cases
    redundant = [r'b',r'e',r'f',r'k',r'r',r's',r't',r'v',r'w',r'y']
    for r in redundant:
        currentCF = re_sub(r'%([\\>])?(\d*\.?\d*)?([\(\{\[\"])?('+r+')([\)\}\]\"])?', r'\3%\1\2'+r.upper()+r'\5', currentCF)
    # more redundant replacement
    currentCF = currentCF.replace('%za1', '%1H')
    # change from multi character author format to single character
    currentCF = re_sub(r'%(.*)za2', r'%\1e', currentCF)
    currentCF = re_sub(r'%(.*)za3', r'%\1f', currentCF)
    # some have made a mistake with this thinking n can be any number, so correct it
    currentCF = re_sub(r'(%\\?z\d+)', r'', currentCF)
    currentCF = currentCF.replace('%\zn', '%zn')
    # remove %S which is not supported
    currentCF = re_sub(r'%([\\>])?(\d*\.?\d*)?([\(\{\[\"])?(S)([\)\}\]\"])?', r'', currentCF)
    return currentCF