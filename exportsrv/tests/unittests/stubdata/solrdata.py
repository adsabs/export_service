# -*- coding: utf-8 -*-

# We have 23 different doctype in Solr, these are bibcode used to extract the data below
# bibcodes = ['2017yCat.113380453S', '2018SAAS...38.....D', '1995ans..agar..390M', '1983aiaa.meetY....K', '2007RJPh....1...35.', '2007AAS...210.2104M',
#             '2009bcet.book...65L', '2018PhRvL.120b9901P', '2018TDM.....5a0201F', '2018Spin....877001P', '2017nova.pres.2388K', '2016iac..talk..872V',
#             '2017PhDT........14C', '2017MsT..........2A', '2018Wthr...73Q..35.', '2017ascl.soft06009C', '2017CBET.4403....2G', '2016emo6.rept.....R',
#             '1995anda.book.....N', '2017sptz.prop13168Y', '2017AAVSN.429....1W', '1991hep.th....8028G', '2012ddsw.rept.....T]



data = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 13,
        u'params': {
            u'sort': u'date desc, bibcode desc',
            u'x-amzn-trace-id': u'Root=1-5dd330a9-5dda490348b6637c4f990929;-',
            u'rows': u'23',
            u'fq': u'{!bitset}',
            u'q': u'*:*',
            u'start': u'0',
            u'wt': u'json',
            u'fl': u'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,version,property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem'
        }
    },
    u'response': {
        u'start': 0,
        u'numFound': 24,
        u'docs': [
            {
                u'read_count': 0,
                u'identifier': [u'10.1002/wea.3072', u'2018Wthr...73Q..35.', u'10.1002/wea.3072'],
                u'pubdate': u'2018-01-00',
                u'abstract': u'Not Available <P />',
                u'pub': u'Weather',
                u'volume': u'73',
                u'page_range': u'35-35',
                u'num_citations': 0,
                u'doi': [u'10.1002/wea.3072'],
                u'year': u'2018',
                u'bibcode': u'2018Wthr...73Q..35.',
                u'bibstem': [u'Wthr', u'Wthr...73'],
                u'issn': [u'0043-1656'],
                u'doctype': u'bookreview',
                u'pub_raw': u'Weather, vol. 73, issue 1, pp. 35-35',
                u'esources': [u'PUB_HTML'],
                u'title': [u'Book reviews'],
                u'property': [u'ESOURCE', u'ARTICLE', u'REFEREED'],
                u'issue': u'1',
                u'page': [u'35'],
                u'num_references': 0
            },
            {
                u'read_count': 0,
                u'issn': [u'2053-1583'],
                u'pubdate': u'2018-01-00',
                u'abstract': u'Not Available <P />',
                u'num_citations': 0,
                u'year': u'2018',
                u'bibcode': u'2018TDM.....5a0201F',
                u'bibstem': [u'TDM', u'TDM.....5'],
                u'aff': [u'Editor in Chief, National Graphene Institute, University of Manchester, United Kingdom', u'Publisher, IOP Publishing, Bristol, United Kingdom'],
                u'esources': [u'PUB_HTML'],
                u'issue': u'1',
                u'pub_raw': u'2D Materials, Volume 5, Issue 1, article id. 010201 (2018).',
                u'num_references': 0,
                u'pub': u'2D Materials',
                u'volume': u'5',
                u'doi': [u'10.1088/2053-1583/aa9403'],
                u'author': [u"Fal'ko, Vladimir", u'Thomas, Ceri-Wyn'],
                u'doctype': u'editorial',
                u'eid': u'010201',
                u'title': [u'2D Materials: maintaining editorial quality'],
                u'property': [u'ESOURCE', u'ARTICLE', u'REFEREED'],
                u'page': [u'010201']
            },
            {
                u'read_count': 0,
                u'pubdate': u'2018-00-00',
                u'abstract': u'Not Available <P />',
                u'num_citations': 0,
                u'year': u'2018',
                u'bibcode': u'2018Spin....877001P',
                u'copyright': u'(c) 2018: World Scientific Publishing Company',
                u'bibstem': [u'Spin', u'Spin....8'],
                u'aff': [u'-', u'-', u'-'],
                u'esources': [u'PUB_HTML', u'PUB_PDF'],
                u'issue': u'4',
                u'pub_raw': u'Spin, Volume 8, Issue 4, id. 1877001',
                u'num_references': 0,
                u'identifier': [u'2018Spin....877001P', u'10.1142/S2010324718770015', u'10.1142/S2010324718770015'],
                u'pub': u'Spin',
                u'volume': u'8',
                u'doi': [u'10.1142/S2010324718770015'],
                u'author': [u'Parkin, Stuart', u'Chantrell, Roy', u'Chang, Ching-Ray'],
                u'doctype': u'obituary',
                u'eid': u'1877001',
                u'title': [u'Obituary: In Memoriam Professor Dr. Shoucheng Zhang, Consulting Editor'],
                u'property': [u'ESOURCE', u'ARTICLE', u'REFEREED'],
                u'page': [u'1877001']
            },
            {
                u'read_count': 3,
                u'isbn': [u'9783662575451'],
                u'pubdate': u'2018-00-00',
                u'series': u'Saas-Fee Advanced Course',
                u'abstract': u'Not Available <P />',
                u'num_citations': 0,
                u'year': u'2018',
                u'property': [u'ESOURCE', u'TOC', u'NONARTICLE', u'NOT REFEREED'],
                u'bibcode': u'2018SAAS...38.....D',
                u'copyright': u'(c) 2018: Springer-Verlag GmbH Germany, part of Springer Nature',
                u'author': [u'Dessauges-Zavadsky, Miroslava', u'Pfenniger, Daniel'],
                u'aff': [u'-', u'-'],
                u'esources': [u'PUB_HTML'],
                u'pub_raw': u'Millimeter Astronomy: Saas-Fee Advanced Course 38. Swiss Society for Astrophysics and Astronomy, Saas-Fee Advanced Course, Volume 38. ISBN 978-3-662-57545-1. Springer-Verlag GmbH Germany, part of Springer Nature, 2018',
                u'num_references': 0,
                u'pub': u'Saas-Fee Advanced Course',
                u'volume': u'38',
                u'doi': [u'10.1007/978-3-662-57546-8'],
                u'keyword': [u'Physics'],
                u'bibstem': [u'SAAS', u'SAAS...38'],
                u'doctype': u'misc',
                u'title': [u'Millimeter Astronomy'],
                u'identifier': [u'2018SAAS...38.....D', u'10.1007/978-3-662-57546-8', u'10.1007/978-3-662-57546-8']
            },
            {
                u'read_count': 0,
                u'issn': [u'0031-9007'],
                u'pubdate': u'2018-01-00',
                u'abstract': u'Not Available <P />',
                u'num_citations': 0,
                u'year': u'2018',
                u'bibcode': u'2018PhRvL.120b9901P',
                u'bibstem': [u'PhRvL', u'PhRvL.120'],
                u'aff': [u'-', u'-', u'-', u'-'],
                u'esources': [u'PUB_HTML'],
                u'issue': u'2',
                u'pub_raw': u'Physical Review Letters, Volume 120, Issue 2, id.029901',
                u'num_references': 4,
                u'identifier': [u'2018PhRvL.120b9901P', u'10.1103/PhysRevLett.120.029901', u'10.1103/PhysRevLett.120.029901'],
                u'pub': u'Physical Review Letters',
                u'volume': u'120',
                u'doi': [u'10.1103/PhysRevLett.120.029901'],
                u'author': [u'Pustilnik, M.', u'van Heck, B.', u'Lutchyn, R. M.', u'Glazman, L. I.'],
                u'doctype': u'erratum',
                u'eid': u'029901',
                u'title': [u'Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)]'],
                u'property': [u'ESOURCE', u'ARTICLE', u'REFEREED'],
                u'page': [u'029901']
            },
            {
                u'read_count': 0,
                u'bibcode': u'2017PhDT........14C',
                u'keyword': [u'galaxies: evolution', u'galaxies: abundances', u'galaxies: ISM'],
                u'pubdate': u'2017-06-00',
                u'bibstem': [u'PhDT', u'PhDT.....'],
                u'property': [u'ESOURCE', u'NONARTICLE', u'REFEREED', u'PUB_OPENACCESS', u'OPENACCESS'],
                u'abstract': u"Chapter 2: As part of the Bluedisk survey we analyse the radial gas-phase metallicity profiles of 50 late-type galaxies. We compare the metallicity profiles of a sample of HI-rich galaxies against a control sample of HI-'normal' galaxies. We find the metallicity gradient of a galaxy to be strongly correlated with its HI mass fraction {M}{HI}) / {M}_{\\ast}). We note that some galaxies exhibit a steeper metallicity profile in the outer disc than in the inner disc. These galaxies are found in both the HI-rich and control samples. This contradicts a previous indication that these outer drops are exclusive to HI-rich galaxies. These effects are not driven by bars, although we do find some indication that barred galaxies have flatter metallicity profiles. By applying a simple analytical model we are able to account for the variety of metallicity profiles that the two samples present. The success of this model implies that the metallicity in these isolated galaxies may be in a local equilibrium, regulated by star formation. This insight could provide an explanation of the observed local mass-metallicity relation. <P />Chapter 3 We present a method to recover the gas-phase metallicity gradients from integral field spectroscopic (IFS) observations of barely resolved galaxies. We take a forward modelling approach and compare our models to the observed spatial distribution of emission line fluxes, accounting for the degrading effects of seeing and spatial binning. The method is flexible and is not limited to particular emission lines or instruments. We test the model through comparison to synthetic observations and use downgraded observations of nearby galaxies to validate this work. As a proof of concept we also apply the model to real IFS observations of high-redshift galaxies. From our testing we show that the inferred metallicity gradients and central metallicities are fairly insensitive to the assumptions made in the model and that they are reliably recovered for galaxies with sizes approximately equal to the half width at half maximum of the point-spread function. However, we also find that the presence of star forming clumps can significantly complicate the interpretation of metallicity gradients in moderately resolved high-redshift galaxies. Therefore we emphasize that care should be taken when comparing nearby well-resolved observations to high-redshift observations of partially resolved galaxies. <P />Chapter 4 We present gas-phase metallicity gradients for 94 star-forming galaxies between (0.08 &lt; z &lt; 0.84). We find a negative median metallicity gradient of (-0.043^{+0.009}_{-0.007}, dex/kpc)/span&gt;, i.e. on average we find the centres of these galaxies to be more metal-rich than their outskirts. However, there is significant scatter underlying this and we find that 10% (9) galaxies have significantly positive metallicity gradients, 39% (37) have significantly negative gradients, 28% (26) have gradients consistent with being flat, the remainder 23% (22) are considered to have unreliable gradient estimates. We find a slight trend for a more negative metallicity gradient with both increasing stellar mass and increasing star formation rate (SFR). However, given the potential redshift and size selection effects, we do not consider these trends to be significant. Indeed when we normalize the SFR of our galaxies relative to the main sequence, we do not observe any trend between the metallicity gradient and the normalized SFR. This finding is contrary to other recent studies of galaxies at similar and higher redshifts. We do, however, identify a novel trend between the metallicity gradient of a galaxy and its size. Small galaxies ((r_d &lt; 3 kpc)) present a large spread in observed metallicity gradients (both negative and positive gradients). In contrast, we find no large galaxies (r_d &gt; 3 kpc) with positive metallicity gradients, and overall there is less scatter in the metallicity gradient amongst the large galaxies. We suggest that these large (well-evolved) galaxies may be analogues of galaxies in the present-day Universe, which also present a common negative metallicity gradient. <P />Chapter 5 The relationship between a galaxy's stellar mass and its gas-phase metallicity results from the complex interplay between star formation and the inflow and outflow of gas. Since the gradient of metals in galaxies is also influenced by the same processes, it is therefore natural to contrast the metallicity gradient with the mass-metallicity relation. Here we study the interrelation of the stellar mass, central metallicity and metallicity gradient, using a sample of 72 galaxies spanning (0.13 &lt; z &lt; 0.84) with reliable metallicity gradient estimates. We find that typically the galaxies that fall below the mean mass-metallicity relation have flat or inverted metallicity gradients. We quantify their relationship taking full account of the covariance between the different variables and find that at fixed mass the central metallicity is anti-correlated with the metallicity gradient. We argue that this is consistent with a scenario that suppresses the central metallicity either through the inflow of metal poor gas or outflow of metal enriched gas. <P />",
                u'author': [u'Carton, David'],
                u'doctype': u'phdthesis',
                u'pub': u'Ph.D. Thesis',
                u'pub_raw': u'PhD Thesis, Leiden University, 2017',
                u'esources': [u'PUB_HTML'],
                u'num_citations': 0,
                u'doi': [u'10.5281/zenodo.581221'],
                u'year': u'2017',
                u'title': [u'Resolving Gas-Phase Metallicity In Galaxies'],
                u'identifier': [u'2017PhDT........14C', u'10.5281/zenodo.581221', u'10.5281/zenodo.581221'],
                u'aff': [u'Leiden University'],
                u'num_references': 1
            },
            {
                u'read_count': 3,
                u'identifier': [u'2017nova.pres.2388K'],
                u'pubdate': u'2017-06-00',
                u'abstract': u'The outlined regions mark the 57 knots in Tycho selected by the authors for velocity measurements. Magenta regions have redshifted line-of-sight velocities (moving away from us); cyan regions have blueshifted light-of-sight velocities (moving toward us). [Williams et al. 2017]The Tycho supernova remnant was first observed in the year 1572. Nearly 450 years later, astronomers have now used X-ray observations of Tycho to build the first-ever 3D map of a Type Ia supernova remnant.Signs of ExplosionsSupernova remnants are spectacular structures formed by the ejecta of stellar explosions as they expand outwards into the surrounding interstellar medium.One peculiarity of these remnants is that they often exhibit asymmetries in their appearance and motion. Is this because the ejecta are expanding into a nonuniform interstellar medium? Or was the explosion itself asymmetric? The best way we can explore this question is with detailed observations of the remnants.Histograms of the velocity in distribution of the knots in the X (green), Y (blue) and Z (red) directions (+Z is away from the observer). They show no evidence for asymmetric expansion of the knots. [Williams et al. 2017]Enter TychoTo this end, a team of scientists led by Brian Williams (Space Telescope Science Institute and NASA Goddard SFC) has worked to map out the 3D velocities of the ejecta in the Tycho supernova remnant. Tycho is a Type Ia supernova thought to be caused by the thermonuclear explosion of a white dwarf in a binary system that was destabilized by mass transfer from its companion.After 450 years of expansion, the remnant now has the morphological appearance of a roughly circular cloud of clumpy ejecta. The forward shock wave from the supernova, however, is known to have twice the velocity on one side of the shell as on the other.To better understand this asymmetry, Williams and collaborators selected a total of 57 knots in Tychos ejecta, spread out around the remnant. They then used 12 years of Chandra X-ray observations to measure both the knots proper motion in the plane of the sky and their line-of-sight velocity. These two measurements were then combined to build a full 3D map of the motion of the ejecta.3D hydrodynamical simulations of Tycho, stopped at the current epoch. These show that both initially smooth (top) and initially clumpy (bottom) ejecta models are consistent with the current observations of the morphology and dynamics of Tychos ejecta. [Adapted from Williams et al. 2017]Symmetry and ClumpsWilliams and collaborators found that the knots have total velocities that range from 2400 to 6600 km/s. Unlike the forward shock of the supernova, Tychos ejecta display no asymmetries in their motion which suggests that the explosion itself was symmetric. The more likely explanation is a density gradient in the interstellar medium, which could slow the shock wave on one side of the remnant without yet affecting the motion of the clumps of ejecta.As a final exploration, the authors attempt to address the origin of Tychos clumpiness. The fact that some of Tychos ejecta knots precede its outer edge has raised the question of whether the ejecta started out clumpy, or if they began smooth and only clumped during expansion. Williams and collaborators matched the morphological and dynamical data to simulations, demonstrating that neither scenario can be ruled out at this time.This first 3D map of a Type Ia supernova represents an important step in our ability to understand these stellar explosions. The authors suggest that well be able to expand on this map in the future with additional observations from Chandra, as well as with new data from future X-ray observatories that will be able to detect fainter emission.CitationBrian J. Williams et al 2017 ApJ 842 28. doi:10.3847/1538-4357/aa7384 <P />',
                u'pub': u'AAS Nova Highlights',
                u'num_citations': 0,
                u'year': u'2017',
                u'data': [u'Chandra:1'],
                u'bibcode': u'2017nova.pres.2388K',
                u'keyword': [u'Features', u'Highlights', u'interstellar medium', u'stellar evolution', u'supernova remnant', u'supernovae', u'white dwarfs'],
                u'author': [u'Kohler, Susanna'],
                u'aff': [u'-'],
                u'bibstem': [u'nova', u'nova.pres'],
                u'doctype': u'pressrelease',
                u'page': [u'2388'],
                u'esources': [u'PUB_HTML'],
                u'eid': u'2388',
                u'title': [u'A 3D View of a Supernova Remnant'],
                u'property': [u'DATA', u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'PUB_OPENACCESS', u'OPENACCESS'],
                u'pub_raw': u'AAS Nova Highlight, 14 Jun 2017, id.2388',
                u'num_references': 0
            },
            {
                u'read_count': 0,
                u'bibcode': u'2017CBET.4403....2G',
                u'num_references': 0,
                u'pubdate': u'2017-06-00',
                u'bibstem': [u'CBET', u'CBET.4403'],
                u'property': [u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'PRIVATE'],
                u'abstract': u'A previous good encounter occurred on 2006 July 29d04h11m UT (r - Delta = +0.0003 AU, solar long. = 125.841 deg). Future encounters are predicted on 2029 July 29d01h53m (+0.0007 AU, 125.816 deg), 2042 July 29d10h48m (+0.0006 AU, 125.886 deg), 2053 July 29d05h35m (+0.0001 AU, 125.848 deg), and on 2068 July 29d02h09m UT (-0.0001 AU, 125.863 deg). <P />',
                u'author': [u'Green, D. W. E.'],
                u'doctype': u'circular',
                u'pub': u'Central Bureau Electronic Telegrams',
                u'pub_raw': u'Central Bureau Electronic Telegrams, 4403, 2 (2017). Edited by Green, D. W. E.',
                u'volume': u'4403',
                u'esources': [u'PUB_HTML'],
                u'num_citations': 0,
                u'year': u'2017',
                u'title': [u'Potential New Meteor Shower from Comet C/2015 D4 (Borisov)'],
                u'identifier': [u'2017CBET.4403....2G'],
                u'aff': [u'-'],
                u'page_range': u'2',
                u'page': [u'2']
            },
            {
                u'read_count': 0,
                u'bibcode': u'2017ascl.soft06009C',
                u'num_references': 0,
                u'keyword': [u'Software'],
                u'pubdate': u'2017-06-00',
                u'bibstem': [u'ascl', u'ascl.soft'],
                u'property': [u'ASSOCIATED', u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'PUB_OPENACCESS', u'OPENACCESS'],
                u'abstract': u'sick infers astrophysical parameters from noisy observed spectra. Phenomena that can alter the data (e.g., redshift, continuum, instrumental broadening, outlier pixels) are modeled and simultaneously inferred with the astrophysical parameters of interest. This package relies on emcee (ascl:1303.002); it is best suited for situations where a grid of model spectra already exists, and one would like to infer model parameters given some data. <P />',
                u'author': [u'Casey, Andrew R.'],
                u'doctype': u'software',
                u'pub': u'Astrophysics Source Code Library',
                u'pub_raw': u'Astrophysics Source Code Library, record ascl:1706.009',
                u'esources': [u'PUB_HTML'],
                u'num_citations': 0,
                u'eid': u'ascl:1706.009',
                u'year': u'2017',
                u'title': [u'sick: Spectroscopic inference crank'],
                u'identifier': [u'2017ascl.soft06009C', u'ascl:1706.009'],
                u'page': [u'ascl:1706.009'],
                u'aff': [u'-']
            },
            {
                u'comment': [u'phot.dat 2930x19 Differential photometry of BM CVn; phot_mlc.dat 2930x19 Differential photometry of BM CVn with MLC removed; res.dat 1319x185 *Numerical results of the CPS analysis; res_mlc.dat 1319x185 *Results of the CPS analysis with MLC removed'],
                u'read_count': 0,
                u'identifier': [u'2017yCat.113380453S'],
                u'pubdate': u'2017-05-00',
                u'abstract': u'The included files present the numerical data of our analysis of the BM CVn photometry. The data consists of differential Johnson V-band photometry using the star HD 116010 as the comparison star. <P />The analysis has been performed using the previously published continuous period search (CPS) method, described in detail in Lehtinen et al., 2011A&amp;A...527A.136L, Cat. J/A+A/527/A136. <P />(4 data files). <P />',
                u'pub': u'VizieR Online Data Catalog',
                u'num_citations': 0,
                u'year': u'2017',
                u'data': [u'Vizier:1'],
                u'bibcode': u'2017yCat.113380453S',
                u'keyword': [u'Stars: variable'],
                u'bibstem': [u'yCat', u'yCat.1133'],
                u'aff': [u'-', u'-', u'-', u'-', u'-', u'-', u'-', u'-', u'-', u'-', u'-', u'-', u'-'],
                u'author': [u'Siltala, J.', u'Jetsu, L.', u'Hackman, T.', u'Henry, G. W.', u'Immonen, L.', u'Kajatkari, P.', u'Lankinen, J.', u'Lehtinen, J.', u'Monira, S.', u'Nikbakhsh, S.', u'Viitanen, A.', u'Viuho, J.', u'Willamo, T.'],
                u'doctype': u'catalog',
                u'page': [u'J/AN/338/453'],
                u'eid': u'J/AN/338/453',
                u'title': [u'VizieR Online Data Catalog: BM CVn V-band differential light curve (Siltala+, 2017)'],
                u'property': [u'ASSOCIATED', u'DATA', u'NONARTICLE', u'NOT REFEREED'],
                u'pub_raw': u'VizieR On-line Data Catalog: J/AN/338/453. Originally published in: 2017AN....338..453S',
                u'num_references': 0
            },
            {
                u'read_count': 4,
                u'identifier': [u'2017AAVSN.429....1W'],
                u'pubdate': u'2017-05-00',
                u'abstract': u'The observing campaign from 2016 on V694 Mon (MWC 560) (AAVSO Alert Notice 538) has been continued, but with different requirements. Photometry is no longer specifically requested on a regular basis (although ongoing observations that do not interfere with other obligations are welcome). Spectroscopy on a cadence of a week or two is requested to monitor changes in the disk outflow. Investigator Adrian Lucy writes: "Adrian Lucy and Dr. Jeno Sokoloski (Columbia University) have requested spectroscopic monitoring of the broad-absorption-line symbiotic star V694 Mon (MWC 560), as a follow-up to coordinated multi-wavelength observations obtained during its recent outburst (ATel #8653, #8832, #8957; #10281). This system is a perfect place in which to study the relationship between an accretion disk and disk winds/jets, and a high-value target for which even low-resolution spectra can be extraordinarily useful...Optical brightening in MWC 560 tends to predict higher-velocity absorption, but sometimes jumps in absorption velocity also appear during optical quiescence (e.g., Iijima 2001, ASPCS, 242, 187). If such a velocity jump occurs during photometric quiescence, it may prompt radio observations to confirm and test the proposed outflow origin for recently-discovered flat-spectrum radio emission (Lucy et al. ATel #10281)...Furthermore, volunteer spectroscopic monitoring of this system has proved useful in unpredictable ways. For example, \'amateur\' spectra obtained by Somogyi P\xe9ter in 2015 December demonstrated that the velocity of absorption was very low only a month before an optical outburst peak prompted absorption troughs up to 3000 km/s, which constrains very well the timing of the changes to the outflow to a degree that would not have been otherwise possible. Any resolution can be useful. A wavelength range that can accommodate a blueshift of at least 140 angstroms (6000 km/s) from the rest wavelengths of H-alpha at 6562 angstroms and/or H-beta at 4861 angstroms is ideal, though spectra with a smaller range can still be useful. Photometry could potentially still be useful, but will be supplementary to medium-cadence photometry being collected by the ANS collaboration." "Spectroscopy may be uploaded to the ARAS database (http://www.astrosurf.com/aras/Aras_DataBase/DataBase.htm), or sent to Adrian and Jeno directly at &lt;lucy@astro.columbia.edu&gt;. Finder charts with sequence may be created using the AAVSO Variable Star Plotter (https://www.aavso.org/vsp). Photometry should be submitted to the AAVSO International Database. See full Special Notice for more details. <P />',
                u'pub': u'AAVSO Special Notice',
                u'volume': u'429',
                u'page_range': u'1',
                u'num_citations': 0,
                u'year': u'2017',
                u'bibcode': u'2017AAVSN.429....1W',
                u'keyword': [u'astronomical databases: miscellaneous', u'binaries: symbiotic', u'stars: individual (V694 Mon', u'MWC 560)'],
                u'copyright': u'(C) AAVSO 2017',
                u'author': [u'Waagen, Elizabeth O.'],
                u'aff': [u'AAVSO'],
                u'bibstem': [u'AAVSN', u'AAVSN.429'],
                u'doctype': u'newsletter',
                u'page': [u'1'],
                u'esources': [u'PUB_HTML'],
                u'title': [u'V694 Mon (MWC 560) spectroscopy requested'],
                u'property': [u'ESOURCE', u'NONARTICLE', u'NOT REFEREED'],
                u'pub_raw': u'AAVSO Special Notice #429',
                u'num_references': 6
            },
            {
                u'read_count': 0,
                u'bibcode': u'2017sptz.prop13168Y',
                u'num_references': 0,
                u'pubdate': u'2017-04-00',
                u'bibstem': [u'sptz', u'sptz.prop'],
                u'property': [u'DATA', u'NONARTICLE', u'NOT REFEREED'],
                u'abstract': u'ULIRG F01004-2237 had a strong optical flare, peaked in 2010, and the follow-up optical spectra classified this event as a TDE candidate (Tadhunter et al. 2017, Nature Astronomy). In early 2017, using archival WISE data, we discovered that its 3.4 and 4.6um fluxes have been steadily rising since 2013, increased by a factor of 3.5 and 2.6 respectively. The last epoch data from WISE on 2016-12-12 shows that F01004-2237 has reached 7.5 and 14mJy at 3.4 and 4.6um. We interpret the mid-IR LCs as infrared echoes from the earlier optical flare. We infer a convex, dust ring with a radius of 1 pc from the central heating source. Our model predicts that if this event is indeed a TDE, its mid-IR LCs should start to fade in next 5-12 months because it has already reprocessed most of the UV/optical energy from the tidal disruption. However, if this event is due to activities from an AGN, its mid-IR LCs could last over a much longer time scale. We request a total of 3.2 hours of Spitzer time to monitor the mid-IR variations in next 12 months. This will provide the critical data to confirm the nature of this transient event. <P />',
                u'author': [u'Yan, Lin'],
                u'doctype': u'proposal',
                u'pub': u'Spitzer Proposal',
                u'pub_raw': u'Spitzer Proposal ID 13168',
                u'page_range': u'13168',
                u'num_citations': 0,
                u'year': u'2017',
                u'title': [u'Confirm the Nature of a TDE Candidate in ULIRG F01004-2237 Using Spitzer mid-IR Light Curves'],
                u'identifier': [u'2017sptz.prop13168Y'],
                u'data': [u'Spitzer:1'],
                u'aff': [u'-'],
                u'page': [u'13168']
            },
            {
                u'read_count': 0,
                u'bibcode': u'2017MsT..........2A',
                u'num_references': 4,
                u'pubdate': u'2017-03-00',
                u'bibstem': [u'MsT', u'MsT......'],
                u'property': [u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'AUTHOR_OPENACCESS', u'OPENACCESS'],
                u'abstract': u'The African Very-long-baseline interferometry Network (AVN) is a joint project between South Africa and eight partner African countries aimed at establishing a VLBI (Very-Long-Baseline Interferometry) capable network of radio telescopes across the African continent. An existing structure that is earmarked for this project, is a 32 m diameter antenna located in Ghana that has become obsolete due to advances in telecommunication. The first phase of the conversion of this Ghana antenna into a radio astronomy telescope is to upgrade the antenna to observe at 5 GHz to 6.7 GHz frequency and then later to 18 GHz within a required performing tolerance. The surface and pointing accuracies for a radio telescope are much more stringent than that of a telecommunication antenna. The mechanical pointing accuracy of such telescopes is influenced by factors such as mechanical alignment, structural deformation, and servo drive train errors. The current research investigates the numerical simulation of the surface and pointing accuracies of the Ghana 32 m diameter radio astronomy telescope due to its structural deformation mainly influenced by gravity, wind and thermal loads. <P />',
                u'author': [u'Azankpo, Severin'],
                u'doctype': u'mastersthesis',
                u'pub': u'Masters Thesis',
                u'pub_raw': u'Masters thesis, University of Stellenbosch, March 2017, 120 pages',
                u'esources': [u'AUTHOR_PDF', u'PUB_HTML', u'PUB_PDF'],
                u'num_citations': 0,
                u'year': u'2017',
                u'title': [u'Surface Accuracy and Pointing Error Prediction of a 32 m Diameter Class Radio Astronomy Telescope'],
                u'identifier': [u'2017MsT..........2A'],
                u'aff': [u'University of Stellenbosch'],
                u'page_range': u'2',
                u'page': [u'2']
            },
            {
                u'read_count': 3,
                u'bibcode': u'2016emo6.rept.....R',
                u'keyword': [u'THE MOON', u'ECLIPSES', u'PARTIAL', u'PENUMBRAL', u'ASTROPHOTOGRAPHY'],
                u'pubdate': u'2016-10-00',
                u'author': [u'Rotaru, Adrian', u'Pteancu, Mircea', u'Zaharia, Cristian'],
                u'abstract': u"The web page represents circumstances and photographs from the Moon's partial/penumbral eclipse from 16 September 2016 obtained from few various places in Romania (East Europe). A part of photographs give the maximum phase of the Eclipse, while another give the reddened Moon. <P />",
                u'bibstem': [u'emo6', u'emo6.rept'],
                u'doctype': u'techreport',
                u'pub': u'http://www.astronomy.ro/forum/viewtopic.php?p=159287#159287 (Comments in Romanian',
                u'pub_raw': u'http://www.astronomy.ro/forum/viewtopic.php?p=159287#159287 (Comments in Romanian)',
                u'property': [u'NONARTICLE', u'NOT REFEREED'],
                u'num_citations': 0,
                u'year': u'2016',
                u'title': [u"The penumbral Moon's eclipse form 16 september 2016"],
                u'identifier': [u'2016emo6.rept.....R'],
                u'aff': [u'Bragadiru, Romania', u'Private Astronomical Observatory, Arad, Romania', u'Private Astronomical Observatory, Ploiesti, Romania'],
                u'num_references': 0
            },
            {
                u'read_count': 0,
                u'bibcode': u'2016iac..talk..872V',
                u'num_references': 1,
                u'author': [u'Velasco, Sergio'],
                u'pubdate': u'2016-03-00',
                u'page_range': u'872',
                u'property': [u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'AUTHOR_OPENACCESS', u'OPENACCESS'],
                u'abstract': u'Not Available <P />',
                u'bibstem': [u'iac', u'iac..talk'],
                u'doctype': u'talk',
                u'pub': u'IAC Talks, Astronomy and Astrophysics Seminars from the Instituto de Astrof&iacute;sica de Canarias',
                u'pub_raw': u'IAC Talks, Astronomy and Astrophysics Seminars from the Instituto de Astrof\xedsica de Canarias, 872',
                u'esources': [u'AUTHOR_HTML', u'PUB_HTML'],
                u'num_citations': 0,
                u'year': u'2016',
                u'title': [u'Living on the edge: Adaptive Optics+Lucky Imaging'],
                u'identifier': [u'2016iac..talk..872V'],
                u'aff': [u'Instituto de Astrof\xedsica de Canarias'],
                u'page': [u'872']
            },
            {
                u'read_count': 0,
                u'isbn': [u'9789048123674'],
                u'pubdate': u'2009-00-00',
                u'abstract': u'The discovery of the physical phenomenon of Nuclear Magnetic Resonance (NMR) in 1946 gave rise to the spectroscopic technique that has become a remarkably versatile research tool. One could oversimplify NMR spectros-copy by categorizing it into the two broad applications of structure elucidation of molecules (associated with chemistry and biology) and imaging (associated with medicine). But, this certainly does not do NMR spectroscopy justice in demonstrating its general acceptance and utilization across the sciences. This manuscript is not an effort to present an exhaustive, or even partial review of NMR spectroscopy applications, but rather to provide a glimpse at the wide-ranging uses of NMR spectroscopy found within the confines of a single magnetic resonance research facility, the Stanford Magnetic Resonance Laboratory. Included here are summaries of projects involving protein structure determination, mapping of intermolecular interactions, exploring fundamental biological mechanisms, following compound cycling in the environmental, analysis of synthetic solid compounds, and microimaging of a model organism. <P />',
                u'num_citations': 0,
                u'year': u'2009',
                u'bibcode': u'2009bcet.book...65L',
                u'copyright': u'(c) 2009: Springer Netherlands',
                u'bibstem': [u'bcet', u'bcet.book'],
                u'aff': [u'Stanford Magnetic Resonance Laboratory, Stanford University', u'Department of Chemistry, Stanford University; , Genencor', u'Department of Geological &amp; Environmental Sciences, Stanford University; , ConocoPhillips Company', u'Department of Molecular and Cellular Physiology, Stanford University; Department of Structural Biology, Stanford University', u'Department of Geological &amp; Environmental Sciences, Stanford University; , Agriculture and Agri-Food Canada', u'Stanford Genome Technology Center, Stanford University; Department of Biochemistry, Stanford University', u'Department of Geological &amp; Environmental Sciences, Stanford University; Air Products and Chemicals, Inc. Allentown', u'Department of Molecular and Cellular Physiology, Stanford University; Department of Structural Biology, Stanford University', u'Department of Biochemistry, Stanford University', u'Department of Chemistry, Stanford University; Department of Biochemistry, Stanford University', u'Department of Biochemistry, Stanford University; Department of Biochemistry, Molecular Biology and Cell Biology, Northwestern University', u'Department of Chemistry, Stanford University; , Institute for Research in Biomedicine', u'Stanford Genome Technology Center, Stanford University; Department of Biochemistry, Stanford University', u'Stanford Magnetic Resonance Laboratory, Stanford University; Department of Structural Biology, Stanford University', u'Department of Molecular and Cellular Physiology, Stanford University; Department of Structural Biology, Stanford University', u'Department of Geological &amp; Environmental Sciences, Stanford University', u'Department of Molecular and Cellular Physiology, Stanford University; Department of Structural Biology, Stanford University'],
                u'esources': [u'PUB_HTML'],
                u'editor': [u'Puglisi, Joseph D.'],
                u'pub_raw': u'Biophysics and the Challenges of Emerging Threats, NATO Science for Peace and Security Series B: Physics and Biophysics. ISBN 978-90-481-2367-4. Springer Netherlands, 2009, p. 65',
                u'num_references': 0,
                u'identifier': [u'2009bcet.book...65L', u'10.1007/978-90-481-2368-1_5', u'10.1007/978-90-481-2368-1_5'],
                u'pub': u'Biophysics and the Challenges of Emerging Threats',
                u'page_range': u'65',
                u'doi': [u'10.1007/978-90-481-2368-1_5'],
                u'keyword': [u'Physics'],
                u'author': [u'Liu, Corey W.', u'Alekseyev, Viktor Y.', u'Allwardt, Jeffrey R.', u'Bankovich, Alexander J.', u'Cade-Menun, Barbara J.', u'Davis, Ronald W.', u'Du, Lin-Shu', u'Garcia, K. Christopher', u'Herschlag, Daniel', u'Khosla, Chaitan', u'Kraut, Daniel A.', u'Li, Qing', u'Null, Brian', u'Puglisi, Joseph D.', u'Sigala, Paul A.', u'Stebbins, Jonathan F.', u'Varani, Luca'], u'doctype': u'inbook', u'title': [u'The Diversity of Nuclear Magnetic Resonance Spectroscopy'],
                u'property': [u'ESOURCE', u'TOC', u'ARTICLE', u'NOT REFEREED'],
                u'page': [u'65'],
                u'doctype': u'inbook'
            },
            {
                u'read_count': 0,
                u'bibcode': u'2007AAS...210.2104M',
                u'num_references': 0,
                u'pubdate': u'2007-05-00',
                u'bibstem': [u'AAS', u'AAS...210'],
                u'series': u'American Astronomical Society Meeting Abstracts',
                u'abstract': u'Palomar-QUEST (PQ) synoptic sky survey has now been routinely processing data from driftscans in real-time. As four photometric bandpasses are utilized in nearly simultaneously, PQ is well suited to search for transient and highly variable objects. Using a series of software filters i.e. programs to select/deselect objects based on certain criteria we shorten the list of candidates from the initially flagged candidate transients. Such filters include looking for known asteroids, known variables, as well as moving, but previously uncatalogued objects based on their motion within a scan as well as between successive scans. Some software filters also deal with instrumental artifacts, edge effects, and use clustering of spurious detections around bright stars. During a typical night when we cover about 500 sq. degrees, we detect hundreds of asteroids, the primary contaminants in the search for astrophysical transients beyond our solar system. <P />Here we describe some statistics based on the software filters we employ and the nature of the objects that seem to survive the process. We also discuss the usefulness of this to amateur astronomers, projects like VOEventNet, and other synoptic sky surveys. <P />We also present an outline of the work we have started on quantifying the variability of quasars, blazars, as well as various classes of Galactic sources, by combining the large number of PQ scans with other existing data sources federated in the Virtual Observatory environment. <P />The PQ survey is partially supported by the U.S. National Science Foundation (NSF). <P />',
                u'author': [u'Mahabal, Ashish A.', u'Drake, A. J.', u'Djorgovski, S. G.', u'Donalek, C.', u'Glikman, E.', u'Graham, M. J.', u'Williams, R.', u'Baltay, C.', u'Rabinowitz, D.', u'PQ Team Caltech', u'Yale', u'NCSA', u'Indiana', u', . . .'],
                u'doctype': u'abstract',
                u'pub': u'American Astronomical Society Meeting Abstracts #210',
                u'pub_raw': u'American Astronomical Society Meeting 210, id.21.04; <ALTJOURNAL>Bulletin of the American Astronomical Society, Vol. 39, p.124</ALTJOURNAL>',
                u'volume': u'210',
                u'property': [u'TOC', u'NONARTICLE', u'NOT REFEREED'],
                u'num_citations': 0,
                u'eid': u'21.04',
                u'year': u'2007',
                u'title': [u'Time Domain Exploration with the Palomar-QUEST Sky Survey'],
                u'identifier': [u'2007BAAS...39..124M', u'2007AAS...210.2104M', u'2007BAAS...39..124M'],
                u'page': [u'21.04'],
                u'aff': [u'Caltech', u'Caltech', u'Caltech', u'Caltech', u'Caltech', u'Caltech', u'Caltech', u'Yale University', u'Yale University', u'-', u'-', u'-', u'-', u'-']
            },
            {
                u'read_count': 0,
                u'issn': [u'1819-3463'],
                u'pubdate': u'2007-01-00',
                u'abstract': u'Not Available <P />',
                u'num_citations': 0,
                u'year': u'2007',
                u'bibcode': u'2007RJPh....1...35.',
                u'bibstem': [u'RJPh', u'RJPh....1'],
                u'aff': [u'-', u'-'],
                u'esources': [u'PUB_HTML'],
                u'issue': u'1',
                u'pub_raw': u'Research Journal of Physics, vol. 1, issue 1, pp. 35-41',
                u'num_references': 0,
                u'identifier': [u'10.3923/rjp.2007.35.41', u'2007RJPh....1...35.', u'10.3923/rjp.2007.35.41'],
                u'pub': u'Research Journal of Physics',
                u'volume': u'1',
                u'page_range': u'35-41',
                u'doi': [u'10.3923/rjp.2007.35.41'],
                u'author': [u'., S. N. Agbo', u'., E. C. Okoroigwe'],
                u'doctype': u'article',
                u'title': [u'Analysis of Thermal Losses in the Flat-Plate Collector of a Thermosyphon Solar Water Heater'],
                u'property': [u'ESOURCE', u'ARTICLE', u'NOT REFEREED', u'PUB_OPENACCESS', u'OPENACCESS'],
                u'page': [u'35']
            },
            {
                u'read_count': 0,
                u'bibcode': u'1995ans..agar..390M',
                u'num_references': 0,
                u'keyword': [u'Earth Orbits', u'Navigation Aids', u'Navigators', u'Onboard Equipment', u'Space Navigation', u'Spacecraft Trajectories', u'Support Systems', u'Technology Assessment', u'Technology Utilization', u'Ascent Trajectories', u'Reentry Trajectories', u'Spacecraft', u'Spacecraft Performance', u'Spacecraft Survivability', u'Tradeoffs', u'Weight (Mass)', u'Space Communications, Spacecraft Communications, Command and Tracking'],
                u'pubdate': u'1995-06-00',
                u'bibstem': [u'ans', u'ans..agar'],
                u'property': [u'ARTICLE', u'NOT REFEREED'],
                u'abstract': u'Spacecraft operation depends upon knowledge of vehicular position and, consequently, navigational support has been required for all such systems. Technical requirements for different mission trajectories and orbits are addressed with consideration given to the various tradeoffs which may need to be considered. The broad spectrum of spacecraft are considered with emphasis upon those of greater military significance (i.e., near earth orbiting satellites). Technical requirements include, but are not limited to, accuracy; physical characteristics such as weight and volume; support requirements such as electrical power and ground support; and system integrity. Generic navigation suites for spacecraft applications are described. It is shown that operational spacecraft rely primarily upon ground-based tracking and computational centers with little or no navigational function allocated to the vehicle, while technology development efforts have been and continue to be directed primarily toward onboard navigation suites. The military significance of onboard navigators is shown to both improve spacecraft survivability and performance (accuracy). <P />',
                u'author': [u'Miller, Judy L.'],
                u'doctype': u'inproceedings',
                u'pub': u'In AGARD',
                u'pub_raw': u'In AGARD, Aerospace Navigation Systems p 390-405 (SEE N96-13404 02-04)',
                u'page_range': u'390-405',
                u'num_citations': 0,
                u'year': u'1995',
                u'title': [u'Spacecraft navigation requirements'],
                u'identifier': [u'1995ans..agar..390M'],
                u'page': [u'390'],
                u'aff': [u'Draper (Charles Stark) Lab., Inc., Cambridge, MA.']
            },
            {
                u'read_count': 2,
                u'bibcode': u'1995anda.book.....N',
                u'pubdate': u'1995-00-00',
                u'bibstem': [u'anda', u'anda.book'],
                u'abstract': u'Not Available <P />',
                u'author': [u'Nayfeh, Ali H.', u'Balachandran, Balakumar'],
                u'doctype': u'book',
                u'pub': u'Wiley series in nonlinear science',
                u'pub_raw': u'Wiley series in nonlinear science, New York; Chichester: Wiley, |c1995',
                u'property': [u'NONARTICLE', u'NOT REFEREED'],
                u'num_citations': 118,
                u'year': u'1995',
                u'title': [u'Applied nonlinear dynamics: analytical, computational and experimental methods'],
                u'identifier': [u'1995anda.book.....N'],
                u'aff': [u'-', u'-'],
                u'num_references': 0
            },
            {
                u'arxiv_class': [u'hep-th'],
                u'read_count': 1143,
                u'pubdate': u'1988-11-00',
                u'abstract': u'These lectures consisted of an elementary introduction to conformal field theory, with some applications to statistical mechanical systems, and fewer to string theory. Contents: 1. Conformal theories in d dimensions 2. Conformal theories in 2 dimensions 3. The central charge and the Virasoro algebra 4. Kac determinant and unitarity 5. Identication of m = 3 with the critical Ising model 6. Free bosons and fermions 7. Free fermions on a torus 8. Free bosons on a torus 9. Affine Kac-Moody algebras and coset constructions 10. Advanced applications <P />',
                u'pub': u'arXiv e-prints',
                u'num_citations': 190,
                u'year': u'1988',
                u'property': [u'ESOURCE', u'INSPIRE', u'ARTICLE', u'NOT REFEREED', u'EPRINT_OPENACCESS', u'OPENACCESS'],
                u'bibcode': u'1991hep.th....8028G',
                u'keyword': [u'High Energy Physics - Theory'],
                u'author': [u'Ginsparg, Paul'],
                u'aff': [u'-'],
                u'bibstem': [u'arXiv', u'arXiv....'],
                u'doctype': u'eprint',
                u'page': [u'hep-th/9108028'],
                u'esources': [u'EPRINT_HTML', u'EPRINT_PDF'],
                u'eid': u'hep-th/9108028',
                u'title': [u'Applied Conformal Field Theory'],
                u'identifier': [u'1991hep.th....8028G', u'arXiv:hep-th/9108028'],
                u'pub_raw': u'eprint arXiv:hep-th/9108028',
                u'num_references': 0
            },
            {
                u'read_count': 0,
                u'bibcode': u'1983aiaa.meetY....K',
                u'keyword': [u'Artificial Satellites', u'Autonomous Navigation', u'Earth-Moon System', u'Lunar Communication', u'Radio Beacons', u'Radio Navigation', u'Space Navigation', u'Doppler Navigation', u'Least Squares Method', u'Orbit Calculation', u'Space Communications, Spacecraft Communications, Command and Tracking'],
                u'pubdate': u'1983-01-00',
                u'bibstem': [u'aiaa', u'aiaa.meet'],
                u'abstract': u"The concept of using lunar beacon signal transmission for on-board navigation for earth satellites and near-earth spacecraft is described. The system would require powerful transmitters on the earth-side of the moon's surface and black box receivers with antennae and microprocessors placed on board spacecraft for autonomous navigation. Spacecraft navigation requires three position and three velocity elements to establish location coordinates. Two beacons could be soft-landed on the lunar surface at the limits of allowable separation and each would transmit a wide-beam signal with cones reaching GEO heights and be strong enough to be received by small antennae in near-earth orbit. The black box processor would perform on-board computation with one-way Doppler/range data and dynamical models. Alternatively, GEO satellites such as the GPS or TDRSS spacecraft can be used with interferometric techniques to provide decimeter-level accuracy for aircraft navigation. <P />",
                u'author': [u'Khatib, A. R.', u'Ellis, J.', u'French, J.', u'Null, G.', u'Yunck, T.', u'Wu, S.'],
                u'doctype': u'proceedings',
                u'pub': u'AIAA, Aerospace Sciences Meeting',
                u'pub_raw': u'American Institute of Aeronautics and Astronautics, Aerospace Sciences Meeting, 21st, Reno, NV, Jan. 10-13, 1983. 7 p.',
                u'property': [u'NONARTICLE', u'NOT REFEREED'],
                u'num_citations': 0,
                u'year': u'1983',
                u'title': [u'Autonomous navigation using lunar beacons'],
                u'identifier': [u'1983aiaa.meetY....K'],
                u'aff': [u'California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA', u'California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA', u'California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA', u'California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA', u'California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA', u'California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA'],
                u'num_references': 0
            },
            {
                u'read_count': 1,
                u'bibcode':'2012ddsw.rept.....T',
                u'copyright': u'Oak Ridge National Laboratory',
                u'keyword': [u'Daymet'],
                u'pubdate':u'2012-04-00',
                u'bibstem':[u'ddsw', u'ddsw.rept'],
                u'abstract':u'Archived and distributed through the ORNL DAAC, the Daymet data set provides gridded estimates of daily weather parameters for North America, including daily continuous surfaces of minimum and maximum temperature, precipitation occurrence and amount, humidity, shortwave radiation, snow water equivalent, and day length. The daily time step, 1 km x 1 km spatial resolution, and North American spatial extent of the data set makes it a unique and valuable contribution to scientific, research, and educational communities. The literature shows that Daymet data have been broadly applied to fields including hydrology, terrestrial vegetation growth models, carbon cycle science, and regional to large scale climate change analysis.',
                u'doi': [u'10.3334/ORNLDAAC/1219'],
                u'author':[u'Thornton, P. E.', u'Thornton, M. M.', u'Mayer, B. W.', u'Wilhelmi, N.', u'Wei, Y.', u'Devarakonda, R.', u'Cook, R.'],
                u'doctype':u'dataset',
                u'pub':u'Oak Ridge National Laboratory (ORNL) Distributed Active Archive Center for Biogeochemical Dynamics (DAAC',
                u'pub_raw':u'Oak Ridge National Laboratory (ORNL) Distributed Active Archive Center for Biogeochemical Dynamics (DAAC)',
                u'property':[u'ESOURCE', u'NONARTICLE', u'NOT REFEREED'],
                u'num_citations': 51,
                u'year': u'2012',
                u'esources': [u'PUB_HTML'],
                u'title': [u'Daymet: Daily surface weather on a 1 km grid for North America, 1980-2008'],
                u'identifier': [u'2012ddsw.rept.....T', u'10.3334/ORNLDAAC/1219'],
                u'aff': [u'-', u'-', u'-', u'-', u'-', u'-', u'-'],
                u'num_references': 0
            },
            {
                "bibcode":"2020EPJC...80...96D",
                "abstract":"Recently Pomme et al. (Solar Phys 292:162, 2017) did an analysis of <inline-formula id=\"IEq3\"><mml:math><mml:mrow><mml:msup><mml:mrow></mml:mrow><mml:mn>36</mml:mn></mml:msup><mml:mtext>Cl</mml:mtext></mml:mrow></mml:math></inline-formula> radioactive decay data from measurements at the Physikalisch-Technische Bundesanstalt (PTB), in order to verify the claims by Sturrock and collaborators of an influence on beta-decay rates measured at Brookhaven National Lab (BNL) due to the rotation-induced modulation of the solar neutrino flux. Their analysis excluded any sinusoidal modulations in the frequency range from 0.2 to 20/year. We carry out an independent analysis of the same PTB and BNL data, using the generalized Lomb–Scargle periodogram to look for any statistically significant peaks in the range from 0 to 14 per year, and by evaluating the significance of every peak using multiple methods. Our results for the PTB data are in agreement with those by Pomme et al. For BNL data, we do find peaks at some of the same frequencies as Sturrock et al., but the significance is much lower. All our analysis codes and datasets have been made publicly available.",
                "aff":["Department of Physics, IIT Hyderabad, 502285, Kandi, Telangana, India",
                  "Department of Physics, IIT Hyderabad, 502285, Kandi, Telangana, India ;"],
                "author":["Dhaygude, Akanksha",
                  "Desai, Shantanu"],
                "bibstem":["EPJC",
                  "EPJC...80"],
                "copyright":"© The Author(s) 2020",
                "doctype":"article",
                "doi":["10.1140/epjc/s10052-020-7683-6",
                  "10.48550/arXiv.1912.06970"],
                "identifier":["2019arXiv191206970D",
                  "10.48550/arXiv.1912.06970",
                  "10.1140/epjc/s10052-020-7683-6",
                  "2020EPJC...80...96D",
                  "arXiv:1912.06970"],
                "keyword":["Astrophysics - High Energy Astrophysical Phenomena",
                  "Astrophysics - Instrumentation and Methods for Astrophysics",
                  "Nuclear Experiment"],
                "pub":"European Physical Journal C",
                "pub_raw":"The European Physical Journal C, Volume 80, Issue 2, article id.96",
                "pubdate":"2020-02-00",
                "title":["Generalized Lomb–Scargle analysis of <inline-formula id=\"IEq1\"><mml:math><mml:mrow><mml:msup><mml:mrow></mml:mrow><mml:mn>36</mml:mn></mml:msup><mml:mi mathvariant=\"normal\">Cl</mml:mi></mml:mrow></mml:math></inline-formula> decay rate measurements at PTB and BNL"],
                "year":"2020",
                "read_count":168,
                "esources":["EPRINT_HTML",
                  "EPRINT_PDF",
                  "PUB_HTML"],
                "property":["ARTICLE",
                  "EPRINT_OPENACCESS",
                  "ESOURCE",
                  "OPENACCESS",
                  "PUB_OPENACCESS",
                  "REFEREED"]
            },
        ]
    }
}

