
# Import CSV for parsing in parser2()
import csv
# Import modules to calculate average price from csv file in parser2()
from statistics import mean
# Import modules to make date calculations in dates()
from datetime import datetime, timedelta
# Import arrays (local file) for list of airports and list of airlines
import arrays
import streamlit as st #type: ignore



def airportinput(origin, dest):
    #likely to be removed, but keeping for now
    # initialize variables    
    add = "yes"
    add2 = "yes"
    inc = 0
    dest1 = ""
   #ask user for first destination airport; do not stop until valid input is given
    while dest1 not in arrays.airportlist:
        dest1 = input("Give me one airport that you'd like to fly to, using its 3 letter code: ")
        dest1 = dest1.upper()
        #if input is not in airport list, ask again
        if dest1 not in arrays.airportlist:
            print("Try Again.")
            continue 
        #if input is in airport list, add to list of origin airports          
        else:
            if len(dest1) == 3:
                dest.append(dest1)
    #as long as the user is not done adding airports, ask for more
    while add != "no":
        # initialize variables
        origin1 = ""
        dest1 = ""
        #ask user for origin airport; do not stop until valid input is given
        while origin1 not in arrays.airportlist:
            origin1 = input("What is an airport that you'd like to fly from? Enter a 3 letter airport code: ")
            origin1 = origin1.upper()
            #if input is not in airport list, ask again
            if origin1 not in arrays.airportlist:
                print("Try Again.")
        #if input is in airport list, add to list of origin airports
        if origin1 not in origin and len(origin1) == 3:
            origin.append(origin1)
            print (f"{inc+1} city pairings.")
            add = input(f"You would like to fly from {origin[inc]} to {dest[0]}. Would you like to add another origin city? If not, type 'no'. Othwerise, hit enter. \n")
            inc+=1  
        #if input is in airport list, but already in list of origin airports, ask again       
        elif origin1 in origin: 
            print("You have already entered this airport.")
            add = input(f"You would like to fly from {origin1} to {dest[0]}. Would you like to add another origin city? If not, type 'no'. Othwerise, hit enter. \n")
        #if input is invalid for any other reason, ask again
        else:
            print("Try Again.")
            add = input(f"You would like to fly from {origin1} to {dest[0]}. Would you like to add another origin city? If not, type 'no'. Othwerise, hit enter. \n")
        
    
    while add2 != "no":
        dest2 = ""
        while dest2 not in arrays.airportlist:
            dest2 = input("Would you like to add more airports that you'd like to fly to? If yes, type in an airport code. Otherwise, type no: \n")
            add2 = dest2
            if dest2 == "no":
                break
            elif dest2 in origin:
                
                q = ''
                while q != 'y' and q != 'n':
                    q = input(f"You have entered {dest2} as an origin airport. Would you like to add it as a destination airport anyways? If so, type 'y'. Otherwise, type 'n'. \n")
                if q == 'y':
                    dest.append(dest2)
            else:
                dest2 = dest2.upper()
                if dest2 not in arrays.airportlist:
                    print("Try Again.")
                dest.append(dest2)
       
    
    
    
    return origin, dest


    '''else:    
        print(origin, dest)'''

def airportinputv2(origin, dest):
    #while no origin airports have been added, ask for airports
    while len(origin) == 0:
        goat = input("What airports would you like to leave from? Input the 3 letter code for each, seperated with a comma. \n")
        # format list of airports from user input
        goat = goat.upper().replace(" ", "").split(",")
        #check if each airport is in the list of airports
        for i in goat:
            if i in arrays.airportlist and i not in origin:
                origin.append(i)
            # if there are any issues, display errors
            else:
                #if there are double inputs, display error
                if i in origin:
                    print(f"You have entered {i} multiple times. Skipping extra occurances.")
                # other general errors
                else:
                    print(f"{i} is not a valid airport code. Not added to list.")
                pass
        # tell user which origin airports have been added
        print(f"Your origin airports are: {origin}")
    #while no destination airports have been added, ask for airports
    while len(dest) == 0:
        #ask user for destination airports
        goat2 = input("What airports would you like to fly to? Input the 3 letter code for each, seperated with a comma. \n")
        # format list of airports from user input
        goat2 = goat2.upper().replace(" ", "").split(",")
        #check if each airport is in the list of airports
        for i in goat2:
            if i in arrays.airportlist and i not in origin and i not in dest:
                dest.append(i)
            # if there are any issues, display errors
            else:
                #if input is in origin airports, display error, and ask user if they want to add it to destination airports
                if i in origin:
                    q = ''
                    while q != 'y' and q != 'n':
                        q = input(f"You have entered {i} as an origin airport. Would you like to add it as a destination airport anyways? If so, type 'y'. Otherwise, type 'n'. \n")
                    if q == 'y':
                        dest.append(i)
                    else:
                        print(f"{i} is already in your list of airport parings. Not added to list.")
                        pass
                # if there are general errors, display error        
                else:
                    print(f"{i} is not a valid airport code. Not added to list.")
                pass
        
       
    return origin, dest

