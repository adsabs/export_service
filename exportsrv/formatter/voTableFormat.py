# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from datetime import datetime
from flask import current_app

from exportsrv.formatter.format import Format
from exportsrv.formatter.strftime import strftime

class VOTableFormat(Format):

    def __get_BBB_base_url(self):
        return current_app.config.get('EXPORT_SERVICE_FROM_BBB_URL').rsplit('/', 1)[0]


    def __tostring(self, data, num_docs):
        """

        :param data:
        :return:
        """
        # add schema
        votable = ET.Element("VOTABLE")
        votable.set("version", "1.1")
        description = ET.SubElement(votable, "DESCRIPTION")
        description.text = "\n   Results generated from the NASA Astrophysics Data System: {base_url}" \
                           "\n   For more information and support please contact ads@cfa.harvard.edu"\
                           "\n".format(base_url=self.__get_BBB_base_url())
        resource = ET.SubElement(votable, "RESOURCE")
        resource.set("type", "results")
        table = ET.SubElement(resource, "TABLE")
        description = ET.SubElement(table, "DESCRIPTION")
        description.text = "\n   ADS Search Results." \
                           "\n   Selected and retrieved {num_docs} records."\
                           "\n".format(num_docs=num_docs)
        fields = [("bibcode", "char" , "19", "The bibcode identifier for the record"), 
                  ("title", "char" , "*", "Title of the paper"), 
                  ("creator", "char" , "*", "List of authors"), 
                  ("source", "char" , "*", "Publication infromation"), 
                  ("date", "char" , "10", "Publication Date"), 
                  ("url", "char" , "*", "Resource URL")]
        for f in fields:
            field = ET.SubElement(table, "FIELD")
            field.set("ID", f[0])
            field.set("datatype", f[1])
            field.set("arraysize", f[2])
            description = ET.SubElement(field, "DESCRIPTION")
            description.text = f[3]
        # append the data and trun to string
        table.append(data)
        format_xml = ET.tostring(votable, encoding='utf8', method='xml')
        # apprently the functionality to add in the doctype is not avaialble in ET
        # so have to add it manually after the first line <?xml version='1.0' encoding='utf8'?>
        format_xml = format_xml.replace(b'?>', b'?><!DOCTYPE VOTABLE SYSTEM "http://cdsweb.u-strasbg.fr/xml/VOTable.dtd" >')
        # insert linefeed
        format_xml = (b'>\n<'.join(format_xml.split(b'><')))
        format_xml = format_xml.replace(b'</TR>', b'</TR>\n')
        # return the formatted string
        return format_xml.decode('utf8')


    def __get_fields(self):
        """
        solr fields

        :return:
        """
        return ['bibcode', 'title', 'author', 'pub_raw', 'pubdate', 'url']


    def __add_clean_pub_raw(self, a_doc):
        """
        parse pub_raw and eliminate tags

        :param a_doc:
        :return:
        """
        pub_raw = ''.join(a_doc.get('pub_raw', ''))
        # proceed only if necessary
        if ('<' in pub_raw) and ('>' in pub_raw):
            for key in self.REGEX_PUB_RAW:
                pub_raw = key.sub(self.REGEX_PUB_RAW[key], pub_raw)
        return pub_raw


    def __format_date(self, solr_date):
        """

        :param solr_date:
        :return:
        """
        # solr_date has the format 2017-12-01
        date_time = datetime.strptime(solr_date.replace('-00', '-01'), '%Y-%m-%d')
        return strftime(date_time, '%Y-%m-X%d').replace('X0', 'X').replace('X', '')


    def __add_in_table_data(self, parent, value):
        """
        add the value into the return structure, only if a value was defined in Solr

        :param parent:
        :param value:
        :return:
        """
        if (len(value) > 0):
            ET.SubElement(parent, 'TD').text = value
        else:
            ET.SubElement(parent, 'TD')


    def __get_doc(self, index, parent):
        """
        for each document from Solr, get the fields, and format them

        :param index:
        :param parent:
        :return:
        """
        a_doc = self.from_solr['response'].get('docs')[index]
        fields = self.__get_fields()
        row = ET.SubElement(parent, 'TR')
        for field in fields:
            if (field == 'bibcode'):
                self.__add_in_table_data(row, a_doc.get(field, ''))
            elif (field == 'title'):
                self.__add_in_table_data(row, ''.join(a_doc.get(field, '')))
            elif (field == 'author'):
                self.__add_in_table_data(row, '; '.join(a_doc.get(field, '')))
            elif (field == 'pub_raw'):
                self.__add_in_table_data(row, self.__add_clean_pub_raw(a_doc))
            elif (field == 'pubdate'):
                self.__add_in_table_data(row, self.__format_date(a_doc.get(field, '')))
            elif (field == 'url'):
                self.__add_in_table_data(row, current_app.config.get('EXPORT_SERVICE_FROM_BBB_URL') + '/' + a_doc.get('bibcode', ''))


    def __get_votable(self):
        """

        :return:
        """
        num_docs = 0
        format = ''
        if (self.status == 0):
            num_docs = self.get_num_docs()
            data = ET.Element("DATA")
            table = ET.SubElement(data, "TABLEDATA")
            for index in range(num_docs):
                self.__get_doc(index, table)
            format = self.__tostring(data, num_docs)
        result_dict = {}
        result_dict['msg'] = 'Retrieved {} abstracts, starting with number 1.'.format(num_docs)
        result_dict['export'] = format
        return result_dict


    def get(self):
        """

        :return: votable format
        """
        return self.__get_votable()
