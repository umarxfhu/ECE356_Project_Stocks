# 356 script to load csv

import pandas as pd
 
df_ipo = pd.read_csv("C:\a_UNI\3B\ECE 356\Project STONKS\daily data & company info\IPODataFull.csv")

df_companyOnly = df_ipo[[	"Symbol",
                        	"Name",
                         	"Sector",
                         	"Industry",
                         	"Summary Quote",
                         	"CEOAge",
                         	"CEOName",
                         	"City",
                         	"stateCountry",
                         	"FiscalDateEnd",
                         	"employees",
                         	"YearFounded",
                          "exactDateFound"
                           ]]


df_companyOnly.to_csv('company.csv', index=False)

df_2014 = pd.read_csv("/content/drive/MyDrive/UNI/3B/ECE 356/356 Project - STONKS/2014_Financial_Data.csv", encoding='latin1')
df_2015 = pd.read_csv("/content/drive/MyDrive/UNI/3B/ECE 356/356 Project - STONKS/2015_Financial_Data.csv", encoding='latin1')
df_2016 = pd.read_csv("/content/drive/MyDrive/UNI/3B/ECE 356/356 Project - STONKS/2016_Financial_Data.csv", encoding='latin1')
df_2017 = pd.read_csv("/content/drive/MyDrive/UNI/3B/ECE 356/356 Project - STONKS/2017_Financial_Data.csv", encoding='latin1')
df_2018 = pd.read_csv("/content/drive/MyDrive/UNI/3B/ECE 356/356 Project - STONKS/2018_Financial_Data.csv", encoding='latin1')

df_2014new = df_2014[[
  "Symbol",
  "Revenue",
  "Revenue Growth",
  "Net Income",
  "EPS",
  "Free Cash Flow margin",
  "Net Profit Margin",
  "currentRatio",
  "returnOnEquity",
  "priceEarningsRatio",
  "Revenue per Share",
  "Market Cap",
  "PE ratio",
  "Dividend Yield",
  "ROIC",
  "3Y Revenue Growth (per Share)"
]]

df_2015new = df_2015[[
  "Symbol",
  "Revenue",
  "Revenue Growth",
  "Net Income",
  "EPS",
  "Free Cash Flow margin",
  "Net Profit Margin",
  "currentRatio",
  "returnOnEquity",
  "priceEarningsRatio",
  "Revenue per Share",
  "Market Cap",
  "PE ratio",
  "Dividend Yield",
  "ROIC",
  "3Y Revenue Growth (per Share)"
]]

df_2016new = df_2016[[
  "Symbol",
  "Revenue",
  "Revenue Growth",
  "Net Income",
  "EPS",
  "Free Cash Flow margin",
  "Net Profit Margin",
  "currentRatio",
  "returnOnEquity",
  "priceEarningsRatio",
  "Revenue per Share",
  "Market Cap",
  "PE ratio",
  "Dividend Yield",
  "ROIC",
  "3Y Revenue Growth (per Share)"
]]

df_2017new = df_2017[[
  "Symbol",
  "Revenue",
  "Revenue Growth",
  "Net Income",
  "EPS",
  "Free Cash Flow margin",
  "Net Profit Margin",
  "currentRatio",
  "returnOnEquity",
  "priceEarningsRatio",
  "Revenue per Share",
  "Market Cap",
  "PE ratio",
  "Dividend Yield",
  "ROIC",
  "3Y Revenue Growth (per Share)"
]]

df_2018new = df_2018[[
  "Symbol",
  "Revenue",
  "Revenue Growth",
  "Net Income",
  "EPS",
  "Free Cash Flow margin",
  "Net Profit Margin",
  "currentRatio",
  "returnOnEquity",
  "priceEarningsRatio",
  "Revenue per Share",
  "Market Cap",
  "PE ratio",
  "Dividend Yield",
  "ROIC",
  "3Y Revenue Growth (per Share)"
]]

df_2014new['year'] = 2014
df_2015new['year'] = 2015
df_2016new['year'] = 2016
df_2017new['year'] = 2017
df_2018new['year'] = 2018

df_all_years = pd.concat(df_2014new, df_2015new, df_2016new, df_2017new, df_2018new)
df_all_years.to_csv('yearlyData.csv', index=False)