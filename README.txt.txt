The main idea behind this screener is to formatt all the PE and EPS data for an industry and
use these values to make growth predictions.

To run the screener, navigate to the project directory and type' python3 wrapper.py'. 
You will then be prompted to input a sector name ('industrials' for example), and then 
input a number corresponding to whichever industry you would like to look at. Note that you 
will need the pandas, numpy, bs4, and openpyxl python modules installed for the code to run correctly. 
When finished running, 2 excel files will be created in a directory at /Documents/excel. 
The industry file models the whole industry while the topPicks (predictably) hold the best picks
based on expected growth, low RSI, and analysts agreeing with my projections.

Possible Errors:
This is some spagetti code and it's very possible you will run into errors. If the tickers
gathered for an industry aren't correct, it's because I can't spell and the industry name in the
constants file is mispelled and is used to create an incorrect url. Just switch it to the correct spelling

TODO:
the scraping is really slow right now because I have to check multiple urls for each industry
and for whatever reason my try/catch that should break the while loop if a page limit is reached
isn't working.

Looking to add technical analysis