data_2 = \
{
    u'responseHeader': {
        u'status':0,
        u'QTime':43,
        u'params': {
            u'q':'bibcode:2018AAS...23221409A',
            u'indent':'on',
            u'fl':'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,num_citations,read_count,bibcode,identifier,copyright,keyword,doctype,num_references,comment,property,esources,data,isbn,pubnote,eid',
            'wt':'json',
            '_':'1529341837285'
        }
    },
    u'response': {
        u'numFound':1,
        u'start':0,
        u'docs':[
            {
                u'read_count':0,
                u'abstract': u'The NASA Astrophysics Data System (ADS) is used daily by researchers and curators as a discovery platform for the Astronomy literature. Over the past several years, the ADS has been adding to the breadth and depth of its contents. Scholarly astronomy articles are now indexed as full-text documents, allowing for complete and accurate literature searches. High-level data products, data links, and software used in refereed astronomy papers are now also being ingested and indexed in our database. All the search functionality exposed in the new ADS interface is also available via its API, which we are continuing to develop and enhance. In this talk I will describe the current system, our current roadmap, and solicit input from the community regarding what additional data, services, and discovery capabilities the ADS should support.',
                u'num_citations':0,
                u'num_references':0,
                u'pubdate': u'2018-06-00',
                u'year': u'2018',
                u'page': [u'214.09'],
                u'bibcode': u'2018AAS...23221409A',
                u'bibstem': [u'AAS', u'AAS...232'],
                u'identifier': [u'2018AAS...23221409A'],
                u'copyright': u'(c) 2018: American Astronomical Society',
                u'author': [u'Accomazzi, Alberto', u'ADS Team'],
                u'aff': [u'Harvard Smithsonian, CfA', u'-'],
                u'volume': u'232',
                u'pub': u'American Astronomical Society Meeting Abstracts #232',
                u'property': [u'NONARTICLE', u'NOT REFEREED'],
                u'doctype': u'abstract',
                u'pub_raw': u'American Astronomical Society, AAS Meeting #232, id.#214.09',
                u'eid': u'214.09',
                u'title': [u'The NASA Astrophysics Data System: Capabilities and Roadmap for the 2020s'],
                u'orcid_pub': ['-', '-']
            }
        ]
    }
}

