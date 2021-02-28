import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import re
from industryComp import *
from constants import *

pd.set_option('display.max_colwidth', 25)

def get_fundamentals(ticker):
    try:
        
        # Set up scraper
        url = ("http://finviz.com/quote.ashx?t=" + ticker.lower())
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        html = soup(webpage, "html.parser")
        # Find fundamentals table
        fundamentals = pd.read_html(str(html), attrs = {'class': 'snapshot-table2'})[0]
        
        # Clean up fundamentals dataframe
        fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        colOne = []
        colLength = len(fundamentals)
        for k in np.arange(0, colLength, 2):
            colOne.append(fundamentals[f'{k}'])
        attrs = pd.concat(colOne, ignore_index=True)
    
        colTwo = []
        colLength = len(fundamentals)
        for k in np.arange(1, colLength, 2):
            colTwo.append(fundamentals[f'{k}'])
        vals = pd.concat(colTwo, ignore_index=True)
        
        fundamentals = pd.DataFrame()
        fundamentals['Attributes'] = attrs
        fundamentals['Values'] = vals
        fundamentals = fundamentals.set_index('Attributes')
        #print(fundamentals.loc['P/E'])
        return fundamentals

    except Exception as e:
        return e
    
def scrape(industryName):
    
    print("Fetching all companies in industry...")
    # Set up scraper
    noAnd = re.sub(r' and ', '', industryName)
    noSpace = re.sub(r' ', '', noAnd)
    noDash = re.sub(r'-', '', noSpace)
    formattedIndustry = re.sub(r',', '', noDash)
    url = ("https://www.finviz.com/screener.ashx?v=161&f=ind_" + formattedIndustry)
    
    #create set of hrefs to ticker quote pages 
    uglyTickers = set()
    tickers = set()
    
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        html = soup(webpage, "html.parser")
    except:
        print("invalid url, dumb dog! Check spelling/url on " + formattedIndustry)
        print(url)
    
    
    for tag in html.find_all('a'):
        uglyTickers.add(tag.get('href'))
   
    page = 2
    while page < 50:
        url = url + "&r=" + str(page) + "1"
        
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            html = soup(webpage, "html.parser")
            
            for tag in html.find_all('a'):
                uglyTickers.add(tag.get('href'))
                
            page = page + 2
            
        except:
            print("Page limit reached")
            break
        
        #parse out the tickers
    for tick in uglyTickers:
        ticker = re.findall(r'[A-Z]{2,4}', tick)
        #print("url " + tick)
        if len(ticker) > 0:
            tickers.add(ticker[0])
    print(tickers)
        
        
    #Collect data for tickers in industry
    tickerData = {}
    for ticker in tickers:
        #print(ticker)
        try:
            data = get_fundamentals(ticker)
            print("Collecting data for " + ticker + "...")
        except:
            data = null
            print("Sorry! Unable to fetch data for " + ticker)
        tickerData[ticker] = data
        
    return tickerData
        
'''
def cnn_forecast(ticker):
    
    forecast = '-'
    try:
        url = ("https://money.cnn.com/quote/forecast/forecast.html?symb=" + ticker)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        html = soup(webpage, "html.parser")
    except:
        print("Bad URL")
        
    try:
        
        print(forecast)
    except:
        print("No CNN forecast available")
        
    return forecast
''' 
    
def get_news():
    try:
        # Find news table
        news = pd.read_html(str(html), attrs = {'class': 'fullview-news-outer'})[0]
        links = []
        for a in html.find_all('a', class_="tab-link-news"):
            links.append(a['href'])
        
        # Clean up news dataframe
        news.columns = ['Date', 'News Headline']
        news['Article Link'] = links
        news = news.set_index('Date')
        return news

    except Exception as e:
        return e

def get_insider():
    try:
        # Find insider table
        insider = pd.read_html(str(html), attrs = {'class': 'body-table'})[0]
        
        # Clean up insider dataframe
        insider = insider.iloc[1:]
        insider.columns = ['Trader', 'Relationship', 'Date', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']
        insider = insider[['Date', 'Trader', 'Relationship', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4']]
        insider = insider.set_index('Date')
        return insider

    except Exception as e:
        return e
'''
data = get_fundamentals("ARRY")
print(data)
print(float(data.loc['P/E']['Values']))
'''