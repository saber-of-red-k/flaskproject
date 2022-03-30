#FUNCTIONS FILE#

import sqlite3
import logging
from class_db import User, Ticket, Flight, Country

logging.basicConfig(filename='main.log' ,level=logging.INFO, format='%(asctime)s: - > %(levelname)s - > %(message)s') #log configure

def get_users():                                        #GET USERS FUNCTION - REST API
    userArray = []
    dbConnect = sqlite3.connect('static/data.db')       #open DB connection
    array = dbConnect.execute('SELECT * FROM users')    #DB query
    for row in array:
        temp = User(row[0], row[1], row[2], row[3])     #transform result to new list
        userArray.append(temp.__dict__)
    dbConnect.close()                                   #close DB connection
    logging.info(f'Read from USERS table success')      #log
    return userArray                                    #return list with data from DB

def post_users(dict):                                   #POST USERS FUNCTION - receive dict from input - REST API
    new_user = User(dict.get("id_AI"), dict.get("full_name"), dict.get("password"), dict.get("real_id"))    #make class from received dictt
    dbConnect = sqlite3.connect('static/data.db')       #open DB
    dbConnect.execute(
        f"INSERT INTO users (full_name, password, real_id) VALUES ('{new_user.full_name}','{new_user.password}','{new_user.real_id}')") #DB query with info from class
    dbConnect.commit()
    dbConnect.close()                                   #commit&close
    logging.info(f'Created {new_user} in USERS table')  #log

def get_user_id(id):                                    #GET USER BY ID - REST API
    userArray = []
    dbConnect = sqlite3.connect('static/data.db')       #DB open
    try:
        array = dbConnect.execute(f'SELECT * FROM users WHERE id_AI = {id}')    #db query
        for row in array:
            temp = User(row[0], row[1], row[2], row[3])     #transform to list
            userArray.append(temp.__dict__)
        dbConnect.close()                               #close db
        logging.info(f'Read {temp} from USERS table success')   #log
        return userArray                                #return list of found user
    except:
        dbConnect.rollback()                            #rollback&close if error
        dbConnect.close()
        logging.error(f'Read from USERS table by ID {id} error')    #log

def delete_user_id(id):                                 #DELETE USER BY ID - REST API
    dbConnect = sqlite3.connect('static/data.db')
    try:
        dbConnect.execute(f'DELETE FROM users WHERE id_AI = {id}')  #DB query with ID passed to func
        dbConnect.commit()
        dbConnect.close()                                           #commit and close
        logging.info(f'Deleted user with ID {id} from USERS table')
    except:
        dbConnect.rollback()                                    #rollback and close if error
        dbConnect.close()

def put_user_id(dict,id):                               #PUT USER BY ID - REST API
    updated_user = User(dict[0].get("id_AI"), dict[0].get("full_name"), dict[0].get("password"), dict[0].get("real_id"))    #make class from passed dict
    dbConnect = sqlite3.connect('static/data.db')
    try:
        dbConnect.execute(                              #DB query with data from class
            f"UPDATE users SET full_name = '{updated_user.full_name}', password = '{updated_user.password}', real_id = '{updated_user.real_id}' WHERE id_AI = {id}")
        dbConnect.commit()                              #commit & close
        dbConnect.close()
        logging.info(f'UPDATED ID {id} with {updated_user} in USERS table')
    except:
        dbConnect.rollback()                        #rollback & close if error
        dbConnect.close()

def get_tickets():                                  #GET TICKETS - REST API
    ticketsArray = []
    dbConnect = sqlite3.connect('static/data.db')   #db open
    array = dbConnect.execute('SELECT * FROM tickets')  #db query
    for row in array:
        temp = Ticket(row[0], row[1], row[2])           #transform to list
        ticketsArray.append(temp.__dict__)
    dbConnect.close()                               #close db
    logging.info(f'Read from TICKETS table success')    #log
    return ticketsArray                             #return list with data from db