data_3 = \
{
    u'responseHeader': {
        u'status':0,
        u'QTime':43,
        u'params': {
            u'q':'bibcode:2000ApJ...533L..25E',
            u'indent':'on',
            u'fl':'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,num_citations,read_count,bibcode,identifier,copyright,keyword,doctype,num_references,comment,property,esources,data,isbn,pubnote,eid',
            'wt':'json',
            '_':'1529341837285'
        }
    },
    u'response': {
        u'numFound':1,
        u'start':0,
        u'docs':[
            {
                u'read_count': 17,
                u'abstract': u"The Dominion Radio Astrophysical Observatory's Synthesis Telescope provides the highest resolution data (1' and 0.82 km s<SUP>-1</SUP>) to date of an H I worm candidate. Observed as part of the Canadian Galactic Plane Survey, mushroom-shaped GW 123.4-1.5 extends only a few hundred parsecs, contains ~10<SUP>5</SUP> M<SUB>solar</SUB> of neutral hydrogen, and appears unrelated to a conventional shell or chimney structure. Our preliminary Zeus two-dimensional models use a single off-plane explosion with a modest (~10<SUP>51</SUP> ergs) energy input. These generic simulations generate, interior to an expanding outer blast wave, a buoyant cloud whose structure resembles the morphology of the observed feature. Unlike typical model superbubbles, the stem can be narrow because its width is not governed by the pressure behind the blast wave or the disk scale height. Using this type of approach, it should be possible to more accurately model the thin stem and other details of GW 123.4-1.5 in the future.",
                u'doctype': u'article',
                u'year': u'2000',
                u'bibcode': u'2000ApJ...533L..25E',
                u'bibstem': [u'ApJL', u'ApJL..533'],
                u'author': [u'English, Jayanne', u'Taylor, A. R.', u'Mashchenko, S. Y.', u'Irwin, Judith A.', u'Basu, Shantanu', u'Johnstone, Doug'],
                u'aff': [u"Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada; Space Telescope Science Institute, Baltimore, MD", u"Department of Physics and Astronomy, University of Calgary, Calgary, Alberta, T2N 1N4, Canada", u"Department de Physique, Universit\u00e9 de Montr\u00e9al, Montr\u00e9al, Qu\u00e9bec, H3C 3J7, Canada", u"Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada", u"Department of Physics and Astronomy, University of Western Ontario, London, Ontario, N6A 3K7, Canada", u"University of Toronto, 60 St. George Street, Toronto, Ontario, M5S 3H8, Canada"],
                u'esources': [u'EPRINT_HTML', u'EPRINT_PDF', u'PUB_HTML', u'PUB_PDF'],
                u'issue': u'1',
                u'pub_raw': u'The Astrophysical Journal, Volume 533, Issue 1, pp. L25-L28.',
                u'pub': u'The Astrophysical Journal',
                u'volume': u'533',
                u'page_range': u'L25-L28',
                u'pubdate': u'2000-04-00',
                u'data': [u'SIMBAD:3'],
                u'doi': [u'10.1086/312592'],
                u'keyword': [u'GALAXY: HALO', u'GALAXY: STRUCTURE', u'ISM: BUBBLES', u'ISM: INDIVIDUAL: ALPHANUMERIC: GW 123.4-1.5', u'ISM: STRUCTURE', u'Astrophysics'],
                u'title': [u'The Galactic Worm GW 123.4-1.5: A Mushroom-shaped H I Cloud'],
                u'num_citations': 16,
                u'num_references': 12,
                u'property': [u'OPENACCESS', u'REFEREED', u'EPRINT_OPENACCESS', u'PUB_OPENACCESS', u'ARTICLE'],
                u'page': [u'L25']
            }
        ]
    }
}

