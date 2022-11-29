# CORE CFP

Python scraper for CORE Conference Portal
----------------------------------------

The target of CORE CFP is to load data about CORE ranked conferences and combine them with information
about call-for-papers such as conference date, submission deadline or conference location.

This is done by scraping the CORE Conference Portal (the scrape preserves DBLP links unlike the Excel export provided)
and completing the data by following the DBLP link and loading CFP details from WikiCFP if linked on DBLP.

Result is a list of conference objects with all the scraped information.

Moreover by using the `CoreCFP.upcoming()` method the list of conferences ordered by submission (or abstract registration) is showed from the specified date (current date by default) as shown in table below.

 **Acronym** | **Name**                                                                                    | **Rank** | **Dates**               | **Submission deadline** | **Abstract registration** | **Location**              | **Rank source** | **CORE ID** | **DBLP**                                 | **WikiCFP**                                
-------------|---------------------------------------------------------------------------------------------|----------|-------------------------|-------------------------|---------------------------|---------------------------|-----------------|-------------|------------------------------------------|--------------------------------------------
 ISPASS      | IEEE International Symposium on Performance Analysis of Systems and Software                | B        | 2023-04-01 - 2023-04-02 | 2022-12-06              | 2022-11-29                | "Raleigh, North Carolina" | CORE2021        | 705         | https://dblp.uni-trier.de/db/conf/ispass | http://www.wikicfp.com/cfp/program?id=1740 
 DSN         | IEEE/IFIP International Conference on Dependable Systems and Networks                       | A        | 2023-06-27 - 2023-06-30 | 2022-12-07              | 2022-12-01                | "Porto, Portugal"         | CORE2021        | 787         | https://dblp.uni-trier.de/db/conf/dsn    | http://www.wikicfp.com/cfp/program?id=769  
 IE          | The International Conference on Intelligent Environments                                    | B        | 2023-06-27 - 2023-06-30 | 2022-12-01              |                           | Mauritius                 | CORE2021        | 2179        | https://dblp.uni-trier.de/db/conf/intenv | http://www.wikicfp.com/cfp/program?id=1532 
 ICECCS      | IEEE International Conference on Engineering of Complex Computer Systems                    | B        | 2023-06-12 - 2023-06-16 | 2022-12-15              | 2022-12-08                | "Toulouse, France"        | CORE2021        | 646         | https://dblp.uni-trier.de/db/conf/iceccs | http://www.wikicfp.com/cfp/program?id=1348 
 ICPC        | "IEEE International Conference on Program Comprehension (previously IWPC, changed in 2006)" | A        | 2023-05-15 - 2023-05-16 | 2022-12-15              | 2022-12-10                | "Melbourne, Australia"    | CORE2021        | 1181        | https://dblp.uni-trier.de/db/conf/iwpc   | http://www.wikicfp.com/cfp/program?id=1444 