def post_tickets(dict):                             #POST TICKETS - REST API
    new_ticket = Ticket(dict.get("ticket_id"), dict.get("user_id"), dict.get("flight_id"))  #make class from passed dict
    dbConnect = sqlite3.connect('static/data.db')
    dbConnect.execute(f"INSERT INTO tickets (user_id, flight_id) VALUES ('{new_ticket.user_id}','{new_ticket.flight_id}')") #db query to make new ticket
    dbConnect.execute(f"UPDATE flights SET remaining_seats = remaining_seats-1 WHERE flight_id = {new_ticket.flight_id}")   #db query to update remain seats in FLIGHTS db
    dbConnect.commit()          #commit&close
    dbConnect.close()
    logging.info(f'Created {new_ticket} in TICKETS table')

def get_tickets_id(id):                             #GET TICKETS BY ID - REST API
    ticketsArray = []
    dbConnect = sqlite3.connect('static/data.db')   #db open
    try:
        array = dbConnect.execute(f'SELECT * FROM tickets WHERE ticket_id = {id}')  #db query - find ticket id
        for row in array:
            temp = Ticket(row[0], row[1], row[2])       #transform found data to list
            ticketsArray.append(temp.__dict__)
        dbConnect.close()
        logging.info(f'Read {temp} from USERS table success')
        return ticketsArray                             #return as list
    except:
        dbConnect.rollback()                            #close&rollback if error
        dbConnect.close()
        logging.error(f'Read from TICKETS table by ID {id} error')

def delete_tickets_id(id):                              #DELETE TICKET - REST API
    dbConnect = sqlite3.connect('static/data.db')
    array = dbConnect.execute(f'SELECT * FROM tickets WHERE ticket_id = {id}')  #db query - fing ticket by ID
    for row in array:
        temp = Ticket(row[0], row[1], row[2])           #make class object to update flight table
    try:
        dbConnect.execute(f'DELETE FROM tickets WHERE ticket_id = {id}')        #delete ticket by ID
        dbConnect.execute(f"UPDATE flights SET remaining_seats = remaining_seats+1 WHERE flight_id = {temp.flight_id}") #update reamining seats+1 if ticket deleted
        dbConnect.commit()
        dbConnect.close()
        logging.info(f'Deleted ticket with ID {id} from TICKETS table')
    except:
        dbConnect.rollback()                                    #rollback&close if error
        dbConnect.close()

def get_flights():                                      #GET FLICHTS - REST API
    flightsArray = []
    dbConnect = sqlite3.connect('static/data.db')
    array = dbConnect.execute('SELECT * FROM flights')  #db query for flights
    for row in array:
        temp = Flight(row[0], row[1], row[2], row[3], row[4])   #make class object
        flightsArray.append(temp.__dict__)                      #and pass if to list
    dbConnect.close()
    logging.info(f'Read from FLIGHTS table success')
    return flightsArray                                 #return created list
    
def post_flights(dict):                                 #POST FLIGHTS - REST API
    new_flight = Flight(dict.get("flight_id"), dict.get("timestamp"), dict.get("remaining_seats"),
                        dict.get("origin_country_id"), dict.get("dest_country_id"))     #make class object from passed dict
    dbConnect = sqlite3.connect('static/data.db')
    dbConnect.execute(                                                                  #send db query with made object data
        f"INSERT INTO flights (timestamp, remaining_seats, origin_country_id, dest_country_id) VALUES ('{new_flight.timestamp}','{new_flight.remaining_seats}','{new_flight.origin_country_id}','{new_flight.dest_country_id}')")
    dbConnect.commit()                                                  #commit&close
    dbConnect.close()
    logging.info(f'Created {new_flight} in FLIGHTS table')

def get_flight_id(id):                                  #GET FLIGHT BY ID - REST API
    flightsArray = []
    dbConnect = sqlite3.connect('static/data.db')
    try:
        array = dbConnect.execute(f'SELECT * FROM flights WHERE flight_id = {id}')  #get flight by id
        for row in array:
            temp = Flight(row[0], row[1], row[2], row[3], row[4])           #make object
            flightsArray.append(temp.__dict__)                              #convert to list
        dbConnect.close()
        logging.info(f'Read {temp} from FLIGHTS table success')             #log
        return flightsArray                                                 #return list
    except:
        dbConnect.rollback()
        dbConnect.close()                                                   #rollback&close if error
        logging.error(f'Read from FLIGHTS table by ID {id} error')

