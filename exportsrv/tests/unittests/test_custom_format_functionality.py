# -*- coding: utf-8 -*-

from flask_testing import TestCase
import unittest

import exportsrv.app as app

from stubdata import solrdata
from exportsrv.formatter.csl import CSL, adsFormatter
from exportsrv.formatter.customFormat import CustomFormat


class TestExportsCustomFormat(TestCase):
    def create_app(self):
        app_ = app.create_app()
        return app_

    def test_export_format(self):
        custom_format = CustomFormat(custom_format=r'')
        # init unicode
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
        assert (custom_format.line_length == 80)
        assert (custom_format.header == '')
        assert (custom_format.footer == '')


    def test_format_date(self):
        custom_format = CustomFormat(custom_format=r'')

        # format year
        assert(custom_format._CustomFormat__format_date('2017-06-01T00:00:00Z', 'Y') == '2017')
        # format date
        assert(custom_format._CustomFormat__format_date('2017-06-01T00:00:00Z', 'D') == '06/2017')


    def test_format_url(self):
        custom_format = CustomFormat(custom_format=r'')

        # long format
        assert(custom_format._CustomFormat__format_url('2018ApJS..236...24F', 'U') == '<a href="https://ui.adsabs.harvard.edu/#abs">2018ApJS..236...24F</a>')
        # short format
        assert(custom_format._CustomFormat__format_url('2018ApJS..236...24F', 'u') == 'https://ui.adsabs.harvard.edu/#abs/2018ApJS..236...24F')
        # no bibcode
        assert(custom_format._CustomFormat__format_url('', 'U') == '')
        assert(custom_format._CustomFormat__format_url('', 'u') == '')


    def test_get_affiliation_list(self):
        custom_format = CustomFormat(custom_format=r'')
        custom_format.set_json_from_solr(solrdata.data)

        # with affiliation
        a_doc = solrdata.data['response'].get('docs')[15]
        expected_aff_list = "AA(Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada; Space Telescope Science Institute, Baltimore, MD); " \
                            "AB(Department of Physics and Astronomy, University of Calgary, Calgary, Alberta, T2N 1N4, Canada); " \
                            "AC(Department de Physique, Universit\u00e9 de Montr\u00e9al, Montr\u00e9al, Qu\u00e9bec, H3C 3J7, Canada); " \
                            "AD(Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada); " \
                            "AE(Department of Physics and Astronomy, University of Western Ontario, London, Ontario, N6A 3K7, Canada); " \
                            "AF(University of Toronto, 60 St. George Street, Toronto, Ontario, M5S 3H8, Canada)"
        assert (custom_format._CustomFormat__get_affiliation_list(a_doc) == expected_aff_list)

        # without affiliation
        a_doc = dict(a_doc)
        a_doc.pop('aff')
        assert (custom_format._CustomFormat__get_affiliation_list(a_doc) == '')


    def test_get_author_list(self):
        custom_format = CustomFormat(custom_format=r'%A,%3.2A,%a,%3.2a,%G,%3.2G,%g,%3.2g,%H,%3.2H,%1.2H,%h,%3.2h,%I,%3.2I,'
                                                   r'%L,%3.2L,%l,%3.2l,%M,%3.2M,%m,%3.2m,%N,%3.2N,%n,%3.2n'
        )
        custom_format.set_json_from_solr(solrdata.data)

        author_format = {
                            '%A':'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S. and Johnstone, D.',
                            '%3.2A':'English, J., Taylor, A. R., et al.',
                            '%a':'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S. \& Johnstone, D.',
                            '%3.2a':'English, J., Taylor, A. R., et al.',
                            '%G':'English J. Taylor A. R. Mashchenko S. Y. Irwin J. A. Basu S. and Johnstone D.',
                            '%3.2G':'English J. Taylor A., et al.',
                            '%g':'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S., Johnstone, D.',
                            '%3.2g':'English, and 5 colleagues',
                            '%H':'English Taylor Mashchenko Irwin Basu and Johnstone',
                            '%3.2H':'English Taylor and Irwin',
                            '%1.2H':'English',
                            '%h':'English Taylor Mashchenko Irwin Basu and Johnstone',
                            '%3.2h':'English \emph{et al.}',
                            '%I':'English, J., A. R. Taylor, S. Y. Mashchenko, J. A. Irwin, S. Basu and D. Johnstone',
                            '%3.2I':'English, and 5 colleagues',
                            '%L': 'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S. and Johnstone, D.',
                            '%3.2L': 'English, and 5 colleagues',
                            '%M':'English, Taylor, Mashchenko, Irwin, Basu and Johnstone',
                            '%3.2M':'English, Taylor, et al.',
                            '%m':'English, Taylor, Mashchenko, Irwin, Basu \& Johnstone',
                            '%3.2m':'English, Taylor, et al.',
                            '%N':'English, J., Taylor, A. R., Mashchenko, S. Y., Irwin, J. A., Basu, S. and Johnstone, D.',
                            '%3.2N': 'English, and 5 colleagues',
                            '%n': 'English,+',
                            '%3.2n': 'English,+',
        }
        for key, value in author_format.iteritems():
            assert (custom_format._CustomFormat__get_author_list(format=key, index=15) == value)


    def test_get_keywords(self):
        custom_format = CustomFormat(custom_format=r'')
        custom_format.set_json_from_solr(solrdata.data)

        # with keywords
        a_doc = solrdata.data['response'].get('docs')[15]
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
        a_doc = solrdata.data['response'].get('docs')[13]
        assert (custom_format._CustomFormat__add_clean_pub_raw(a_doc) == 'American Astronomical Society Meeting 210, id.21.04')

        # no change required
        a_doc = solrdata.data['response'].get('docs')[14]
        assert (custom_format._CustomFormat__add_clean_pub_raw(a_doc) == 'Research Journal of Physics, vol. 1, issue 1, pp. 35-41')


    def test_get_publication(self):
        custom_format = CustomFormat(custom_format=r'')
        custom_format.set_json_from_solr(solrdata.data)

        publication_format = {
                            '%J':'The Astrophysical Journal',
                            '%j':'\\apj',
                            '%Q':'The Astrophysical Journal, Volume 533, Issue 1, pp. L25-L28.',
                            '%q':'ApJ',
                            '%%':'',
        }
        a_doc = solrdata.data['response'].get('docs')[15]
        for key, value in publication_format.iteritems():
            assert (custom_format._CustomFormat__get_publication(key, a_doc) == value)


    def test_encode(self):
        custom_format = CustomFormat(custom_format=r'')

        # encoding is unicode, pass in abstract
        custom_format._CustomFormat__set_export_format('unicode')
        abstract = "The concept of using lunar beacon signal transmission for on-board navigation for earth satellites and near-earth spacecraft is described. The system would require powerful transmitters on the earth-side of the moon's surface and black box receivers with antennae and microprocessors placed on board spacecraft for autonomous navigation. Spacecraft navigation requires three position and three velocity elements to establish location coordinates. Two beacons could be soft-landed on the lunar surface at the limits of allowable separation and each would transmit a wide-beam signal with cones reaching GEO heights and be strong enough to be received by small antennae in near-earth orbit. The black box processor would perform on-board computation with one-way Doppler/range data and dynamical models. Alternatively, GEO satellites such as the GPS or TDRSS spacecraft can be used with interferometric techniques to provide decimeter-level accuracy for aircraft navigation."
        assert (custom_format._CustomFormat__encode(text=abstract, name='abstract') == abstract)

        # encoding is html
        custom_format._CustomFormat__set_export_format('html')
        abstract = "<a>some text with &</a>"
        abstract_escaped = "&lt;a&gt;some text with &amp;&lt;/a&gt;"
        assert (custom_format._CustomFormat__encode(text=abstract, name='abstract') == abstract_escaped)

        # encoding is latex
        custom_format._CustomFormat__set_export_format('latex')
        # for author => convert to latex for author
        author = u'Fjörtoft, R.'
        author_latex = r'Fj{\"o}rtoft, R.'
        assert (custom_format._CustomFormat__encode(text=author, name='author') == author_latex)
        # for pub => no changes
        pub_raw = "Sensing and Imaging, Volume 18, Issue 1, article id.17, <NUMPAGES>12</NUMPAGES> pp."
        assert (custom_format._CustomFormat__encode(text=pub_raw, name='pub') == pub_raw)
        # for everything else => convert to latex
        abstract = u"Chapter 2: As part of the Bluedisk survey we analyse the radial gas-phase metallicity profiles of 50 late-type galaxies. We compare the metallicity profiles of a sample of HI-rich galaxies against a control sample of HI-'normal' galaxies. We find the metallicity gradient of a galaxy to be strongly correlated with its HI mass fraction {M}{HI}) / {M}_{\\ast}). We note that some galaxies exhibit a steeper metallicity profile in the outer disc than in the inner disc. These galaxies are found in both the HI-rich and control samples. This contradicts a previous indication that these outer drops are exclusive to HI-rich galaxies. These effects are not driven by bars, although we do find some indication that barred galaxies have flatter metallicity profiles. By applying a simple analytical model we are able to account for the variety of metallicity profiles that the two samples present. The success of this model implies that the metallicity in these isolated galaxies may be in a local equilibrium, regulated by star formation. This insight could provide an explanation of the observed local mass-metallicity relation. Chapter 3 We present a method to recover the gas-phase metallicity gradients from integral field spectroscopic (IFS) observations of barely resolved galaxies. We take a forward modelling approach and compare our models to the observed spatial distribution of emission line fluxes, accounting for the degrading effects of seeing and spatial binning. The method is flexible and is not limited to particular emission lines or instruments. We test the model through comparison to synthetic observations and use downgraded observations of nearby galaxies to validate this work. As a proof of concept we also apply the model to real IFS observations of high-redshift galaxies. From our testing we show that the inferred metallicity gradients and central metallicities are fairly insensitive to the assumptions made in the model and that they are reliably recovered for galaxies with sizes approximately equal to the half width at half maximum of the point-spread function. However, we also find that the presence of star forming clumps can significantly complicate the interpretation of metallicity gradients in moderately resolved high-redshift galaxies. Therefore we emphasize that care should be taken when comparing nearby well-resolved observations to high-redshift observations of partially resolved galaxies. Chapter 4 We present gas-phase metallicity gradients for 94 star-forming galaxies between (0.08 < z < 0.84). We find a negative median metallicity gradient of (-0.043^{+0.009}_{-0.007}, dex/kpc)/span>, i.e. on average we find the centres of these galaxies to be more metal-rich than their outskirts. However, there is significant scatter underlying this and we find that 10% (9) galaxies have significantly positive metallicity gradients, 39% (37) have significantly negative gradients, 28% (26) have gradients consistent with being flat, the remainder 23% (22) are considered to have unreliable gradient estimates. We find a slight trend for a more negative metallicity gradient with both increasing stellar mass and increasing star formation rate (SFR). However, given the potential redshift and size selection effects, we do not consider these trends to be significant. Indeed when we normalize the SFR of our galaxies relative to the main sequence, we do not observe any trend between the metallicity gradient and the normalized SFR. This finding is contrary to other recent studies of galaxies at similar and higher redshifts. We do, however, identify a novel trend between the metallicity gradient of a galaxy and its size. Small galaxies ((r_d < 3 kpc)) present a large spread in observed metallicity gradients (both negative and positive gradients). In contrast, we find no large galaxies (r_d > 3 kpc) with positive metallicity gradients, and overall there is less scatter in the metallicity gradient amongst the large galaxies. We suggest that these large (well-evolved) galaxies may be analogues of galaxies in the present-day Universe, which also present a common negative metallicity gradient. Chapter 5 The relationship between a galaxy's stellar mass and its gas-phase metallicity results from the complex interplay between star formation and the inflow and outflow of gas. Since the gradient of metals in galaxies is also influenced by the same processes, it is therefore natural to contrast the metallicity gradient with the mass-metallicity relation. Here we study the interrelation of the stellar mass, central metallicity and metallicity gradient, using a sample of 72 galaxies spanning (0.13 < z < 0.84) with reliable metallicity gradient estimates. We find that typically the galaxies that fall below the mean mass-metallicity relation have flat or inverted metallicity gradients. We quantify their relationship taking full account of the covariance between the different variables and find that at fixed mass the central metallicity is anti-correlated with the metallicity gradient. We argue that this is consistent with a scenario that suppresses the central metallicity either through the inflow of metal poor gas or outflow of metal enriched gas."
        abstract_latex = r"Chapter 2: As part of the Bluedisk survey we analyse the radial gas-phase metallicity profiles of 50 late-type galaxies. We compare the metallicity profiles of a sample of HI-rich galaxies against a control sample of HI-'normal' galaxies. We find the metallicity gradient of a galaxy to be strongly correlated with its HI mass fraction {\{}M{\}}{\{}HI{\}}) / {\{}M{\}}{\_}{\{}\ast{\}}). We note that some galaxies exhibit a steeper metallicity profile in the outer disc than in the inner disc. These galaxies are found in both the HI-rich and control samples. This contradicts a previous indication that these outer drops are exclusive to HI-rich galaxies. These effects are not driven by bars, although we do find some indication that barred galaxies have flatter metallicity profiles. By applying a simple analytical model we are able to account for the variety of metallicity profiles that the two samples present. The success of this model implies that the metallicity in these isolated galaxies may be in a local equilibrium, regulated by star formation. This insight could provide an explanation of the observed local mass-metallicity relation. Chapter 3 We present a method to recover the gas-phase metallicity gradients from integral field spectroscopic (IFS) observations of barely resolved galaxies. We take a forward modelling approach and compare our models to the observed spatial distribution of emission line fluxes, accounting for the degrading effects of seeing and spatial binning. The method is flexible and is not limited to particular emission lines or instruments. We test the model through comparison to synthetic observations and use downgraded observations of nearby galaxies to validate this work. As a proof of concept we also apply the model to real IFS observations of high-redshift galaxies. From our testing we show that the inferred metallicity gradients and central metallicities are fairly insensitive to the assumptions made in the model and that they are reliably recovered for galaxies with sizes approximately equal to the half width at half maximum of the point-spread function. However, we also find that the presence of star forming clumps can significantly complicate the interpretation of metallicity gradients in moderately resolved high-redshift galaxies. Therefore we emphasize that care should be taken when comparing nearby well-resolved observations to high-redshift observations of partially resolved galaxies. Chapter 4 We present gas-phase metallicity gradients for 94 star-forming galaxies between (0.08 < z < 0.84). We find a negative median metallicity gradient of (-0.043^{\{}+0.009{\}}{\_}{\{}-0.007{\}}, dex/kpc)/span>, i.e. on average we find the centres of these galaxies to be more metal-rich than their outskirts. However, there is significant scatter underlying this and we find that 10{\%} (9) galaxies have significantly positive metallicity gradients, 39{\%} (37) have significantly negative gradients, 28{\%} (26) have gradients consistent with being flat, the remainder 23{\%} (22) are considered to have unreliable gradient estimates. We find a slight trend for a more negative metallicity gradient with both increasing stellar mass and increasing star formation rate (SFR). However, given the potential redshift and size selection effects, we do not consider these trends to be significant. Indeed when we normalize the SFR of our galaxies relative to the main sequence, we do not observe any trend between the metallicity gradient and the normalized SFR. This finding is contrary to other recent studies of galaxies at similar and higher redshifts. We do, however, identify a novel trend between the metallicity gradient of a galaxy and its size. Small galaxies ((r{\_}d < 3 kpc)) present a large spread in observed metallicity gradients (both negative and positive gradients). In contrast, we find no large galaxies (r{\_}d > 3 kpc) with positive metallicity gradients, and overall there is less scatter in the metallicity gradient amongst the large galaxies. We suggest that these large (well-evolved) galaxies may be analogues of galaxies in the present-day Universe, which also present a common negative metallicity gradient. Chapter 5 The relationship between a galaxy's stellar mass and its gas-phase metallicity results from the complex interplay between star formation and the inflow and outflow of gas. Since the gradient of metals in galaxies is also influenced by the same processes, it is therefore natural to contrast the metallicity gradient with the mass-metallicity relation. Here we study the interrelation of the stellar mass, central metallicity and metallicity gradient, using a sample of 72 galaxies spanning (0.13 < z < 0.84) with reliable metallicity gradient estimates. We find that typically the galaxies that fall below the mean mass-metallicity relation have flat or inverted metallicity gradients. We quantify their relationship taking full account of the covariance between the different variables and find that at fixed mass the central metallicity is anti-correlated with the metallicity gradient. We argue that this is consistent with a scenario that suppresses the central metallicity either through the inflow of metal poor gas or outflow of metal enriched gas."
        assert (custom_format._CustomFormat__encode(text=abstract, name='abstract') == abstract_latex)


if __name__ == '__main__':
    unittest.main()
