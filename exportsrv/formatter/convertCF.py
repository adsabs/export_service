#!/usr/bin/env python
# coding=utf-8

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
    currentCF = re_sub(r'%([\\])?(\d*\.?\d*)?([\(\{\[\"])?(\w+)([\)\}\]\"])?', r'\3%\2\4\1\5', classicCF)
    redundant = ['%b','%e','%f','%k','%r','%s','%t','%v','%w','%y']
    for r in redundant:
        currentCF = currentCF.replace(r, r.upper())
    currentCF = currentCF.replace('%za1', '%H').replace('%za2', '%L').replace('%za3', '%M')
    return currentCF