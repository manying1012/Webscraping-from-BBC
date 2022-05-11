import pytest
import json
import requests
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import spacy
from collections import Counter
import en_core_web_sm

def bbc_scraper(url):
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    data = {}

    # extracting URL, title, date published
    data['URL'] = str(url)
    data['Title'] = soup.find('h1', id = "main-heading").text
    date = soup.time
    data['Date_published'] = date.text

    #extracting article contents
    content = []
    main_text = soup.find('article', class_="ssrcss-1072xwf-ArticleWrapper e1nh2i2l6")
    for line in main_text.find_all('p', class_ = "ssrcss-1q0x1qg-Paragraph eq5iqo00"):
      content.append(line.text)
    content = list(filter(None, content))
    content[:] = [" ".join(content[:])]
    data['Content'] = content[0]

    results_json = json.dumps(data)
    
    return results_json
  
  def extract_entities(string):

  # naming entities in string
  nlp = en_core_web_sm.load()
  sentence = nlp(string)
  entity_labels = [(word.text, word.label_) for word in sentence.ents]

  # creating lists of entities 
  entities = {}

  lists = ['people', 'places', 'organisations']
  entity_list = ['PERSON', 'GPE', 'ORG']
  
  for entity in range(0, len(entity_list)):
    entity_name = lists[entity]
    lists[entity] = []
    for label in entity_labels:
      if label[1] == entity_list[entity]:
        lists[entity].append(label[0])
    entities[entity_name] = lists[entity]

  entities_json = json.dumps(entities)

  return entities_json

####################################################################
# Test cases

def test_bbc_scrape():
    results = {'URL': 'https://www.bbc.co.uk/news/uk-52255054',
                'Title': 'Coronavirus: \'We need Easter as much as ever,\' says the Queen',
                'Date_published': '11 April 2020',
                'Content': '"Coronavirus will not overcome us," the Queen has said, in an Easter message to the nation. While celebrations would be different for many this year, she said: "We need Easter as much as ever." Referencing the tradition of lighting candles to mark the occasion, she said: "As dark as death can be - particularly for those suffering with grief - light and life are greater." It comes as the number of coronavirus deaths in UK hospitals reached 9,875. Speaking from Windsor Castle, the Queen said many religions had festivals celebrating light overcoming darkness, which often featured the lighting of candles. She said: "They seem to speak to every culture, and appeal to people of all faiths, and of none. "They are lit on birthday cakes and to mark family anniversaries, when we gather happily around a source of light. It unites us." The monarch, who is head of the Church of England, said: "As darkness falls on the Saturday before Easter Day, many Christians would normally light candles together.  "In church, one light would pass to another, spreading slowly and then more rapidly as more candles are lit. It\'s a way of showing how the good news of Christ\'s resurrection has been passed on from the first Easter by every generation until now." As far as we know, this is the first time the Queen has released an Easter message. And coming as it does less than a week since the televised broadcast to the nation, it underlines the gravity of the situation as it is regarded by the monarch. It serves two purposes really; it is underlining the government\'s public safety message, acknowledging Easter will be difficult for us but by keeping apart we keep others safe, and the broader Christian message of hope and reassurance.  We know how important her Christian faith is, and coming on the eve of Easter Sunday, it is clearly a significant time for people of all faiths, but particularly Christian faith. She said the discovery of the risen Christ on the first Easter Day gave his followers new hope and fresh purpose, adding that we could all take heart from this.  Wishing everyone of all faiths and denominations a blessed Easter, she said: "May the living flame of the Easter hope be a steady guide as we face the future." The Queen, 93, recorded the audio message in the White Drawing Room at Windsor Castle, with one sound engineer in the next room.  The Palace described it as "Her Majesty\'s contribution to those who are celebrating Easter privately".  It follows a speech on Sunday, in which the monarch delivered a rallying message to the nation. In it, she said the UK "will succeed" in its fight against the coronavirus pandemic, thanked people for following government rules about staying at home and praised those "coming together to help others". She also thanked key workers, saying "every hour" of work "brings us closer to a return to more normal times".'}
    scraper_result = bbc_scraper('https://www.bbc.co.uk/news/uk-52255054')
    print(scraper_result)
    assert json.loads(scraper_result) == results


def test_extract_entities_amazon_org():
    input_string = "I work for Amazon."
    results_dict = {'people':[],
                    'places':[],
                    'organisations': ['Amazon']
                    }
    extracted_entities_results = extract_entities(input_string)
    print(extracted_entities_results)
    assert json.loads(extracted_entities_results) == results_dict


def test_extract_entities_name():
    input_string = "My name is Bob"
    results_dict = {'people':['Bob'],
                    'places':[],
                    'organisations': []
                    }
    extracted_entities_results = extract_entities(input_string)
    print(extracted_entities_results)
    assert json.loads(extracted_entities_results) == results_dict
    
    
    
test_bbc_scrape()
test_extract_entities_amazon_org()
test_extract_entities_name()
