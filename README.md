# Stockalizer

## Basics
This project at the moment has two subdirectories. A twitter-scraper to stream tweets from a twitter profile.
And a tweet classifier which takes th tweet and performs a sentiment analysis on it.

## Installation
To run these programs, head into one of the folders and run this command in a terminal:
``` 
pip install -r requirements
```

## Twitter-Scraper
This scraper runs a stream to get all new tweets which a definabel user posts and fetches them via the twitter-api.

To be able to run this scraper you need a twitter devloper Account and insert your api-key, api-key-secret, access-token and access-token-secret into a keys.py file which should be placed inside of an ssh folder right below the twitter-scraper

## Create requirements file

Head into the desired directory and simply run this command:
```
pip freeze > requirements.txt
```