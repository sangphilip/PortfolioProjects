#importing the necessary modules
from time import sleep
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import date, timedelta
from IPython.display import display, HTML

#This function validates that the airport code is entered as three letters
def validate_airport_code(code):
    return len(code) == 3 and code.isalpha()

#This fuction validates that the month is entered correctly
def validate_month(month):
    return int(month) > 0 and int(month) <= 12

#This function validates the correct amount of days in each month
def validate_day(month, day,year):
    month = int(month)
    day = int(day)
    if month == 2:
        #This if statement accounts for leap years
        if year % 4 == 0 and (year % 100 !=0 or year % 400 == 0):
            return day >0 and day <=29
        else:
            return day > 0 and day <= 28
    elif month in [4, 6, 9, 11]:
        return day > 0 and day <= 30
    else:
        return day > 0 and day <= 31

#This function gets user input and validates according to the 
#validator function chosen to make sure user input is valid
def get_user_input(prompt, validator, *args):
    while True:
        user_input = input(prompt)
        if validator(user_input, *args):
            return user_input
        else:
            print('Invalid input, please try again.')

#This function formats the date accordingly so that there are always 2 numbers in month and day for necessary url format
def format_date(year, month, day):
    return f"{year}-{month:02d}-{day:02d}"

#This function opens up the webpage using custom url given the user input and web scrapes the necessary information
#Appending all the necessary information into a list first then a dictionary and finally pandas dataframe
def scrape_flight_data(ori, des, start_date, end_date):
    date = []
    mileage = []
    tax_amount = []
    flight_class = []
    flight_duration = []
    dep = []
    arr = []
    dep_time = []
    arr_time = []
    with webdriver.Chrome() as driver:
        delta = end_date - start_date
        for i in range(delta.days + 1):
            current_date = start_date + timedelta(days=i)
            formatted_date = format_date(current_date.year, current_date.month, current_date.day)
            url = f'https://www.aa.com/booking/search?locale=en_US&pax=1&adult=1&type=OneWay&searchType=Award&cabin=&carriers=ALL&slices=%5B%7B%22orig%22:%22{ori}%22,%22origNearby%22:false,%22dest%22:%22{des}%22,%22destNearby%22:false,%22date%22:%22{formatted_date}%22%7D%5D'
            driver.get(url)
            sleep(randint(5, 8))

            flight_rows = driver.find_elements(By.XPATH, '//div[@class="grid-x grid-padding-x ng-star-inserted"]')

            for WebElement in flight_rows:
                elementHTML = WebElement.get_attribute('outerHTML')
                elementSoup = BeautifulSoup(elementHTML, 'html.parser')
                
                #Finding flight duration
                flight= elementSoup.find("div", {"class" : "duration"}).text.strip()
                #Finding departure and arrival cities
                departure = elementSoup.find("div", {"class" : "cell large-3 origin"}).find("div", {"class" : "city-code"}).text.strip()
                arrival = elementSoup.find("div", {"class": "cell large-3 destination"}).find("div", {"class" : "city-code"}).text.strip()
                prices = elementSoup.find_all("div", {"class": "cell auto pad-left-xxs pad-right-xxs ng-star-inserted"})
                
                #For loop that loops through all different fare prices in a flight
                for x in prices:
                    miles = x.find("span", {"class" : "per-pax-amount ng-star-inserted"})
                    taxes = x.find("div", {"class" : "per-pax-addon ng-star-inserted"})
                    carriage = x.find("span", {"class" : "hidden-accessible hidden-product-type"})

                    #Some fares aren't available so need this if statement otherwise None type data will cause errors
                    if miles and taxes:
                        date.append(formatted_date)
                        mileage.append(miles.text)
                        tax_amount.append(taxes.text.replace("+ $", ""))
                        flight_class.append(carriage.text)
                        flight_duration.append(flight)
                        dep.append(departure)
                        arr.append(arrival)
                        dep_time.append(elementSoup.find("div", {"class" : "cell large-3 origin"}).find("div", {"class": "flt-times"}).text)
                        arr_time.append(elementSoup.find("div", {"class": "cell large-3 destination"}).find("div", {"class": "flt-times"}).text)
                    else:
                        continue
    
    
    #This removes the K from the end of Miles and changes it to thousands when displaying as a number
    new_miles = [float(sub[:-1])*1000 for sub in mileage]    

    #This creates a dictionary with the name as key and the lists as values so
    #we can import these into a pandas dataframe
    dict = {'Date' : date, 'Origin' : dep, 'Destination' : arr, 'Departure_Time' : dep_time,
    'Arrival_Time' : arr_time, "Duration" : flight_duration,
    'Class' : flight_class, 'Miles' : new_miles, 'Tax' : tax_amount}

    #Some formatting to display data better
    df = pd.DataFrame(dict)
    df['Miles'] = df['Miles'].astype(int)
    df.set_index('Date', inplace=True)
    
    return df

#This is the main function that calls all the functions listed before to run the entire code.
def main():
    ori = get_user_input('Please enter your desired departure airport code (3 Letters): ', validate_airport_code)
    des = get_user_input('Please enter your desired arrival airport code (3 Letters): ', validate_airport_code)
    year = int(input('Please enter your earliest flight date year: '))
    month = int(get_user_input('Please enter your earliest flight month: ', validate_month))
    day = int(get_user_input('Please enter your earliest flight day: ', validate_day, month, year))

    l_year = int(input('Please enter your latest flight date year: '))
    l_month = int(get_user_input('Please enter your latest flight month: ', validate_month))
    l_day = int(get_user_input('Please enter your latest flight day: ', validate_day, l_month, l_year))

    start_date = date(year, month, day)
    end_date = date(l_year, l_month, l_day)

    appended_data = scrape_flight_data(ori, des, start_date, end_date)
    
    if not appended_data.empty:
        appended_data = appended_data.sort_values(['Miles', 'Duration'], ascending=True)
        #appended_data.to_csv('Reward Flight.csv', index=False)
        display(HTML(appended_data.to_html()))
    else:
        print("No flight data found.")
