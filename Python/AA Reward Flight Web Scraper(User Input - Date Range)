#This program will web scrape American Airline's Reward Flight page based on Origin, Destination
#flight date(range) provided by the user and display the results in a dataframe view as well as save the data
#to a csv file

#importing the necessary modules
from time import sleep
from random import randint
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from IPython.display import display, HTML
from datetime import date, timedelta


appended_data = []

#Getting user input
#Origin, destination and date variables(run time will depend on date range, the longer the range
#the longer the run time) for the flight details we want

#This while loop asks for origin airportcode and checks if it is 3 letters
while True:
    ori = input('Please enter your desired departure airport code(3 Letters): ')
    if len(ori) == 3 and ori.isalpha():
        break
    else:
        print('You did not enter a 3 letter airport code, please try again.')

#This while loop asks for destination airportcode and checks if it is 3 letters        
while True:        
    des = input('Please enter your desired arrival airport code(3 Letters): ')
    if len(des) == 3 and ori.isalpha():
        break
    else:
        print('You did not enter a 3 letter airport code, please try again.')


#Please use flight dates within a year otherwise there could be an error due to unavailable flight data
year = int(input('Please enter your earliest flight date year: '))

#Creating a dictionary to change format of the day/month since 
#it needs to be in two digit format otherwise webpage will not load properly
digit_converter = {'1':'01', '2':'02', '3':'03', '4':'04', '5':'05', '6':'06','7':'07', '8':'08','9':'09'}

#This while loop checks if it is a valid month
m = True
while m:
    try:
        month = int(input('Please enter your earliest flight month: '))
        if month>0 and month <=12:
            m = False
        else:
            print('You did not enter a valid month, please try again.')
    except:
        print('You did not enter a valid month, please try again.')


#This while loop checks if it is a valid day
#Creating a list for month with 31 days
longer_month = [1,3, 5,7,8,10,12]
#Creating list for month with 30 days
shorter_month = [4,6,9,11]
d = True
while d:
    try:
        day = int(input('Please enter your earilest flight day: '))
        if month in longer_month and day >0 and day <=31:
            d = False
        elif month in shorter_month and day >0 and day <=30:
            d = False
        elif month == 2 and day >0 and day <=28:
            d = False
        else:
            print('You did not enter a valid day, please try again.')
    except:
        print('You did not enter a valid day, please try again.')


l_year = int(input('Please enter your latest flight date year: '))

#Creating a dictionary to change format of the day/month since 
#it needs to be in two digit format otherwise webpage will not load properly
digit_converter = {'1':'01', '2':'02', '3':'03', '4':'04', '5':'05', '6':'06','7':'07', '8':'08','9':'09'}

#This while loop checks if it is a valid month and if it is after earliest month
l_m = True
while l_m:
    try:
        l_month = int(input('Please enter your latest flight month: '))
        if l_month>=month and l_month <=12:
            l_m = False
        else:
            print('You did not enter a valid month, please try again.')
    except:
        print('You did not enter a valid month, please try again.')


#This while loop checks if it is a valid day
l_d = True
while l_d:
    try:
        l_day = int(input('Please enter your latest flight day: '))
        if l_month in longer_month and l_day >0 and l_day <=31:
            l_d = False
        elif l_month in shorter_month and l_day >0 and l_day <=30:
            l_d = False
        elif l_month == 2 and l_day >0 and l_day <=28:
            l_d = False
        else:
            print('You did not enter a valid day, please try again.')
    except:
        print('You did not enter a valid day, please try again.')