data_4 = \
{
    u'responseHeader': {
        u'status':0,
        u'QTime':43,
        u'params': {
            u'q':'bibcode:2017wfc..rept...16R',
            u'indent':'on',
            u'fl':'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,num_citations,read_count,bibcode,identifier,copyright,keyword,doctype,num_references,comment,property,esources,data,isbn,pubnote,eid',
            'wt':'json',
            '_':'1529341837285'
        }
    },
    u'response': {
        u'numFound':1,
        u'start':0,
        u'docs':[
            {
                u'read_count': 0,
                u'bibcode': u'2017wfc..rept...16R',
                u'bibstem': [u'wfc', u'wfc..rept'],
                u'keyword': [u'Hubble Space Telescope', u'HST', u'Space Telescope Science Institute', u'STScI', u'WFC3', u'infrared blobs', u'IR blobs'],
                u'page_range': u'16',
                u'abstract': u'We present a investigation into possible overlaps between the known IR blobs with the grism aperture reference positions and the IR dither patterns. Each aperture was designed to place the science target (e.g. a specific star) on a cosmetically clean area of the IR detector. Similarly, the dither patterns were designed to mitigate cosmetic defects by rarely (or ideally never) placing such targets on known defects. Because blobs accumulate with time, the originally defined apertures and dither patterns may no longer accomplish their goals, it is important to reverify these combinations. We find two potential overlaps between the blob, aperture, and dither combinations, but do not recommend any changes to the current suite of aperture references positions and/or dither patterns for two reasons. First, one of the overlaps occurs with a dither/aperture combination that is seldom used for high-value science operations, but rather more common for wide-field surveys/mosaics. Second, the other overlap is 8.7 pix from a blob that has a fiducial radius of 10 pix, which already represents a very conservative distance. We conclude that a similar analysis should be repeated as new blobs occur, to continue to ensure ideal operations for high-value science targets. The purpose of this report is to document the analysis in order to facilitate its repetition in the future.',
                u'author': [u'Ryan, R. E.', u'McCullough, P. R.'],
                u'doctype': u'techreport',
                u'pub': u'Space Telescope WFC Instrument Science Report',
                u'num_citations': 0,
                u'num_references': 0,
                u'esources': [u'PUB_PDF'],
                u'pub_raw': u'Instrument Science Report WFC3 2017-16, 6 pages',
                u'year': u'2017',
                u'pubdate': u'2017-06-00',
                u'title': [u'Possible Overlaps Between Blobs, Grism Apertures, and Dithers'],
                u'property': [u'NONARTICLE', u'NOT REFEREED'],
                u'page': [u'16'],
                u'aff': [u'Space Telescope Science Institute', u'Space Telescope Science Institute']
            }
        ]
    }
}

data_5 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 13,
        u'params': {
            u'sort': u'date desc, bibcode desc',
            u'rows': u'1',
            u'fq': u'{!bitset}',
            u'q': u'*:*',
            u'start': u'0',
            u'wt': u'json',
            u'fl': u'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,version,property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem'
        }
    },
    u'response': {
        u'start': 0,
        u'numFound': 1,
        u'docs': [
            {
                u'read_count': 0,
                u'issn': [u'0031-9007'],
                u'pubdate': u'2018-01-00',
                u'abstract': u'Not Available <P />',
                u'num_citations': 0,
                u'year': u'2018',
                u'bibcode': u'2018PhRvL.120b9901P',
                u'bibstem': [u'PhRvL', u'PhRvL.120'],
                u'aff': [u'-', u'-', u'-', u'-'],
                u'esources': [u'PUB_HTML'],
                u'issue': u'2',
                u'pub_raw': u'Physical Review Letters, Volume 120, Issue 2, id.029901',
                u'num_references': 4,
                u'identifier': [u'2018PhRvL.120b9901P', u'10.1103/PhysRevLett.120.029901', u'10.1103/PhysRevLett.120.029901'],
                u'pub': u'Physical Review Letters',
                u'volume': u'120',
                u'doi': [u'10.1103/PhysRevLett.120.029901'],
                u'author': [u'Pustilnik, M.', u'van Heck, B.', u'Lutchyn, R. M.', u'Glazman, L. I.'],
                u'doctype': u'erratum',
                u'eid': u'029901',
                u'title': [u'Erratum: Quantum Criticality in Resonant Andreev Conduction [Phys. Rev. Lett. 119, 116802 (2017)]'],
                u'property': [u'ESOURCE', u'ARTICLE', u'REFEREED'],
                u'page': [u'029901']
            }
        ]
    }
}

data_6 = \
{
    u'responseHeader':{
        u'status': 0,
        u'QTime': 4,
        u'params':{
            u'q': u'first_author:accomazzi',
            u'indent': u'on',
            u'fl': u'bibcode,author,year,pub,bibstem',
            u'sort': u'pub desc',
            u'wt': u'json'
        }
    },
    u'response': {
        u'numFound': 10,
        u'start': 0,
        u'docs': [
            {
                u'year':'2020',
                u'bibcode':'2020AAS...23528705A',
                u'author':['Accomazzi, A.', 'Kurtz, M.', 'Henneken, E.', 'Grant, C.', 'Thompson, D.', 'Chyla, R.', 'McDonald, S.', 'Blanco-Cuaresma, S.', 'Shapurian, G.', 'Hostetler, T.', 'Templeton, M.', 'Lockhart, K.', 'Bukovi, K.'],
                u'pub':'American Astronomical Society Meeting Abstracts',
                u'bibstem':['AAS', 'AAS...235'],
                u'identifier':['2020AAS...23528705A']
            },
            {
                u'year':'2019',
                u'bibcode':'2019EPSC...13.1911A',
                u'author':['Accomazzi, Alberto', 'Kurtz, Michael', 'Henneken, Edwin'],
                u'pub':'EPSC-DPS Joint Meeting 2019',
                u'bibstem':['EPSC', 'EPSC...13'],
                u'identifier': ['2019EPSC...13.1911A']
            },
            {
                u'year':'2015',
                u'bibcode':'2015scop.confE...3A',
                u'author':['Accomazzi, Alberto'],
                u'pub':'Science Operations 2015: Science Data Management',
                u'bibstem':['scop', 'scop.conf'],
                u'identifier':['2015scop.confE...3A', '10.5281/zenodo.34494', '10.5281/zenodo.34494']
            },
            {
                u'year':'2019',
                u'bibcode':'2019AAS...23338108A',
                u'author':['Accomazzi, Alberto', 'Kurtz, Michael J.', 'Henneken, Edwin', 'Grant, Carolyn S.', 'Thompson, Donna M.', 'Chyla, Roman', 'McDonald, Stephen', 'Blanco-Cuaresma, Sergi', 'Shapurian, Golnaz', 'Hostetler, Timothy', 'Templeton, Matthew', 'Lockhart, Kelly'],
                u'pub':'American Astronomical Society Meeting Abstracts #233',
                u'bibstem':['AAS', 'AAS...233'],
                u'identifier': ['2019AAS...23338108A'],
            },
            {
                u'year':'2019',
                u'bibcode':'2019AAS...23320704A',
                u'author':['Accomazzi, Alberto'],
                u'pub':'American Astronomical Society Meeting Abstracts #233',
                u'bibstem':['AAS', 'AAS...233'],
                u'identifier': ['2019AAS...23320704A'],
            },
            {
                u'year':'2018',
                u'bibcode':'2018EPJWC.18608001A',
                u'author':['Accomazzi, Alberto', 'Kurtz, Michael J.', 'Henneken, Edwin A.', 'Grant, Carolyn S.', 'Thompson, Donna M.', 'Chyla, Roman', 'McDonald, Steven', 'Shaulis, Taylor J.', 'Blanco-Cuaresma, Sergi', 'Shapurian, Golnaz', 'Hostetler, Timothy W.', 'Templeton, Matthew R.'],
                u'pub':'European Physical Journal Web of Conferences',
                u'bibstem':['EPJWC', 'EPJWC.186'],
                u'identifier':['2017arXiv171008505A', '2018EPJWC.18608001A', '10.1051/epjconf/201818608001', 'arXiv:1710.08505', '10.1051/epjconf/201818608001', '2017arXiv171008505A']
            },
            {
                u'year':'2018',
                u'bibcode':'2018AAS...23221409A',
                u'author':['Accomazzi, Alberto', 'ADS Team'],
                u'pub':'American Astronomical Society Meeting Abstracts #232',
                u'bibstem':['AAS', 'AAS...232'],
                u'identifier': ['2018AAS...23221409A'],
            },
            {
                u'year':'2017',
                u'bibcode':'2017ASPC..512...45A',
                u'author':['Accomazzi, A.', 'Kurtz, M. J.', 'Henneken, E. A.', 'Grant, C. S.', 'Thompson, D. M.', 'Chyla, R.', 'Holachek, A.', 'Elliott, J.'],
                u'pub':'Astronomical Data Analysis Software and Systems XXV',
                u'bibstem':['ASPC', 'ASPC..512'],
                u'identifier': ['2017adass..25...45A', '2018ASPC..512...45A', '2016arXiv160107858A', '2017ASPC..512...45A', 'arXiv:1601.07858', '2017adass..25...45A', '2018ASPC..512...45A', '2016arXiv160107858A'],
            },
            {
                u'year':'2018',
                u'bibcode':'2018AAS...23136217A',
                u'author':['Accomazzi, Alberto', 'Kurtz, Michael J.', 'Henneken, Edwin', 'Grant, Carolyn S.', 'Thompson, Donna M.', 'Chyla, Roman', 'McDonald, Steven', 'Shaulis, Taylor J.', 'Blanco-Cuaresma, Sergi', 'Shapurian, Golnaz', 'Hostetler, Timothy W.', 'Templeton, Matthew R.', 'Lockhart, Kelly E.'],
                u'pub':'American Astronomical Society Meeting Abstracts #231',
                u'bibstem':['AAS', 'AAS...231'],
                u'identifier': ['2018AAS...23136217A'],
            },
            {
                u'year':'2018',
                u'bibcode':'2018AAS...23130709A',
                u'author':['Accomazzi, Alberto'],
                u'pub':'American Astronomical Society Meeting Abstracts #231',
                u'bibstem':['AAS', 'AAS...231'],
                u'identifier': ['2018AAS...23130709A'],
            },
        ]
    }
}

data_7 = \
{
    u'responseHeader':{
        u'status': 0,
        u'QTime': 8,
        u'params':{
            u'q': u'bibcode:2005GML...tmp....1A',
            u'indent': u'on',
            u'fl': u'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,version,property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem',
            u'wt': u'json'
        }
    },
    u'response': {
        u'numFound': 1,
        u'start': 0,
        u'docs':[
            {
                u'read_count': 0,
                u'doctype': u'article',
                u'bibstem': [u'GML', u'GML...tmp'],
                u'bibcode': u'2005GML...tmp....1A',
                u'identifier': [u'2005GML...tmp....1A', u'10.1007/s00367-005-0006-y', u'10.1007/s00367-005-0006-y'],
                u'pubdate': u'2005-12-00',
                u'copyright': u'(c) 2005: Springer-Verlag',
                u'aff': [u'Department of Geological Sciences, The University of Alabama'],
                u'esources': [u'PUB_HTML'],
                u'year': u'2005',
                u'pub': u'Geo-Marine Letters',
                u'doi': [u'10.1007/s00367-005-0006-y'],
                u'author': [u'Aharon, Paul'],
                u'pub_raw': u'Geo-Marine Letters, Online First',
                u'issn': [u'0276-0460'],
                u'title': [u'Catastrophic flood outbursts in mid-continent left imprints in the Gulf of Mexico'],
                u'property': [u'ESOURCE', u'ARTICLE', u'REFEREED'],
                u'num_references': 0,
                u'num_citations': 2
            }
        ]
    }
}

data_8 = \
{
    u'responseHeader':{
        u'status':0,
        u'QTime':41,
        u'params':{
            u'q':'bibcode:(2017EPJD...71..191Y or 2017JDSO...13...25K)',
            u'indent':'on',
            u'fl':'bibcode,author,year,pub,volume,page,page_count',
            u'wt':'json'
        }
    },
    u'response':{
        u'numFound':2,
        u'start':0,
        u'docs':[
            {
                u'page_count':9,
                u'year': '2017',
                u'page':['191'],
                u'bibcode':'2017EPJD...71..191Y',
                u'author':[u'Yang, Huihui', u'Chen, Hongshan'],
                u'pub':'European Physical Journal D',
                u'volume':'71'
            },
            {
                u'page_count':6,
                u'year': '2017',
                u'page':['25'],
                u'bibcode':'2017JDSO...13...25K',
                u'author':[u'Knapp, Wilfried', u'Thuemen, Chris'],
                u'pub':'Journal of Double Star Observations',
                u'volume':'13'
            }
        ]
    }
}

