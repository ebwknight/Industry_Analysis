"""
Created on Wed Feb 24 15:33:12 2021

@author: evanb
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import re
from dataCollector import *
from constants import *


'''
Calculating industry average RSI values
Omitting companies with no or negative RSI
'''
def ave_RSI(industryData):
    RSIaverage = 0
    RSIsum = 0
    RSIcount = 0
    for ticker in industryData:
        data = industryData[ticker]
        try:
            RSI = data.loc['RSI (14)']['Values']
        except:
            print("unable to index RSI for " + ticker)
        if RSI != '-': 
            #Hey, maybe add in some sophisticated math here
            RSIsum += float(RSI)
            RSIcount += 1
            #print("RSI for " + ticker + " is " + RSI)
        #else:
            #print(ticker + " currently has no PE, a negative PE, or is over 50")
        
    RSIaverage = RSIsum/RSIcount
    #print("Industry average P/E: " + str(PEaverage))
    return RSIaverage

'''
Calculating industry average P/B ratios
Omitting companies with no or negative P/B
'''
def ave_PB(industryData):
    PBaverage = 0
    PBsum = 0
    PBcount = 0
    for ticker in industryData:
        data = industryData[ticker]
        try:
            PB = data.loc['P/B']['Values']
        except:
            print("unable to index P/B for " + ticker)
        if PB != '-': 
            #Hey, maybe add in some sophisticated math here
            PBsum += float(PB)
            PBcount += 1
            #print("PE for " + ticker + " is " + PE)
        #else:
            #print(ticker + " currently has no PE, a negative PE, or is over 50")
        
    PBaverage = PBsum/PBcount
    #print("Industry average P/E: " + str(PEaverage))
    return PBaverage
'''
Calculating industry average P/E ratios
Omitting companies with no or negative P/E
Ommitting P/E values over 50 that skew the average
'''
def ave_PE(industryData):
    PEaverage = 0
    PEsum = 0
    PEcount = 0
    for ticker in industryData:
        data = industryData[ticker]
        try:
            PE = data.loc['P/E']['Values']
        except:
            print("unable to index P/E for " + ticker)
        if PE != '-' and float(PE) < 50: 
            #Hey, maybe add in some sophisticated math here
            PEsum += float(PE)
            PEcount += 1
            #print("PE for " + ticker + " is " + PE)
        #else:
            #print(ticker + " currently has no PE, a negative PE, or is over 50")
        
    PEaverage = PEsum/PEcount
    #print("Industry average P/E: " + str(PEaverage))
    return PEaverage


'''
Calculating industry average Forward P/E ratios
Omitting companies with no or negative Forward P/E
Ommitting Forward P/E values over 50 that skew the average
'''
def ave_FPE(industryData):
    fwdPEaverage = 0
    fwdPEsum = 0
    fwdPEcount = 0
    for ticker in industryData:
        data = industryData[ticker]
        try:
            fwdPE = data.loc['Forward P/E']['Values']
        except:
            print("unable to index Forward P/E for " + ticker)
        if fwdPE != '-' and float(fwdPE) < 50: 
            #Hey, maybe add in some sophisticated math here
            fwdPEsum += float(fwdPE)
            fwdPEcount += 1
            #print("Forward PE for " + ticker + " is " + fwdPE)
        #else:
            #print(ticker + " currently has no PE, a negative PE, or is over 50")
        
    fwdPEaverage = fwdPEsum/fwdPEcount
    #print("Industry average Forward P/E: " + str(fwdPEaverage))
    return fwdPEaverage

'''
Calculates a target price using 
    - current PE (or industry average) x nexy year EPS estimates
'''
def TP_PExNYEPS(stockData, industryPE):
    
    stockFEPS = stockData.loc['EPS next Y']['Values'][0]
    stockPE = stockData.loc['P/E']['Values']
    tPrice = 0
    if stockFEPS != '-' and float(stockFEPS) > 0:
        if stockPE != '-':
            if (float(stockPE) < 50):
                tPrice = float(stockPE) * float(stockFEPS)
            else:
                tPrice = industryPE * float(stockFEPS)
        else:
            tPrice = industryPE * float(stockFEPS)
      
    return tPrice

'''
First, estimate next year EPS assuming average EPS growth
    - current EPS x (1 + avereage EPS growth rate)

Second, use current price and ttm EPS to calculate ttm PE
    - current price / ttm EPS
    
Thrid, caluclate target price
    - TP = NY EPS estimate x trailing PE
'''

def TP_TTMPExNYEPS(stockData):
    
    stockTP = 0
    stockFEPS = 0
    stockTTMPE = 0
    
    #try:
        #step 1
    
    stockEPS = stockData.loc['EPS (ttm)']['Values']
    stockEPSgrowth = stockData.loc['EPS past 5Y']['Values']
        
    if stockEPS != '-' and stockEPSgrowth != '-':
        stockEPSgrowth = stockEPSgrowth[:-1] #chop off % sign
        stockFEPS = float(stockEPS) * (1 + (float(stockEPSgrowth)/100))
    else:
        print("No EPS or EPS growth data available")
        
        #step 2
    stockPrice =stockData.loc['Price']['Values']
    stockTTMEPS = stockData.loc['EPS (ttm)']['Values']
        
    if stockPrice != '-' and stockTTMEPS != '-':
        stockTTMPE = float(stockPrice) / float(stockTTMEPS)
    else:
        print("No Price or ttm EPS data available")
            
        #step 3
    stockTP = stockFEPS * stockTTMPE
    
    #except:
        #print("Missing EPS or PE data")
    
    return stockTP
    

def PE_variance(stock, industryData):
    
    av_PE = ave_PE(industryData)
    stockData = industryData[stock.upper()]
    stockPE = stockData.loc['P/E']['Values']
    PE_percent_diff = 0
    
    if stockPE != '-':
        PEdiff = (float(stockPE) - av_PE) / 100
        PE_percent_diff = PEdiff * 100
    
    return PE_percent_diff

def FPE_variance(stock, industryData):
    
    av_FPE = ave_FPE(industryData)
    stockData = industryData[stock.upper()]
    stockFPE = stockData.loc['Forward P/E']['Values']
    FPE_percent_diff = 0
    
    if stockFPE != '-':
        FPEdiff = (float(stockFPE) - av_FPE) / 100
        FPE_percent_diff = FPEdiff * 100
    
    return FPE_percent_diff

def PB_variance(stock, industryData):
    
    av_PB = ave_PB(industryData)
    stockData = industryData[stock.upper()]
    stockPB = stockData.loc['P/B']['Values']
    PB_percent_diff = 0
    
    if stockPB != '-':
        PBdiff = (float(stockPB) - av_PB) / 100
        PB_percent_diff = PBdiff * 100
    
    return PB_percent_diff

def RSI_variance(stock, industryData):
    
    av_RSI = ave_RSI(industryData)
    stockData = industryData[stock.upper()]
    stockRSI = stockData.loc['RSI (14)']['Values']
    RSI_percent_diff = 0
    
    if stockRSI != '-':
        RSIdiff = (float(stockRSI) - av_RSI) / 100
        RSI_percent_diff = RSIdiff * 100
    
    return RSI_percent_diff

def check(stockData):
        
    badStocks = []
    for stock in stockData:
        try:
            price = stockData[stock].loc['Price']['Values']
        except:
            print(stock.upper() + " is invalid - Removing from data set...")
            badStocks.append(stock.upper())
            
    for bad in badStocks:
        del stockData[bad]

    return stockData


def eval_stock(stockData, industryPE, ticker):
    
    stockPrice = stockData.loc['Price']['Values']
    stockPE = stockData.loc['P/E']['Values']
    stockFPE = stockData.loc['Forward P/E']['Values']
    stockRSI = stockData.loc['RSI (14)']['Values']
    stockPB = stockData.loc['P/B']['Values']
    stockFprice1 = round(TP_PExNYEPS(stockData, industryPE), 2)
    stockFprice2 = round(TP_TTMPExNYEPS(stockData), 2)
    stockATP = stockData.loc['Target Price']['Values']
    stockGrowth = 0
    
    growth1 = 100 * (float(stockFprice1) - float(stockPrice)) / float(stockPrice)
    growth2 = 100 * (float(stockFprice2) - float(stockPrice)) / float(stockPrice)
    growth3 = 0
    if stockATP != '-':
        growth3 = 100 * (float(stockATP) - float(stockPrice)) / float(stockPrice)
    
    if growth1 != 0:
        if growth2 != 0:
            if growth3 != 0:
                stockGrowth = round((growth1 + growth2 + growth3) / 3, 2)    
            else:
                stockGrowth = round((growth1 + growth2) / 2, 2)
        elif growth3 != 0:
                stockGrowth = round((growth1 + growth3) / 2, 2)
        else:
            stockGrowth = round(growth1, 2)
    elif growth2 != 0:
            if growth3 != 0:
                stockGrowth = round((growth2 + growth3) / 2, 2)
            else:
                stockGrowth = stockGrowth = round(growth2, 2)
    elif growth3 != 0:
                stockGrowth = round(growth3, 2)
                
    return [ticker, stockPrice, stockPE, stockFPE, stockPB, stockRSI, stockFprice1, stockFprice2, stockATP, stockGrowth]


def industry_growth(stockArray):
    #calculate average industry growth 
    growthSum = 0
    growthCount = 0
    for stock in stockArray:
        if stock[9] != 0 and stock[9] < 200:
            growthSum += stock[9]
            growthCount += 1
    industryGrowth = growthSum / growthCount
    return industryGrowth

def parse_value(stockArray):
    
    goodStocks = []
    for stock in stockArray:
        if stock[9] > 0 and float(stock[5]) < 60:
            if stock[7] != 'NA' and stock[7] != '-' and stock[8] != 'NA' and stock[8] != '-':
                if (abs((float(stock[8]) - float(stock[7])) / float(stock[8]) * 100) < 15) or float(stock[8]) > float(stock[7]):
                    goodStocks.append(stock)
    return goodStocks


def industry_req():
    
    print("Please input the name of a sector: \n")
    for sec in SECTORS:
        print(sec)
    sector = input().lower()
    
    print("\nPlease select an Industry by inputting the number: \n")
    #Also please make a reasonable switch statement in python
    
    if sector == "basic materials": 
        for ind in BASIC_MATERIALS:
            print(str(ind) + ": " + BASIC_MATERIALS[ind])
    
    elif sector == "communication services":
        for ind in COMMUNICATION_SERVICES:
            print(str(ind) + ": " + COMMUNICATION_SERVICES[ind])
            
    elif sector == "consumer cyclical":
        for ind in CONSUMER_CYCLICAL:
            print(str(ind) + ": " + CONSUMER_CYCLICAL[ind])
            
    elif sector == "consumer defense":
        for ind in CONSUMER_DEFENSE:
            print(str(ind) + ": " + CONSUMER_DEFENSE[ind])
            
    elif sector == "energy":
        for ind in ENERGY:
            print(str(ind) + ": " + ENERGY[ind])
    
    elif sector == "financial":
        for ind in FINANCIAL:
            print(str(ind) + ": " + FINANCIAL[ind])
    
    elif sector == "healthcare":
        for ind in HEALTHCARE:
            print(str(ind) + ": " + HEALTHCARE[ind])
        
    elif sector == "industrials":
        for ind in INDUSTRIALS:
            print(str(ind) + ": " + INDUSTRIALS[ind])
        
    elif sector == "real estate":
        for ind in REAL_ESTATE:
            print(str(ind) + ": " + REAL_ESTATE[ind])
    
    elif sector == "technology":
        for ind in TECHNOLOGY:
            print(str(ind) + ": " + TECHNOLOGY[ind])
            
    else:
        for ind in UTILITIES:
            print(str(ind) + ": " + UTILITIES[ind])
            
    ind = int(input())
    indName = SECTORS[sector][ind]
    
    return indName


    
def SMA_rating(stockData):
    
        return