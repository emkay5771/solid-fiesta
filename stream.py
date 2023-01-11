import streamlit as st #type: ignore
import arrays
import requests
from bs4 import BeautifulSoup
import start
import os
from datetime import timedelta
import datetime
from datetime import date
import pandas as pd
import plotly.express as px #type: ignore
import plotly.graph_objects as go #type: ignore


 #TODO: Smartly determine if the user wants to include low cost airlines

st.set_page_config(page_title="MultiDest", page_icon="🛫", layout="wide", initial_sidebar_state="collapsed")

def bugcheck():
    # If specific airline is selected, skip the entry and inform the user.
                                            if soup == '':
                                                st.write("No Soup :shrug:")
                                            if airlinefind == '':
                                                st.write("No Airlinefind :shrug:")
                                            else:
                                                st.write(f"Found AirlineFind :thumbsup:")
                                            if pricefind == '':
                                                st.write("No Pricefind :shrug:")
                                            else:
                                                st.write(f"Found Pricefind :thumbsup:")
                                            if len(airlines) == 0:
                                                st.write("No Airlines parsed list :shrug:")
                                            else:
                                                st.write(f"{airlines}")
                                            if len(prices) == 0:
                                                st.write("No Prices parsed list :shrug:")
                                            else:
                                                st.write(f"{prices}")
                                            if len(new) == 0:
                                                st.write("No New parsed list :shrug:")
                                            else:
                                                st.write(f"{new}")

def lowcosts():
    if airlinein != "":
        lowcost == True
                
    else:
        if airlinein in arrays.lowcost:
                lowcost == True
                
        elif lowcost == True:
                print("Good idea! We'll include low cost airlines. \n")
                lowcost == True
                
        else:
                lowcost == False
                print("Agreed! We'll only search for major airlines. \n")

def date_lists(date):	
        if ranges == 'Day':
                date_list.append(date)
        if ranges == 'Week':
                for i in range(-3, 4):
                        date_list.append((date + timedelta(days=i)).strftime('%Y-%m-%d')) #convert date from mm-dd-yyyy format to yyyy-mm-dd format
        #create a list of days 15 days before and 15 days after:
        if ranges == 'Month':
                for i in range(-15, 15):    #create a list of days 15 days before and 15 days after:
                        date_list.append((date + timedelta(days=i)).strftime('%Y-%m-%d')) #convert date from mm-dd-yyyy format to yyyy-mm-dd format
        print("GREAT SUCCESS!")
        for i in range(len(date_list)):
                print(date_list[i])
        return date_list

#@st.cache(allow_output_mutation=True, suppress_st_warning=True)
origin, dest, date_list = [], [], []
airline, nonstop, lowcost= '', '', ''
expert = False