data_9 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 13,
        u'params': {
            u'sort': u'date desc, bibcode desc',
            u'rows': u'1',
            u'fq': u'{!bitset}',
            u'q': u'*:*',
            u'start': u'0',
            u'wt': u'json',
            u'fl': u'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,version,property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem'
        }
    },
    u'response': {
        u'start': 0,
        u'numFound': 1,
        u'docs': [
            {
                u'identifier': [u'2021arXiv210101542A', u'2021A&A...645L..11A', u'10.1051/0004-6361/202039988', u'arXiv:2101.01542', u'2021arXiv210101542A', u'10.1051/0004-6361/202039988'],
                u'pubdate': u'2021-01-00',
                u'abstract': u"We present a new summary statistic for weak lensing observables, higher than second order, suitable for extracting non-Gaussian cosmological information and inferring cosmological parameters. We name this statistic the `starlet ℓ<SUB>1</SUB>-norm' as it is computed via the sum of the absolute values of the starlet (wavelet) decomposition coefficients of a weak lensing map. In comparison to the state-of-the-art higher-order statistics - weak lensing peak counts and minimum counts, or the combination of the two - the ℓ<SUB>1</SUB>-norm provides a fast multi-scale calculation of the full void and peak distribution, avoiding the problem of defining what a peak is and what a void is: the ℓ<SUB>1</SUB>-norm carries the information encoded in all pixels of the map, not just the ones in local maxima and minima. We show its potential by applying it to the weak lensing convergence maps provided by the MassiveNus simulations to get constraints on the sum of neutrino masses, the matter density parameter, and the amplitude of the primordial power spectrum. We find that, in an ideal setting without further systematics, the starlet ℓ<SUB>1</SUB>-norm remarkably outperforms commonly used summary statistics, such as the power spectrum or the combination of peak and void counts, in terms of constraining power, representing a promising new unified framework to simultaneously account for the information encoded in peak counts and voids. We find that the starlet ℓ<SUB>1</SUB>-norm outperforms the power spectrum by 72% on M<SUB>ν</SUB>, 60% on Ω<SUB>m</SUB>, and 75% on A<SUB>s</SUB> for the Euclid-like setting considered; it also improves upon the state-of-the-art combination of peaks and voids for a single smoothing scale by 24% on M<SUB>ν</SUB>, 50% on Ω<SUB>m</SUB>, and 24% on A<SUB>s</SUB>.",
                u'year': u'2021',
                u'property': [u'ARTICLE', u'EPRINT_OPENACCESS', u'ESOURCE', u'OPENACCESS', u'PUB_OPENACCESS', u'REFEREED'],
                u'page': [u'L11'],
                u'bibcode': u'2021A&A...645L..11A',
                u'bibstem': [u'A&A', u'A&A...645'],
                u'author': [u'Ajani, Virginia', u'Starck, Jean-Luc', u'Pettorino, Valeria'],
                u'aff': [u'AIM, CEA, CNRS, Université Paris-Saclay, Université de Paris, Sorbonne Paris Cité, 91191, Gif-sur-Yvette, France',
                         u'AIM, CEA, CNRS, Université Paris-Saclay, Université de Paris, Sorbonne Paris Cité, 91191, Gif-sur-Yvette, France',
                         u'AIM, CEA, CNRS, Université Paris-Saclay, Université de Paris, Sorbonne Paris Cité, 91191, Gif-sur-Yvette, France'],
                u'esources': [u'EPRINT_HTML', u'EPRINT_PDF', u'PUB_HTML', u'PUB_PDF'],
                u'arxiv_class': [u'astro-ph.CO'],
                u'pub': u'Astronomy and Astrophysics',
                u'volume': u'645',
                u'issn': [u'0004-6361'],
                u'doi': [u'10.1051/0004-6361/202039988'],
                u'keyword': [u'cosmological parameters', u'large-scale structure of Universe', u'methods: statistical',
                             u'neutrinos', u'surveys', u'Astrophysics - Cosmology and Nongalactic Astrophysics'],
                u'doctype': u'article',
                u'read_count': 157,
                u'pub_raw': u'Astronomy &amp; Astrophysics, Volume 645, id.L11, <NUMPAGES>8</NUMPAGES> pp.',
                u'eid': u'L11',
                u'title': [u'Starlet ℓ<SUB>1</SUB>-norm for weak lensing cosmology'],
                u'num_references': 0,
                u'num_citations': 0,
            }
        ]
    }
}

data_10 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 13,
        u'params': {
            u'sort': u'date desc, bibcode desc',
            u'rows': u'1',
            u'fq': u'{!bitset}',
            u'q': u'*:*',
            u'start': u'0',
            u'wt': u'json',
            u'fl': u'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,version,property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem'
        }
    },
    u'response': {
        u'start': 0,
        u'numFound': 1,
        u'docs': [
            {
                u'identifier': [u'2003iha..book..109G', u'2003ASSL..285..109G', u'10.1007/0-306-48080-8_7', u'2003iha..book..109G', u'10.1007/0-306-48080-8_7'],
                u'pubdate': u'2003-03-00',
                u'abstract': u'At this writing, the AIPS package has been in active development and use for over 23 years. It is still the software of choice for all phases of data reduction for the Very Large Array, the most productive groundbased telescope in the world. It is the primary reduction system for most Very Long Baseline Interferometry including the VLBA and has been used to reduce data from other radio interferometers and single-dish telescopes as well as data taken at other wavelengths. The history and general structure of this software package are reviewed and a number of the scientific achievements for which it has been used are summarized.',
                u'year': u'2003',
                u'property': [u'ARTICLE', u'ESOURCE', u'REFEREED', u'TOC'],
                u'page': [u'109'],
                u'bibcode': u'2003ASSL..285..109G',
                u'copyright': u'(c) 2003: Kluwer Academic Publishers',
                u'author': [u'Greisen, E. W.'],
                u'aff': [u'National Radio Astronomy Observatory'],
                u'esources': [u'PUB_HTML'],
                u'editor': [u'Heck, André'],
                u'pub': u'Information Handling in Astronomy - Historical Vistas',
                u'volume': u'285',
                u'page_range': u'109',
                u'doi': [u'10.1007/0-306-48080-8_7'],
                u'bibstem': [u'ASSL', u'ASSL..285'],
                u'doctype': u'inbook',
                u'read_count': 35,
                u'pub_raw': u'Information Handling in Astronomy - Historical Vistas. Edited by André Heck, Strasbourg Astronomical Observatory, France. Astrophysics and Space Science Library, Vol. 285.  Dordrecht: Kluwer Academic Publishers, 2003., p.109',
                u'title': [u'AIPS, the VLA, and the VLBA'],
                u'num_references': 0,
                u'num_citations': 0,
            }
        ]
    }
}

data_11 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 2,
        u'params': {
              u'q': u'bibcode:2016ApJ...818L..26F',
              u'fl': u'read_count,bibcode,doctype,[citations],bibstem',
              u'_':' u1626894650747'}},
    'response': {
        u'numFound': 1,
        u'start': 0,
        u'docs': [
            {
                u'bibcode': u'2016ApJ...818L..26F',
                u'bibstem': [u'ApJL', u'ApJL..818'],
                u'doctype': u'article',
                u'read_count': 2,
                u'[citations]': {u'num_references': 40, u'num_citations': 29},
                u'identifier': [u'2016ApJ...818L..26F',
                                u'2016arXiv160201096F',
                                u'10.3847/2041-8205/818/2/L26',
                                u'2016arXiv160201096F',
                                u'10.3847/2041-8205/818/2/L26',
                                u'arXiv:1602.01096'],

            }
        ]
    }
}

data_12 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 79,
        u'params': {
            u'q': u'bibcode:("2020AAS...23528705A" OR "2019EPSC...13.1911A" OR "2019AAS...23338108A" OR "2019AAS...23320704A")',
            u'fl': u'bibcode,aff,aff_canonical',
            u'_': '1646837683191'}},
    u'response': {
        u'numFound': 4,
        u'start': 0,
        u'docs': [
            {
                u'bibcode': u'2019AAS...23320704A',
                u'identifier':[u'2019AAS...23320704A'],
                u'aff': [u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States'],
                u'aff_canonical': [u'Harvard Smithsonian Center for Astrophysics']},
            {
                u'bibcode': u'2020AAS...23528705A',
                u'identifier': [u'2020AAS...23528705A'],
                u'aff': [
                    u'ADS, Center for Astrophysics | Harvard & Smithsonian, Cambridge, MA',
                    u'-',
                    u'-',
                    u'-',
                    u'-',
                    u'-',
                    u'ADS, Center for Astrophysics | Harvard & Smithsonian, Cambridge, MA',
                    u'-',
                    u'ADS, Center for Astrophysics | Harvard & Smithsonian, Cambridge, MA',
                    u'ADS, Center for Astrophysics | Harvard & Smithsonian, Cambridge, MA',
                    u'-',
                    u'-',
                    u'ADS, Center for Astrophysics | Harvard & Smithsonian, Cambridge, MA'],
                u'aff_canonical': [
                    u'NASA Astrophysics Data System, Center for Astrophysics | Harvard & Smithsonian, Cambridge MA, United States',
                    u'-',
                    u'-',
                    u'-',
                    u'-',
                    u'-',
                    u'NASA Astrophysics Data System, Center for Astrophysics | Harvard & Smithsonian, Cambridge MA, United States',
                    u'-',
                    u'NASA Astrophysics Data System, Center for Astrophysics | Harvard & Smithsonian, Cambridge MA, United States',
                    u'NASA Astrophysics Data System, Center for Astrophysics | Harvard & Smithsonian, Cambridge MA, United States',
                    u'-',
                    u'-',
                    u'NASA Astrophysics Data System, Center for Astrophysics | Harvard & Smithsonian, Cambridge MA, United States'],
            },
            {
                u'bibcode': u'2019EPSC...13.1911A',
                u'identifier': [u'2019EPSC...13.1911A'],
                u'aff': [
                    u'NASA Astrophysics Data System, Center for Astrophysics | Harvard & Smithsonian, Cambridge MA, United States',
                    u'NASA Astrophysics Data System, Center for Astrophysics | Harvard & Smithsonian, Cambridge MA, United States',
                    u'NASA Astrophysics Data System, Center for Astrophysics | Harvard & Smithsonian, Cambridge MA, United States'],
            },
            {
                u'bibcode': u'2019AAS...23338108A',
                u'identifier': [u'2019AAS...23338108A'],
                u'aff': [
                    u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United States',
                        u'Harvard-Smithsonian Center for Astrophysics, Cambridge, MA, United Statesu'],
                u'aff_canonical': [
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics',
                        u'Harvard Smithsonian Center for Astrophysics']
            }
        ]
    }
}