def delete_flight_id(id):                               #DELETE FLIGHT by ID - REST API
    dbConnect = sqlite3.connect('static/data.db')
    try:
        dbConnect.execute(f'DELETE FROM flights WHERE flight_id = {id}')        #delete flight by ID
        dbConnect.commit()                                                      #commit&close
        dbConnect.close()
        logging.info(f'Deleted FLIGHT with ID {id} from FLIGHTS table')         #log
    except:
        dbConnect.rollback()                                                    #rollback&close if error
        dbConnect.close()

def put_flight_id(dict,id):                                                     #PUT FLIGHT BY ID - REST API
    updated_flight = Flight(dict.get("flight_id"), dict.get("timestamp"), dict.get("remaining_seats"), dict.get("origin_country_id"), dict.get("dest_country_id"))
    dbConnect = sqlite3.connect('static/data.db')                               #make object and connect to DB
    try:
        dbConnect.execute(                                                      #send query with object data
            f"UPDATE flights SET timestamp = '{updated_flight.timestamp}', remaining_seats = '{updated_flight.remaining_seats}', origin_country_id = '{updated_flight.origin_country_id}', dest_country_id = '{updated_flight.dest_country_id}' WHERE flight_id = {id}")
        dbConnect.commit()
        dbConnect.close()
        logging.info(f'UPDATED ID {id} with {updated_flight} in FLIGHTS table') #log
    except:
        dbConnect.rollback()                                                    #rollback&close if error
        dbConnect.close()

def get_countries():                                                        #GET COUNTRIES - REST API
    countryArray = []
    dbConnect = sqlite3.connect('static/data.db')
    array = dbConnect.execute('SELECT * FROM countries')                    #db query for countries
    for row in array:
        temp = Country(row[0], row[1])                                      #make class object
        countryArray.append(temp.__dict__)                                  #transform to list
    dbConnect.close()
    logging.info(f'Read from COUNTRIES table success')
    return countryArray                                                     #return list

def post_countries(dict):                                               #POST COUNTRIES - REST API
    new_country = Country(dict.get("code_AI"), dict.get("name"))    #make object from dict
    dbConnect = sqlite3.connect('static/data.db')
    dbConnect.execute(f"INSERT INTO countries (name) VALUES ('{new_country.name}')")    #send query to DB - new country
    dbConnect.commit()
    dbConnect.close()
    logging.info(f'Created {new_country} in USERS table')           #log

def get_country_id(id):                                     #GET COUNTRY BY ID - REST API
    countryArray = []
    dbConnect = sqlite3.connect('static/data.db')           #db open
    try:
        array = dbConnect.execute(f'SELECT * FROM countries WHERE code_AI = {id}')  #select by id from DB
        for row in array:
            temp = Country(row[0], row[1])                  #make class object
            countryArray.append(temp.__dict__)              #transform to list
        dbConnect.close()
        logging.info(f'Read {temp} from COUNTRIES table success')
        return countryArray                                 #return list
    except:
        dbConnect.rollback()                                #rollback&close if error
        dbConnect.close()
        logging.error(f'Read from COUNTRIES table by ID {id} error')    #log

def delete_country_id(id):                  #DELETE COUNTRY BY ID - REST API
    dbConnect = sqlite3.connect('static/data.db')
    try:
        dbConnect.execute(f'DELETE FROM countries WHERE code_AI = {id}')    #delete db query
        dbConnect.commit()
        dbConnect.close()                                                   #commit&close
        logging.info(f'Deleted country with ID {id} from COUNTRIES table')
    except:
        dbConnect.rollback()                                                #rollback&close if error
        dbConnect.close()

def put_country_id(dict,id):                                        #PUT COUNTRY by ID - REST API
    updated_country = Country(dict.get("code_AI"), dict.get("name"))    #make class object
    dbConnect = sqlite3.connect('static/data.db')
    try:
        dbConnect.execute(f"UPDATE countries SET name = '{updated_country.name}' WHERE code_AI = {id}") #update in DB
        dbConnect.commit()
        dbConnect.close()
        logging.info(f'UPDATED ID {id} with {updated_country} in COUNTRIES table')  #log
    except:
        dbConnect.rollback()                                    #rollback&close if error
        dbConnect.close()

