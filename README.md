# CORE CFP

Python scraper for CORE Conference Portal
----------------------------------------

The target of CORE CFP is to load data about CORE ranked conferences and combine them with information
about call-for-papers such as conference date, submission deadline or conference location.

This is done by scraping the CORE Conference Portal (the scrape preserves DBLP links unlike the Excel export provided)
and completing the data by following the DBLP link and loading CFP details from WikiCFP if linked on DBLP.

Result is a list of conference objects with all the scraped information.

|Acronym     |Name                                                                           |Rank|Dates                  |Submission deadline|Abstract registration|Location        |Rank source|CORE ID|DBLP                                  |WikiCFP                                   |
|------------|-------------------------------------------------------------------------------|----|-----------------------|-------------------|---------------------|----------------|-----------|-------|--------------------------------------|------------------------------------------|
|PERVASIVE   |International Conference on Pervasive Computing (Joined with UbiComp from 2013)|A*  |                       |                   |                     |                |CORE2014   |1171   |                                      |                                          |
|ICIS        |International Conference on Information Systems                                |A*  |2019-12-15 - 2019-12-18|2019-05-01         |                     |Munich          |CORE2018   |1078   |https://dblp.uni-trier.de/db/conf/icis|http://www.wikicfp.com/cfp/program?id=1394|
|JCDL        |ACM Conference on Digital Libraries                                            |A*  |2022-06-20 - 2022-06-24|2022-01-21         |                     |Cologne, Germany|CORE2018   |2085   |https://dblp.uni-trier.de/db/conf/jcdl|http://www.wikicfp.com/cfp/program?id=1880|
|RSS         |Robotics: Science and Systems                                                  |A*  |                       |                   |                     |                |CORE2018   |1709   |https://dblp.uni-trier.de/db/conf/rss |                                          |
|IEEE InfoVis|IEEE Information Visualization Conference                                      |A*  |2012-10-14 - 2012-10-19|2012-03-31         |2012-03-21           |Seattle, USA    |CORE2020   |623    |https://dblp.org/db/conf/infovis      |http://www.wikicfp.com/cfp/program?id=1611|