data_13 = \
{
    u'responseHeader': {
        u'status':0,
        u'QTime':43,
        u'params': {
            u'q':'bibcode:2017wfc..rept...16R',
            u'indent':'on',
            u'fl':'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,num_citations,read_count,bibcode,identifier,copyright,keyword,doctype,num_references,comment,property,esources,data,isbn,pubnote,eid',
            'wt':'json',
            '_':'1529341837285'
        }
    },
    u'response': {
        u'numFound':1,
        u'start':0,
        u'docs':[
            {
                u'bibcode': u'2009A&A...506..287L',
                u'abstract': u'Aims: We report the discovery of very shallow (Δ F/F ≈ 3.4× 10<SUP>-4</SUP>), periodic dips in the light curve of an active V = 11.7 G9V star observed by the CoRoT satellite, which we interpret as caused by a transiting companion. We describe the 3-colour CoRoT data and complementary ground-based observations that support the planetary nature of the companion. <BR />Methods: We used CoRoT colours information, good angular resolution ground-based photometric observations in- and out- of transit, adaptive optics imaging, near-infrared spectroscopy, and preliminary results from radial velocity measurements, to test the diluted eclipsing binary scenarios. The parameters of the host star were derived from optical spectra, which were then combined with the CoRoT light curve to derive parameters of the companion. <BR />Results: We examined all conceivable cases of false positives carefully, and all the tests support the planetary hypothesis. Blends with separation &gt;0.40´´or triple systems are almost excluded with a 8 × 10<SUP>-4</SUP> risk left. We conclude that, inasmuch we have been exhaustive, we have discovered a planetary companion, named CoRoT-7b, for which we derive a period of 0.853 59 ± 3 × 10<SUP>-5</SUP> day and a radius of R<SUB>p</SUB> = 1.68 ± 0.09 R_Earth. Analysis of preliminary radial velocity data yields an upper limit of 21 M_Earth for the companion mass, supporting the finding. <BR />Conclusions: CoRoT-7b is very likely the first Super-Earth with a measured radius. This object illustrates what will probably become a common situation with missions such as Kepler, namely the need to establish the planetary origin of transits in the absence of a firm radial velocity detection and mass measurement. The composition of CoRoT-7b remains loosely constrained without a precise mass. A very high surface temperature on its irradiated face, ≈1800-2600 K at the substellar point, and a very low one, ≈50 K, on its dark face assuming no atmosphere, have been derived. <P />The CoRoT space mission, launched on 27 December 2006, has been developed and is operated by CNES, with the contribution of Austria, Belgium, Brazil, ESA, Germany, and Spain. First CoRoT data are available to the public from the CoRoT archive: http://idoc-corot.ias.u-psud.fr. The complementary observations were obtained with MegaPrime/MegaCam, a joint project of CFHT and CEA/DAPNIA, at the Canada-France-Hawaii Telescope (CFHT) which is operated by NRC in Canada, INSU-CNRS in France, and the University of Hawaii; ESO Telescopes at the La Silla and Paranal Observatories under programme ID 081.C-0413(C), DDT 282.C-5015; the IAC80 telescope operated by the Instituto de Astrofísica de Tenerife at the Observatorio del Teide; the Isaac Newton Telescope (INT), operated on the island of La Palma by the Isaac Newton group in the Spanish Observatorio del Roque de Los Muchachos of the Instituto de Astrofisica de Canarias; and at the Anglo-Australian Telescope that have been funded by the Optical Infrared Coordination network (OPTICON), a major international collaboration supported by the Research Infrastructures Programme of the European Commissions Sixth Framework Programme; Radial-velocity observations were obtained with the SOPHIE spectrograph at the 1.93m telescope of Observatoire de Haute Provence, France.',
                u'aff': [
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LUTH, UMR 8102 CNRS, Observatoire de Paris-Meudon, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'Thüringer Landessternwarte Tautenburg, Sternwarte 5, 07778 Tautenburg, Germany',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Instituto de Astrofísica de Canarias, C. via Lactea S/N, 38200 La Laguna, Spain',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'School of Physics, University of Exeter, Stocker Road, Exeter EX4 4QL, UK',
                    u'School of Physics, University of Exeter, Stocker Road, Exeter EX4 4QL, UK',
                    u'Instituto de Astrofísica de Canarias, C. via Lactea S/N, 38200 La Laguna, Spain',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'Observatoire de Haute Provence, USR 2207 CNRS, OAMP, 04870 St. Michel l\'Observatoire, France',
                    u'Institute of Planetary Research, DLR, Rutherfordstr. 2, 12489 Berlin, Germany LUTH, UMR 8102 CNRS, Observatoire de Paris-Meudon, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Rheinisches Institut für Umweltforschung, Universität zu Köln, Abt. Planetenforschung, Aachener Str. 209, 50931 Köln, Germany',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'Institute of Planetary Research, DLR, Rutherfordstr. 2, 12489 Berlin, Germany',
                    u'Institute for Astronomy, University of Vienna, Türkenschanzstrasse 17, 1180 Vienna, Austria',
                    u'Institute of Planetary Research, DLR, Rutherfordstr. 2, 12489 Berlin, Germany',
                    u'Instituto de Astronomia, Geofisica e Ciências Atmosféricas, USP, Sao Paulo, Brazil',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'Observatoire de la Côte d\'Azur, Laboratoire Cassiopée, CNRS UMR 6202, BP 4229, 06304 Nice Cedex 4, France',
                    u'Thüringer Landessternwarte Tautenburg, Sternwarte 5, 07778 Tautenburg, Germany',
                    u'Observatoire de Genève, Université de Genève, 51 Ch. des Maillettes, 1290 Sauverny, Switzerland',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'Laboratoire de Planétologie et Géodynamique, UMR-CNRS 6112, 2 rue de la Houssiniére, 44322 NANTES Cedex 03, France',
                    u'Observatoire de la Côte d\'Azur, Laboratoire Cassiopée, CNRS UMR 6202, BP 4229, 06304 Nice Cedex 4, France',
                    u'Thüringer Landessternwarte Tautenburg, Sternwarte 5, 07778 Tautenburg, Germany',
                    u'Institut d\'Astrophysique de Paris, UMR7095 CNRS, Université Pierre &amp; Marie Curie, 98bis Bd Arago, 75014 Paris, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Space Research Institute, Austrian Academy of Sciences, Schmiedlstrasse 6, 8042 Graz, Austria',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France; Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Observatoire de Genève, Université de Genève, 51 Ch. des Maillettes, 1290 Sauverny, Switzerland',
                    u'School of Physics and Astronomy, R. and B. Sackler Faculty of Exact Sciences, Tel Aviv University, Tel Aviv 69978, Israel',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Rheinisches Institut für Umweltforschung, Universität zu Köln, Abt. Planetenforschung, Aachener Str. 209, 50931 Köln, Germany',
                    u'School of Physics, University of Exeter, Stocker Road, Exeter EX4 4QL, UK',
                    u'Observatoire de Genève, Université de Genève, 51 Ch. des Maillettes, 1290 Sauverny, Switzerland',
                    u'Institute of Planetary Research, DLR, Rutherfordstr. 2, 12489 Berlin, Germany Center for Astronomy and Astrophysics, TU Berlin, Hardenbergstr. 36, 10623 Berlin, Germany',
                    u'Institute of Planetary Research, DLR, Rutherfordstr. 2, 12489 Berlin, Germany Laboratoire d\'Astronomie de Lille, Université de Lille 1, 1 impasse de l\'Observatoire, 59000 Lille, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'School of Physics and Astronomy, R. and B. Sackler Faculty of Exact Sciences, Tel Aviv University, Tel Aviv 69978, Israel',
                    u'Laboratoire de Planétologie et Géodynamique, UMR-CNRS 6112, 2 rue de la Houssiniére, 44322 NANTES Cedex 03, France',
                    u'Instituto de Astrofísica de Canarias, C. via Lactea S/N, 38200 La Laguna, Spain',
                    u'Thüringer Landessternwarte Tautenburg, Sternwarte 5, 07778 Tautenburg, Germany',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Institute of Robotics and Mechatronics, DLR, Rutherfordstr. 2, 12489 Berlin, Germany',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'Centre Spatial de Liège, ULG Science Park, av. du Pré-Aly, 4031, Angleur-Liège, Belgique',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Space Research Institute, Austrian Academy of Sciences, Schmiedlstrasse 6, 8042 Graz, Austria',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France; Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Centre Spatial de Liège, ULG Science Park, av. du Pré-Aly, 4031, Angleur-Liège, Belgique',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'Institut d\'Astrophysique Spatiale, UMR 8617 CNRS, Bât. 121, Université Paris-Sud, 91405 Orsay, France',
                    u'Space Research Institute, Austrian Academy of Sciences, Schmiedlstrasse 6, 8042 Graz, Austria',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Institute of Robotics and Mechatronics, DLR, Rutherfordstr. 2, 12489 Berlin, Germany',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre Spatial de Liège, ULG Science Park, av. du Pré-Aly, 4031, Angleur-Liège, Belgique',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Institute of Robotics and Mechatronics, DLR, Rutherfordstr. 2, 12489 Berlin, Germany',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Institute of Robotics and Mechatronics, DLR, Rutherfordstr. 2, 12489 Berlin, Germany',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'Space Research Institute, Austrian Academy of Sciences, Schmiedlstrasse 6, 8042 Graz, Austria',
                    u'Research and Scientific Support Department, European Space Agency, ESTEC, 2200 Noordwijk, The Netherlands',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Ingenieurbüro Ulmer, Im Technologiepark 1, 15236 Frankfurt/Oder, Germany',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Centre National d\'Études Spatiales, 2 place Maurice Quentin 75039 Paris Cedex 01, France',
                    u'Laboratoire d\'Astrophysique de Marseille, UMR 6110 CNRS, Technopôle de Marseille- Etoile, 13388 Marseille Cedex 13, France',
                    u'LESIA, UMR 8109 CNRS, Observatoire de Paris, UVSQ, Université Paris-Diderot, 5 place J. Janssen, 92195 Meudon, France'
                ],
                u'author': [u'Léger, A.', u'Rouan, D.', u'Schneider, J.', u'Barge, P.', u'Fridlund, M.', u'Samuel, B.', u'Ollivier, M.', u'Guenther, E.', u'Deleuil, M.', u'Deeg, H. J.', u'Auvergne, M.', u'Alonso, R.', u'Aigrain, S.', u'Alapini, A.', u'Almenara, J. M.', u'Baglin, A.', u'Barbieri, M.', u'Bruntt, H.', u'Bordé, P.', u'Bouchy, F.', u'Cabrera, J.', u'Catala, C.', u'Carone, L.', u'Carpano, S.', u'Csizmadia, Sz.', u'Dvorak, R.', u'Erikson, A.', u'Ferraz-Mello, S.', u'Foing, B.', u'Fressin, F.', u'Gandolfi, D.', u'Gillon, M.', u'Gondoin, Ph.', u'Grasset, O.', u'Guillot, T.', u'Hatzes, A.', u'Hébrard, G.', u'Jorda, L.', u'Lammer, H.', u'Llebaria, A.', u'Loeillet, B.', u'Mayor, M.', u'Mazeh, T.', u'Moutou, C.', u'Pätzold, M.', u'Pont, F.', u'Queloz, D.', u'Rauer, H.', u'Renner, S.', u'Samadi, R.', u'Shporer, A.', u'Sotin, Ch.', u'Tingley, B.', u'Wuchterl, G.', u'Adda, M.', u'Agogu, P.', u'Appourchaux, T.', u'Ballans, H.', u'Baron, P.', u'Beaufort, T.', u'Bellenger, R.', u'Berlin, R.', u'Bernardi, P.', u'Blouin, D.', u'Baudin, F.', u'Bodin, P.', u'Boisnard, L.', u'Boit, L.', u'Bonneau, F.', u'Borzeix, S.', u'Briet, R.', u'Buey, J. -T.', u'Butler, B.', u'Cailleau, D.', u'Cautain, R.', u'Chabaud, P. -Y.', u'Chaintreuil, S.', u'Chiavassa, F.', u'Costes, V.', u'Cuna Parrho, V.', u'de Oliveira Fialho, F.', u'Decaudin, M.', u'Defise, J. -M.', u'Djalal, S.', u'Epstein, G.', u'Exil, G. -E.', u'Fauré, C.', u'Fenouillet, T.', u'Gaboriaud, A.', u'Gallic, A.', u'Gamet, P.', u'Gavalda, P.', u'Grolleau, E.', u'Gruneisen, R.', u'Gueguen, L.', u'Guis, V.', u'Guivarc\'h, V.', u'Guterman, P.', u'Hallouard, D.', u'Hasiba, J.', u'Heuripeau, F.', u'Huntzinger, G.', u'Hustaix, H.', u'Imad, C.', u'Imbert, C.', u'Johlander, B.', u'Jouret, M.', u'Journoud, P.', u'Karioty, F.', u'Kerjean, L.', u'Lafaille, V.', u'Lafond, L.', u'Lam-Trong, T.', u'Landiech, P.', u'Lapeyrere, V.', u'Larqué, T.', u'Laudet, P.', u'Lautier, N.', u'Lecann, H.', u'Lefevre, L.', u'Leruyet, B.', u'Levacher, P.', u'Magnan, A.', u'Mazy, E.', u'Mertens, F.', u'Mesnager, J. -M.', u'Meunier, J. -C.', u'Michel, J. -P.', u'Monjoin, W.', u'Naudet, D.', u'Nguyen-Kim, K.', u'Orcesi, J. -L.', u'Ottacher, H.', u'Perez, R.', u'Peter, G.', u'Plasson, P.', u'Plesseria, J. -Y.', u'Pontet, B.', u'Pradines, A.', u'Quentin, C.', u'Reynaud, J. -L.', u'Rolland, G.', u'Rollenhagen, F.', u'Romagnan, R.', u'Russ, N.', u'Schmidt, R.', u'Schwartz, N.', u'Sebbag, I.', u'Sedes, G.', u'Smit, H.', u'Steller, M. B.', u'Sunter, W.', u'Surace, C.', u'Tello, M.', u'Tiphène, D.', u'Toulouse, P.', u'Ulmer, B.', u'Vandermarcq, O.', u'Vergnault, E.', u'Vuillemin, A.', u'Zanatta, P.'],
                u'doctype': u'article',
                u'doi': [u'10.1051/0004-6361/200911933'],
                u'identifier': [u'2009A&A...506..287L', u'10.1051/0004-6361/200911933', u'arXiv:0908.0241', u'2009arXiv0908.0241L'],
                u'issue': "1",
                u'keyword': [u'techniques: photometric', u'techniques: spectroscopic', u'planetary systems', u'techniques: high angular resolution',
                             u'techniques: radial velocities', u'Astrophysics - Earth and Planetary Astrophysics'],
                u'page': [u'287'],
                u'pub': u'Astronomy and Astrophysics',
                u'pubnote': [u'Accepted in Astronomy and Astrophysics; typos and language corrections; version sent to the printer w few upgrades; doi:10.1051/0004-6361/200911933'],
                u'pub_raw': u'Astronomy and Astrophysics, Volume 506, Issue 1, 2009, pp.287-302',
                u'pubdate': "2009-10-00",
                u'title': [u'Transiting exoplanets from the CoRoT space mission. VIII. CoRoT-7b: the first super-Earth with measured radius'],
                u'volume': u'506',
                u'year': u'2009',
                u'page_range': u'287-302',
                u'read_count': 45,
                u'data': [u'ESO:1', u'IRSA:1', u'NExScI:1', u'SIMBAD:8'],
                u'esources': [u'EPRINT_HTML', u'EPRINT_PDF', u'PUB_HTML', u'PUB_PDF'],
                u'property': [u'ARTICLE', u'ASSOCIATED', u'DATA', u'EPRINT_OPENACCESS', u'ESOURCE', u'OPENACCESS', u'PUB_OPENACCESS', u'REFEREED']}]
    }
}

data_14 = \
{
    u'responseHeader': {
        u'status':0,
        u'QTime':8,
        u'params': {
            u'q': u'author:(\'Sameer,\' \'Baliyan, K\' \'Kaur, N\') year:2015',
            u'fl': u'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,version,property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem',
            u'sort': u'bibcode desc',
            u'rows': u'2',
            u'_': u'1671468058045'}
    },
    u'response': {
        'numFound':2,
        'start':0,
        'docs':[
            {
                u'bibcode': u'2015ATel.7495....1S',
                u'abstract': u'FSRQ PKS1510-089 (quasar BZQJ1512-0905, cross identified with the gamma-ray source 2FGLJ1512.8-0906) was detected as VHE source (E &gt; 100MeV) at 5-sigma level by AGILE (Bulgarelli et al Atel # 6366) during the observations integrated over July 13-Aug 2, 2014. ...',
                u'aff':[u'-', u'-', u'-', u'-', u'-'],
                u'author':[u'Sameer', u'Kaur, Navpreet', u'Ganesh, S.', u'Kumar, V.', u'Baliyan, K. S.'],
                u'bibstem':['ATel', u'ATel.7495'],
                u'doctype': u'circular',
                u'identifier':['2015ATel.7495....1S'],
                u'page':[u'1'],
                u'pub': u"The Astronomer's Telegram",
                u'pub_raw': u"The Astronomer's Telegram, No.7495",
                u'pubdate': u'2015-05-00',
                u'title':[u'ATel 7495: Near Infrared flaring of the blazar FSRQ PKS 1510-089: MIRO Observations'],
                u'volume': u'7495',
                u'year': u'2015',
                u'page_range': u'1',
                u'read_count':0,
                u'data':[u'SIMBAD:1'],
                u'esources':[u'PUB_HTML'],
                u'property':[u'DATA', u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'OPENACCESS', u'PUB_OPENACCESS'],
                u'[citations]': {
                    u'num_references':0,
                    u'num_citations':1
                }
            },
            {
                u'bibcode': u'2015ATel.7494....1S',
                u'abstract': u'Larionov et al (Atel # 7474) reported violent optical activity in the source FSRQ B2 1156+29(= 4C +29.45 = Ton 599) during April 11 to May 2, 2015, with source brightening from R=16.7 to R=15.1 levels. ...',
                u'aff':[u'-', u'-', u'-', u'-', u'-'],
                u'author':[u'Sameer', u'Ganesh, S.', u'Kaur, Navpreet', u'Kumar, V.', u'Baliyan, K. S.'],
                u'bibstem':[u'ATel', u'ATel.7494'],
                u'doctype': u'circular',
                u'identifier':['2015ATel.7494....1S'],
                u'page':[u'1'],
                u'pub': u"The Astronomer's Telegram",
                u'pub_raw': u"The Astronomer's Telegram, No.7494",
                u'pubdate': u'2015-05-00',
                u'title':[u'ATel 7494: FSRQ B2 1156+29: NIR follow up observations from MIRO'],
                u'volume': u'7494',
                u'year': u'2015',
                u'page_range': u'1',
                u'read_count':0,
                u'data':[u'SIMBAD:1'],
                u'esources':[u'PUB_HTML'],
                u'property':[u'DATA', u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'OPENACCESS', u'PUB_OPENACCESS'],
                u'[citations]': {
                    u'num_references':0,
                    u'num_citations':0
                }
            }
        ]
    }
}

data_15 = \
{
    u'responseHeader': {
         u'status': 0,
         u'QTime': 8,
         u'params': {
             u'q': u'bibcode:(2023JSMTE2023b3301M OR 2023yCat..19220186H OR 2019Sci...365..565B)',
             u'fl': u'bibcode,comment,pubnote',
             u'_': u'1686158703270'
         }
    },
    u'response': {
        u'numFound': 3,
        u'start': 0,
        u'docs': [
            {
                u'bibcode': u'2019Sci...365..565B',
                u'comment': [u'Galaxies B and C from figures 2 are not in SIMBAD.'],
                u'pubnote': [u'Published online in Science 27 June 2019; doi:10.1126/science.aaw5903']},
            {
                u'bibcode': u'2023JSMTE2023b3301M',
                u'pubnote': [u'doi:10.1088/1742-5468/acaf82']},
            {
                u'bibcode': u'2023yCat..19220186H',
                u'comment': [u'fig1.dat 6946x39 Keck/NIRES near-IR spectrum of peculiar type Ia; SN2020qxp/ASASSN-20jq taken at +191d past the epoch ; of rest-frame B-band maximum (MJD=59277.50)']
            }
        ]
    }
}

data_16 = \
{
  u'responseHeader':{
        u'status':0,
        u'QTime':6,
        u'params': {
            u'q': u'bibcode:(2023zndo...8083529K OR 2023BoSAB..34......)',
            u'fl': u'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,read_count,bibcode,identifier,copyright,keyword,doctype,[citations],comment,version,property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem',
            u'_': u'1702925108780'
        }
  },
  u'response': {
      'numFound':3,
      'start':0,
      'docs':[
        {
            u'bibcode': u'2023zndo...8083529K',
            u'abstract': u'[Background.] Empirical research in requirements engineering (RE) is a constantly evolving topic, with a growing number of publications. Several papers address this topic using literature reviews to provide a snapshot of its \'current\' state and evolution. However, these papers have never built on or updated earlier ones, resulting in overlap and redundancy. The underlying problem is the unavailability of data from earlier works. Researchers need technical infrastructures to conduct sustainable literature reviews. [Aims.] We examine the use of the Open Research Knowledge Graph (ORKG) as such an infrastructure to build and publish an initial Knowledge Graph of Empirical research in RE (KG-EmpiRE) whose data is openly available. Our long-term goal is to continuously maintain KG-EmpiRE with the research community to synthesize a comprehensive, up-to-date, and long-term available overview of the state and evolution of empirical research in RE. [Method.] We conduct a literature review using the ORKG to build and publish KG-EmpiRE which we evaluate against competency questions derived from a published vision of empirical research in software (requirements) engineering for 2020 -- 2025. [Results.] From 570 papers of the IEEE International Requirements Engineering Conference (2000 -- 2022), we extract and analyze data on the reported empirical research and answer 16 out of 77 competency questions. These answers show a positive development towards the vision, but also the need for future improvements. [Conclusions.] The ORKG is a ready-to-use and advanced infrastructure to organize data from literature reviews as knowledge graphs. The resulting knowledge graphs make the data openly available and maintainable by research communities, enabling sustainable literature reviews.',
            u'aff': [u'TIB - Leibniz Information Centre for Science and Technology <ORCID>0000-0001-5336-6899</ORCID>'],
            u'author': [u'Karras, Oliver'],
            u'bibstem': [u'zndo'],
            u'doctype': u'software',
            u'doi': ['10.5281/zenodo.8083529'],
            u'eid': '10.5281/zenodo.8083529',
            u'identifier': [u'2023zndo...8083529K', u'10.5281/zenodo.8083529'],
            u'keyword': [u'Python', u'Jupyter notebook', u'Analysis', u'Empirical research', u'Requirements engineering'],
            u'property': [u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'PUB_OPENACCESS', u'OPENACCESS', u'RELEASE'],
            u'pub': u'Zenodo',
            u'pub_raw': u'Zenodo',
            u'pubdate': u'2023-06-26',
            u'title': [u'Analysis of the State and Evolution of Empirical Research in Requirements Engineering'],
            u'year': '2023',
            u'esources': [u'PUB_HTML'],
            u'publisher': u'Zenodo',
            u'version': u'v1.0',
            u'read_count': 0,
            u'[citations]': {u'num_references': 0, u'num_citations': 1}
        },
        {
            u'bibcode': u'2023BoSAB..34......',
            u'bibstem': [u'BoSAB', u'BoSAB..34'],
            u'doctype': u'misc',
            u'identifier': [u'2023BoSAB..34......'],
            u'pub': u'Boletim da Sociedade Astrônomica Brasileira. Proceedings da XLV Reunião Anual da SAB',
            u'pub_raw': u'Boletim da Sociedade Astrônomica Brasileira. Proceedings da XLV Reunião Anual da SAB',
            u'pubdate': u'2023-00-00',
            u'title': [u'Proceedings da XLV Reunião Anual da SAB'],
            u'volume': u'34',
            u'year': u'2023',
            u'read_count': 0,
            u'property':[u'ARTICLE', u'NOT REFEREED'],
            u'[citations]':{u'num_references':0, u'num_citations':0}
        },
        {
            u'read_count': 1,
            u'bibcode': '2012ddsw.rept.....T',
            u'copyright': u'Oak Ridge National Laboratory',
            u'keyword': [u'Daymet'],
            u'pubdate': u'2012-04-00',
            u'bibstem': [u'ddsw', u'ddsw.rept'],
            u'abstract': u'Archived and distributed through the ORNL DAAC, the Daymet data set provides gridded estimates of daily weather parameters for North America, including daily continuous surfaces of minimum and maximum temperature, precipitation occurrence and amount, humidity, shortwave radiation, snow water equivalent, and day length. The daily time step, 1 km x 1 km spatial resolution, and North American spatial extent of the data set makes it a unique and valuable contribution to scientific, research, and educational communities. The literature shows that Daymet data have been broadly applied to fields including hydrology, terrestrial vegetation growth models, carbon cycle science, and regional to large scale climate change analysis.',
            u'doi': [u'10.3334/ORNLDAAC/1219'],
            u'author': [u'Thornton, P. E.', u'Thornton, M. M.', u'Mayer, B. W.', u'Wilhelmi, N.', u'Wei, Y.', u'Devarakonda, R.', u'Cook, R.'],
            u'doctype': u'dataset',
            u'pub': u'Oak Ridge National Laboratory (ORNL) Distributed Active Archive Center for Biogeochemical Dynamics (DAAC',
            u'pub_raw': u'Oak Ridge National Laboratory (ORNL) Distributed Active Archive Center for Biogeochemical Dynamics (DAAC)',
            u'property': [u'ESOURCE', u'NONARTICLE', u'NOT REFEREED'],
            u'num_citations': 51,
            u'year': u'2012',
            u'esources': [u'PUB_HTML'],
            u'title': [u'Daymet: Daily surface weather on a 1 km grid for North America, 1980-2008'],
            u'identifier': [u'2012ddsw.rept.....T', u'10.3334/ORNLDAAC/1219'],
            u'aff': [u'-', u'-', u'-', u'-', u'-', u'-', u'-'],
            u'num_references': 0
        },

      ]
  }
}

