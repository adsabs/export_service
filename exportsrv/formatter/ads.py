# -*- coding: utf-8 -*-

# these three classes are basically just enums, verifying valid members

class adsFormatter:
    """
    We are supporting four formats (unicode, html, latex, and csv) for custom format,
    for most of csl formats, we are supporting the first three only (unicode, html, and latex).
    There are formats that are inherently xml, or latex.
    The csl formats, listed below in ads_CLS, are the ones that can encoded as per user
    specification, and we assume that they are inherently unicode.

    """
    default, unicode, html, latex, csv, xml = range(6)

    native_latex = ['BibTex', 'BibTex Abs', '3']
    native_xml = ['DublinCore', 'Reference', 'ReferenceAbs']

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
        """
        this is called from /csl which only supports 3 formats of unicode, html, and latex
        :param format:
        :return:
        """
        if self.__is_number(format):
            format = int(format)
            if (format == adsFormatter.unicode) or (format == adsFormatter.html) or (format == adsFormatter.latex):
                return True
        return False

    def native_encoding(self, native_format):
        """
        to determine which encoding to apply, unicode, xml, or latex
        :param native_format:
        :return:
        """
        if native_format in self.native_latex:
            return adsFormatter.latex
        if native_format in self.native_xml:
            return adsFormatter.xml
        return adsFormatter.unicode

class adsOrganizer:
    plain, citation_bibliography, bibliography = range(3)

class adsCSLStyle:
    ads_CLS = ['aastex', 'icarus', 'mnras', 'soph', 'aspc', 'apsj', 'aasj', 'ieee', 'agu', 'gsa', 'ams']

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

class adsJournalFormat:
    ads_journal_Format = default, macro, abbreviated, full = range(4)

    def verify(self, style):
        """

        :param style:
        :return:
        """
        # allow `style` to be an integer (ie, 0, 1, ...)
        if isinstance(style, int):
            if 0 <= style < 4:
                return True

        # allow `style` to be a string (ie, '0', '1', ...)
        if isinstance(style, str):
            format = int(style)
            if 0 <= format < 4:
                return True

        if (style in self.ads_journal_Format):
            return True

        return False


class adsOutputFormat:
    ads_output_format = default, classic, individual = range(3)

    def verify(self, format):
        """

        :param format:
        :return:
        """
        # allow `format` to be an integer (ie, 0, 1, ...)
        if isinstance(format, int):
            if 0 <= format < 3:
                return self.ads_output_format[format]

        # allow `format` to be a string (ie, '0', '1', ...)
        if isinstance(format, str):
            format = int(format)
            if 0 <= format < 3:
                return self.ads_output_format[format]

        if (format in self.ads_output_format):
            return format

        return None


adsOutputFormat().verify("2")