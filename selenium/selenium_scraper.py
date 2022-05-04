import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re

start = time.time()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

one_hundred_pages = True

# Collected datapoints
name = []
birthday = []
birth_location = []
grade = []
no_opinions = []
awards_str = []
known_for = []
best_roles = []
newest_productions = []
ranking = []
awards =[]
nominations = []

# List of sub pages
list_of_links =[]

# Collecting links to sub pages
if one_hundred_pages == True:
    paginations = 10 # 10 x 10 = 100 subpages
else:
    paginations = 1000 # There are 1ths pages in total

for page in range(1, paginations+1):
    driver.get(f"https://www.filmweb.pl/persons/search?orderBy=popularity&descending=true&page={page}")
    driver.implicitly_wait(2.5)
    
    #Click cookies popup
    try:
        abc = driver.find_element(By.XPATH, "//button[@id ='didomi-notice-agree-button']").click()       
    except:
        pass
           
    # Getting all links from list of actors on a given page
    abc = driver.find_elements(By.XPATH, "//h3/a[starts-with(@href, '/person/')]")
    for x in abc:
        list_of_links.append(x.get_attribute("href"))
    

# Going into subpages
for link in list_of_links:
    
    driver.get(link)
    driver.implicitly_wait(2.5)
    
    # Name
    abc = driver.find_element(By.XPATH, "//div[@class='personCareerHistorySection__subtitle']")
    name.append(abc.text)
    
    # Birthday
    abc = driver.find_element(By.XPATH, "//span[@itemprop='birthDate']")
    birthday.append(abc.text)
    
    # birth_location
    abc = driver.find_element(By.XPATH, "//span[@itemprop='birthPlace']")
    birth_location.append(abc.text)
    
    # birthcountry <- this will be split at the end from birth city
    
    # grade
    abc = driver.find_element(By.XPATH, "//span[@class='personRating__rate']")
    grade.append(abc.text)
    
    # no_opinions
    abc = driver.find_element(By.XPATH, "//span[@class='personRating__count--value']")
    no_opinions.append(abc.text)
    
    # awards string
    try:
        abc = driver.find_element(By.XPATH, "//div[@class='awardsSection__title']")
        awards_str.append(abc.text)
    except:
        awards_str.append(None)
    
    # awards - need to split string 
    # case 1: "Zdobył Oscar, 33 inne nagrody i 90 nominacji" -> extract 33 plus add 1
    # case 2: "Zdobył 2 nagrody Oscar, 34 inne nagrody" -> extract 34 plus add extracted 2
    # case 3: No list of awards -> except
    
    try:
        abc = driver.find_element(By.XPATH, "//div[@class='awardsSection__title']")
        
        # create list of all numbers in string
        lista = [int(s) for s in re.findall(r'\b\d+\b', abc.text)]
        
        # case 2
        if len(lista) == 3:
            nominations1 =  lista[2]
            total_awards = lista[0] + lista[1]
        # case 1   
        else:
            nominations1 = lista[1]
            total_awards = lista[0] + 1

        nominations.append(nominations1)
        awards.append(total_awards)
    
    # case 3
    except:
        nominations.append(None)
        awards.append(None)
        
                                                 
    # Known for
    abc = driver.find_elements(By.XPATH, "//a[@class='personKnownFor__productionLink']")
    t =''
    for x in abc:
        t += str(x.text) + ", "    
    known_for.append(t)
    
    # Best roles
    abc = driver.find_elements(By.XPATH, "//span[@class='personRoleCharacter__characterName']")
    t =''
    for x in abc:
        t += str(x.text) + ", "    
    best_roles.append(t)
    
    # newest_productions
    abc = driver.find_elements(By.XPATH, "//a[@class='personRolePreview__title']")
    t =''
    for x in abc:
        t += str(x.text) + ", "    
    newest_productions.append(t)
    
    # Ranking
    try:
        abc = driver.find_element(By.XPATH, 
                                   "//div[@class='page__container']/a[starts-with(@href,'/ranking/person/actors/')]")
        ranking.append(abc.text.split(" ")[0].split("#")[1])
    except:  
        try:
            abc = driver.find_element(By.XPATH, 
                                       "//div[@class='page__container']/a[starts-with(@href,'/ranking/person/director')]")
            ranking.append(abc.text.split(" ")[0].split("#")[1])
        except:   
            ranking.append(None)
    
    
# Creating dataframe with variables                          
df = pd.DataFrame(list(zip(
                            name,
                            birthday,
                            birth_location,
                            grade,
                            no_opinions,
                            awards_str,
                            known_for,
                            best_roles,
                            newest_productions,
                            ranking,
                            awards,
                            nominations
                           )),
                        columns =[
                            'name',
                            'birthday',
                            'birth_location',
                            'grade',
                            'no_opinions',
                            'awards_str',
                            'known_for',
                            'best_roles',
                            'newest_productions',
                            'ranking',
                            'awards',
                            'nominations'
                           ])
end = time.time()
print("Scraping time: ",round(end - start,2), " seconds")

# Some data cleaning 
df['Country_of_birth'] = df['birth_location'].apply(lambda x: x.split(",")[-1])
df['City_of_birth'] = df['birth_location'].apply(lambda x: x.split(",")[0])

# Flag 1 if won 0 if not
df['won_oscar'] = df['awards_str'].apply(lambda x: 1 if 'Oscar' in str(x) else 0)

# Replacing comma with dot in grade variable
df['grade'] = df['grade'].apply(lambda x: str(x.replace(',','.'))).astype(float)

# Grade remove space in the middle
df['no_opinions'] = df['no_opinions'].apply(lambda x: x.replace(' ', '')).astype(int)

# Making sure variable types are right
df['ranking'] = df['ranking'].astype('Int64')
df['awards'] = df['awards'].astype('Int64')
df['nominations'] = df['nominations'].astype('Int64')
df['won_oscar'] = df['won_oscar'].astype('Int64')
display(df)
