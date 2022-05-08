import scrapy
import re
import time

start = time.time()

class Filmweb(scrapy.Spider):
    name = 'filmweb2'
    
    
    try:
    	with open("output.csv", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()][1:]
    except:
        start_urls = []
        
        

    # --------------------------------------------------------------------------------------------------------------------------- 			

    def parse(self, response):

        try:
            name = response.xpath('//span[@itemprop="name"]/text()').extract()
        except:
            name = ''

        try:
            birthdate = response.xpath('//span[@itemprop="birthDate"]/text()').extract()[0]
        except:
            birthdate = ''

            # the code above returns a string  like: ' 18 grudnia 1946 ',
            # let's extract the age of the actor by splitting the string above, taking last
            # element of the new list created by the string split
            # and substract birthyear from the current year (2022).

        try:
            age = 2022 - int(birthdate.split()[-1])
        except:
            age = ''

        try:
            birthplace_strings = (response.xpath('//span[@itemprop="birthPlace"]/text()').extract()[0])
        except:
            birthplace_strings = ''

            # the code above returns a one element list like: ["Owensboro, Kentucky, USA"],
            # let's extract a birthcity and birthcountry from it by splitting the string above
            # and taking last as birthcountry and last-but-one as birthcity:

        try:
            birthcity = birthplace_strings.split(', ')[-2]
        except:
            birthcity = ''

        try:
            birthcountry = birthplace_strings.split(', ')[-1]
        except:
            birthcountry = ''

        try:
            grade = response.xpath('//div[@class = "personRating personRating personRating--lg"]/div[@class = "personRating__rating"]/span[@class="personRating__rate"]/text()').extract()
        except:
            grade = ''

        try:
            top_text = response.xpath("//div[@class='page__container']/a[starts-with(@href,'/ranking/person')]/text()").extract()[0]
        except:
            top_text = ''

        try:

            top_number =  top_text.split()[0][1:]
        except:
            top_number = ''

        try:
            profession = top_text.split()[-1]
        except:
            profession = ''

        try:
            no_opinions = response.xpath('//div[@class = "personRating__rating"]/div[@class = "personRating__count"]/span[@class="personRating__count--value"]/text()').extract()[0]
        except:
            no_opinions = ''

        try:
            awards_text = response.xpath('//div[@class="awardsSection__title"]/text()').extract()[0]
        except:
            awards_text = ''
        # the code above returns a one element list like: ["Zdobył 2 Złote Globy, 23 inne nagrody i 73 nominacje"],
        # let's extract numbers from this string, then extract number of nominations and awards:

        numbers_from_award_text = [int(i) for i in awards_text.split() if i.isdigit()]

        # If a person won two or more oscars/ golden globes, baftas or any other
        # important award, then there will be 3 integers from the string like in the example above,
        # the first two integers are awards and the 3rd one number of nominations.
        #When the actor/actress won only one oscar/bafta etc. the string looks like "Zdobył  Złoty Glob, 23 inne nagrody i 73 nominacje",
        # so the number of awards must be incremented by one.

        try:
            if len(numbers_from_award_text) == 3:
                no_awards = numbers_from_award_text[-2]+numbers_from_award_text[-3]
            else: no_awards = numbers_from_award_text[-2] + 1
        except:
            no_awards = ''

        #The last element of the extracted integer list is number of nominations

        try:
            no_nominations = numbers_from_award_text[-1]
        except:
            no_nominations = ""

        try:
            known_for = response.xpath('//a[@class="personKnownFor__productionLink"]/text()').extract()[:3]
        except:
            known_for = ''

        # taking the 3 best and unique roles
        try:
            best_roles = list(set(response.xpath('//span[@class="personRoleCharacter__characterName"]/text()').extract()[:3]))
        except:
            best_roles = ''
        # if a person is not an actor/actress then the set is empty

        # 3 newest productions
        try:
            newest_productions = response.xpath('//a[@class="personRolePreview__title"]/text()').extract()[:3]
        except:
            newest_productions = ''


        yield {"name": name,
               "age" : age,
                "birthcity" : birthcity,
               "birthcountry" : birthcountry,
                #"top_text" : top_text,
                "top_number" : top_number,
                "profession" : profession,
               "grade" : grade,
               "no_opinions" : no_opinions,
               "no_awards" : no_awards,
               "no_nominations" : no_nominations,
               "known_for" : known_for,
               "best_roles" : best_roles,
               "newest_productions" : newest_productions
               }



end = time.time()
print("Scraping time: ",round(end - start,2), " seconds")