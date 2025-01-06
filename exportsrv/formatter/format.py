
import re
from itertools import product, islice
from string import ascii_uppercase

import xml.etree.cElementTree as ET

from exportsrv.formatter.ads import adsOutputFormat

class Format:
    """
    This is a parent class for all the formats that get data from solr to maniuplate.
    """
    status = -1
    from_solr = {}

    REGEX_REMOVE_TAGS_PUB_RAW = re.compile(r"(\<.*?\>)")
    REGEX_PUB_RAW = dict([
        (re.compile(r"(\;?\s*\<ALTJOURNAL\>.*\</ALTJOURNAL\>\s*)"), r""),  # remove these
        (re.compile(r"(\;?\s*\<CONF_METADATA\>.*\<CONF_METADATA\>\s*)"), r""),
        (re.compile(r"(?:\<ISBN\>)(.*)(?:\</ISBN\>)"), r"\1"),  # get value inside the tag for these
        (re.compile(r"(?:\<NUMPAGES\>)(.*)(?:</NUMPAGES>)"), r"\1"),
    ])
    REGEX_ABBREVIATION = re.compile(r'^[^.]*')


    def __init__(self, from_solr):
        """

        :param from_solr:
        """
        if from_solr is not None:
            self.from_solr = from_solr
            if (self.from_solr.get('responseHeader')):
                self.status = self.from_solr['responseHeader'].get('status', self.status)

        self.xml_placeholder_references = ''

    def get_status(self):
        """

        :return: status of solr query
        """
        return self.status

    def get_num_docs(self):
        """

        :return: number of docs returned by solr query
        """
        if (self.status == 0):
            if (self.from_solr.get('response')):
                return self.from_solr['response'].get('numFound', 0)
        return 0

    def generate_counter_id(self, length):
        """
        Generate two-character labels, if run out, then move to three characters
        :param length:
        :return:
        """
        if length < 26**2:
            return [''.join(i) for i in islice(product(ascii_uppercase, repeat=2), 0, length)]
        return [''.join(i) for i in islice(product(ascii_uppercase, repeat=2), 0, 26**2)] + \
               [''.join(i) for i in islice(product(ascii_uppercase, repeat=3), 0, length-(26**2))]

    def get_pub_abbrev(self, bibstem):
        """

        :param bibstem:
        :return:
        """
        if len(bibstem) == 2:
            short, long = bibstem[0], bibstem[1]
            if re.match(r'^[\.\d]+$', long[5:9]):
                # is a serial publication, use short bibstem
                return short.replace('.', '')
            else:
                # is book/conference/arxiv, use long bibstem
                return re.sub(r'\.+$', '', long)
        return self.get_bibstem(bibstem)

    def get_bibstem(self, bibstem):
        """

        :param bibstem:
        :return:
        """
        if len(bibstem) > 0:
            return bibstem[0]
        return ''

    def add_xml_placeholder_references(self, parent, tag):
        """

        :param parent:
        :param tag:
        :return:
        """
        ET.SubElement(parent, tag).text = "references section"
        self.xml_placeholder_references = f'<{tag}>references section</{tag}>'

    def get_top_and_bottom_xml_references(self, xml_string):
        """

        :param xml_string:
        :return:
        """
        parts = xml_string.split(self.xml_placeholder_references)
        return parts[0], parts[1].lstrip('\n')

    def formatted_export(self, output_format, num_docs, references, bibcodes, separator, header='', footer=''):
        """

        :param output_format:
        :param num_docs:
        :param references:
        :param bibcodes:
        :param separator:
        :param header:
        :param footer:
        :return:
        """
        if output_format == adsOutputFormat.default:
            return ''.join(references)

        if output_format == adsOutputFormat.classic:
            export = ''
            if len(header) > 0:
                export += header + separator
            export += separator.join(references) + separator
            if len(footer) > 0:
                export += separator + footer

            result_dict = {}
            result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
            result_dict['export'] = export
            return result_dict

        if output_format == adsOutputFormat.individual:
            result_dict = {}
            result_dict['num_docs'] = num_docs
            result_dict['docs'] = []
            for bibcode, reference in zip(bibcodes, references):
                result_dict['docs'].append({'bibcode': bibcode, 'reference': reference})
            if len(header) > 0:
                result_dict['header'] = header
            if len(footer) > 0:
                result_dict['footer'] = footer
            return result_dict
