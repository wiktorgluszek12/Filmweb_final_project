from bs4 import BeautifulSoup as BS
from urllib import request as re
import pandas as pd
import numpy
import re as RE


import time

start = time.time()




# Zbieranie linków do substron --------------------------------------------------------------------------
one_hundred_pages = True

list_of_links = []

if one_hundred_pages == True:
    paginations = 10 # 10 x 10 = 100 subpages
else:
    paginations = 1000 # There are 1ths pages in total

# Collecting links to sub pages
for page in range(1, paginations+1):
    html = re.urlopen(f"https://www.filmweb.pl/persons/search?orderBy=popularity&descending=true&page={page}")
    bs = BS(html.read(), 'html.parser')
    list_1 = ['https://www.filmweb.pl' + str(link.get('href')) for link in bs.find_all('a')]
    for x in list_1:
        if "/person/" in x and '/actors/' not in x:
             list_of_links.append(x)

list_of_links = list(set(list_of_links))



d = pd.DataFrame({'name': [],
                  'age': [],
                  'birthcity': [],
                  'birthcountry': [] ,
                  'grade': [] ,
                  'no_opinions': [] ,
                  'no_awards': [] ,
                  'no_nominations': [] ,
                  'top_number': [] ,
                  'profession': [] ,
                  'known_for_list': [],
                  'three_best_roles' :[],
                  'newest_productions' : [] })

for link in list_of_links:

    html = re.urlopen(link)
    bs_actor = BS(html.read(), 'html.parser')

    try:
        name = bs_actor.find('span', {'itemprop': 'name'}).text
    except:
        name = ""


    try:
        age0 = bs_actor.find('span', {'itemprop': 'birthDate'}).text
    except:
        age0 = ''

    try:
        age = int(2022 - int(age0.split()[-1]))
    except:
        age = ''

    try:
        birthplace_strings = bs_actor.find('span', {'itemprop': 'birthPlace'}).text.split(', ')
        birthcity = birthplace_strings[-2]
        birthcountry = birthplace_strings[-1]

    except:
        birthcity = ''
        birthcountry = ''


    try:
        grade = bs_actor.find('span', {'class': 'personRating__rate'}).text
    except:
        grade = ''

    try:
        no_opinions = bs_actor.find('span', {'class': 'personRating__count--value'}).text
    except:
        no_opinions = ''


    try:
        awards_text = (bs_actor.find('div', {'class': 'awardsSection__title'})).text
        numbers_from_award_text = [int(i) for i in awards_text.split() if i.isdigit()]
    except:
        pass

    # If a person won two or more oscars/ golden globes, baftas or any other
    # important award, then there will be 3 integers from the string like in the example above,
    # the first two integers are awards and the 3rd one number of nominations.
    # When the actor/actress won only one oscar/bafta etc. the string looks like "Zdobył  Złoty Glob, 23 inne nagrody i 73 nominacje",
    # so the number of awards must be incremented by one.

    try:
        if len(numbers_from_award_text) == 3:
            no_awards = int(numbers_from_award_text[-2] + numbers_from_award_text[-3])
        else:
            no_awards = int(numbers_from_award_text[-2] + 1)
    except:
        no_awards = ''

    # The last element of the extracted integer list is number of nominations

    try:
        no_nominations = int(numbers_from_award_text[-1])
    except:
        no_nominations = ""



    # TOP -  when null, then person is outside the list of top 500 of their profession

    try:
        top =  bs_actor(text=RE.compile(' TOP '))[0]
        top = top.split()
    except:
        top = ''


    # number of top of the list (if not on the list of top professionals, then empty)

    try:

        top_number = int(top[0][1:])
    except:
        top_number = ''


    try:
        profession = top[-1]
    except:
        profession = ''



    # the 3 most popular movies the actor is known for

    try:
        known_for = (bs_actor.find_all('a', {'class': 'personKnownFor__productionLink'}))
        known_for_list = [known_for_i.text for known_for_i in known_for][:3]
    except:
        known_for_list = ''



    # the  best unique  roles

    try:
        best_roles = (bs_actor.find_all('span', {'class': 'personRoleCharacter__characterName'}))
        three_best_roles = [best_roles_i.text for best_roles_i in best_roles][:3]
    except:
        three_best_roles = ''



    # 3 newest productions
    try:
        newest_productions = (bs_actor.find_all('a', {'class': 'personRolePreview__title'}))
        newest_productions = [newest_productions_i.text for newest_productions_i in newest_productions][:3]
    except:
        newest_productions = ''

    person = {'name': name,
              'age': age,
              'birthcity': birthcity,
              'birthcountry': birthcountry,
              'grade': grade,
               'no_opinions': no_opinions,
              'no_awards': no_awards,
              'no_nominations': no_nominations,
              'top_number': top_number,
              'profession': profession,
              'known_for_list': known_for_list,
              'three_best_roles': three_best_roles,
              'newest_productions' : newest_productions}


    d = d.append(person, ignore_index=True)
    print(d)


d.to_csv('person.csv')


end = time.time()
print(end - start)