def dates(date_list, datein):
    datein= ''
    #while date not in correct format, ask for date
    while datein == '':
        try:
            #ask user for date input in mm-dd-yyyy format
            date = input("What date would you like to fly on? Please use MM-DD-YY Formatting. \n" )
            datein = date
            #convert date from mm-dd-yyyy format to yyyy-mm-dd format
            date = datetime.strptime(date, '%m-%d-%y').strftime('%Y-%m-%d') #convert date from mm-dd-yyyy format to yyyy-mm-dd format
            ranges = input("Would you like a week of data, or a month? A month will take much longer. \nPress 1 for a week, 2 for a month. \n")
            if ranges not in ['1', '2']:
                print("Invalid Input. Try Again.")
                ranges = input("Would you like a week of data, or a month? A month will take much longer. \nPress 1 for a week, 2 for a month. \n")
            if ranges == '1':
                for i in range(-3, 4):
                    date_list.append((datetime.strptime(date, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')) #convert date from mm-dd-yyyy format to yyyy-mm-dd format
            #create a list of days 15 days before and 15 days after:
            if ranges == '2':
                for i in range(-15, 15):    #create a list of days 15 days before and 15 days after:
                    date_list.append((datetime.strptime(date, '%Y-%m-%d') + timedelta(days=i)).strftime('%Y-%m-%d')) #convert date from mm-dd-yyyy format to yyyy-mm-dd format
            return date_list, datein 
        except:
            print("Invalid Input. Try Again.")
            datein = ''

def flightoptions(airline, nonstop, lowcost):
        print("\nLet's go through a few options to narrow down your search! \n")
        # Ask for airline input; allows option to leave blank
        airlinein = 'empty'
        while airlinein.casefold() not in {air.casefold() for air in arrays.airlinelist} and not airlinein =='':
            airlinein = input("Is there any specific airline that you'd like to search? If not, leave this blank. \n")
            if airlinein == "":
                    airline = f''
                    print("Got it! We'll search all airlines. \n")
            else:
                    airline = f'+{airlinein}'
                    print(f"Got it! We'll only search for {airlinein.capitalize()}. \n")
        
        # Ask if they only want nonstop flights
        nonstopin = input("\nDo you only want nonstop flights? \nOtherwise, I will average the cheapest cost, regardless of connections. \n\nIf you only want nonstop flights, input '1'. If not, leave this blank. \n")
        if nonstopin == "1":
                nonstop = f'+nonstop'
                print("Sure thing! We'll only search for nonstop flights. \n")
        else:
                nonstop = f''
                print("Sure thing! We'll search for all flights, including those with with connections. \n")


        # Ask if they only want low cost flights
        while lowcost not in ['1', '2']:
            if airlinein != "":
                lowcost == True
                break
            else:
                lowcost = input("\nWould you like low cost airlines to be included in the results? \nIf you do want them included, input '1'. If not, input '2'. \n")
                if lowcost == "1":
                        lowcost = True
                        print("Good idea! We'll include low cost airlines. \n")
                        break
                elif lowcost == "2":
                        lowcost = False
                        print("Agreed! We'll only search for major airlines. \n")
                        break
                else:
                    print("Try Again. ")

        return airline, nonstop, lowcost
      
def parser2(expert):
    #taking data from fights.csv, make a dict of dicts {dest: {date: price}}
    #open flights.csv
    try:   
        with open('flights.csv', 'r') as f:
            #get average price for each destination
            reader = csv.reader(f)
            destlist = []
            pricelist = []
            datelist=[]
            originlist = []
            for row in reader:
                destlist.append(row[1].lstrip())
                datelist.append(row[0].lstrip())
                originlist.append(row[2].lstrip())
                #convert price to int
                pricelist.append(int(row[4].lstrip(' $')))
            f.close() #close file


        #make a dict of dicts {origin{unique dest: {date: price}}}
        dest_dict = {}
        for i in range(len(pricelist)):
            if originlist[i] not in dest_dict:
                dest_dict[originlist[i]] = {}
            if destlist[i] not in dest_dict[originlist[i]]:
                dest_dict[originlist[i]][destlist[i]] = {}
            dest_dict[originlist[i]][destlist[i]][datelist[i]] = pricelist[i]
        if expert == True:
            print(dest_dict)

        #get average price for each destination
        for origin in dest_dict:
            for destination in dest_dict[origin]:
                print(f"The average cost of flying from {destination} to {origin} is ${mean(dest_dict[origin][destination].values()):.2f}.")
                st.write(f"The average cost of flying from {destination} to {origin} is ${mean(dest_dict[origin][destination].values()):.2f}.")
    except:
        print("No data to parse. Please run the program again.")
        st.experimental_rerun()
        st.error("No data to parse. Please run the program again.")