with st.form(key='my_form', clear_on_submit=False):
    st.title("MULTIDEST (beta) :airplane:")
    col1, col2 = st.columns(2)
    with col1:
        origin = st.multiselect('Where were you planning on leaving from? 🌎', arrays.airportlist)
    with col2:
        dest = st.multiselect('Where would you like to go? 🌎', arrays.airportlist) 
    date = st.date_input('What date would you like to travel?', min_value=datetime.date.today())
    ranges = st.radio('How many days should we search?', ["Day", "Week", "Month"], help='Note that Week is +-3 days, and Month is +-15.')
    airlinein = st.selectbox('If you would like to limit your search to 1 airline, select it here.', arrays.airlinelistoptions, index = 0)
    nonstops = st.checkbox('Nonstop Flights Only')
    st.write('Note: If you selected a low cost airline above, make sure to leave this checked to prevent bugs.')
    lowcost = st.checkbox('Include Low Cost Airlines', value=True, help="This will include airlines like Spirit, Frontier, and Allegiant. If you select a specific airline, this will be ignored.")
    collectall = st.checkbox('Collect all data?', value=True, help="Leaving this enabled will have the program collect all flights available, instead of just the cheapest one. Will affect averages, as well as other things, I'd assume :shrug:.")
    submit = st.form_submit_button('Begin Search! :arrow_forward:', type="primary")
    if submit:
        date_lists(date)
        print(date_list)
        if os.path.exists('flights.csv'):
                os.remove("flights.csv")
        if os.path.exists('lowest.csv'):
                os.remove("lowest.csv")

        # Ask for airline input; allows option to leave blank         
        if airlinein == "":
                airline = f''
                print("Got it! We'll search all airlines. \n")
        else:
                airline = f'+{airlinein}'
                print(f"Got it! We'll only search for {airlinein.capitalize()}. \n")
        
        # Ask if they only want nonstop flights
        if nonstops == True:
                nonstop = f'+nonstop'
                print("Sure thing! We'll only search for nonstop flights. \n")
        else:
                nonstop = f''
                print("Sure thing! We'll search for all flights, including those with with connections. \n")
        placeholder = st.empty()
        placeholder2 = st.text('')
        placeholder3 = st.write('')

        if submit:               
            for destination in dest:       
                    for origins in origin:
                        with placeholder:
                            with st.spinner(f"Searching flights from {origins} to {destination}..."): 
                                for date in date_list:
                    # Try to extract each flight price from Google search page and print
                                    
                                    try:
                                            # Get the data from the website, using the parameters from start.py, collected above 
                                            localheaders={'User-Agent': 'python-requests/2.28.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
                                            otherheader={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
                                            browser = requests.get(f'https://www.google.com/search?q=fly{airline}+from+{origins}+to+{destination}+on+{date}+one+way{nonstop}', headers=localheaders)
                                            soup = BeautifulSoup(browser.content, 'html.parser') 
                                            #collect all potential airlines from the page, using the class name
                                            airlinefind = soup.find_all(class_='BNeawe s3v9rd AP7Wnd')
                                            #collect all potential prices from the page, using the class name
                                            pricefind = soup.find_all(class_='BNeawe DwrKqd s3v9rd AP7Wnd')
                                            # initialize the price and airline arrays needed for appending later, as well as variables for the price and airline indices
                                            airlines, prices, new=[], [], []
                                            x=0
                                            z=0
                                            y=0
                                            #first layer filters out non-airline results, specifically empty strings, long ones (>19), and southwest (doesn't display price)
                                            for air in airlinefind:
                                                if airlinefind[x].string != None and airlinefind[x].string != 'Southwest':
                                                    if len(airlinefind[x].string) > 19:
                                                        #st.write(f"Broke at 112; {airlinefind[x].string}, position {x} :thumbsdown:")
                                                        break                                                   
                                                    airlines.append(airlinefind[x].string)
                                                    #st.write(f"{airlinefind[x].string} :thumbsup:")                                                    
                                                x+=1
                                                
                                            #secondary filter for airlines, to remove entries with spaces which are not airline names (primarily flight times) and non-airline results
                                            for air in airlines:
                                                if " " in air and air not in arrays.airlinelist:
                                                    #st.write(f"{air} 😠")
                                                    pass
                                                else:
                                                    new.append(air)
                                                    #st.write(f"{air} :airplane:")

                                            #make list of prices, removing blank entries
                                            for value in pricefind:
                                                if pricefind[z].string != None: 
                                                    prices.append(int(pricefind[z].string.lstrip('$')))
                                                    #st.write(f"Price appended 💵")    
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
                                                                    
                                            # Print the cheapest flight and price
                                            print(f"Flying from {origins} to {destination} on {airline1} on {date} will cost at least ${price}.")
                                            with placeholder2:
                                                st.write(f"Flying from {origins} to {destination} on {airline1} on {date} will cost at least ${price}.")

                                            #write to file, organized by date, csv format (date, origin, dest, airline, price)
                                            with open('flights.csv', 'a') as f:
                                                if collectall==True and lowcost==True:
                                                    for n in range(len(sorted_zip)):
                                                        airline1 = str(sorted_zip[n][0])
                                                        price = int(sorted_zip[n][1])
                                                        f.write(f'{date}, {origins}, {destination}, {airline1}, {price}\n')
                                                elif collectall==True and lowcost==False:
                                                    for n in range(len(sorted_zip)):
                                                        if sorted_zip[n][0] in arrays.lowcost:
                                                            n+=1
                                                            pass
                                                        else:
                                                            airline1 = str(sorted_zip[n][0])
                                                            price = int(sorted_zip[n][1])
                                                            f.write(f'{date}, {origins}, {destination}, {airline1}, {price}\n')
                                                else:
                                                    f.write(f'{date}, {origins}, {destination}, {airline1}, {price}\n')
                                            #close file
                                            f.close()
                                            #collect lowest price for each date
                                            with open('lowest.csv', 'a') as f:
                                                airline1 = str(sorted_zip[0][0])
                                                price = int(sorted_zip[0][1])
                                                f.write(f'{date}, {origins}, {destination}, {airline1}, {price}\n')
                                            f.close()
    
                                    # If it can't get the data, skip the entry and inform the user.
                                    except:   
                                            if airline != '':
                                                    print(f"Couldn't find a flight from {origins} to {destination} on {date}, flying exclusively on {airline.lstrip('+').capitalize()}. Please try again.")
                                                    with placeholder2:
                                                        st.write(f"Couldn't find a flight from {origins} to {destination} on {date}, flying exclusively on {airline.lstrip('+').capitalize()}. Please try again.")
                                            # If specific airline is not selected, skip the entry and inform the user.
                                            else:
                                                    print(f"No such itinerary exists for {origins} to {destination} on {date}. Please try again.")
                                                    with placeholder2:
                                                        st.write(f"No such itinerary exists for {origins} to {destination} on {date}. Please try again.")
                                            continue
                                #status update to user
                                print("Searching... Please Wait")
            # Let user know that searching is complete
            print("Search complete.")
            with placeholder:
                st.success("Search complete.")
            placeholder2.empty()

        # Parse data collected from Google Search, outputting the average price for each destination at the end of the program.
        start.parser2(expert)
        
if submit:
    with st.expander("Show Results"):
        

        tab1, tab3, tab4 =st.tabs(['All Data', 'Lowest Price', 'Raw Data/ Export'])

        with tab1:
            alldata = pd.read_csv('flights.csv', names=['Date', 'Origin', 'Destination', 'Airline', 'Price'])
            fig = px.scatter(alldata, x='Date', y='Price', facet_col='Destination', facet_row='Origin', color='Airline', hover_name="Airline", hover_data={'Airline':False, 'Date':False, 'Origin':False, 'Destination':False})
            fig.layout.hovermode = 'x'
            st.plotly_chart(fig, use_container_width=True)
        
        
        

        with tab3:
            df = pd.read_csv('lowest.csv', names=['Date', 'Origin', 'Destination', 'Airline', 'Price'])
            grouped = df.groupby(['Origin', 'Destination'])

            data=[]
            # create a list of trace
            for (Origin, Destination), group in grouped:
                text_list = ["City Pair: " + str(a) + "-" + str(b) + "<br>Airline: " + str(j) + "<br>Price: $" + str(i) for i,j,a,b in zip(group["Price"],group["Airline"],group["Origin"],group["Destination"])]
                data.append(go.Scatter(x=group['Date'], y=group['Price'], name=f'{Origin} to {Destination}',line=dict(width=2.5),mode = 'lines+markers',
                            text=text_list, hovertemplate='%{text}<extra></extra>'))

            layout = dict(title='Lowest Flight Prices',
                            xaxis_title='Date',
                            yaxis_title='Price')

            fig3 = go.Figure(data=data, layout=layout)

            st.plotly_chart(fig3, use_container_width=True)
        
        with tab4:
            col1, col2 = st.columns(2)

            with col1:
                st.write("Full, Raw Data")
                st.write(pd.read_csv('flights.csv', index_col=0, names=['Date', 'Origin', 'Destination', 'Airline', 'Price']))
                st.download_button(label="Download Data", data='flights.csv', file_name='flights.csv', mime='text/csv')

            with col2:
                st.write("Lowest Price for Each Date")
                st.write(pd.read_csv('lowest.csv', index_col=0, names=['Date', 'Origin', 'Destination', 'Airline', 'Price']))
                st.download_button(label="Download Data", data='lowest.csv', file_name='lowest.csv', mime='text/csv')


            
        



        


        
















