# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest
import mock

from collections import OrderedDict

import exportsrv.app as app

from exportsrv.tests.unittests.stubdata import solrdata
from exportsrv.formatter.csl import CSL, adsFormatter
from exportsrv.formatter.customFormat import CustomFormat
from exportsrv.utils import get_solr_data

class TestExportsCustomFormat(TestCase):

    maxDiff = None

    def create_app(self):
        self.current_app = app.create_app()
        return self.current_app

    def test_export_format(self):
        custom_format = CustomFormat(custom_format=r'')
        # init unicode (also accepting UTF-8 for backward compatibility)
        custom_format._CustomFormat__set_export_format('utf-8')
        assert (custom_format.export_format == adsFormatter.unicode)
        custom_format._CustomFormat__set_export_format('unicode')
        assert (custom_format.export_format == adsFormatter.unicode)
        # init html
        custom_format._CustomFormat__set_export_format('html')
        assert (custom_format.export_format == adsFormatter.html)
        # init latex
        custom_format._CustomFormat__set_export_format('latex')
        assert (custom_format.export_format == adsFormatter.latex)
        # anything else is init to unicode
        custom_format._CustomFormat__set_export_format('')
        assert (custom_format.export_format == adsFormatter.unicode)


    def test_parse_enumeration(self):
        # enumeration is included
        custom_format = CustomFormat(custom_format=r'%zn%10i %(Y), %T,%\J,%\V,%\p')
        custom_format._CustomFormat__parse_enumeration()
        assert (custom_format.enumeration == True)

        # enumeration is not included
        custom_format = CustomFormat(custom_format=r'%10i %(Y), %T,%\J,%\V,%\p')
        custom_format._CustomFormat__parse_enumeration()
        assert (custom_format.enumeration == False)


    def test_parse_command(self):
        # command is included
        custom_format = CustomFormat(custom_format=r'%ZEncoding:latex %ZHeader:"at the top of the page" %ZFooter:"at the bottom of the page" %ZLinelength:100 %zn\\item %N,%Y,{\\em %J\}, \{\\bf %V\}, %p--%P (%c citations)\n')
        custom_format._CustomFormat__parse_command()
        assert (custom_format.export_format == adsFormatter.latex)
        assert (custom_format.line_length == 100)
        assert (custom_format.header == 'at the top of the page')
        assert (custom_format.footer == 'at the bottom of the page')

        # command is not included, so check for default initialization
        custom_format = CustomFormat(custom_format=r'\\item %N,%Y,{\\em %J\}, \{\\bf %V\}, %p--%P (%c citations)\n')
        custom_format._CustomFormat__parse_command()
        assert (custom_format.export_format == adsFormatter.unicode)
        assert (custom_format.line_length == 0)
        assert (custom_format.header == '')
        assert (custom_format.footer == '')


    def test_format_date(self):
        custom_format = CustomFormat(custom_format=r'')

        # format year
        assert(custom_format._CustomFormat__format_date('2017-06-01', 'Y') == '2017')
        # format date
        assert(custom_format._CustomFormat__format_date('2017-06-01', 'D') == '06/2017')


    def test_format_url(self):
        custom_format = CustomFormat(custom_format=r'')

        # long format
        assert(custom_format._CustomFormat__format_url('2018ApJS..236...24F', 'U') == '<a href="https://ui.adsabs.harvard.edu/abs/2018ApJS..236...24F">2018ApJS..236...24F</a>')
        # short format
        assert(custom_format._CustomFormat__format_url('2018ApJS..236...24F', 'u') == 'https://ui.adsabs.harvard.edu/abs/2018ApJS..236...24F')
        # no bibcode
        assert(custom_format._CustomFormat__format_url('', 'U') == '')
        assert(custom_format._CustomFormat__format_url('', 'u') == '')


    def test_get_affiliation_list(self):
        custom_format = CustomFormat(custom_format=r'')
        custom_format.set_json_from_solr(solrdata.data_3)

        # with affiliation
        a_doc = solrdata.data_3['response'].get('docs')[0]
        expected_aff_list = u"AA(Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada; Space Telescope Science Institute, Baltimore, MD); " \
                            u"AB(Department of Physics and Astronomy, University of Calgary, Calgary, Alberta, T2N 1N4, Canada); " \
                            u"AC(Department de Physique, Université de Montréal, Montréal, Québec, H3C 3J7, Canada); " \
                            u"AD(Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada); " \
                            u"AE(Department of Physics and Astronomy, University of Western Ontario, London, Ontario, N6A 3K7, Canada); " \
                            u"AF(University of Toronto, 60 St. George Street, Toronto, Ontario, M5S 3H8, Canada)"
        assert (custom_format._CustomFormat__get_affiliation_list(a_doc) == expected_aff_list)

        # without affiliation
        a_doc = dict(a_doc)
        a_doc.pop('aff')
        assert (custom_format._CustomFormat__get_affiliation_list(a_doc) == '')


    def test_get_affiliation_list_limit(self):
        custom_format = CustomFormat(custom_format=r'%2F')
        custom_format.set_json_from_solr(solrdata.data_3)

        # with only 2 affiliations
        a_doc = solrdata.data_3['response'].get('docs')[0]
        expected_aff_list = "AA(Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada; Space Telescope Science Institute, Baltimore, MD); " \
                            "AB(Department of Physics and Astronomy, University of Calgary, Calgary, Alberta, T2N 1N4, Canada)"
        assert (custom_format._CustomFormat__get_affiliation_list(a_doc) == expected_aff_list)


    def test_get_author_list(self):
        # Optional parameters for author field: n.m
        # If the number of authors in the list is larger than n, the list will be truncated and m authors are returned
        custom_format = CustomFormat(custom_format=r'%A,%3.2A,%a,%3.2a,%G,%3.2G,%g,%3.2g,'
                                                   r'%H,%3.2H,%2.1H,%h,%3.2h,%I,%3.2I,%i,%3.2i,'
                                                   r'%L,%3.2L,%l,%3.2l,%M,%3.2M,%m,%3.2m,'
                                                   r'%N,%3.2N,%n,%3.2n,%e,%3.2e,%f,%3.2f,'
                                                   r'%O,%3.2O,%o,%3.2o,%k,%3.2k,'
                                                   r'%^A,%^a,%^G,%^g,%^H,%^h,%^I,%^i,%^L,%^l,%^M,%^m,%^N,%^n,%^e,%^f,'
                                                   r'%^O,%^o,%^k'
        )
        custom_format.set_json_from_solr(solrdata.data_3)

        # acutal data from solr: ['English, Jayanne', 'Taylor, A. R.', 'Mashchenko, S. Y.', 'Irwin, Judith A.', 'Basu, Shantanu', 'Johnstone, Doug']
        author_format = OrderedDict([
                            ('%A', 'English, Jayanne, Taylor, A. R., Mashchenko, S. Y., Irwin, Judith A., Basu, Shantanu, and Johnstone, Doug'),
                            ('%3.2A', 'English, Jayanne, Taylor, A. R., and 4 colleagues'),
                            ('%a', 'English, Jayanne, Taylor, A. R., Mashchenko, S. Y., Irwin, Judith A., Basu, Shantanu, & Johnstone, Doug'),
                            ('%3.2a', 'English, Jayanne, Taylor, A. R., et al.'),
                            ('%G', 'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S., Johnstone, D.'),
                            ('%3.2G', 'English, J., Taylor, A. R., et al.'),
                            ('%g', 'English J., Taylor A. R., Mashchenko S. Y., Irwin J. A., Basu S., Johnstone D.'),
                            ('%3.2g', 'English J., Taylor A. R., et al.'),
                            ('%H', 'English'),
                            ('%3.2H', 'English Taylor'),
                            ('%2.1H', 'English'),
                            ('%h', 'English'),
                            ('%3.2h', 'English Taylor'),
                            ('%I', 'English, J., A. R. Taylor, S. Y. Mashchenko, J. A. Irwin, S. Basu, and D. Johnstone'),
                            ('%3.2I', 'English, J., A. R. Taylor, and 4 colleagues'),
                            ('%i', 'English, J., A. R. Taylor, S. Y. Mashchenko, J. A. Irwin, S. Basu, & D. Johnstone'),
                            ('%3.2i', 'English, J., A. R. Taylor, et al.'),
                            ('%L',  'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S., and Johnstone, D.'),
                            ('%3.2L',  'English, J., Taylor, A. R., and 4 colleagues'),
                            ('%l',  'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S., & Johnstone, D.'),
                            ('%3.2l',  'English, J., Taylor, A. R., et al.'),
                            ('%M', 'English, Taylor, Mashchenko, Irwin, Basu, and Johnstone'),
                            ('%3.2M', 'English, Taylor et al.'),
                            ('%m', 'English, Taylor, Mashchenko, Irwin, Basu, & Johnstone'),
                            ('%3.2m', 'English, Taylor et al.'),
                            ('%N', 'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S., Johnstone, D.'),
                            ('%3.2N',  'English, J., Taylor, A. R., and 4 colleagues'),
                            ('%n',  'English,+'),
                            ('%3.2n',  'English,+'),
                            ('%e', 'English, J., Taylor, A.R., Mashchenko, S.Y., Irwin, J.A., Basu, S., and Johnstone, D.'),
                            ('%3.2e', 'English, J., Taylor, A.R., and 4 colleagues'),
                            ('%f', 'English, Taylor, Mashchenko, Irwin, Basu, and Johnstone'),
                            ('%3.2f', 'English, Taylor \\emph{et al.}'),
                            ('%O', 'J. English, A. R. Taylor, S. Y. Mashchenko, J. A. Irwin, S. Basu, and D. Johnstone'),
                            ('%3.2O', 'J. English, A. R. Taylor, and 4 colleagues'),
                            ('%o', 'J. English, A. R. Taylor, S. Y. Mashchenko, J. A. Irwin, S. Basu, & D. Johnstone'),
                            ('%3.2o', 'J. English, A. R. Taylor, et al.'),
                            ('%k', 'Jayanne English, A. R. Taylor, S. Y. Mashchenko, Judith A. Irwin, Shantanu Basu, and Doug Johnstone'),
                            ('%3.2k', 'Jayanne English, A. R. Taylor, et al.'),
                            ('%^A', 'English, Jayanne'),
                            ('%^a', 'English, Jayanne'),
                            ('%^G', 'English, J.'),
                            ('%^g', 'English J.'),
                            ('%^H', 'English'),
                            ('%^h', 'English'),
                            ('%^I', 'English, J.'),
                            ('%^i', 'English, J.'),
                            ('%^L', 'English, J.'),
                            ('%^l', 'English, J.'),
                            ('%^M', 'English'),
                            ('%^m', 'English'),
                            ('%^N', 'English, J.'),
                            ('%^n', 'English'),
                            ('%^e', 'English, J.'),
                            ('%^f', 'English'),
                            ('%^O', 'J. English'),
                            ('%^o', 'J. English'),
                            ('%^k', 'Jayanne English'),
        ])
        for key, value in author_format.items():
            assert (custom_format._CustomFormat__get_author_list(format=key, index=0) == value)


    def test_get_keywords(self):
        custom_format = CustomFormat(custom_format=r'')
        custom_format.set_json_from_solr(solrdata.data_3)

        # with keywords
        a_doc = solrdata.data_3['response'].get('docs')[0]
        expected_keywords = "GALAXY: HALO, GALAXY: STRUCTURE, ISM: BUBBLES, ISM: INDIVIDUAL: ALPHANUMERIC: GW 123.4-1.5, ISM: STRUCTURE, Astrophysics"
        assert (custom_format._CustomFormat__get_keywords(a_doc) == expected_keywords)

        # without keywords
        a_doc = dict(a_doc)
        a_doc.pop('keyword')
        assert (custom_format._CustomFormat__get_keywords(a_doc) == '')


    def test_add_clean_pub_raw(self):
        custom_format = CustomFormat(custom_format=r'')
        custom_format.set_json_from_solr(solrdata.data)

        # need clean up
        a_doc = solrdata.data['response'].get('docs')[16]
        assert (custom_format._CustomFormat__add_clean_pub_raw(a_doc) == 'American Astronomical Society Meeting 210, id.21.04')

        # no change required
        a_doc = solrdata.data['response'].get('docs')[17]
        assert (custom_format._CustomFormat__add_clean_pub_raw(a_doc) == 'Research Journal of Physics, vol. 1, issue 1, pp. 35-41')


    def test_get_publication(self):
        custom_format = CustomFormat(custom_format=r'')
        custom_format.set_json_from_solr(solrdata.data_3)

        publication_format = {
                            '%J':'The Astrophysical Journal',
                            '%j':'\\apjl',
                            '%Q':'The Astrophysical Journal, Volume 533, Issue 1, pp. L25-L28.',
                            '%q':'ApJL',
                            '%%':'',
        }
        a_doc = solrdata.data_3['response'].get('docs')[0]
        for key, value in publication_format.items():
            assert (custom_format._CustomFormat__get_publication(key, a_doc) == value)

    def test_encode(self):
        custom_format = CustomFormat(custom_format=r'')

        # encoding is unicode, pass in abstract
        custom_format._CustomFormat__set_export_format('unicode')
        abstract = "The concept of using lunar beacon signal transmission for on-board navigation for earth satellites and near-earth spacecraft is described. The system would require powerful transmitters on the earth-side of the moon's surface and black box receivers with antennae and microprocessors placed on board spacecraft for autonomous navigation. Spacecraft navigation requires three position and three velocity elements to establish location coordinates. Two beacons could be soft-landed on the lunar surface at the limits of allowable separation and each would transmit a wide-beam signal with cones reaching GEO heights and be strong enough to be received by small antennae in near-earth orbit. The black box processor would perform on-board computation with one-way Doppler/range data and dynamical models. Alternatively, GEO satellites such as the GPS or TDRSS spacecraft can be used with interferometric techniques to provide decimeter-level accuracy for aircraft navigation."
        assert (custom_format._CustomFormat__encode(value=abstract, field='abstract') == abstract)

        # encoding is html
        custom_format._CustomFormat__set_export_format('html')
        abstract = "<a>some text with &</a>"
        abstract_escaped = "&lt;a&gt;some text with &amp;&lt;/a&gt;"
        assert (custom_format._CustomFormat__encode(value=abstract, field='abstract') == abstract_escaped)

        # encoding is latex
        custom_format._CustomFormat__set_export_format('latex')
        # for author => convert to latex for author
        author = u'Fjörtoft, R.'
        author_latex = r'Fj{\"o}rtoft, R.'
        assert (custom_format._CustomFormat__encode(value=author, field='author') == author_latex)
        # for pub => no changes
        pub_raw = "Sensing and Imaging, Volume 18, Issue 1, article id.17, <NUMPAGES>12</NUMPAGES> pp."
        assert (custom_format._CustomFormat__encode(value=pub_raw, field='pub') == pub_raw)
        # for everything else => convert to latex
        abstract = u"Chapter 2: As part of the Bluedisk survey we analyse the radial gas-phase metallicity profiles of 50 late-type galaxies. We compare the metallicity profiles of a sample of HI-rich galaxies against a control sample of HI-'normal' galaxies. We find the metallicity gradient of a galaxy to be strongly correlated with its HI mass fraction {M}{HI}) / {M}_{\ast}). We note that some galaxies exhibit a steeper metallicity profile in the outer disc than in the inner disc. These galaxies are found in both the HI-rich and control samples. This contradicts a previous indication that these outer drops are exclusive to HI-rich galaxies. These effects are not driven by bars, although we do find some indication that barred galaxies have flatter metallicity profiles. By applying a simple analytical model we are able to account for the variety of metallicity profiles that the two samples present. The success of this model implies that the metallicity in these isolated galaxies may be in a local equilibrium, regulated by star formation. This insight could provide an explanation of the observed local mass-metallicity relation. Chapter 3 We present a method to recover the gas-phase metallicity gradients from integral field spectroscopic (IFS) observations of barely resolved galaxies. We take a forward modelling approach and compare our models to the observed spatial distribution of emission line fluxes, accounting for the degrading effects of seeing and spatial binning. The method is flexible and is not limited to particular emission lines or instruments. We test the model through comparison to synthetic observations and use downgraded observations of nearby galaxies to validate this work. As a proof of concept we also apply the model to real IFS observations of high-redshift galaxies. From our testing we show that the inferred metallicity gradients and central metallicities are fairly insensitive to the assumptions made in the model and that they are reliably recovered for galaxies with sizes approximately equal to the half width at half maximum of the point-spread function. However, we also find that the presence of star forming clumps can significantly complicate the interpretation of metallicity gradients in moderately resolved high-redshift galaxies. Therefore we emphasize that care should be taken when comparing nearby well-resolved observations to high-redshift observations of partially resolved galaxies. Chapter 4 We present gas-phase metallicity gradients for 94 star-forming galaxies between (0.08 < z < 0.84). We find a negative median metallicity gradient of (-0.043^{+0.009}_{-0.007}, dex/kpc), i.e. on average we find the centres of these galaxies to be more metal-rich than their outskirts. However, there is significant scatter underlying this and we find that 10% (9) galaxies have significantly positive metallicity gradients, 39% (37) have significantly negative gradients, 28% (26) have gradients consistent with being flat, the remainder 23% (22) are considered to have unreliable gradient estimates. We find a slight trend for a more negative metallicity gradient with both increasing stellar mass and increasing star formation rate (SFR). However, given the potential redshift and size selection effects, we do not consider these trends to be significant. Indeed when we normalize the SFR of our galaxies relative to the main sequence, we do not observe any trend between the metallicity gradient and the normalized SFR. This finding is contrary to other recent studies of galaxies at similar and higher redshifts. We do, however, identify a novel trend between the metallicity gradient of a galaxy and its size. Small galaxies ((r_d < 3 kpc)) present a large spread in observed metallicity gradients (both negative and positive gradients). In contrast, we find no large galaxies (r_d > 3 kpc) with positive metallicity gradients, and overall there is less scatter in the metallicity gradient amongst the large galaxies. We suggest that these large (well-evolved) galaxies may be analogues of galaxies in the present-day Universe, which also present a common negative metallicity gradient. Chapter 5 The relationship between a galaxy's stellar mass and its gas-phase metallicity results from the complex interplay between star formation and the inflow and outflow of gas. Since the gradient of metals in galaxies is also influenced by the same processes, it is therefore natural to contrast the metallicity gradient with the mass-metallicity relation. Here we study the interrelation of the stellar mass, central metallicity and metallicity gradient, using a sample of 72 galaxies spanning (0.13 < z < 0.84) with reliable metallicity gradient estimates. We find that typically the galaxies that fall below the mean mass-metallicity relation have flat or inverted metallicity gradients. We quantify their relationship taking full account of the covariance between the different variables and find that at fixed mass the central metallicity is anti-correlated with the metallicity gradient. We argue that this is consistent with a scenario that suppresses the central metallicity either through the inflow of metal poor gas or outflow of metal enriched gas."
        abstract_latex = u"Chapter 2: As part of the Bluedisk survey we analyse the radial gas-phase metallicity profiles of 50 late-type galaxies. We compare the metallicity profiles of a sample of HI-rich galaxies against a control sample of HI-'normal' galaxies. We find the metallicity gradient of a galaxy to be strongly correlated with its HI mass fraction \{M\}\{HI\}) / \{M\}\_\{\x07st\}). We note that some galaxies exhibit a steeper metallicity profile in the outer disc than in the inner disc. These galaxies are found in both the HI-rich and control samples. This contradicts a previous indication that these outer drops are exclusive to HI-rich galaxies. These effects are not driven by bars, although we do find some indication that barred galaxies have flatter metallicity profiles. By applying a simple analytical model we are able to account for the variety of metallicity profiles that the two samples present. The success of this model implies that the metallicity in these isolated galaxies may be in a local equilibrium, regulated by star formation. This insight could provide an explanation of the observed local mass-metallicity relation. Chapter 3 We present a method to recover the gas-phase metallicity gradients from integral field spectroscopic (IFS) observations of barely resolved galaxies. We take a forward modelling approach and compare our models to the observed spatial distribution of emission line fluxes, accounting for the degrading effects of seeing and spatial binning. The method is flexible and is not limited to particular emission lines or instruments. We test the model through comparison to synthetic observations and use downgraded observations of nearby galaxies to validate this work. As a proof of concept we also apply the model to real IFS observations of high-redshift galaxies. From our testing we show that the inferred metallicity gradients and central metallicities are fairly insensitive to the assumptions made in the model and that they are reliably recovered for galaxies with sizes approximately equal to the half width at half maximum of the point-spread function. However, we also find that the presence of star forming clumps can significantly complicate the interpretation of metallicity gradients in moderately resolved high-redshift galaxies. Therefore we emphasize that care should be taken when comparing nearby well-resolved observations to high-redshift observations of partially resolved galaxies. Chapter 4 We present gas-phase metallicity gradients for 94 star-forming galaxies between (0.08 < z < 0.84). We find a negative median metallicity gradient of (-0.043\^\{+0.009\}\_\{-0.007\}, dex/kpc), i.e. on average we find the centres of these galaxies to be more metal-rich than their outskirts. However, there is significant scatter underlying this and we find that 10\% (9) galaxies have significantly positive metallicity gradients, 39\% (37) have significantly negative gradients, 28\% (26) have gradients consistent with being flat, the remainder 23\% (22) are considered to have unreliable gradient estimates. We find a slight trend for a more negative metallicity gradient with both increasing stellar mass and increasing star formation rate (SFR). However, given the potential redshift and size selection effects, we do not consider these trends to be significant. Indeed when we normalize the SFR of our galaxies relative to the main sequence, we do not observe any trend between the metallicity gradient and the normalized SFR. This finding is contrary to other recent studies of galaxies at similar and higher redshifts. We do, however, identify a novel trend between the metallicity gradient of a galaxy and its size. Small galaxies ((r\_d < 3 kpc)) present a large spread in observed metallicity gradients (both negative and positive gradients). In contrast, we find no large galaxies (r\_d > 3 kpc) with positive metallicity gradients, and overall there is less scatter in the metallicity gradient amongst the large galaxies. We suggest that these large (well-evolved) galaxies may be analogues of galaxies in the present-day Universe, which also present a common negative metallicity gradient. Chapter 5 The relationship between a galaxy's stellar mass and its gas-phase metallicity results from the complex interplay between star formation and the inflow and outflow of gas. Since the gradient of metals in galaxies is also influenced by the same processes, it is therefore natural to contrast the metallicity gradient with the mass-metallicity relation. Here we study the interrelation of the stellar mass, central metallicity and metallicity gradient, using a sample of 72 galaxies spanning (0.13 < z < 0.84) with reliable metallicity gradient estimates. We find that typically the galaxies that fall below the mean mass-metallicity relation have flat or inverted metallicity gradients. We quantify their relationship taking full account of the covariance between the different variables and find that at fixed mass the central metallicity is anti-correlated with the metallicity gradient. We argue that this is consistent with a scenario that suppresses the central metallicity either through the inflow of metal poor gas or outflow of metal enriched gas."
        assert (custom_format._CustomFormat__encode(value=abstract, field='abstract') == abstract_latex)
        # test double quotes
        comment = u"""The NASA Astrophysics Data System is phasing out support for its legacy interface ("ADS Classic") in favor of a more modern, featureful system ("the new ADS")."""
        comment_latex = u"The NASA Astrophysics Data System is phasing out support for its legacy interface (``ADS Classic'') in favor of a more modern, featureful system (``the new ADS'')."
        assert (custom_format._CustomFormat__encode(value=comment, field='comment') == comment_latex)

    def test_author_sep(self):
        # verify when missing it is False
        custom_format = CustomFormat(custom_format=r'%ZEncoding:latex %ZHeader:"at the top of the page" %ZFooter:"at the bottom of the page" %ZLinelength:100 %zn\\item %N,%Y,{\\em %J\}, \{\\bf %V\}, %p--%P (%c citations)\n')
        custom_format._CustomFormat__parse_command()
        assert (len(custom_format.author_sep) == 0)

        # verify when the parameter is defined, comma is replaced by the defined seprator
        custom_format = CustomFormat(custom_format=r'%ZAuthorSep:"; " %A')
        custom_format.set_json_from_solr(solrdata.data_3)
        author_list_with_new_sep = u'English, Jayanne; Taylor, A. R.; Mashchenko, S. Y.; Irwin, Judith A.; Basu, Shantanu; and Johnstone, Doug'
        assert (custom_format._CustomFormat__get_author_list('%A', index=0) == author_list_with_new_sep)

    def test_markup_strip(self):
        # verify when missing it is False
        custom_format = CustomFormat(custom_format=r'%ZEncoding:latex %ZHeader:"at the top of the page" %ZFooter:"at the bottom of the page" %ZLinelength:100 %zn\\item %N,%Y,{\\em %J\}, \{\\bf %V\}, %p--%P (%c citations)\n')
        custom_format._CustomFormat__parse_command()
        assert (custom_format.markup_strip == False)

        # verify when the parameter is keep it is False and the no markup is removed
        custom_format = CustomFormat(custom_format=r'%ZMarkup:keep %B\n')
        custom_format._CustomFormat__parse_command()
        assert (custom_format.markup_strip == False)
        abstract = u"We present a large grid of stellar evolutionary tracks, which are suitable to modelling star clusters and galaxies by means of population synthesis. The tracks are presented for the initial chemical compositions [Z=0.0004, Y=0.23], [Z=0.001, Y=0.23], [Z=0.004, Y=0.24], [Z=0.008, Y=0.25], [Z=0.019, Y=0.273] (solar composition), and [Z=0.03, Y=0.30]. They are computed with updated opacities and equation of state, and a moderate amount of convective overshoot. The range of initial masses goes from 0.15 M<SUB>sun</SUB> to 7 M<SUB>sun</SUB>, and the evolutionary phases extend from the zero age main sequence (ZAMS) till either the thermally pulsing AGB regime or carbon ignition. We also present an additional set of models with solar composition, computed using the classical Schwarzschild criterion for convective boundaries. From all these tracks, we derive the theoretical isochrones in the Johnson-Cousins UBVRIJHK broad-band photometric system."
        abstract_with_markup = abstract
        assert (custom_format._CustomFormat__encode(value=abstract, field='abstract') == abstract_with_markup)

        # verify when the parameter is strip it is True and the markup is removed
        custom_format = CustomFormat(custom_format=r'%ZMarkup:strip %B\n')
        custom_format._CustomFormat__parse_command()
        assert (custom_format.markup_strip == True)
        abstract_without_markup = u"We present a large grid of stellar evolutionary tracks, which are suitable to modelling star clusters and galaxies by means of population synthesis. The tracks are presented for the initial chemical compositions [Z=0.0004, Y=0.23], [Z=0.001, Y=0.23], [Z=0.004, Y=0.24], [Z=0.008, Y=0.25], [Z=0.019, Y=0.273] (solar composition), and [Z=0.03, Y=0.30]. They are computed with updated opacities and equation of state, and a moderate amount of convective overshoot. The range of initial masses goes from 0.15 Msun to 7 Msun, and the evolutionary phases extend from the zero age main sequence (ZAMS) till either the thermally pulsing AGB regime or carbon ignition. We also present an additional set of models with solar composition, computed using the classical Schwarzschild criterion for convective boundaries. From all these tracks, we derive the theoretical isochrones in the Johnson-Cousins UBVRIJHK broad-band photometric system."
        assert (custom_format._CustomFormat__encode(value=abstract, field='abstract') == abstract_without_markup)

    def test_field_encoding(self):
        # latex field encoding
        custom_format = CustomFormat(custom_format=r'%\A')
        custom_format.set_json_from_solr(solrdata.data_4)
        author_list_encoded = u'Ryan, R.~E. and McCullough, P.~R.'
        assert (custom_format._CustomFormat__encode(value=custom_format._CustomFormat__get_author_list(format=r'%\A', index=0),
                                                    field='author', field_format=r'%\A') == author_list_encoded)
        # html field encoding
        abstract = u"We present a large grid of stellar evolutionary tracks, which are suitable to modelling star clusters and galaxies by means of population synthesis. The tracks are presented for the initial chemical compositions [Z=0.0004, Y=0.23], [Z=0.001, Y=0.23], [Z=0.004, Y=0.24], [Z=0.008, Y=0.25], [Z=0.019, Y=0.273] (solar composition), and [Z=0.03, Y=0.30]. They are computed with updated opacities and equation of state, and a moderate amount of convective overshoot. The range of initial masses goes from 0.15 M<SUB>sun</SUB> to 7 M<SUB>sun</SUB>, and the evolutionary phases extend from the zero age main sequence (ZAMS) till either the thermally pulsing AGB regime or carbon ignition. We also present an additional set of models with solar composition, computed using the classical Schwarzschild criterion for convective boundaries. From all these tracks, we derive the theoretical isochrones in the Johnson-Cousins UBVRIJHK broad-band photometric system."
        abstract_html = "We present a large grid of stellar evolutionary tracks, which are suitable to modelling star clusters and galaxies by means of population synthesis. The tracks are presented for the initial chemical compositions [Z=0.0004, Y=0.23], [Z=0.001, Y=0.23], [Z=0.004, Y=0.24], [Z=0.008, Y=0.25], [Z=0.019, Y=0.273] (solar composition), and [Z=0.03, Y=0.30]. They are computed with updated opacities and equation of state, and a moderate amount of convective overshoot. The range of initial masses goes from 0.15 M&lt;SUB&gt;sun&lt;/SUB&gt; to 7 M&lt;SUB&gt;sun&lt;/SUB&gt;, and the evolutionary phases extend from the zero age main sequence (ZAMS) till either the thermally pulsing AGB regime or carbon ignition. We also present an additional set of models with solar composition, computed using the classical Schwarzschild criterion for convective boundaries. From all these tracks, we derive the theoretical isochrones in the Johnson-Cousins UBVRIJHK broad-band photometric system."
        assert (custom_format._CustomFormat__encode(value=abstract, field='abstract', field_format='%>B') == abstract_html)

        # hex field encoding

        # url field encoding
        url = '<a href="http://adsabs.harvard.edu/abs/1997AAS...190.1403E">1997AAS...190.1403E</a>'
        url_encoded = '<a+href=%22http://adsabs.harvard.edu/abs/1997AAS...190.1403E%22>1997AAS...190.1403E</a>'
        assert (custom_format._CustomFormat__encode(value=url, field='url', field_format='%/U') == url_encoded)

    def test_end_record_insert(self):
        # verify string specified with %ZEOL gets inserted after each record
        # no EOL string
        custom_format = CustomFormat(custom_format=r'%ZEOL:"" %R')
        custom_format.set_json_from_solr(solrdata.data_6)
        assert (custom_format.get().get('export', '') == "2020AAS...23528705A2019EPSC...13.1911A2015scop.confE...3A2019AAS...23338108A2019AAS...23320704A2018EPJWC.18608001A2018AAS...23221409A2017ASPC..512...45A2018AAS...23136217A2018AAS...23130709A")
        # do not specify EOL string, and default linefeed is added in
        custom_format = CustomFormat(custom_format=r'%R')
        custom_format.set_json_from_solr(solrdata.data_6)
        assert (custom_format.get().get('export', '') == "2020AAS...23528705A\n2019EPSC...13.1911A\n2015scop.confE...3A\n2019AAS...23338108A\n2019AAS...23320704A\n2018EPJWC.18608001A\n2018AAS...23221409A\n2017ASPC..512...45A\n2018AAS...23136217A\n2018AAS...23130709A\n")
        # specify EOL string
        custom_format = CustomFormat(custom_format=r'%ZEOL:"--END" %R')
        custom_format.set_json_from_solr(solrdata.data_6)
        assert (custom_format.get().get('export', '') == "2020AAS...23528705A--END2019EPSC...13.1911A--END2015scop.confE...3A--END2019AAS...23338108A--END2019AAS...23320704A--END2018EPJWC.18608001A--END2018AAS...23221409A--END2017ASPC..512...45A--END2018AAS...23136217A--END2018AAS...23130709A--END")

    def test_page_count(self):
        # verify %pc outputs page_count properly
        formatted = [u'Yang, Huihui and Chen, Hongshan. (2017). 71, 191, 9 pp.\n',
                     u'Knapp, Wilfried and Thuemen, Chris. (2017). 13, 25, 6 pp.\n']
        custom_format = CustomFormat(custom_format=r'%A. (%Y). %q, %V, %p, %pc pp.')
        custom_format.set_json_from_solr(solrdata.data_8)
        assert (custom_format.get().get('export', '') == ''.join(formatted))

    def test_num_citiations(self):
        # verify %c outputs num_citations
        with mock.patch.object(self.current_app.client, 'get') as get_mock:
            get_mock.return_value = mock_response = mock.Mock()
            mock_response.json.return_value = solrdata.data_11
            mock_response.status_code = 200
            solr_data = get_solr_data(bibcodes=["2016ApJ...818L..26F"], fields='read_count,bibcode,doctype,[citations],bibstem',
                                      sort=self.current_app.config['EXPORT_SERVICE_NO_SORT_SOLR'])
            self.assertEqual(solr_data['response']['docs'][0]['num_citations'], 29)
        custom_format = CustomFormat(custom_format=r'%R: %c')
        custom_format.set_json_from_solr(solrdata.data_11)
        assert (custom_format.get().get('export', '') == "2016ApJ...818L..26F: 29\n")

    def test_escaping_literal(self):
        # verify for example %%R is translated to %R and not recognized as field ID bibcode
        formatted = [u'%R 2017EPJD...71..191Y\n%D 2017\n',
                     u'%R 2017JDSO...13...25K\n%D 2017\n']
        custom_format = CustomFormat(custom_format=u'%%R %R\n%%D %Y')
        custom_format.set_json_from_solr(solrdata.data_8)
        assert (custom_format.get().get('export', '') == r''.join(formatted))


if __name__ == '__main__':
    unittest.main()
