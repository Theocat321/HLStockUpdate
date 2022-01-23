#---------------------------------------------------------------------#
# File: c:\Adam\Coding\HLStockUpdate\webscrape.py
# Project: c:\Adam\Coding\HLStockUpdate
# Created Date: Sunday, January 23rd 2022, 3:58:35 pm
# Description: 
# Author: Adam O'Neill
# Copyright (c) 2022 Adam O'Neill
# -----
# Last Modified: Sun Jan 23 2022
# Modified By: Adam O'Neill
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	---------------------------------------------------------
#---------------------------------------------------------------------#
 
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

def getUrls():
    fundUrls = []

    # Opens Funds text file
    f = open("Funds.txt","r")

    #loops through every line
    for line in f:

        #removes the new line from the end of the line
        line.strip("\n")
        fundUrls.append(line)
    
    f.close()
    
    return fundUrls

def webScrape (my_url):
    # Opens connection to page
    uClient = uReq(my_url)

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

def convertCsv():
    pass

def main():
    fundUrls = getUrls
    currentUrl = "https://www.hl.co.uk/funds/fund-discounts,-prices--and--factsheets/search-results/j/jpm-uk-smaller-companies-class-c-accumulation/fund-analysis"
    
    # Scrape data from the URL and add to main array
    webScrape(currentUrl)
    print(page_data_list)

page_data_list = []
main()