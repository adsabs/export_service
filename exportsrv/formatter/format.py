
import re
from itertools import product
from string import ascii_uppercase

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
        if length < 26^2:
            return product(ascii_uppercase, repeat=2)
        return product(ascii_uppercase, repeat=3)

