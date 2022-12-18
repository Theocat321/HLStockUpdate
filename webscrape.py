#---------------------------------------------------------------------#
# File: c:\Adam\Coding\HLStockUpdate\webscrape.py
# Project: c:\Adam\Coding\HLStockUpdate
# Created Date: Sunday, January 23rd 2022, 3:58:35 pm
# Description: 
# Author: Adam O'Neill
# Copyright (c) 2022 Adam O'Neill
# -----
# Last Modified: Sun Dec 18 2022
# Modified By: Adam O'Neill
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
#---------------------------------------------------------------------#
 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os

from matplotlib.pyplot import pause

def getUrls():
    fundUrlsList = []

    # Opens Funds text file
    f = open("Funds.txt","r")

    #loops through every line
    for line in f:

        #removes the new line from the end of the line
        line.strip("\n")
        fundUrlsList.append(line)
    
    f.close()
    return fundUrlsList

def scrapeTableData (fund_url,page_data_list):
    # Opens connection to page
    uClient = uReq(fund_url)

    # Page contents into variable
    page_html = uClient.read()

    # Closes connection
    uClient.close()

    # html parsing into soup
    page_soup = soup(page_html, "html.parser")


    # grab tables, We want second table [1] as this contains info we want
    info_tables = page_soup.findAll("table", {"class":"factsheet-table"})
    info_table = info_tables[1]

    # grabs table body
    info_table_contents = info_table.tbody

    # Creates list of all the table rows
    table_rows = info_table_contents.findAll("tr")

    # Loops through all the rows
    for row in table_rows:

        # Creates list of all the table d within the current row
        table_d = row.findAll("td")


        # Creates temp list for holding each row data to be put into 2d array
        temp_row_list = []

        # Loops through each <td>
        for d in table_d:
            current_text = d.text
            temp_row_list.append(current_text)
        
        # Appends the temp_row_list to page data list
        page_data_list.append(temp_row_list)
    
    return page_data_list

def scrapeFundName(fund_url):

    # Opens connection
    uClient = uReq(fund_url)

    # Saves data as variable
    page_html = uClient.read()

    uClient.close()

    # Converts into soup data type
    page_soup = soup(page_html, "html.parser")

    fundName = page_soup.title.text
    
    return fundName

def finalisePreviousFundCsv():

    # Deletes the previous fund file
    try:
        os.remove("previousFunds.csv")
    except:
        pass
    
    # Renames currentFund.csv to previous fund
    os.rename("currentFunds.csv","previousFunds.csv")

def initaliseCurrentFundsCsv():
    f = open("currentFunds.csv","w")

    #Creates Header for the csv file
    Headers = "Company Name, Fund \n"
    f.write(Headers)
    f.close()

def addCurrentFundToCurrentCsv(fundList, fundName): # Adds current fund data to the Current Fund csv file
    f = open("currentFunds.csv","a")
     
    for array in fundList:
        wline = array[1] + "," + fundName + "\n"
        f.write(wline)
         
    f.close()

def compareCurrentPreviousCsv():
    
    # Initalises array to show differences in the files
    differencesList = []

    # Opens both files and converts to a list
    currentCsv = open("currentFunds.csv","r")
    previousCsv = open("previousFunds.csv")
    currentList = currentCsv.readlines()
    previousList = previousCsv.readlines()
    currentCsv.close()
    previousCsv.close()

    # Loop the length of list 
    for x in range(len(currentList)):
        
        # Compare which are different
        if currentList[x] != previousList[x]:
            differencesList.append([currentList[x].strip("\n")+","+previousList[x].strip("\n")])
        
    # returns fifferences
    return differencesList

def initaliseDifferenceCsv():
    f = open("differences.csv","w")

    Headers = "New Company Name, Previous Company Name, Fund \n"
    f.write(Headers)

    f.close

def appendDifferencesToCsv(differencesList):
    f = open("differences.csv","a")

    for list in differencesList:
        element = list[0].split(",")
        wline = element[0] + "," + element[2] + "," + element[1] + "\n"
        f.write(wline)
    
    f.close()


def main():

    finalisePreviousFundCsv()
    initaliseCurrentFundsCsv()
    fundUrls = getUrls()
    for fUrl in fundUrls:
        page_data_list = []

        # Scrape data from the URL and add to main array 
        page_data_list = scrapeTableData(fUrl,page_data_list)

        # Scrape name of the fund
        fundName = scrapeFundName(fUrl)
        
        # Adds the data for the current funds to the Current fund csv file
        addCurrentFundToCurrentCsv(page_data_list,fundName)
    
    # Comparing the data
    # Compares current and previous csv file to find differences and puts into 2d array
    differencesList = compareCurrentPreviousCsv()

    # Initalises differences csv file
    initaliseDifferenceCsv()

    # Adds the differences data to the differences csv
    appendDifferencesToCsv(differencesList)



main()