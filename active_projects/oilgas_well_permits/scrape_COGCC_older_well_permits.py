import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time

# Getting well permit info from Colorado Oil & Gas Conservation
#    Commission (COGCC) website
url = 'https://cogcc.state.co.us/cogis/FacilitySearch.asp'

# Setting up Selenium webdriver using Chrome browser
path_to_chromedriver = '/home/griggs/chromedriver'
browser = webdriver.Chrome(executable_path = \
                           path_to_chromedriver)

# Opening webpage
browser.get(url)

# Setting constant value for number of Colorado
#   counties
num_colorado_counties = 64

# Initializing empty table to hold well permit table values
table_list = []

# Looping through all Colorado counties to get well permit info for
#    each of them
for county in xrange(1, num_colorado_counties+1):
    facility_type = browser.find_element_by_xpath('/html/body/font/font/blockquote/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[1]/select/option[1]').click()

    county_name = browser.find_element_by_xpath('/html/body/font/font/blockquote/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[3]/font[1]/select/option[' + str(county) + ']').click()

    facility_status =  browser.find_element_by_xpath('/html/body/font/font/blockquote/table/tbody/tr[1]/td[1]/table/tbody/tr[2]/td[5]/select/option[18]').click()

    limit_records = browser.find_element_by_xpath('/html/body/font/font/blockquote/table/tbody/tr[7]/td[2]/select/option[4]').click()

    # Now that all options are set from above, click the search
    #    database button
    browser.find_element_by_id('Button1').click()

    # Setting html to be read into BeautifulSoup
    html = browser.find_element_by_xpath('/html').get_attribute('innerHTML')
    soup = BeautifulSoup(html)

    # Using BeautifulSoup to get table elements (well info)
    table = soup.find_all("table")[1]
    table_body = table.find('tbody')

    # Looping through rows & columns of well info table and appending
    #    table_list
    rows = table_body.find_all('tr')
    for tr in rows:
        cols = tr.find_all('td')
        for td in cols:
            table_list.append(td.text)
            print td.text

    # Sleep for 5 seconds
    time.sleep(5)

    # Have the browser go back to the page to select new search
    #    criteria for the next county
    browser.execute_script("window.history.go(-1)")


# Load all table values to a DataFrame
df = pd.DataFrame({'facility_type' :  table_list[0::8],
                   'facility_id_API' : table_list[1::8],
                   'facility_name_num' : table_list[2::8],
                   'operator_name_num' : table_list[3::8],
                   'status' : table_list[4::8],
                   'field_name_num' : table_list[5::8],
                   'location' : table_list[6::8],
                   'related_facilities' : table_list[7::8]})

# Encode unicode as utf-8
for col in df.columns:
    df[col].str.encode('utf-8')

# Output DataFrame to csv file
df.to_csv('older_well_permits.csv')
