
import re
from itertools import product, islice
from string import ascii_uppercase

from adsutils.ads_utils import get_pub_abbreviation

class Format:
    """
    This is a parent class for all the formats that get data from solr to maniuplate.
    """
    status = -1
    from_solr = {}

    REGEX_REMOVE_TAGS_PUB_RAW = re.compile("(\<.*?\>)")
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


    def get_pub_abbrev(self, pub, bibcode):
        """

        :param pub:
        :param bibcode:
        :return:
        """
        abbreviation = get_pub_abbreviation(pub, numBest=1, exact=False)
        if (len(abbreviation) > 0):
            return re.search(self.REGEX_ABBREVIATION, abbreviation[0][1]).group(0)
        # for now grab the bibstem from the bibcode until get_pub_abbreviation is fixed
        if len(bibcode) == 19:
            return re.search(self.REGEX_ABBREVIATION, bibcode[4:8]).group(0)
        return ''

    def get_main_bibstem(self, bibstem):
        """

        :param bibstem:
        :return:
        """
        if len(bibstem) > 0:
            return bibstem[0]
        return ''