def tickets_gui(id):                                            #TICKETS VIEW FUNCTION FOR GUI
    ticketsArr = []
    dbConnect = sqlite3.connect('static/data.db')               #db open - work same as REST API
    array = dbConnect.execute(                                  #another DB query with JOIN to see data from flights
        f'SELECT tickets.ticket_id, tickets.flight_id, flights.timestamp from tickets INNER JOIN flights ON tickets.flight_id = flights.flight_id WHERE tickets.user_id = {id}')
    for row in array:
        temp = [row[0], row[1], row[2]]                         #make list
        ticketsArr.append(temp)
    logging.info(f'Read from TICKETS and FLIGHTS table success')
    return ticketsArr                                           #return list to display in html template

def buy_ticket_gui():                                           #FLIGHTS VIEW FOR GUI
    dbConnect = sqlite3.connect('static/data.db')
    flightsArr = []

    try:
        array = dbConnect.execute('SELECT * FROM flights')      #db to show flights
        for row in array:
            temp = [row[0], row[1], row[2], row[3], row[4]]     #make list
            flightsArr.append(temp)
        logging.info(f'Read from FLIGHTS table success')
    except:
        logging.info(f'Read from FLIGHTS table error')

    country_code = []

    try:                                                        #DB query to access COUNTRIES
        array2 = dbConnect.execute('SELECT * from countries')
        for row in array2:
            temp = [row[0], row[1]]                             #make countries DB
            country_code.append(temp)
        logging.info(f'Read from COUNTRIES table success')
    except:
        logging.error(f'Read from COUNTRIES table success')

    for row in flightsArr:                                      #change in flightArr - swap counry code with country name for GUI
        for row2 in country_code:
            if row[3] == row2[0]:
                row[3] = row2[1]
            if row[4] == row2[0]:
                row[4] = row2[1]
    dbConnect.close()
    return flightsArr                                           #return list to display for GUI

def new_user(full_name,password,real_id):                       #NEW USER CREATE FOR GUI
    new_user = User(1, full_name, password, real_id)            #make object, id - 1 because we don't care about ID in db, it's autoincrement
    dbConnect = sqlite3.connect('static/data.db')
    try:
        dbConnect.execute(                                      #send info to DB
            f"INSERT INTO users (full_name, password, real_id) VALUES ('{new_user.full_name}','{new_user.password}','{new_user.real_id}')")
        dbConnect.commit()
        dbConnect.close()
        logging.info(f'Created {new_user} in USERS table')
    except:
        dbConnect.rollback()                                    #rollback&close if error
        dbConnect.close()
        logging.error(f'Error creating {new_user} in table USERS')


def delete_ticket_gui(id):                                      #DELETE TICKET FOR GUI
    dbConnect = sqlite3.connect('static/data.db')
    ticketsArray = []
    array = dbConnect.execute(f'SELECT * FROM tickets WHERE ticket_id = {id}')  #db query to find ticket
    for row in array:
        temp = Ticket(row[0], row[1], row[2])                   #make object to update after this remaining seats
    try:
        dbConnect.execute(f'DELETE FROM tickets WHERE ticket_id = {id}')        #delete ticket
        dbConnect.execute(f"UPDATE flights SET remaining_seats = remaining_seats+1 WHERE flight_id = {temp.flight_id}") #update flights
        dbConnect.commit()
        dbConnect.close()
        logging.info(f'Deleted ticket with ID {id} from TICKETS table')
    except:
        dbConnect.rollback()                                    #rollback&close if error
        dbConnect.close()
        logging.error(f'Error deleting ticket with ID {id} from TICKETS table') #log

def buy_ticket_form(flight_id, current_id):                     #BUY TICKETS for GUI
    new_ticket = Ticket(1, current_id, flight_id)               #make class - 1 because in db it's autoincrement
    dbConnect = sqlite3.connect('static/data.db')
    dbConnect.execute(
        f"INSERT INTO tickets (user_id, flight_id) VALUES ('{new_ticket.user_id}','{new_ticket.flight_id}')")   #write new ticket in DB
    dbConnect.execute(
        f"UPDATE flights SET remaining_seats = remaining_seats-1 WHERE flight_id = {new_ticket.flight_id}")     #update flight for remaining_seats - 1
    dbConnect.commit()
    dbConnect.close()                                           #commit&close
    logging.info(f'Created {new_ticket} in TICKETS table')      #log