#This is getting the date range between earliest flight date and latest flight date
start_date = date(year,month, day) 
end_date = date(l_year,l_month,l_day)
# returns timedelta
delta = end_date - start_date
#loops to get all the dates
for i in range(delta.days + 1):
    dates = start_date + timedelta(days=i)
    year = str(dates.year)
    month = dates.month
    day = dates.day

    #Converting month/day into two digit string format
    if str(month) in digit_converter:
        month = digit_converter[str(month)]
    else:
        month = str(month)
    if str(day) in digit_converter:
        day = digit_converter[str(day)]
    else:
        day = str(day)


     #Creating web browser using Selenium
    driver = webdriver.Chrome()

    #Setting URL for webpage we want to webscrape
    aa = 'https://www.aa.com/booking/search?locale=en_US&pax=1&adult=1&type=OneWay&searchType=Award&cabin=&carriers=ALL&slices=%5B%7B%22orig%22:%22'+ori+'%22,%22origNearby%22:false,%22dest%22:%22'+des+'%22,%22destNearby%22:false,%22date%22:%22'+year+'-'+month+'-'+day+'%22%7D%5D'

    #Getting the webpage
    driver.get(aa)

    #Sleeping for random time between 5 and 8 seconds so webpage can load
    sleep(randint(5,8))


    #Getting flight details through xpath looking for div class of all the reward flights
    flight_rows = driver.find_elements(By.XPATH, '//div[@class="grid-x grid-padding-x ng-star-inserted"]')

    #Creating list variables of the information we want to pull from
    #the website that we will be able to insert into a pandas dataframe
    mileage = []
    tax_amount = []
    flight_class = []
    flight_duration = []
    dep = []
    arr = []
    dep_time = []
    arr_time = []

    #Loop that extracts the flight information we want from all the flights
    for WebElement in flight_rows:
        #This gives the exact HTML content of the webelement
        elementHTML = WebElement.get_attribute('outerHTML')

        #Now we can parse with beautifulsoup to extract the info that we want
        elementSoup = BeautifulSoup(elementHTML, 'html.parser')

        #Finding flight duration
        flight= elementSoup.find("div", {"class" : "duration"})
        #Finding departure and arrival cities
        departure = elementSoup.find("div", {"class" : "cell large-3 origin"})
        arrival = elementSoup.find("div", {"class": "cell large-3 destination"})

        #Finding the blocks containing flight prices
        temp_price = elementSoup.find_all("div", {"class": "cell auto pad-left-xxs pad-right-xxs ng-star-inserted"})

        #There are multiple flight prices between different fare classes so
        #using a for loop to iterate through all prices of the same flight
        for x in temp_price:
            #This finds the mileage costs, tax costs and fare class of the flight
            miles = x.find("span", {"class" : "per-pax-amount ng-star-inserted"})
            taxes = x.find("div", {"class" : "per-pax-addon ng-star-inserted"})
            carriage = x.find("span", {"class" : "hidden-accessible hidden-product-type"})

            #Need this if statement since there are fares with None type which cause errors when appending the data
            if miles != None and taxes != None:
                #Appending all the necessary data to the corresponding lists created above
                mileage.append(miles.text)
                tax_amount.append(taxes.text)
                flight_class.append(carriage.text)
                flight_duration.append(flight.text)
                dep.append(departure.find("div", {"class": "city-code"}).text)
                arr.append(arrival.find("div", {"class": "city-code"}).text)
                dep_time.append(departure.find("div", {"class": "flt-times"}).text)
                arr_time.append(arrival.find("div", {"class": "flt-times"}).text)
            else:
                continue
    #Changing from string to float to display as 42500.0 instead of 42.5K
    #which causes sorting errors when sorting through string
    new_miles = [float(sub[:-1])*1000 for sub in mileage]    

    dict = {}
    #This creates a dictionary with the name as key and the lists as values so
    #we can import these into a pandas dataframe
    dict = {'Origin' : dep, 'Destination' : arr, 'Departure_Time' : dep_time,
        'Arrival_Time' : arr_time, "Duration" : flight_duration,
       'Class' : flight_class, 'Miles' : new_miles, 'Tax' : tax_amount}

    #Creating the pandas dataframe from the dictionary created before
    df = pd.DataFrame(dict)

    #Creating a Date column
    df['Date'] = month+'/'+day
    df.set_index('Date', inplace=True)

    #Changing the Miles column from float to int to drop decimal points when displaying the values
    df['Miles'] = df['Miles'].astype(int)

    #Changing the Tax amount column from string to float to remove symbols
    df['Tax'] = df['Tax'].str.replace('+ $','', regex=False).astype(float)

    appended_data.append(df)

#Sorting the df by Miles and flight time ascending
appended_data = pd.concat(appended_data)

#Sorting the df by Miles and flight time ascending
appended_data = appended_data.sort_values(['Miles','Duration'], ascending=True)

#Saves the data to a csv file named Reward Flight
appended_data.to_csv('Reward Flight.csv')

#Displays the data in a nice view
display(HTML(appended_data.to_html()))
