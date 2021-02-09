# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import OrderedDict
from flask import current_app
from textwrap import fill

from exportsrv.formatter.format import Format

class RSSFormat(Format):

    def __get_BBB_base_url(self):
        return current_app.config.get('EXPORT_SERVICE_FROM_BBB_URL').rsplit('/', 1)[0]


    def __get_fields(self):
        """
        from solr to each types' tags

        :return:
        """
        fields = [('hybrid', 'title'), ('url', 'link'), ('abstract', 'description')]
        return OrderedDict(fields)


    def __get_author_title(self, a_doc):
        first_author = ''
        if 'author' in a_doc:
            first_author = a_doc['author'][0]
        title = ''.join(a_doc.get('title', ''))
        if len(first_author) > 0 and len(title) > 0:
            return first_author + ': ' + title
        if len(first_author) > 0:
            return first_author
        if len(title) > 0:
            return title
        return ''


    def __format_line_wrapped(self, text):
        """

        :param text:
        :return:
        """
        return fill(text, width=72)


    def __add_in(self, parent, field, value):
        """
        add the value into the return structure if a value was defined in Solr, otherwise add `Not Available`

        :param parent:
        :param field:
        :param value:
        :return:
        """
        if (len(value) > 0):
            ET.SubElement(parent, field).text = value
        else:
            ET.SubElement(parent, field).text = 'Not Available'


    def __get_doc(self, index, parent):
        """
        for each document from Solr, get the fields, and format them

        :param index:
        :param parent:
        :return:
        """
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields()
        item = ET.SubElement(parent, 'item')
        for field in fields:
            if (field == 'hybrid'):
                self.__add_in(item, fields[field], self.__get_author_title(a_doc))
            elif (field == 'url'):
                self.__add_in(item, fields[field], current_app.config.get('EXPORT_SERVICE_FROM_BBB_URL') + '/' + a_doc.get('bibcode', ''))
            elif (field == 'abstract'):
                self.__add_in(item, fields[field], self.__format_line_wrapped(a_doc.get(field, '')))


    def __get_rss(self, link):
        """

        :return:
        """
        num_docs = 0
        format = ''
        if (self.status == 0):
            # add header nodes
            rss = ET.Element("rss")
            rss.set('version', '2.0')
            channel = ET.SubElement(rss, "channel")
            ET.SubElement(channel, "title").text = 'ADS (Cites/AR query)'
            ET.SubElement(channel, "link").text = self.__format_line_wrapped(link if len(link) > 0 else self.__get_BBB_base_url())
            ET.SubElement(channel, "description").text = 'The SAO/NASA ADS Abstract service provides a search system for the Astronomy and Physics literature'
            image = ET.SubElement(channel, "image")
            ET.SubElement(image, "url").text = 'http://ads.harvard.edu/figs/ads_icon_144.png'
            ET.SubElement(image, "title").text = 'SAO/NASA ADS'
            ET.SubElement(image, "link").text = 'https://ui.adsabs.harvard.edu'
            ET.SubElement(image, "width").text = '144'
            ET.SubElement(image, "height").text = '122'
            # add data nodes
            num_docs = self.get_num_docs()
            for index in range(num_docs):
                self.__get_doc(index, channel)
            format = ET.tostring(rss, encoding='utf8', method='xml')
            format = (b'>\n<'.join(format.split(b'><')))
            format = format.replace(b'<item>', b'\n<item>')
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = format.decode('utf8')
        return result_dict


    def get(self, link=''):
        """

        :return: rss format
        """
        return self.__get_rss(link)
