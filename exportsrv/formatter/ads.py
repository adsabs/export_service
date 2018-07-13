# -*- coding: utf-8 -*-

# these three classes are basically just enums, verifying valid members

class adsFormatter:
    unicode, html, latex, csv = range(4)

    def __is_number(self, s):
        """

        :param s:
        :return:
        """
        try:
            int(s)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass
        return False

    def verify(self, format):
        if self.__is_number(format):
            format = int(format)
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
