import requests
from bs4 import BeautifulSoup
import start
import time
import arrays
import os
from sys import argv
from sys import exit
#############################################################

#TODO: select flights intelligently, based on location on the page 
#      (whether it is Nonstop, or is "Connecting flight", etc) 
#      (will require refactoring the parsing... for now, we can rely on the prompt before searching to weed out indirect flights)

#TODO: make web UI for this, using Flask or Django(?)

#############################################################
def search():
        # Instantiate needed variables for program
        datein = ''
        # Objects needed for start.py
        origin, dest, date_list = [], [], []
        airline, nonstop, lowcost, prompt, expert = '', '', '', '', ''
        # Options to enable expert mode
        try:
                if argv[1] == 'expert':
                        expert = True
                        print("Expert mode enabled.")
        except:
                if input("Run in expert mode? Just hit enter if you don't know what that means. \n") == 'expert':
                        expert = True
                        print("Expert mode enabled.")
                else:
                        expert = False
        
        # Dispkay welcome message unless expert mode is enabled
        while prompt != "no" and prompt != "yes" and expert == False:
                print("Welcome to Multidest (Alpha)! \nRandom things may break, and this is far from the final UI. \n\nLet's get started.\n")
                prompt = input("Would you like to be guided through the process of selecting your origins and destinations? \nThe guided process is more annoying, in my view, and will likely be deprecated. \nIf you still want to use it, type 'yes'. Otherwise, type 'no'. \n")
        # If user wants to be guided through the process, run the old input function to get origin and destination airports
        if prompt == "yes":
                start.airportinput(origin, dest)
        # If user wants to be left alone, run the new input function to get origin and destination airports
        else:
                start.airportinputv2(origin, dest)
        print(origin, dest)

        # Get dates on which search should be conducted from start.py
        start.dates(date_list, datein)

        # Get airline, stopping preference from start.py
        airline, nonstop, lowcost = start.flightoptions(airline, nonstop, lowcost)

        # Get the data from the website
        # If expert == True, start a timer for data collection
        if expert == True:
                start_time = time.time()
        for destination in dest:       
                for origins in origin:
                        for date in date_list:
                # Try to extract each flight price from Google search page and print    
                                try:
                                        # Get the data from the website, using the parameters from start.py, collected above
                                        browser = requests.get(f'https://www.google.com/search?q=fly{airline}+from+{origins}+to+{destination}+on+{date}+one+way{nonstop}')
                                        soup = BeautifulSoup(browser.content, 'html.parser')
                                        #collect all potential airlines from the page, using the class name
                                        airlinefind = soup.find_all(class_='BNeawe s3v9rd AP7Wnd')
                                        #collect all potential prices from the page, using the class name
                                        pricefind = soup.find_all(class_='BNeawe DwrKqd s3v9rd AP7Wnd')
                                        # initialize the price and airline arrays needed for appending later, as well as variables for the price and airline indices
                                        airlines, prices, new=[], [], []
                                        x=0
                                        z=0
                                        #first layer filters out non-airline results, specifically empty strings, long ones (>19), and southwest (doesn't display price)
                                        for air in airlinefind:
                                            if airlinefind[x].string != None and airlinefind[x].string != 'Southwest':
                                                if len(airlinefind[x].string) > 19:
                                                        break                                                   
                                                airlines.append(airlinefind[x].string)                                                    
                                            x+=1
                                        #secondary filter for airlines, to remove entries with spaces which are not airline names (primarily flight times) and non-airline results
                                        for air in airlines:
                                            if " " in air and air not in arrays.airlinelist:
                                                pass
                                            else:
                                                new.append(air)

                                        #make list of prices, removing blank entries
                                        for value in pricefind:
                                            if pricefind[z].string != None: 
                                                prices.append(int(pricefind[z].string.lstrip('$')))    
                                            z+=1

                                        # match prices to airlines
                                        zip_iterator = zip(new, prices)
                                        #sort zip_iterator by lowest price
                                        sorted_zip = sorted(zip_iterator, key=lambda x: x[1])
                                        
                                        #select cheapest flight and airline, adding to zipped list below
                                        #if the user wants to see all airlines (see start.flightoptions above), including low cost ones, this will be displayed
                                        if lowcost == True:                                               
                                                airline1 = str(sorted_zip[0][0])
                                                price = int(sorted_zip[0][1])
                                        #if the user does not want to see low cost airlines, as determined in start.flightoptions, this will engage instead
                                        else: 
                                                n=0   
                                                # iterate through sorted list until a non-low cost airline is found    
                                                while sorted_zip[n][0] in arrays.lowcost:
                                                        #if expert mode is enabled, print the low cost airlines that are being skipped
                                                        if expert == True:
                                                                print(f"Ifed: {sorted_zip[n][0]}")
                                                        n+=1
                                                # if expert mode is enabled, print the non-low cost airline that was selected
                                                if expert == True:
                                                        print(f"Elsed: {sorted_zip[n][0]}")
                                                #assign the non-low cost airline and price to variables
                                                airline1 = str(sorted_zip[n][0])
                                                price = int(sorted_zip[n][1])
                                                                
                                                                
                                                                
                                        # If expert mode is enabled, print all airline and price data                
                                        if expert == True:
                                                print(sorted_zip)
                                        # Print the cheapest flight and price
                                        print(f"Flying from {origins} to {destination} on {airline1} on {date} will cost at least ${price}.")

                                        #write to file, organized by date, csv format (date, origin, dest, airline, price)
                                        with open('flights.csv', 'a') as f:
                                                f.write(f'{date}, {origins}, {destination}, {airline1}, {price}\n')
                                        #close file
                                        f.close()
                                
                                # If it can't get the data, skip the entry and inform the user.
                                except:
                                        # If specific airline is selected, skip the entry and inform the user.
                                        if airline != '':
                                                print(f"Couldn't find a flight from {origins} to {destination} on {date}, flying exclusively on {airline.lstrip('+').capitalize()}. Please try again.")
                                        # If specific airline is not selected, skip the entry and inform the user.
                                        else:
                                                print(f"No such itinerary exists for {origins} to {destination} on {date}. Please try again.")
                                        continue
                        #status update to user
                        print("Searching... Please Wait")
        # Let user know that searching is complete
        print("Search complete.")


        # Parse data collected from Google Search, outputting the average price for each destination at the end of the program.
        start.parser2(expert)
        
        # Print the time it took to run the program, if expert mode is enabled.
        if expert == True:
                print(time.time() - start_time, 's') #type: ignore
        
        # Delete flights.csv, if so desired while in expert mode. Otherwise, automatically delete it.
        if expert == True:
                if os.path.exists('flights.csv'):
                        q = input("Would you like to delete the flights.csv file? If so, press '1'. If not, press any other key. \n")
                        if q == "1":
                                os.remove("flights.csv")
                                print("flights.csv has been deleted.")
                        else:
                                print("flights.csv has not been deleted.")
                else:
                        print("Program Complete. No CSV deletion needed.")
        else:
                if os.path.exists('flights.csv'):
                        os.remove("flights.csv")
                else:
                        exit()




if __name__ == "__main__":
        search()