data_17 = \
{
  u'responseHeader':{
    u'status':0,
    u'QTime':73,
    u'params':{
      u'q':u'bibcode:("2023uwff.book.....R" OR "2024asal.book..204V" OR "2018scrp.conf.....K" OR "2024wsp..conf...20V" OR "2024zndo..10908474S")',
      u'fl':u'author,title,year,pubdate,pub,pub_raw,issue,volume,page,page_range,aff,aff_canonical,doi,abstract,read_count,bibcode,identifier,copyright,keyword,doctype[citations],comment,pubnote,version,property,esources,data,isbn,eid,issn,arxiv_class,editor,series,publisher,bibstem,page_count,orcid_pub',
      u'_':u'1712746528052'
    }
  },
  u'response':{
    u'numFound':5,
    u'start':0,
    u'docs':[
      {
        u'bibcode':u'2024zndo..10908474S',
        u'abstract':u'Changes:    improved installation mechanism for Julia  spelling fixes in README.MD',
        u'aff':[u'Paderborn Center for Parallel Computing @DCM-UPB'],
        u'author':[u'Schade, Robert'],
        u'bibstem':[u'zndo'],
        u'doi':[u'10.5281/zenodo.10908474'],
        u'eid':u'10.5281/zenodo.10908474',
        u'identifier':[u'2024zndo..10908474S', u'10.5281/zenodo.10908474'],
        u'property':[u'ESOURCE', u'NONARTICLE', u'NOT REFEREED', u'PUB_OPENACCESS', u'OPENACCESS', u'RELEASE'],
        u'pub':u'Zenodo',
        u'pub_raw':u'Zenodo',
        u'publisher':u'Zenodo',
        u'pubdate':u'2024-04-02',
        u'title':[u'pc2/pqdts: v2024.2'],
        u'year':u'2024',
        u'esources':[u'PUB_HTML'],
        u'version':u'v2024.2',
        u'aff_canonical':[u'-'],
        u'read_count':0,
        u'doctype':u'software',
        u'num_references':0,
        u'num_citations':0
      },
      {
        u'bibcode':u'2024wsp..conf...20V',
        u'abstract':u'Now the surface of Mars is a waterless desert, over which storms rage, raising sand and dust to a height of tens of kilometers. Under modern conditions, open bodies of water cannot exist on Mars. And water on the planet is contained either in the soil layer as permafrost, or in the form of open ice and snow; a very small amount of water is present in gaseous form in the atmosphere. The large reservoirs of water ice on Mars are the polar caps. Studies of Mars by spacecraft have shown that there is a huge amount of ice, and possibly liquid water, under the surface layer at a shallow depth. Analysis of the collected data allowed us to come to the conclusion that liquid water existed in significant quantities on the surface of Mars several billion years ago. That is, in the past, Mars had a full-fledged hydrosphere and a rather powerful atmosphere with a pressure near the surface of more than 0.4 bar. Later, the planet\'s climate changed. It lost much of its atmosphere and water, turning into a cold world. On the surface of Mars, there are numerous winding valleys with a long length, reminiscent of the dried-up channels of terrestrial rivers. A significant portion of the water that once flowed along currently dry riverbeds must now be under the surface of the planet. It is also possible that some channels are the result of the action of not liquid water, but a mixture of mud, ice and steam that flow only episodically. It is possible that the meandering valleys formed moving masses of glaciers. There is every reason to believe that there is still a lot of water on Mars, and it still exists in the form of permafrost. A perspective image of the Echus Chasma region suggests that liquid water was present on this part of the Martian surface up to a billion years ago. Later, the planet cooled down, the lakes froze, and glaciers formed, which \'cut\' the Kasei Valles with their streams.',
        u'aff':[u'National University of Life and Environmental Sciences of Ukraine'],
        u'author':[u'Vidmachenko, A.'],
        u'bibstem':[u'wsp', u'wsp..conf'],
        u'identifier':[u'2024wsp..conf...20V'],
        u'isbn':[u'9789244513880'],
        u'keyword':[u'Mars', u'riverbeds', u'meandering valleys', u'glaciers', u'eternal permafrost'],
        u'orcid_pub':[u'0000-0002-0523-5234'],
        u'page':[u'20'],
        u'pub':u'Proceedings of the VIII International Scientific and Practical Conference. World science priorities (February 08 – 09',
        u'pub_raw':u'Proceedings of the VIII International Scientific and Practical Conference. World science priorities (February 08 – 09, 2024) Chapter Astronomy. Publisher: «World of Conferences». Vienna. Austria. P. 20-25. ISBN 978-92-44513-88-0.',
        u'publisher': u'World of Conferences',
        u'pubdate':u'2024-02-00',
        u'title':[u'A modern view of former rivers on Mars.'],
        u'year':u'2024',
        u'page_count':6,
        u'page_range':u'20-25',
        u'aff_canonical':[u'-'],
        u'read_count':3,
        u'esources':[u'AUTHOR_HTML'],
        u'property':[u'ARTICLE', u'AUTHOR_OPENACCESS', u'ESOURCE', u'NOT REFEREED', u'OPENACCESS'],
        u'doctype':u'inproceedings',
        u'num_references':0,
        u'num_citations':0
      },
      {
        u'bibcode':u'2024asal.book..204V',
        u'abstract':u'In the next few years, several new astronomical instruments are planned to be launched on Earth and in space. Each of these devices is very expensive! But many countries allocate large amounts of money for this, and plan to receive more and more recent data about the surrounding universe. Telescopes are devices for observing distant objects. The very first working telescope was created in 1608 by the Dutch optician Hans Lippersgei. The creation of the telescope was also attributed to such masters as another Dutch eyeglass maker from Middelburg, Zachary Janssen, and Jacob Mathews from the city of Alkmaar. These earliest telescopes consisted of a convex lens as an objective and a concave lens that served as an eyepiece. In 1609, Galileo Galilei significantly improved the design of the telescope, achieving a 30-fold increase in the original images. With its help, Galileo performed the first survey of the heavenly bodies. Therefore, even now, the creation of astronomical instruments, whose characteristics significantly improve previous examples of telescope construction, is considered extremely important in astronomical research. The Hubble telescope was the first to provide interesting information about the features of images of the most distant galaxies. They are significantly different from those formed relatively recently. One of the world\'s largest ground-based telescopes, the Giant Magellan Telescope, is under construction. It is being built in Chile and its gradual commissioning will begin in 2024. Segments of seven monolithic mirrors, with a diameter of 8.4 m each, create an optical surface with an equivalent diameter of 24.5 m. Larger will be the 30-meter telescope, which is planned to be built on the island of Hawaii, next to the two 9-meter Keck reflectors at the Mauna Kea observatory. The mirror surface of this telescope will consist of almost five hundred hexagonal segments and will reach a diameter of 30 m. It is expected to be tested in 2027. In 2014, the European Southern Observatory started the construction of the Extremely Large Telescope. In 2025, it is planned to become the most powerful optical astronomical instrument in the world, with an equivalent diameter of its mirror surface of 39 m.',
        u'aff':[u'National University of Life and Environmental Sciences of Ukraine'],
        u'author':[u'Vidmachenko, A.'],
        u'bibstem':[u'asal', u'asal.book'],
        u'identifier':[u'2024asal.book..204V'],
        u'keyword':[u'new astronomical instruments', u'Telescopes', u'telescope construction', u'astronomical research'],
        u'orcid_pub':[u'0000-0002-0523-5234'],
        u'page':[u'204'],
        u'pub':u'In book: Astronomical almanac',
        u'pub_raw':u'In book: Astronomical almanac, 70, Edition: MAO NAS of Ukraine. Publisher: Kyiv, Akademperiodika, p. 204-209.',
        u'publisher': u'Kyiv',
        u'pubdate':u'2024-01-00',
        u'title':[u'New generation telescopes for the astronomy of the future.'],
        u'year':u'2024',
        u'page_count':6,
        u'page_range':u'204-209',
        u'aff_canonical':[u'-'],
        u'read_count':2,
        u'esources':[u'AUTHOR_HTML'],
        u'property':[u'ARTICLE', u'AUTHOR_OPENACCESS', u'ESOURCE', u'NOT REFEREED', u'OPENACCESS'],
        u'doctype':u'inbook',
        u'num_references':0,
        u'num_citations':0
      },
      {
        u'bibcode':u'2018scrp.conf.....K',
        u'abstract':u'The portable Raspberry Pi computing platform with the power of Linux yields an exciting exploratory tool for beginning scientific computing. Science and Computing with Raspberry Pi takes the reader through explorations in a variety of computing exercises with the physical sciences. The book guides the user through: configuring your Raspberry Pi and Linux operating system; understanding the software requirements while using the Pi for scientific computing; computing exercises in physics, astronomy, chaos theory, and machine learning.',
        u'aff':[u'NRAO'],
        u'author':[u'Kent, Brian R.'],
        u'bibstem':[u'scrp', u'scrp.conf'],
        u'copyright':u'Copyright (c) 2018 Morgan & Claypool Publishers',
        u'identifier':[u'2018scrp.conf.....K'],
        u'isbn':[u'9781681749969', u'9781681749938'],
        u'keyword':[u'single board computing', u'astronomy', u'very large array', u'astrophysics', u'visualization', u'data science', u'computing', u'radio astronomy'],
        u'orcid_pub':[u'-'],
        u'pub':u'Science and Computing with Raspberry Pi',
        u'pub_raw':u'Science and Computing with Raspberry Pi, by Brian R. Kent. Online ISBN: 978-1-6817-4996-9,  Print ISBN: 978-1-6817-4993-8, Morgan &amp; Claypool Publishers, 2018',
        u'publisher': u'Morgan & Claypool',
        u'pubdate':u'2018-07-00',
        u'title':[u'Science and Computing with Raspberry Pi'],
        u'year':u'2018',
        u'read_count':0,
        u'esources':[u'PUB_HTML'],
        u'property':[u'ESOURCE', u'NONARTICLE', u'NOT REFEREED'],
        u'aff_canonical':[u'National Radio Astronomy Observatory, Virginia'],
        u'doctype':u'proceedings',
        u'num_references':0,
        u'num_citations':0
      },
      {
        u'bibcode':u'2023uwff.book.....R',
        u'abstract':u'A forecast for New Zealand\'s changing climate and why it matters to our everyday lives A warmer world will change more than just our weather patterns. It will change the look of the land around us, what grows and lives on it - including us. Drawing on climate models that can travel to ice ages and hothouses of the deep past, Professor James Renwick untangles how we know exactly what the future holds and why it matters to our everyday lives. He looks at New Zealand\'s more frequent natural disasters, warming and increasingly acidic waters, the creep of rising sea levels, and the ways that the changing weather will affect our agriculture, lifestyle, food security and economy.Arresting, galvanizing and clear-sighted, Under the Weather is a picture of a miraculous planet in danger, a stock-take on what it means for this small country, and a reminder that the shape of our future is up to us.\'--Publisher description.',
        u'aff':[u'-'],
        u'author':[u'Renwick, J. A.'],
        u'bibstem':[u'uwff', u'uwff.book'],
        u'identifier':[u'2023uwff.book.....R'],
        u'isbn':[u'9781775541721'],
        u'orcid_pub':[u'-'],
        u'pub':u'Under the weather: a future forecast for New Zealand',
        u'pub_raw':u'Under the weather: a future forecast for New Zealand, by J. A. Renwick, 2023. Auckland: HarperCollins Publishers. OCLC: 1388369161. ISBN: 9781775541721.',
        u'publisher': u'HarperCollins',
        u'pubdate':u'2023-00-00',
        u'title':[u'Under the weather: a future forecast for New Zealand'],
        u'year':u'2023',
        u'aff_canonical':[u'-'],
        u'read_count':0,
        u'esources':[u'PUB_HTML'],
        u'property':[u'ESOURCE', u'NONARTICLE', u'NOT REFEREED'],
        u'doctype':u'book',
        u'num_references':0,
        u'num_citations':0
      }
    ]
  }
}

data_18 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 141,
        u'params': {
            u'q': u'bibcode:(2001physics...2042S OR 2017isra.book.....T OR 1990ApJ...355..726W OR 1978Navig..25..121S OR 2013Ecogr..36.1058M OR 2009AGUFMPP31D1382A OR 1992ApJ...392..310W OR 1971ApJ...164..399S)',
            u'fl': u'bibcode,author',
            u'_': u'1731959426353'
        }
    },
    u'response':{
        u'numFound':8,
        u'start':0,
        u'docs':[
          {
            u'bibcode': u'2001physics...2042S',
            u'author':[u'Smith, Frank D., Jr']},
          {
            u'bibcode': u'2017isra.book.....T',
            u'author':[u'Thompson, A. Richard', u'Moran, James M.', u'Swenson, George W., Jr.']},
          {
            u'bibcode': u'1990ApJ...355..726W',
            u'author':[u'Wang, Y. -M.', u'Sheeley, N. R., Jr.']},
          {
            u'bibcode': u'1978Navig..25..121S',
            u'author':[u'Spilker, J. J., Jr.']},
          {
            u'bibcode': u'2009AGUFMPP31D1382A',
            u'author':[u'Anderson, D. G.', u'Goodyear, A. C.', u'Stafford, T. W., Jr.', u'Kennett, J.', u'West, A.']},
          {
            u'bibcode': u'1992ApJ...392..310W',
            u'author':[u'Wang, Y. -M.', u'Sheeley, N. R., Jr.']},
          {
            u'bibcode': u'1971ApJ...164..399S',
            u'author':[u'Spitzer, Lyman, Jr.', u'Hart, Michael H.']},
          {
            u'bibcode': u'2013Ecogr..36.1058M',
            u'author':[u'Merow, Cory', u'Smith, Matthew J.', u'Silander, John A., Jr.']}
        ]
    }
}

data_19 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 42,
        u'params': {
            'q':'author:\'shapurian,g\'',
            u'fl': u'bibcode,author,pub_raw,year',
            u'_': u'1732120045561'
        }
    },
    u'response':{
        u'numFound':3,
        u'start':0,
        u'docs':[
          {
            u'bibcode': u'2023arXiv231208579S',
            u'author':[u'Shapurian, Golnaz', u'Kurtz, Michael J', u'Accomazzi, Alberto'],
            u'pub_raw': u'eprint arXiv:2312.08579',
            u'year': u'2023'},
          {
            u'bibcode': u'2024arXiv240611400S',
            u'author':[u'Shapurian, Golnaz'],
            u'pub_raw': u'eprint arXiv:2406.11400',
            u'year': u'2024'},
          {
            u'bibcode': u'2023AAS...24117714K',
            u'author':[u'Koch, Jennifer', u'Shapurian, Golnaz', u'Grant, Carolyn', u'Thompson, Donna', u'ADS Team'],
            u'pub_raw': u'American Astronomical Society Meeting #241, id. 177.14. <ALTJOURNAL>Bulletin of the American Astronomical Society, Vol. 55, No. 2 e-id 2023n2i177p14</ALTJOURNAL>',
            u'year': u'2023'}
        ]
    }
}

data_20 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 163,
        u'params': {
            'q':'author:\'^André\'',
            u'fl': u'bibcode,author,pub_raw,year',
            u'_': u'1732120045561'
        }
    },
    u'response':{
        u'numFound':1,
        u'start':0,
        u'docs':[
            {
                u'bibcode': u'2014prpl.conf...27A',
                u'author': [u'André, P.', u'Di Francesco, J.', u'Ward-Thompson, D.', u'Inutsuka, S. -I.', u'Pudritz, R. E.', u'Pineda, J. E.'],
                u'pub_raw': u'Protostars and Planets VI, Henrik Beuther, Ralf S. Klessen, Cornelis P. Dullemond, and Thomas Henning (eds.), University of Arizona Press, Tucson, p.27-51',
                u'year': u'2014'}
        ]
    }
}

