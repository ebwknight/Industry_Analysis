"""
Created on Thu Feb 25 13:36:39 2021

@author: evanb
"""
from constants import *
from industryComp import *
from dataCollector import *
import math

indName = industry_req()
tickerData = scrape(indName)
tickerData = check(tickerData)

#industry averages
industryPE = ave_PE(tickerData)
industryFPE = ave_FPE(tickerData)
industryPB = ave_PB(tickerData)
industryRSI = ave_RSI(tickerData)
industryGrowth = 0 #temp

stockArray = []
for ticker in tickerData:
    stockArray.append(eval_stock(tickerData[ticker], industryPE, ticker))

#calculate average growth accross industry
industryGrowth = industry_growth(stockArray)

#add row of indsutry averages
stockArray.append(['Industry', 'NA', industryPE, industryFPE, industryPB, industryRSI,'NA', 'NA', 'NA', industryGrowth])

#parse out favorabel stocks within industry
goodStocks = parse_value(stockArray)

#create data frame of good stocks and export to excel
top_picks_df = pd.DataFrame(goodStocks, columns = ['Stock', 'Price', 'P/E', 'Forward P/E', 'P/B', 'RSI', 'TP (PE x EPS)', 'TP (ttmPE x EPS)', 'Analysts mean TP', 'Growth'])
industry_df = pd.DataFrame(stockArray, columns = ['Stock', 'Price', 'P/E', 'Forward P/E', 'P/B', 'RSI', 'TP (PE x EPS)', 'TP (ttmPE x EPS)', 'Analysts mean TP', 'Growth'])

try:
    top_picks_df.to_excel(r'~/Documents/excel/topPicks.xlsx', index = False)
    industry_df.to_excel(r'~/Documents/excel/industry.xlsx', index = False)
    print("Successfully exported to Excel.")
except:
    print("Unable to export to Excel. Make sure the export file isn't already open and that the openpyxl module is installed")


