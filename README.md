:movie_camera: :clapper: :desktop_computer:  Filmweb web scraper  :desktop_computer: :clapper: :movie_camera:



IDs:

Edyta Pszczółkowska 435022 

Wiktor Głuszek 387182


Instruction how to use:

1. Selenium - download the file selenium_scraper.py and run it. Program should install webdiver automatically in current directory. In selenium folder there is also csv file, with data from 100 scraped pages. 

2. BeautifulSoup - just run the .py file 

3. Scrapy- for the results of scrapy go to scrapy folder, first run step1.py file using command   'scrapy crawl step1 -o output.csv' - this file will write the links of 10 pages into a output.csv file. In the file step2.py from all those 10 links  10 pages will be scraped (together 10* 10 =  100 pages) about the most popular people in movie industry.
To get the final file with the scrapped data run command scrapy crawl filmweb2 -o final_output.csv.
