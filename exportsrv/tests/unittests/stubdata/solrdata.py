# -*- coding: utf-8 -*-

# We have 19 different doctype in Solr, these are bibcode used to extrac the data below
# bibcodes = ['2017SenIm..18...17Z', '2000astro.ph..3081G','2007AAS...210.2104M', '2009bcet.book...65L', '2007RJPh....1...35.', '1983aiaa.meetY....K',
#             '1995anda.book.....N','1995ans..agar..390M','2016iac..talk..872V','2017ascl.soft06009C','2017sptz.prop13168Y','2017nova.pres.2388K',
#             '2017CBET.4403....2G','2017AAVSN.429....1W','2017yCat.113380453S','2017PhDT........14C','2017MsT..........2A','2016emo6.rept.....R','2017wfc..rept...16R']

data = \
{
   "responseHeader":{
      "status":0,
      "QTime":1,
      "params":{
         "sort":"date desc",
         "fq":"{!bitset}",
         "rows":"19",
         "q":"*:*",
         "start":"0",
         "wt":"json",
         "fl":"author,title,year,date,pub,pub_raw,issue,volume,page,page_range,aff,doi,abstract,citation_count,read_count,bibcode,identification,copyright,keyword,doctype,reference,comment,property,esources,data"
      }
   },
   "response":{
      "start":0,
      "numFound":19,
      "docs":[
         {
            "read_count":0,
            "doi":[
               "10.1007/s11220-017-0166-7"
            ],
            "keyword":[
               "Free-space method",
               "Artificial material",
               "Anti-reflection layer",
               "Attenuation",
               "Phase shift"
            ],
            "reference":[
               "1991ITMTT..39..828K",
               "1992MiOTL...5..184S",
               "2000PhRvL..85.3966P",
               "2002PhRvB..65s5104S",
               "2006ApPhL..88h1101D",
               "2009ApOpt..48.6635Z",
               "2012ITTST...2..113S",
               "2013ITAP...61.5408S",
               "2015ITAP...63.4702D"
            ],
            "title":[
               "A Microwave Free-Space Method Using Artificial Lens with Anti-reflection Layer"
            ],
            "abstract":"This paper describes a microwave free-space method using flat artificial lens antennas with anti-reflection layer. The lens antenna is made of an artificial material of metal particle. Comparing with our previous study, Anti-reflection (AR) layers are supplemented to the lens in this study to obtain a wave matching on the air-lens interface. The improved lens is in a disk shape of 50 mm diameter and 5.9 mm thickness. The lens is applied in a free-space setup, in which it is set in front of a patch antenna resonating at 15 GHz to get a high gain. The free-space setup is used to measure microwave attenuation and phase shift through a sawdust sample. The experimental results show that the multiple-reflection in the free-space method becomes small, because the reflection on air-lens interface has been reduced. The proposed AR lens antenna is flat and very small in the size. It is possible to construct a very compact and low cost free-space setup using the improved lens.",
            "year":"2017",
            "citation_count":0,
            "pub":"Sensing and Imaging",
            "page":[
               "17"
            ],
            "volume":"18",
            "esources":[
               "PUB_HTML"
            ],
            "bibcode":"2017SenIm..18...17Z",
            "copyright":"(c) 2017: Springer Science+Business Media New York",
            "doctype":"article",
            "date":"2017-12-01T00:00:00Z",
            "author":[
               "Zhang, Yangjun",
               "Aratani, Yuki",
               "Nakazima, Hironari"
            ],
            "property":[
               "REFEREED",
               "ARTICLE"
            ],
            "issue":"1",
            "pub_raw":"Sensing and Imaging, Volume 18, Issue 1, article id.17, <NUMPAGES>12</NUMPAGES> pp.",
            "aff":[
               "Department of Electronics and Informatics, Ryukoku University",
               "Department of Electronics and Informatics, Ryukoku University",
               "Department of Electronics and Informatics, Ryukoku University"
            ]
         },
         {
            "read_count":0,
            "bibcode":"2017wfc..rept...16R",
            "keyword":[
               "Hubble Space Telescope",
               "HST",
               "Space Telescope Science Institute",
               "STScI",
               "WFC3",
               "infrared blobs",
               "IR blobs"
            ],
            "page_range":"16",
            "abstract":"We present a investigation into possible overlaps between the known IR blobs with the grism aperture reference positions and the IR dither patterns. Each aperture was designed to place the science target (e.g. a specific star) on a cosmetically clean area of the IR detector. Similarly, the dither patterns were designed to mitigate cosmetic defects by rarely (or ideally never) placing such targets on known defects. Because blobs accumulate with time, the originally defined apertures and dither patterns may no longer accomplish their goals, it is important to reverify these combinations. We find two potential overlaps between the blob, aperture, and dither combinations, but do not recommend any changes to the current suite of aperture references positions and/or dither patterns for two reasons. First, one of the overlaps occurs with a dither/aperture combination that is seldom used for high-value science operations, but rather more common for wide-field surveys/mosaics. Second, the other overlap is 8.7 pix from a blob that has a fiducial radius of 10 pix, which already represents a very conservative distance. We conclude that a similar analysis should be repeated as new blobs occur, to continue to ensure ideal operations for high-value science targets. The purpose of this report is to document the analysis in order to facilitate its repetition in the future.",
            "author":[
               "Ryan, R. E.",
               "McCullough, P. R."
            ],
            "doctype":"techreport",
            "pub":"Space Telescope WFC Instrument Science Report",
            "citation_count":0,
            "esources":[
               "PUB_PDF"
            ],
            "pub_raw":"Instrument Science Report WFC3 2017-16, 6 pages",
            "year":"2017",
            "date":"2017-06-01T00:00:00Z",
            "title":[
               "Possible Overlaps Between Blobs, Grism Apertures, and Dithers"
            ],
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "page":[
               "16"
            ],
            "aff":[
               "Space Telescope Science Institute",
               "Space Telescope Science Institute"
            ]
         },
         {
            "read_count":7,
            "bibcode":"2017PhDT........14C",
            "keyword":[
               "galaxies: evolution",
               "galaxies: abundances",
               "galaxies: ISM"
            ],
            "reference":[
               "2006ApJ...638..797D"
            ],
            "author":[
               "Carton, David"
            ],
            "abstract":"Chapter 2: As part of the Bluedisk survey we analyse the radial gas-phase metallicity profiles of 50 late-type galaxies. We compare the metallicity profiles of a sample of HI-rich galaxies against a control sample of HI-'normal' galaxies. We find the metallicity gradient of a galaxy to be strongly correlated with its HI mass fraction {M}{HI}) / {M}_{\\ast}). We note that some galaxies exhibit a steeper metallicity profile in the outer disc than in the inner disc. These galaxies are found in both the HI-rich and control samples. This contradicts a previous indication that these outer drops are exclusive to HI-rich galaxies. These effects are not driven by bars, although we do find some indication that barred galaxies have flatter metallicity profiles. By applying a simple analytical model we are able to account for the variety of metallicity profiles that the two samples present. The success of this model implies that the metallicity in these isolated galaxies may be in a local equilibrium, regulated by star formation. This insight could provide an explanation of the observed local mass-metallicity relation. Chapter 3 We present a method to recover the gas-phase metallicity gradients from integral field spectroscopic (IFS) observations of barely resolved galaxies. We take a forward modelling approach and compare our models to the observed spatial distribution of emission line fluxes, accounting for the degrading effects of seeing and spatial binning. The method is flexible and is not limited to particular emission lines or instruments. We test the model through comparison to synthetic observations and use downgraded observations of nearby galaxies to validate this work. As a proof of concept we also apply the model to real IFS observations of high-redshift galaxies. From our testing we show that the inferred metallicity gradients and central metallicities are fairly insensitive to the assumptions made in the model and that they are reliably recovered for galaxies with sizes approximately equal to the half width at half maximum of the point-spread function. However, we also find that the presence of star forming clumps can significantly complicate the interpretation of metallicity gradients in moderately resolved high-redshift galaxies. Therefore we emphasize that care should be taken when comparing nearby well-resolved observations to high-redshift observations of partially resolved galaxies. Chapter 4 We present gas-phase metallicity gradients for 94 star-forming galaxies between (0.08 < z < 0.84). We find a negative median metallicity gradient of (-0.043^{+0.009}_{-0.007}, dex/kpc)/span>, i.e. on average we find the centres of these galaxies to be more metal-rich than their outskirts. However, there is significant scatter underlying this and we find that 10% (9) galaxies have significantly positive metallicity gradients, 39% (37) have significantly negative gradients, 28% (26) have gradients consistent with being flat, the remainder 23% (22) are considered to have unreliable gradient estimates. We find a slight trend for a more negative metallicity gradient with both increasing stellar mass and increasing star formation rate (SFR). However, given the potential redshift and size selection effects, we do not consider these trends to be significant. Indeed when we normalize the SFR of our galaxies relative to the main sequence, we do not observe any trend between the metallicity gradient and the normalized SFR. This finding is contrary to other recent studies of galaxies at similar and higher redshifts. We do, however, identify a novel trend between the metallicity gradient of a galaxy and its size. Small galaxies ((r_d < 3 kpc)) present a large spread in observed metallicity gradients (both negative and positive gradients). In contrast, we find no large galaxies (r_d > 3 kpc) with positive metallicity gradients, and overall there is less scatter in the metallicity gradient amongst the large galaxies. We suggest that these large (well-evolved) galaxies may be analogues of galaxies in the present-day Universe, which also present a common negative metallicity gradient. Chapter 5 The relationship between a galaxy's stellar mass and its gas-phase metallicity results from the complex interplay between star formation and the inflow and outflow of gas. Since the gradient of metals in galaxies is also influenced by the same processes, it is therefore natural to contrast the metallicity gradient with the mass-metallicity relation. Here we study the interrelation of the stellar mass, central metallicity and metallicity gradient, using a sample of 72 galaxies spanning (0.13 < z < 0.84) with reliable metallicity gradient estimates. We find that typically the galaxies that fall below the mean mass-metallicity relation have flat or inverted metallicity gradients. We quantify their relationship taking full account of the covariance between the different variables and find that at fixed mass the central metallicity is anti-correlated with the metallicity gradient. We argue that this is consistent with a scenario that suppresses the central metallicity either through the inflow of metal poor gas or outflow of metal enriched gas.",
            "title":[
               "Resolving Gas-Phase Metallicity In Galaxies"
            ],
            "doctype":"phdthesis",
            "pub":"Ph.D. Thesis",
            "citation_count":0,
            "esources":[
               "PUB_HTML"
            ],
            "doi":[
               "10.5281/zenodo.581221"
            ],
            "pub_raw":"PhD Thesis, Leiden University, 2017",
            "year":"2017",
            "date":"2017-06-01T00:00:00Z",
            "property":[
               "OPENACCESS",
               "REFEREED",
               "PUB_OPENACCESS",
               "NONARTICLE"
            ],
            "aff":[
               "Leiden University"
            ]
         },
         {
            "read_count":4,
            "bibcode":"2017ascl.soft06009C",
            "keyword":[
               "Software"
            ],
            "author":[
               "Casey, Andrew R."
            ],
            "abstract":"sick infers astrophysical parameters from noisy observed spectra. Phenomena that can alter the data (e.g., redshift, continuum, instrumental broadening, outlier pixels) are modeled and simultaneously inferred with the astrophysical parameters of interest. This package relies on emcee (ascl:1303.002); it is best suited for situations where a grid of model spectra already exists, and one would like to infer model parameters given some data.",
            "title":[
               "sick: Spectroscopic inference crank"
            ],
            "citation_count":0,
            "doctype":"software",
            "pub":"Astrophysics Source Code Library",
            "page":[
               "ascl:1706.009"
            ],
            "esources":[
               "PUB_HTML"
            ],
            "pub_raw":"Astrophysics Source Code Library, record ascl:1706.009",
            "year":"2017",
            "date":"2017-06-01T00:00:00Z",
            "property":[
               "OPENACCESS",
               "PUB_OPENACCESS",
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "aff":[
               "-"
            ]
         },
         {
            "read_count":0,
            "bibcode":"2017CBET.4403....2G",
            "page_range":"2",
            "aff":[
               "-"
            ],
            "author":[
               "Green, D. W. E."
            ],
            "doctype":"circular",
            "pub":"Central Bureau Electronic Telegrams",
            "citation_count":0,
            "volume":"4403",
            "esources":[
               "PUB_HTML"
            ],
            "pub_raw":"Central Bureau Electronic Telegrams, 4403, 2 (2017). Edited by Green, D. W. E.",
            "year":"2017",
            "date":"2017-06-01T00:00:00Z",
            "title":[
               "Potential New Meteor Shower from Comet C/2015 D4 (Borisov)"
            ],
            "property":[
               "PRIVATE",
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "abstract":"A previous good encounter occurred on 2006 July 29d04h11m UT (r - Delta = +0.0003 AU, solar long. = 125.841 deg). Future encounters are predicted on 2029 July 29d01h53m (+0.0007 AU, 125.816 deg), 2042 July 29d10h48m (+0.0006 AU, 125.886 deg), 2053 July 29d05h35m (+0.0001 AU, 125.848 deg), and on 2068 July 29d02h09m UT (-0.0001 AU, 125.863 deg).",
            "page":[
               "2"
            ]
         },
         {
            "read_count":5,
            "bibcode":"2017nova.pres.2388K",
            "author":[
               "Kohler, Susanna"
            ],
            "keyword":[
               "Features",
               "Highlights",
               "interstellar medium",
               "stellar evolution",
               "supernova remnant",
               "supernovae",
               "white dwarfs"
            ],
            "title":[
               "A 3D View of a Supernova Remnant"
            ],
            "abstract":"The outlined regions mark the 57 knots in Tycho selected by the authors for velocity measurements. Magenta regions have redshifted line-of-sight velocities (moving away from us); cyan regions have blueshifted light-of-sight velocities (moving toward us). [Williams et al. 2017]The Tycho supernova remnant was first observed in the year 1572. Nearly 450 years later, astronomers have now used X-ray observations of Tycho to build the first-ever 3D map of a Type Ia supernova remnant.Signs of ExplosionsSupernova remnants are spectacular structures formed by the ejecta of stellar explosions as they expand outwards into the surrounding interstellar medium.One peculiarity of these remnants is that they often exhibit asymmetries in their appearance and motion. Is this because the ejecta are expanding into a nonuniform interstellar medium? Or was the explosion itself asymmetric? The best way we can explore this question is with detailed observations of the remnants.Histograms of the velocity in distribution of the knots in the X (green), Y (blue) and Z (red) directions (+Z is away from the observer). They show no evidence for asymmetric expansion of the knots. [Williams et al. 2017]Enter TychoTo this end, a team of scientists led by Brian Williams (Space Telescope Science Institute and NASA Goddard SFC) has worked to map out the 3D velocities of the ejecta in the Tycho supernova remnant. Tycho is a Type Ia supernova thought to be caused by the thermonuclear explosion of a white dwarf in a binary system that was destabilized by mass transfer from its companion.After 450 years of expansion, the remnant now has the morphological appearance of a roughly circular cloud of clumpy ejecta. The forward shock wave from the supernova, however, is known to have twice the velocity on one side of the shell as on the other.To better understand this asymmetry, Williams and collaborators selected a total of 57 knots in Tychos ejecta, spread out around the remnant. They then used 12 years of Chandra X-ray observations to measure both the knots proper motion in the plane of the sky and their line-of-sight velocity. These two measurements were then combined to build a full 3D map of the motion of the ejecta.3D hydrodynamical simulations of Tycho, stopped at the current epoch. These show that both initially smooth (top) and initially clumpy (bottom) ejecta models are consistent with the current observations of the morphology and dynamics of Tychos ejecta. [Adapted from Williams et al. 2017]Symmetry and ClumpsWilliams and collaborators found that the knots have total velocities that range from 2400 to 6600 km/s. Unlike the forward shock of the supernova, Tychos ejecta display no asymmetries in their motion which suggests that the explosion itself was symmetric. The more likely explanation is a density gradient in the interstellar medium, which could slow the shock wave on one side of the remnant without yet affecting the motion of the clumps of ejecta.As a final exploration, the authors attempt to address the origin of Tychos clumpiness. The fact that some of Tychos ejecta knots precede its outer edge has raised the question of whether the ejecta started out clumpy, or if they began smooth and only clumped during expansion. Williams and collaborators matched the morphological and dynamical data to simulations, demonstrating that neither scenario can be ruled out at this time.This first 3D map of a Type Ia supernova represents an important step in our ability to understand these stellar explosions. The authors suggest that well be able to expand on this map in the future with additional observations from Chandra, as well as with new data from future X-ray observatories that will be able to detect fainter emission.CitationBrian J. Williams et al 2017 ApJ 842 28. doi:10.3847/1538-4357/aa7384",
            "year":"2017",
            "citation_count":0,
            "pub":"AAS Nova Highlights",
            "page":[
               "2388"
            ],
            "esources":[
               "PUB_HTML"
            ],
            "doctype":"pressrelease",
            "date":"2017-06-01T00:00:00Z",
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "data":[
               "CXO:14"
            ],
            "pub_raw":"AAS Nova Highlight, 14 Jun 2017, id.2388",
            "aff":[
               "-"
            ]
         },
         {
            "read_count":3,
            "bibcode":"2017AAVSN.429....1W",
            "copyright":"(C) AAVSO 2017",
            "reference":[
               "2001ASPC..242..187I",
               "2016AAN...538....1W",
               "2016ATel.8653....1M",
               "2016ATel.8832....1L",
               "2016ATel.8957....1L",
               "2017ATel10281....1L"
            ],
            "page_range":"1",
            "abstract":"The observing campaign from 2016 on V694 Mon (MWC 560) (AAVSO Alert Notice 538) has been continued, but with different requirements. Photometry is no longer specifically requested on a regular basis (although ongoing observations that do not interfere with other obligations are welcome). Spectroscopy on a cadence of a week or two is requested to monitor changes in the disk outflow. Investigator Adrian Lucy writes: \"Adrian Lucy and Dr. Jeno Sokoloski (Columbia University) have requested spectroscopic monitoring of the broad-absorption-line symbiotic star V694 Mon (MWC 560), as a follow-up to coordinated multi-wavelength observations obtained during its recent outburst (ATel #8653, #8832, #8957; #10281). This system is a perfect place in which to study the relationship between an accretion disk and disk winds/jets, and a high-value target for which even low-resolution spectra can be extraordinarily useful...Optical brightening in MWC 560 tends to predict higher-velocity absorption, but sometimes jumps in absorption velocity also appear during optical quiescence (e.g., Iijima 2001, ASPCS, 242, 187). If such a velocity jump occurs during photometric quiescence, it may prompt radio observations to confirm and test the proposed outflow origin for recently-discovered flat-spectrum radio emission (Lucy et al. ATel #10281)...Furthermore, volunteer spectroscopic monitoring of this system has proved useful in unpredictable ways. For example, 'amateur' spectra obtained by Somogyi P\u00c3\u00a9ter in 2015 December demonstrated that the velocity of absorption was very low only a month before an optical outburst peak prompted absorption troughs up to 3000 km/s, which constrains very well the timing of the changes to the outflow to a degree that would not have been otherwise possible. Any resolution can be useful. A wavelength range that can accommodate a blueshift of at least 140 angstroms (6000 km/s) from the rest wavelengths of H-alpha at 6562 angstroms and/or H-beta at 4861 angstroms is ideal, though spectra with a smaller range can still be useful. Photometry could potentially still be useful, but will be supplementary to medium-cadence photometry being collected by the ANS collaboration.\" \"Spectroscopy may be uploaded to the ARAS database (http://www.astrosurf.com/aras/Aras_DataBase/DataBase.htm), or sent to Adrian and Jeno directly at <lucy@astro.columbia.edu>. Finder charts with sequence may be created using the AAVSO Variable Star Plotter (https://www.aavso.org/vsp). Photometry should be submitted to the AAVSO International Database. See full Special Notice for more details.",
            "author":[
               "Waagen, Elizabeth O."
            ],
            "doctype":"newsletter",
            "pub":"AAVSO Special Notice",
            "citation_count":0,
            "volume":"429",
            "esources":[
               "PUB_HTML"
            ],
            "pub_raw":"AAVSO Special Notice #429",
            "keyword":[
               "astronomical databases: miscellaneous",
               "binaries: symbiotic",
               "stars: individual (V694 Mon",
               "MWC 560)"
            ],
            "year":"2017",
            "date":"2017-05-01T00:00:00Z",
            "title":[
               "V694 Mon (MWC 560) spectroscopy requested"
            ],
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "page":[
               "1"
            ],
            "aff":[
               "AAVSO"
            ]
         },
         {
            "comment":[
               "phot.dat 2930x19 Differential photometry of BM CVn; phot_mlc.dat 2930x19 Differential photometry of BM CVn with MLC removed; res.dat 1319x185 *Numerical results of the CPS analysis; res_mlc.dat 1319x185 *Results of the CPS analysis with MLC removed"
            ],
            "read_count":4,
            "bibcode":"2017yCat.113380453S",
            "keyword":[
               "Stars: variable"
            ],
            "author":[
               "Siltala, J.",
               "Jetsu, L.",
               "Hackman, T.",
               "Henry, G. W.",
               "Immonen, L.",
               "Kajatkari, P.",
               "Lankinen, J.",
               "Lehtinen, J.",
               "Monira, S.",
               "Nikbakhsh, S.",
               "Viitanen, A.",
               "Viuho, J.",
               "Willamo, T."
            ],
            "abstract":"The included files present the numerical data of our analysis of the BM CVn photometry. The data consists of differential Johnson V-band photometry using the star HD 116010 as the comparison star. The analysis has been performed using the previously published continuous period search (CPS) method, described in detail in Lehtinen et al., 2011A&A...527A.136L, Cat. J/A+A/527/A136. (4 data files).",
            "title":[
               "VizieR Online Data Catalog: BM CVn V-band differential light curve (Siltala+, 2017)"
            ],
            "doctype":"catalog",
            "pub":"VizieR Online Data Catalog",
            "citation_count":0,
            "pub_raw":"VizieR On-line Data Catalog: J/AN/338/453. Originally published in: 2017AN....338..453S",
            "year":"2017",
            "date":"2017-05-01T00:00:00Z",
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "data":[
               "Vizier:1"
            ],
            "page":[
               "J/AN/338/453"
            ],
            "aff":[
               "-",
               "-",
               "-",
               "-",
               "-",
               "-",
               "-",
               "-",
               "-",
               "-",
               "-",
               "-",
               "-"
            ]
         },
         {
            "read_count":3,
            "bibcode":"2017sptz.prop13168Y",
            "author":[
               "Yan, Lin"
            ],
            "abstract":"ULIRG F01004-2237 had a strong optical flare, peaked in 2010, and the follow-up optical spectra classified this event as a TDE candidate (Tadhunter et al. 2017, Nature Astronomy). In early 2017, using archival WISE data, we discovered that its 3.4 and 4.6um fluxes have been steadily rising since 2013, increased by a factor of 3.5 and 2.6 respectively. The last epoch data from WISE on 2016-12-12 shows that F01004-2237 has reached 7.5 and 14mJy at 3.4 and 4.6um. We interpret the mid-IR LCs as infrared echoes from the earlier optical flare. We infer a convex, dust ring with a radius of 1 pc from the central heating source. Our model predicts that if this event is indeed a TDE, its mid-IR LCs should start to fade in next 5-12 months because it has already reprocessed most of the UV/optical energy from the tidal disruption. However, if this event is due to activities from an AGN, its mid-IR LCs could last over a much longer time scale. We request a total of 3.2 hours of Spitzer time to monitor the mid-IR variations in next 12 months. This will provide the critical data to confirm the nature of this transient event.",
            "title":[
               "Confirm the Nature of a TDE Candidate in ULIRG F01004-2237 Using Spitzer mid-IR Light Curves"
            ],
            "citation_count":0,
            "doctype":"proposal",
            "pub":"Spitzer Proposal",
            "page":[
               "13168"
            ],
            "page_range":"13168",
            "pub_raw":"Spitzer Proposal ID 13168",
            "year":"2017",
            "date":"2017-04-01T00:00:00Z",
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "data":[
               "Spitzer:1"
            ],
            "aff":[
               "-"
            ]
         },
         {
            "read_count":0,
            "bibcode":"2017MsT..........2A",
            "reference":[
               "1966IEEEP..54..633R",
               "2004SPIE.5489.1029P",
               "2007IAPM...49...24B",
               "2011PASP..123.1087H"
            ],
            "page_range":"2",
            "aff":[
               "University of Stellenbosch"
            ],
            "author":[
               "Azankpo, Severin"
            ],
            "doctype":"mastersthesis",
            "pub":"Masters Thesis",
            "citation_count":0,
            "esources":[
               "AUTHOR_PDF",
               "PUB_HTML",
               "PUB_PDF"
            ],
            "pub_raw":"Masters thesis, University of Stellenbosch, March 2017, 120 pages",
            "year":"2017",
            "date":"2017-03-01T00:00:00Z",
            "title":[
               "Surface Accuracy and Pointing Error Prediction of a 32 m Diameter Class Radio Astronomy Telescope"
            ],
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "abstract":"The African Very-long-baseline interferometry Network (AVN) is a joint project between South Africa and eight partner African countries aimed at establishing a VLBI (Very-Long-Baseline Interferometry) capable network of radio telescopes across the African continent. An existing structure that is earmarked for this project, is a 32 m diameter antenna located in Ghana that has become obsolete due to advances in telecommunication. The first phase of the conversion of this Ghana antenna into a radio astronomy telescope is to upgrade the antenna to observe at 5 GHz to 6.7 GHz frequency and then later to 18 GHz within a required performing tolerance. The surface and pointing accuracies for a radio telescope are much more stringent than that of a telecommunication antenna. The mechanical pointing accuracy of such telescopes is influenced by factors such as mechanical alignment, structural deformation, and servo drive train errors. The current research investigates the numerical simulation of the surface and pointing accuracies of the Ghana 32 m diameter radio astronomy telescope due to its structural deformation mainly influenced by gravity, wind and thermal loads.",
            "page":[
               "2"
            ]
         },
         {
            "read_count":2,
            "bibcode":"2016emo6.rept.....R",
            "keyword":[
               "THE MOON",
               "ECLIPSES",
               "PARTIAL",
               "PENUMBRAL",
               "ASTROPHOTOGRAPHY"
            ],
            "author":[
               "Rotaru, Adrian",
               "Pteancu, Mircea",
               "Zaharia, Cristian"
            ],
            "abstract":"The web page represents circumstances and photographs from the Moon's partial/penumbral eclipse from 16 September 2016 obtained from few various places in Romania (East Europe). A part of photographs give the maximum phase of the Eclipse, while another give the reddened Moon.",
            "title":[
               "The penumbral Moon's eclipse form 16 september 2016"
            ],
            "doctype":"techreport",
            "pub":"http://www.astronomy.ro/forum/viewtopic.php?p=159287#159287 (Comments in Romanian",
            "citation_count":0,
            "pub_raw":"http://www.astronomy.ro/forum/viewtopic.php?p=159287#159287 (Comments in Romanian)",
            "year":"2016",
            "date":"2016-10-01T00:00:00Z",
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "aff":[
               "Bragadiru, Romania",
               "Private Astronomical Observatory, Arad, Romania",
               "Private Astronomical Observatory, Ploiesti, Romania"
            ]
         },
         {
            "read_count":0,
            "bibcode":"2016iac..talk..872V",
            "reference":[
               "2016MNRAS.460.3519V"
            ],
            "author":[
               "Velasco, Sergio"
            ],
            "aff":[
               "Instituto de Astrof\u00edsica de Canarias"
            ],
            "title":[
               "Living on the edge: Adaptive Optics+Lucky Imaging"
            ],
            "doctype":"talk",
            "pub":"IAC Talks, Astronomy and Astrophysics Seminars from the Instituto de Astrof&iacute;sica de Canarias",
            "citation_count":0,
            "esources":[
               "AUTHOR_HTML",
               "PUB_HTML"
            ],
            "year":"2016",
            "date":"2016-03-01T00:00:00Z",
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "pub_raw":"IAC Talks, Astronomy and Astrophysics Seminars from the Instituto de Astrof\u00edsica de Canarias, 872",
            "page_range":"872",
            "page":[
               "872"
            ]
         },
         {
            "read_count":0,
            "bibcode":"2009bcet.book...65L",
            "keyword":[
               "Physics"
            ],
            "copyright":"(c) 2009: Springer Netherlands",
            "page_range":"65",
            "abstract":"The discovery of the physical phenomenon of Nuclear Magnetic Resonance (NMR) in 1946 gave rise to the spectroscopic technique that has become a remarkably versatile research tool. One could oversimplify NMR spectros-copy by categorizing it into the two broad applications of structure elucidation of molecules (associated with chemistry and biology) and imaging (associated with medicine). But, this certainly does not do NMR spectroscopy justice in demonstrating its general acceptance and utilization across the sciences. This manuscript is not an effort to present an exhaustive, or even partial review of NMR spectroscopy applications, but rather to provide a glimpse at the wide-ranging uses of NMR spectroscopy found within the confines of a single magnetic resonance research facility, the Stanford Magnetic Resonance Laboratory. Included here are summaries of projects involving protein structure determination, mapping of intermolecular interactions, exploring fundamental biological mechanisms, following compound cycling in the environmental, analysis of synthetic solid compounds, and microimaging of a model organism.",
            "author":[
               "Liu, Corey W.",
               "Alekseyev, Viktor Y.",
               "Allwardt, Jeffrey R.",
               "Bankovich, Alexander J.",
               "Cade-Menun, Barbara J.",
               "Davis, Ronald W.",
               "Du, Lin-Shu",
               "Garcia, K. Christopher",
               "Herschlag, Daniel",
               "Khosla, Chaitan",
               "Kraut, Daniel A.",
               "Li, Qing",
               "Null, Brian",
               "Puglisi, Joseph D.",
               "Sigala, Paul A.",
               "Stebbins, Jonathan F.",
               "Varani, Luca"
            ],
            "doctype":"inbook",
            "pub":"Biophysics and the Challenges of Emerging Threats",
            "citation_count":0,
            "esources":[
               "PUB_HTML"
            ],
            "doi":[
               "10.1007/978-90-481-2368-1_5"
            ],
            "pub_raw":"Biophysics and the Challenges of Emerging Threats, NATO Science for Peace and Security Series B: Physics and Biophysics. ISBN 978-90-481-2367-4. Springer Netherlands, 2009, p. 65",
            "year":"2009",
            "date":"2009-01-01T00:00:00Z",
            "title":[
               "The Diversity of Nuclear Magnetic Resonance Spectroscopy"
            ],
            "property":[
               "ARTICLE",
               "NOT REFEREED"
            ],
            "page":[
               "65"
            ],
            "aff":[
               "Stanford Magnetic Resonance Laboratory, Stanford University",
               "Department of Chemistry, Stanford University; , Genencor",
               "Department of Geological & Environmental Sciences, Stanford University; , ConocoPhillips Company",
               "Department of Molecular and Cellular Physiology, Stanford University; Department of Structural Biology, Stanford University",
               "Department of Geological & Environmental Sciences, Stanford University; , Agriculture and Agri-Food Canada",
               "Stanford Genome Technology Center, Stanford University; Department of Biochemistry, Stanford University",
               "Department of Geological & Environmental Sciences, Stanford University; Air Products and Chemicals, Inc. Allentown",
               "Department of Molecular and Cellular Physiology, Stanford University; Department of Structural Biology, Stanford University",
               "Department of Biochemistry, Stanford University",
               "Department of Chemistry, Stanford University; Department of Biochemistry, Stanford University",
               "Department of Biochemistry, Stanford University; Department of Biochemistry, Molecular Biology and Cell Biology, Northwestern University",
               "Department of Chemistry, Stanford University; , Institute for Research in Biomedicine",
               "Stanford Genome Technology Center, Stanford University; Department of Biochemistry, Stanford University",
               "Stanford Magnetic Resonance Laboratory, Stanford University; Department of Structural Biology, Stanford University",
               "Department of Molecular and Cellular Physiology, Stanford University; Department of Structural Biology, Stanford University",
               "Department of Geological & Environmental Sciences, Stanford University",
               "Department of Molecular and Cellular Physiology, Stanford University; Department of Structural Biology, Stanford University"
            ]
         },
         {
            "read_count":0,
            "bibcode":"2007AAS...210.2104M",
            "author":[
               "Mahabal, Ashish A.",
               "Drake, A. J.",
               "Djorgovski, S. G.",
               "Donalek, C.",
               "Glikman, E.",
               "Graham, M. J.",
               "Williams, R.",
               "Baltay, C.",
               "Rabinowitz, D.",
               "PQ Team Caltech",
               "Yale",
               "NCSA",
               "Indiana",
               ", . . ."
            ],
            "abstract":"Palomar-QUEST (PQ) synoptic sky survey has now been routinely processing data from driftscans in real-time. As four photometric bandpasses are utilized in nearly simultaneously, PQ is well suited to search for transient and highly variable objects. Using a series of software filters i.e. programs to select/deselect objects based on certain criteria we shorten the list of candidates from the initially flagged candidate transients. Such filters include looking for known asteroids, known variables, as well as moving, but previously uncatalogued objects based on their motion within a scan as well as between successive scans. Some software filters also deal with instrumental artifacts, edge effects, and use clustering of spurious detections around bright stars. During a typical night when we cover about 500 sq. degrees, we detect hundreds of asteroids, the primary contaminants in the search for astrophysical transients beyond our solar system. Here we describe some statistics based on the software filters we employ and the nature of the objects that seem to survive the process. We also discuss the usefulness of this to amateur astronomers, projects like VOEventNet, and other synoptic sky surveys. We also present an outline of the work we have started on quantifying the variability of quasars, blazars, as well as various classes of Galactic sources, by combining the large number of PQ scans with other existing data sources federated in the Virtual Observatory environment. The PQ survey is partially supported by the U.S. National Science Foundation (NSF).",
            "title":[
               "Time Domain Exploration with the Palomar-QUEST Sky Survey"
            ],
            "doctype":"abstract",
            "pub":"American Astronomical Society Meeting Abstracts #210",
            "citation_count":0,
            "pub_raw":"American Astronomical Society Meeting 210, id.21.04; <ALTJOURNAL>Bulletin of the American Astronomical Society, Vol. 39, p.124</ALTJOURNAL>",
            "year":"2007",
            "date":"2007-05-01T00:00:00Z",
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "page":[
               "21.04"
            ],
            "aff":[
               "Caltech",
               "Caltech",
               "Caltech",
               "Caltech",
               "Caltech",
               "Caltech",
               "Caltech",
               "Yale University",
               "Yale University",
               "-",
               "-",
               "-",
               "-",
               "-"
            ]
         },
         {
            "read_count":0,
            "bibcode":"2007RJPh....1...35.",
            "page_range":"35-41",
            "aff":[
               "-",
               "-"
            ],
            "author":[
               "., S. N. Agbo",
               "., E. C. Okoroigwe"
            ],
            "doctype":"article",
            "pub":"Research Journal of Physics",
            "citation_count":0,
            "volume":"1",
            "esources":[
               "PUB_HTML"
            ],
            "doi":[
               "10.3923/rjp.2007.35.41"
            ],
            "pub_raw":"Research Journal of Physics, vol. 1, issue 1, pp. 35-41",
            "year":"2007",
            "date":"2007-01-01T00:00:00Z",
            "title":[
               "Analysis of Thermal Losses in the Flat-Plate Collector of a Thermosyphon Solar Water Heater"
            ],
            "property":[
               "OPENACCESS",
               "PUB_OPENACCESS",
               "ARTICLE",
               "NOT REFEREED"
            ],
            "page":[
               "35"
            ]
         },
         {
            "read_count":17,
            "reference":[
               "1973ApJ...182..559J",
               "1983ApJ...270..119M",
               "1984ApJS...55..585H",
               "1987A&A...179..219T",
               "1989ApJ...337..141M",
               "1990A&A...237..207T",
               "1990ARA&A..28..215D",
               "1992ApJ...390..108K",
               "1992ApJ...392..131S",
               "1992ApJS...80..753S",
               "1993A&A...275...67B",
               "1995ApJ...440..634R",
               "1996Natur.380..687N",
               "1997ApJ...491..216M",
               "1997MNRAS.287..455B"
            ],
            "abstract":"The Dominion Radio Astrophysical Observatory's Synthesis Telescope provides the highest resolution data (1' and 0.82 km s<SUP>-1</SUP>) to date of an H I worm candidate. Observed as part of the Canadian Galactic Plane Survey, mushroom-shaped GW 123.4-1.5 extends only a few hundred parsecs, contains ~10<SUP>5</SUP> M<SUB>solar</SUB> of neutral hydrogen, and appears unrelated to a conventional shell or chimney structure. Our preliminary Zeus two-dimensional models use a single off-plane explosion with a modest (~10<SUP>51</SUP> ergs) energy input. These generic simulations generate, interior to an expanding outer blast wave, a buoyant cloud whose structure resembles the morphology of the observed feature. Unlike typical model superbubbles, the stem can be narrow because its width is not governed by the pressure behind the blast wave or the disk scale height. Using this type of approach, it should be possible to more accurately model the thin stem and other details of GW 123.4-1.5 in the future.",
            "doctype":"article",
            "year":"2000",
            "bibcode":"2000ApJ...533L..25E",
            "author":[
               "English, Jayanne",
               "Taylor, A. R.",
               "Mashchenko, S. Y.",
               "Irwin, Judith A.",
               "Basu, Shantanu",
               "Johnstone, Doug"
            ],
            "aff":[
               "Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada; Space Telescope Science Institute, Baltimore, MD",
               "Department of Physics and Astronomy, University of Calgary, Calgary, Alberta, T2N 1N4, Canada",
               "Department de Physique, Universit\u00e9 de Montr\u00e9al, Montr\u00e9al, Qu\u00e9bec, H3C 3J7, Canada",
               "Department of Physics, Queen's University, Kingston, Ontario, K7L 3N6, Canada",
               "Department of Physics and Astronomy, University of Western Ontario, London, Ontario, N6A 3K7, Canada",
               "University of Toronto, 60 St. George Street, Toronto, Ontario, M5S 3H8, Canada"
            ],
            "esources":[
               "EPRINT_HTML",
               "EPRINT_PDF",
               "PUB_HTML",
               "PUB_PDF"
            ],
            "issue":"1",
            "pub_raw":"The Astrophysical Journal, Volume 533, Issue 1, pp. L25-L28.",
            "pub":"The Astrophysical Journal",
            "volume":"533",
            "page_range":"L25-L28",
            "date":"2000-04-01T00:00:00Z",
            "data":[
               "SIMBAD:3"
            ],
            "doi":[
               "10.1086/312592"
            ],
            "keyword":[
               "GALAXY: HALO",
               "GALAXY: STRUCTURE",
               "ISM: BUBBLES",
               "ISM: INDIVIDUAL: ALPHANUMERIC: GW 123.4-1.5",
               "ISM: STRUCTURE",
               "Astrophysics"
            ],
            "title":[
               "The Galactic Worm GW 123.4-1.5: A Mushroom-shaped H I Cloud"
            ],
            "citation_count":16,
            "property":[
               "OPENACCESS",
               "REFEREED",
               "EPRINT_OPENACCESS",
               "PUB_OPENACCESS",
               "ARTICLE"
            ],
            "page":[
               "L25"
            ]
         },
         {
            "read_count":0,
            "bibcode":"1995ans..agar..390M",
            "keyword":[
               "Earth Orbits",
               "Navigation Aids",
               "Navigators",
               "Onboard Equipment",
               "Space Navigation",
               "Spacecraft Trajectories",
               "Support Systems",
               "Technology Assessment",
               "Technology Utilization",
               "Ascent Trajectories",
               "Reentry Trajectories",
               "Spacecraft",
               "Spacecraft Performance",
               "Spacecraft Survivability",
               "Tradeoffs",
               "Weight (Mass)",
               "Space Communications, Spacecraft Communications, Command and Tracking"
            ],
            "author":[
               "Miller, Judy L."
            ],
            "abstract":"Spacecraft operation depends upon knowledge of vehicular position and, consequently, navigational support has been required for all such systems. Technical requirements for different mission trajectories and orbits are addressed with consideration given to the various tradeoffs which may need to be considered. The broad spectrum of spacecraft are considered with emphasis upon those of greater military significance (i.e., near earth orbiting satellites). Technical requirements include, but are not limited to, accuracy; physical characteristics such as weight and volume; support requirements such as electrical power and ground support; and system integrity. Generic navigation suites for spacecraft applications are described. It is shown that operational spacecraft rely primarily upon ground-based tracking and computational centers with little or no navigational function allocated to the vehicle, while technology development efforts have been and continue to be directed primarily toward onboard navigation suites. The military significance of onboard navigators is shown to both improve spacecraft survivability and performance (accuracy).",
            "title":[
               "Spacecraft navigation requirements"
            ],
            "doctype":"inproceedings",
            "pub":"In AGARD",
            "citation_count":0,
            "page_range":"390-405",
            "pub_raw":"In AGARD, Aerospace Navigation Systems p 390-405 (SEE N96-13404 02-04)",
            "year":"1995",
            "date":"1995-06-01T00:00:00Z",
            "property":[
               "ARTICLE",
               "NOT REFEREED"
            ],
            "page":[
               "390"
            ],
            "aff":[
               "Draper (Charles Stark) Lab., Inc., Cambridge, MA."
            ]
         },
         {
            "read_count":7,
            "bibcode":"1995anda.book.....N",
            "author":[
               "Nayfeh, Ali H.",
               "Balachandran, Balakumar"
            ],
            "aff":[
               "-",
               "-"
            ],
            "title":[
               "Applied nonlinear dynamics: analytical, computational and experimental methods"
            ],
            "doctype":"book",
            "pub":"Wiley series in nonlinear science",
            "citation_count":116,
            "year":"1995",
            "date":"1995-01-01T00:00:00Z",
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "pub_raw":"Wiley series in nonlinear science, New York; Chichester: Wiley, |c1995"
         },
         {
            "read_count":0,
            "bibcode":"1983aiaa.meetY....K",
            "keyword":[
               "Artificial Satellites",
               "Autonomous Navigation",
               "Earth-Moon System",
               "Lunar Communication",
               "Radio Beacons",
               "Radio Navigation",
               "Space Navigation",
               "Doppler Navigation",
               "Least Squares Method",
               "Orbit Calculation",
               "Space Communications, Spacecraft Communications, Command and Tracking"
            ],
            "author":[
               "Khatib, A. R.",
               "Ellis, J.",
               "French, J.",
               "Null, G.",
               "Yunck, T.",
               "Wu, S."
            ],
            "abstract":"The concept of using lunar beacon signal transmission for on-board navigation for earth satellites and near-earth spacecraft is described. The system would require powerful transmitters on the earth-side of the moon's surface and black box receivers with antennae and microprocessors placed on board spacecraft for autonomous navigation. Spacecraft navigation requires three position and three velocity elements to establish location coordinates. Two beacons could be soft-landed on the lunar surface at the limits of allowable separation and each would transmit a wide-beam signal with cones reaching GEO heights and be strong enough to be received by small antennae in near-earth orbit. The black box processor would perform on-board computation with one-way Doppler/range data and dynamical models. Alternatively, GEO satellites such as the GPS or TDRSS spacecraft can be used with interferometric techniques to provide decimeter-level accuracy for aircraft navigation.",
            "title":[
               "Autonomous navigation using lunar beacons"
            ],
            "doctype":"proceedings",
            "pub":"AIAA, Aerospace Sciences Meeting",
            "citation_count":0,
            "pub_raw":"American Institute of Aeronautics and Astronautics, Aerospace Sciences Meeting, 21st, Reno, NV, Jan. 10-13, 1983. 7 p.",
            "year":"1983",
            "date":"1983-01-01T00:00:00Z",
            "property":[
               "NONARTICLE",
               "NOT REFEREED"
            ],
            "aff":[
               "California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA",
               "California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA",
               "California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA",
               "California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA",
               "California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA",
               "California Institute of Technology, Jet Propulsion Laboratory, Pasadena, CA"
            ]
         }
      ]
   }
}

###################
# to produce the above data
#
# import requests
# import json
#
# queryURL = 'http://localhost:4000/'
#
# bibcodes = ['2017SenIm..18...17Z', '2000astro.ph..3081G', '2007AAS...210.2104M', '2009bcet.book...65L', \
#             '2007RJPh....1...35.', '1983aiaa.meetY....K', '1995anda.book.....N', '1995ans..agar..390M', \
#             '2016iac..talk..872V', '2017ascl.soft06009C', '2017sptz.prop13168Y', '2017nova.pres.2388K', \
#             '2017CBET.4403....2G', '2017AAVSN.429....1W', '2017yCat.113380453S', '2017PhDT........14C', \
#             '2017MsT..........2A', '2016emo6.rept.....R', '2017wfc..rept...16R']
# payload = {'bibcode': bibcodes}
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# response = requests.post(queryURL, data=json.dumps(payload), headers=headers)
# print json.dumps(response.content, sort_keys=True, indent=True);