data_21 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 51,
        u'params': {
            u'q': u'author:"^accomazzi" year:2019',
            u'indent': u'on',
            u'fl': u'bibcode,author,pub,year',
            u'wt': u'json',
            u'_': u'1560183872951'
        }
    },
    u'response': {
        u'numFound': 3,
        u'start': 0,
        u'docs': [
            {
                u'year': u'2019',
                u'bibcode': u'2019AAS...23338108A',
                u'bibstem': [u'AAS', u'AAS...233'],
                u'author': [u'Accomazzi, Alberto', u'Kurtz, Michael J.', u'Henneken, Edwin', u'Grant, Carolyn S.',
                            u'Thompson, Donna M.', u'Chyla, Roman', u'McDonald, Stephen',
                            u'Blanco-Cuaresma, Sergi', u'Shapurian, Golnaz', u'Hostetler, Timothy',
                            u'Templeton, Matthew', u'Lockhart, Kelly'],
                u'pub': u'American Astronomical Society Meeting Abstracts #233'
            },
            {
                u'year': u'2019',
                u'bibcode': u'2019AAS...23320704A',
                u'bibstem': [u'AAS', u'AAS...233'],
                u'author': [u'Accomazzi, Alberto'],
                u'pub': u'American Astronomical Society Meeting Abstracts #233'
            },
            {
                u'year': u'2019',
                u'bibcode': u'2019hsax.conf..526G',
                u'author': [u'Garzón, F.', u'Patrick, L.', u'Hammersley, P.', u'Streblyanska, A.',
                            u'Insausti, M.', u'Barreto, M.', u'Fernández, P.', u'Joven, E.',
                            u'López, P.', u'Mato, A.', u'Moreno, H.', u'Núñez, M.', u'Patrón, J.',
                            u'Pascual, S.', u'Cardiel, N.'],
                u'pub': u'Highlights on Spanish Astrophysics X',
                u'bibstem': [u'hsax', u'hsax.conf']
            }
        ]
    }
}

data_22 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 29,
        u'params': {
            u'q': u'author:"accomazzi" AND doctype:eprint AND year:2021',
            u'fl': u'bibcode,eid,eprint',
            u'sort': u'bibcode desc',
            u'rows': u'300',
            u'_': u'1642527401469'
        }
    },
    u'response': {
        u'numFound': 2,
        u'start': 0,
        u'docs': [
            {
                u'bibcode': u'2021arXiv211200590G',
                u'eid': u'arXiv:2112.00590'
            },
            {
                u'bibcode': u'2021arXiv210601477C',
                u'eid': u'arXiv:2106.01477'
            }
        ]
    }
}

data_23 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 1,
        u'params': {
            u'sort': u'date desc',
            u'fq': u'{!bitset}',
            u'rows': u'19',
            u'q': u'*:*',
            u'start': u'0',
            u'wt': u'json',
            u'fl': u'author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,num_citations,read_count,bibcode,identification,copyright,keyword,doctype,num_references,comment,property,esources,data'
        }
    },
    u'response': {
        u'start': 0,
        u'numFound': 4,
        u'docs': [
            {
                u'title': [u'A Microwave Free-Space Method Using Artificial Lens with Anti-reflection Layer'],
                u'author': [ u'Zhang, Yangjun', u'Aratani, Yuki', u'Nakazima, Hironari' ]
            },
            {
                u'author': [u'Ryan, R. E.', u'McCullough, P. R.']
            },
            {
                u'title': [ u'Resolving Gas-Phase Metallicity In Galaxies']
            },
            {
                u'bibcode': u'2017ascl.soft06009C'
            }
        ]
    }
}

data_24 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 2,
        u'params': {
            u'q': u'title:"lt;"',
            u'indent': u'on',
            u'fl': u'bibcode,title,abstract',
            u'wt': u'json',
            u'_': u'1592510843440'
        }
    },
    u'response': {
        u'numFound': 4,
        u'start': 0,
        u'docs': [
            {
                u'bibcode': u'2016JLwT...34.4926L',
                u'title': [u'Study of SiO{}_{{{x}}} (1 &lt; x lt; 2) Thin-Film Optical Waveguides']
            },
            {
                u'bibcode': u'2016ApJ...832..124B',
                u'abstract': u'Using Hubble Space Telescope Cosmic Origins Spectrograph observations of 89 QSO sightlines through the Sloan Digital Sky Survey footprint, we study the relationships between C IV absorption systems and the properties of nearby galaxies, as well as the large-scale environment. To maintain sensitivity to very faint galaxies, we restrict our sample to 0.0015&lt; z&lt; 0.015, which defines a complete galaxy survey to L≳ 0.01 L\\ast or stellar mass {M}<SUB>* </SUB>≳ {10}<SUP>8</SUP> {M}<SUB>☉ </SUB>. We report two principal findings. First, for galaxies with impact parameter ρ &lt; 1 {r}<SUB>{vir</SUB>}, C IV detection strongly depends on the luminosity/stellar mass of the nearby galaxy. C IV is preferentially associated with galaxies with {M}<SUB>* </SUB>&gt; {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB>; lower-mass galaxies rarely exhibit significant C IV absorption (covering fraction {f}<SUB>C</SUB>={9}<SUB>-6</SUB><SUP>+12</SUP> % for 11 galaxies with {M}<SUB>* </SUB>&lt; {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB>). Second, C IV detection within the {M}<SUB>* </SUB>&gt; {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB> population depends on environment. Using a fixed-aperture environmental density metric for galaxies with ρ &lt; 160 kpc at z&lt; 0.055, we find that {57}<SUB>-13</SUB><SUP>+12</SUP> % (8/14) of galaxies in low-density regions (regions with fewer than seven L&gt; 0.15 L\\ast galaxies within 1.5 Mpc) have affiliated C IV absorption; however, none (0/7) of the galaxies in denser regions show C IV. Similarly, the C IV detection rate is lower for galaxies residing in groups with dark matter halo masses of {M}<SUB>{halo</SUB>}&gt; {10}<SUP>12.5</SUP> {M}<SUB>☉ </SUB>. In contrast to C IV, H I is pervasive in the circumgalactic medium without regard to mass or environment. These results indicate that C IV absorbers with {log} N({{C}} {{IV}})≳ 13.5 {{cm}}<SUP>-2</SUP> trace the halos of {M}<SUB>* </SUB>&gt; {10}<SUP>9.5</SUP> {M}<SUB>☉ </SUB> galaxies but also reflect larger-scale environmental conditions.'
            },
            {
                u'bibcode': u'2015hst..prop14424B',
                u'title': [u'STIS CCD Amp A, C, &amp; D Gains']
            },
            {
                u'bibcode': u'2016BaltA..25..310K',
                u'abstract': u'We use the Apparent Motion Parameters (AMP) method for the determination of orbits of visual double stars (Kiselev &amp; Kiyaeva 1980). The quality of AMP orbits is completely dependent on the precision of parameters of relative positions and motions at the same instant. They are calculated on the basis of a short arc of observations. To determine these parameters, we use recent high precision observations obtained with the best modern techniques. New orbits of three stars are presented.'
            }
        ]
    }
}

data_25 = \
{
    u'responseHeader': {
        u'status': 1,
        u'QTime': 1,
        u'params': {
            u'sort': u'date desc',
            u'fq': u'{!bitset}',
            u'rows': u'19',
            u'q': u'*:*',
            u'start': u'0',
            u'wt': u'json',
            u'fl': u'author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,num_citations,read_count,bibcode,identification,copyright,keyword,doctype,num_references,comment,property,esources,data'
        }
    }
}

# records with various doctypes having doi
# note that as of end of 2024 there no records with doi for the following doctypes
# proposal, pressrelease, talk
data_26 = \
{
    u'responseHeader': {
        u'status': 0,
        u'QTime': 3310,
        u'params': {
            u'q': u'doi:"10.*"',
            u'fl': u'doc_type,bibcode,author,year,pub_raw,doi',
            u'start': u'0',
            u'internal_logging_params': u'X-Amzn-Trace-Id=Root=1-676448cf-4ba786881db5c3346f632766',
            u'boost': u'add(doctype_boost, 1)',
            u'sort': u'date desc',
            u'rows': u'1',
            u'wt': 'json'
        }
    },
    u'response': {
        u'numFound': 20,
        u'start': 0,
        u'numFoundExact': True,
        u'docs': [
            {
                u'bibcode': u'2025NML....17...42Y',
                u'author': [u'Yin, Hao', u'Li, Yanting', u'Tian, Zhiying', u'Li, Qichao', u'Jiang, Chenhui',
                            u'Liang, Enfu', u'Guo, Yiping'],
                u'doctype': u'article',
                u'doi': [u'10.1007/s40820-024-01539-6'],
                u'pub_raw': u'Nano-Micro Letters, Volume 17, Issue 1, id.42',
                u'pub': u'Nano-Micro Letters',
                u'year': u'2025'
            },
            {
                u'bibcode': '2024E3SWC.50307004O',
                u'author': [u'Okselni, Tia', u'Efdi, Mai'],
                u'doctype': u'inproceedings',
                u'doi': [u'10.1051/e3sconf/202450307004'],
                u'pub_raw': u'The 9th International Symposium on Applied Chemistry in conjuction with the 5th International Conference on Chemical and Material Engineering (ISAC-ICCME 2023), Serpong, Banten, Indonesia, Edited by Dwi Anggoro, D.; Kumoro, A.C.; Dahnum, D.; Restu, W.K.; Sembiring, K.C.; Indriyati, ; Ndruru, S.T.C.L.; Putri, A.M.H.; E3S Web of Conferences, Volume 503, id.07004',
                u'pub': u'E3S Web of Conferences',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024arXiv241203744G',
                u'author': [u'Gadhia, Nandini', u'Smyrnakis, Michalis', u'Liu, Po-Yu', u'Blake, Damer', u'Hay, Melanie',
                            u'Nguyen, Anh', u'Richards, Dominic', u'Xia, Dong', u'Krishna, Ritesh'],
                u'doctype': u'eprint',
                u'doi': [u'10.48550/arXiv.2412.03744'],
                u'pub_raw': u'eprint arXiv:2412.03744',
                u'pub': u'arXiv e-prints',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024AbICA...8....1A',
                u'author': [u'Adolf, Albert', u'Karsznia, Izabela'],
                u'doctype': u'abstract',
                u'doi': [u'10.5194/ica-abs-8-1-2024'],
                u'pub_raw': u'Abstracts of the ICA, Volume 8, page 1',
                u'pub': u'Abstracts of the ICA',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024sisy.rept...14Z',
                u'author': [u'Zusi, Michele', u'Simioni, Emanuele', u'Vincenzo, Della Corte', u'Andrea, Cicchetti',
                            u'Politi, Romolo', u'Cremonese, Gabriele', u'Capaccioni, Fabrizio', u'Doressoundiram, Alain',
                            u'Palumbo, Pasquale', u'Re, Cristina', u'Vincendon, Mathieu'],
                u'doctype': u'techreport',
                u'doi': [u'10.5281/zenodo.13890990'],
                u'pub_raw': u'SIMBIO-SYS Instrument Documentation, id. 14',
                u'pub': u'SIMBIO-SYS Instrument Documentation',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024PhDT........20B',
                u'author': [u'Braemer, Adrian Lukas'],
                u'doctype': u'phdthesis',
                u'doi': [u'10.11588/heidok.00035657'],
                u'pub_raw': u'PhD thesis from Heidelberg University, Combined Faculty of Mathematics, Engineering and Natural Sciences',
                u'pub': u'Ph.D. Thesis',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024CSSP...43.7972Y',
                u'author': [u'Yuan, Sihan', u'Ning, Gengxin', u'Lin, Yushen'],
                u'doctype': u'circular',
                u'doi': [u'10.1007/s00034-024-02838-4'],
                u'pub_raw': u'Circuits, Systems, and Signal Processing, Volume 43, Issue 12, pp. 7972-7988',
                u'pub': u'Circuits Systems and Signal Processing',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024oenh.book..506D',
                u'author': [u'Dormady, Noah'],
                u'doctype': u'inbook',
                u'doi': [u'10.1093/acrefore/9780199389407.013.506'],
                u'pub_raw': u'Oxford Research Encyclopedia of Natural Hazard Science.  Edited by Djillali Benouar et al. ISBN: 978-0-199-38940-7. Oxford University Press, article id. 506',
                u'pub': u'Oxford Research Encyclopedia of Natural Hazard Science',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024PRegS.103j0043A',
                u'author': [u'Alifah, Julia Nurul', u'Fauziyah, Annisa Salma', u'Pranoto, Joko', u'Miu, Iwan'],
                u'doctype': u'bookreview',
                u'doi': [u'10.1016/j.pirs.2024.100043'],
                u'pub_raw': u'Papers in Regional Science, vol. 103, issue 6, p. 100043',
                u'pub': u'Papers in Regional Science',
                u'year': u'2024'
            },
            {
                u'bibcode': '2025psge.book.....B',
                u'author': [u'Byun, Sung-Soo', u'Forrester, Peter J.'],
                u'doctype': u'book',
                u'doi': [u'10.1007/978-981-97-5173-0'],
                u'pub_raw': u'Progress on the Study of the Ginibre Ensembles, by Sung-Soo Byun and Peter J. Forrester. KIAS Springer Series in Mathematics, volume 3, 2025',
                u'pub': u'Progress on the Study of the Ginibre Ensembles',
                u'year': u'2025'
            },
            {
                u'bibcode': '2025NuPhA105322966M',
                u'author': [u'Moumene, Imane', u'Bonaccorso, Angela'],
                u'doctype': u'erratum',
                u'doi': [u'10.1016/j.nuclphysa.2024.122966'],
                u'pub_raw': u'Nuclear Physics, Section A, Volume 1053, id.122966',
                u'pub': u'Nuclear Physics A',
                u'year': u'2025'
            },
            {
                u'bibcode': '2024SPIE13420E....X',
                u'author': [u'Xu, Jinyang', u'Davim, J. Paulo'],
                u'doctype': u'proceedings',
                u'doi': [u'10.1117/12.3055927'],
                u'pub_raw': u'Third International Conference on New Materials, Machinery, and Vehicle Engineering (NMMVE 2024). Edited by Xu, Jinyang; Davim, J. Paulo. Proceedings of the SPIE, Volume 13420 (2024).',
                u'pub': u'Third International Conference on New Materials, Machinery, and Vehicle Engineering (NMMVE 2024)',
                u'year': u'2024'
            },
            {
                u'bibcode': '2025JTerr.11701032T',
                u'author': [u'Tekeste, Mehari'],
                u'doctype': u'editorial',
                u'doi': [u'10.1016/j.jterra.2024.101032'],
                u'pub_raw': u'Journal of Terramechanics, Volume 117, id.101032',
                u'pub': u'Journal of Terramechanics',
                u'year': u'2025'
            },
            {
                u'bibcode': '2019GCN.25753....1L',
                u'author': [u'LIGO Scientific Collaboration', u'Virgo Collaboration'],
                u'doctype': u'newsletter',
                u'doi': [u'10.1007/s11433-010-4137-4'],
                u'pub_raw': u'GRB Coordinates Network, Circular Service, No. 25753',
                u'pub': u'GRB Coordinates Network',
                u'year': u'2019'
            },
            {
                u'bibcode': '2024zndo..10053554S',
                u'author': [u'susannawinkelbauer'],
                u'doctype': u'software',
                u'doi': [u'10.5281/zenodo.10053554'],
                u'pub_raw': u'Zenodo',
                u'pub': u'Zenodo',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024pds..data...79T',
                u'author': [u'Tedesco, Edward', u'Davis, Donald R.'],
                u'doctype': u'dataset',
                u'doi': [u'10.26033/ms2j-v867'],
                u'pub_raw': u'NASA Planetary Data System, urn:nasa:pds:gbo.ast.loneos.survey::1.0',
                u'pub': u'NASA Planetary Data System',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024MsT..........5R',
                u'author': [u'Reynoso, Armando'],
                u'doctype': u'mastersthesis',
                u'doi': [u'10.48550/arXiv.2312.10071'],
                u'pub_raw': u'ProQuest Dissertations And Thesis; Thesis (M.S.)--California State University, Long Beach, 2024.; Publication Number: AAT 31336259; ISBN: 9798384481096; Source: Masters Abstracts International, Volume: 86-04.; 66 p.',
                u'pub': u'Masters Thesis',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024JLum..27620834B',
                u'author': [u'Bettinelli, Marco'],
                u'doctype': u'obituary',
                u'doi': [u'10.1016/j.jlumin.2024.120834'],
                u'pub_raw': u'Journal of Luminescence, Volume 276, id.120834',
                u'pub': u'Journal of Luminescence',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024..............S',
                u'author': [u'Stovall, J. Willis'],
                u'doctype': u'misc',
                u'doi': [u'10.2475/001c.118656'],
                u'pub_raw': u'American Journal of Science, issue 202',
                u'pub': u'American Journal of Science',
                u'year': u'2024'
            },
            {
                u'bibcode': '2024MPEC....C....9B',
                u'author': [u'Beuden, T.', u'Carvajal, V. F.', u'Fay, D.', u'Fazekas, J. B.', u'Fuls, D. C.',
                            u'Gibbs, A. R.', u'Grauer, A. D.', u'Groeller, H.', u'Hogan, J. K.', u'Kowalski, R. A.',
                            u'Larson, S. M.', u'Leonard, G. J.', u'Rankin, D.', u'Seaman, R. L.', u'Shelly, F. C.',
                            u'Wierzchos, K. W.', u'Watanabe, H.', u'Kozhukhov, A. M.', u'Kechin, Y.', u'Lipunov, V.',
                            u'Gorbovskoy, E.', u'Tiurina, N.', u'Balanutsa, P.', u'Kornilov, V.', u'Kuznetsov, A.',
                            u'Gress, O.', u'Zimnukhov, D.', u'Yazev, S.', u'Budnev, N.', u'Hahn, R.', u'Ursache, F.',
                            u'Dupouy, P.', u'Buzzi, L.', u'Hug, G.', u'Linder, T.', u'Holmes, R.', u'Horn, L.',
                            u'Denneau, L.', u'Erasmus, N.', u'Fitzsimmons, A.', u'Lawrence, A.', u'Robinson, J.',
                            u'Siverd, R.', u'Tonry, J.', u'Weiland, H.'],
                u'doctype': u'catalog',
                u'doi': [u'10.48377/MPEC/2024-C09'],
                u'pub_raw': u'Minor Planet Electronic Circ., No. 2024-C09',
                u'pub': u'Minor Planet Electronic Circulars',
                u'year': u'2024'
            },
        ]
    }
}
