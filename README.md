# Stockalizer
The Stockalizer project is a university project to analyse news and twitter data with sentiment analysis, to draw conclusions from this for the stock market.
The project is written in Python and consists of various scrapers for collecting raw data, a neural network for analysing news data and various utilities. For more information see below.

## Twitter-Scraper
This scraper runs a stream to get all new tweets which a definabel user posts and fetches them via the twitter-api.

To be able to run this scraper you need a twitter devloper Account and insert your api-key, api-key-secret, access-token and access-token-secret into a keys.py file which should be placed inside of an ssh folder right below the twitter-scraper

## Backtesting
Contains all backtesting relevant files, the trading strategy and the analysis scripts for the news and Twitter data.

## Livetrading
Livetrading runs mainly via Microsoft Azure and is located in its own repo. Accessible via this link: [Stockalizer Azure Repo](https://github.com/SoenkeSobott/stockalizer-time-trigger)

## Disclosure
This is a university project and should be seen as such. This project is a object of change. If you have any questions, 
please contact sobott.soenke@gmail.com or alexander.staehle@htwg-konstanz.de .
