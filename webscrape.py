#---------------------------------------------------------------------#
# File: c:\Adam\Coding\HLStockUpdate\webscrape.py
# Project: c:\Adam\Coding\HLStockUpdate
# Created Date: Sunday, January 23rd 2022, 3:58:35 pm
# Description: 
# Author: Adam O'Neill
# Copyright (c) 2022 Adam O'Neill
# -----
# Last Modified: Wed Dec 21 2022
# Modified By: Adam O'Neill
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
# 2022-12-21	AO	Added functionality for creating backups of the current and previous funds in the case of error
# 2022-12-18	AO	All logic for fetching the information and moving the previous week information is correct
#---------------------------------------------------------------------#
 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os
from datetime import datetime
import shutil


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

def findDifferences():
    def getDataFromFile(fileName):
        fileData = []
        f = open(fileName,"r")
        
        for line in f:
            fileData.append(line.strip("\n"))
        f.close()
        return fileData

    def findDifferences(fund1,fund2):
        diffArr = []
        for index in fund1:
            if index not in fund2:
                diffArr.append(index)
        return diffArr

    # Open each file and get data
    currentFundArr = getDataFromFile("currentFunds.csv")
    previousFundArr = getDataFromFile("previousFunds.csv")
    
    # Find new companies
    newCompaniesArr = findDifferences(currentFundArr,previousFundArr)
    oldCompaniesArr = findDifferences(previousFundArr,currentFundArr)

    return newCompaniesArr, oldCompaniesArr


def initaliseDifferenceCsv():
    f = open("differences.csv","w")

    Headers = "Comany Name, Fund, Key \n"
    f.write(Headers)

    f.close

def appendDifferencesToCsv(newArr,oldArr):
    f = open("differences.csv","a")
    
    # for each item in arr prepare for presenting on csv
    def preparePresent(f,arr,key):
        for comp in arr:
            comAarr = comp.split(",")
            compName = comAarr[0]
            compFund = comAarr[1]
            compstr = compName + "," + compFund + "," + key + "\n"
            f.write(compstr)
        
    preparePresent(f,newArr,"New")
    preparePresent(f,oldArr,"Old")

def saveCsvFiles():

    # Get current date and time
    currentDateAndTime = datetime.now()

    # Create dir containing the files from before the execution
    dir_path = os.path.dirname(os.path.realpath(__file__))  
    dir_path = dir_path + "/csvArch"

    path = os.path.join(dir_path, str(currentDateAndTime))

    os.mkdir(path)

    # Copy Both CSV files into this dir

    shutil.copy("currentFunds.csv",f"/{path}")
    shutil.copy("previousFunds.csv",f"/{path}")


def main():

    # Create Backups of current and previous fund CSV before algorithm
    saveCsvFiles()

    # Delete previous funds file
    finalisePreviousFundCsv()

    #Creates file for current funds
    initaliseCurrentFundsCsv()

    # Create array of fund links
    fundUrls = getUrls()
    for fUrl in fundUrls:
        page_data_list = []

        # Scrape data from the URL and add to main array 
        page_data_list = scrapeTableData(fUrl,page_data_list)

        # Scrape name of the fund
        fundName = scrapeFundName(fUrl)
        
        # Adds the data for the current funds to the Current fund csv file
        try:
            addCurrentFundToCurrentCsv(page_data_list,fundName)
        except:
            pass
    
    # Compare companies from previous weeks
    newCompArr, oldCompArr = findDifferences()

    # Initalises differences csv file
    initaliseDifferenceCsv()

    # Adds the differences data to the differences csv
    appendDifferencesToCsv(newCompArr,oldCompArr)

    print("Successfully Completed")
main()
