#!/usr/bin/env python
# -*- coding: utf-8 -*-

# these three classes are basically just enums, verifying valid members

class adsFormatter:
    unicode, html, latex = range(3)

    def verify(self, format):
        if (format == adsFormatter.unicode) or (format == adsFormatter.html) or (format == adsFormatter.latex):
            return True
        return False

class adsOrganizer:
    plain, citation_bibliography, bibliography = range(3)

class adsCSLStyle:
    ads_CLS = ['aastex', 'icarus', 'mnras', 'soph', 'aspc', 'apsj', 'aasj']

    def verify(self, style):
        if (style in self.ads_CLS):
            return True
        return False

    def get(self):
        separator = ', '
        styles = ''
        for style in self.ads_CLS:
            styles += style + separator
        return styles[:-len(separator)]
