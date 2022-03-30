import idlelib.rpc
import logging          #import logging module

from flask import Flask
from flask import render_template,request,redirect,url_for      #import flask modules
import json                                                     #import json

import functions
from class_db import User, Ticket, Flight, Country              #import functions file + classes from class_db file

import sqlite3                                                  #import sqlite module

app = Flask(__name__)

logging.basicConfig(filename='main.log' ,level=logging.INFO, format='%(asctime)s: - > %(levelname)s - > %(message)s')   #logging configure

current_user = 0
current_id = 0                                                  #global variables for current user session (id, real id, name)
current_user_name = ''

@app.route('/users', methods = ['GET', 'POST'])                 #USERS GET,POST REST API
def getpostUser():

    if request.method == 'GET':
        try:
            userArray = functions.get_users()                   #launch function from functions file
            return  json.dumps(userArray)                       #return as json
        except:
            logging.error(f'Read from USERS table error')       #log in case of error
            return f'Read from USERS table error'

    if request.method == 'POST':
        try:
            dict = request.get_json()                           #receive data as dict for json
            functions.post_users(dict)                          #pass data to function
            return f'User Created'
        except:
            logging.error(f'Write to USERS table error')        #log in case of error
            return f'Write to USERS table error'

@app.route('/users/<int:id>', methods = ['GET', 'PUT', 'DELETE'])   #USERS GET,DELETE,PUT REST API
def idUser(id):

    if request.method == 'GET':
        try:
            userArray = functions.get_user_id(id)               #receive array as return from function
            return json.dumps(userArray)                        #return to postman as json
        except:
            return f'Read from USERS table by ID {id} error'    #log for error

    if request.method == 'DELETE':
        try:
            functions.delete_user_id(id)                        #pass id for delete to function
            return f'User ID {id} deleted'
        except:
            logging.error(f'Delete from USERS table by ID {id} error')  #log in case of error
            return f'Delete from USERS table by ID {id} error'

    if request.method == 'PUT':
        dict = request.get_json()                               #receive json to dict
        try:
            functions.put_user_id(dict,id)                      #send to function for writing to DB
            return f'User with ID {id} updated'
        except:
            logging.error(f'Updating user with ID {id} error')  #log in case of error
            return f'Updating user with ID {id} error'

@app.route('/tickets', methods=['GET', 'POST'])                 #TICKETS GET,POST REST API
def getpostTickets():

    if request.method == 'GET':
        try:
            ticketsArray = functions.get_tickets()              #receive array from func
            return json.dumps(ticketsArray)                     #convert to json and return
        except:
            logging.error(f'Read from TICKETS table error')     #log for error
            return f'Read from TICKETS table error'

    if request.method == 'POST':
        try:
            dict = request.get_json()                           #receive json to dict
            functions.post_tickets(dict)                        #send to function for work
            return f'Ticket Created'
        except:
            logging.error(f'Write to TICKETS table error')      #log for error
            return f'Write to TICKETS table error'

@app.route('/tickets/<int:id>', methods=['GET', 'DELETE'])      #TICKETS GET,DELETE REST API
def idTicket(id):

    if request.method == 'GET':
        try:
            ticketsArray = functions.get_tickets_id(id)         #receive array from func
            return json.dumps(ticketsArray)                     #return as json
        except:
            return f'Read from TICKETS table by ID {id} error'  #log in case of error

    if request.method == 'DELETE':
        try:
            functions.delete_tickets_id(id)                     #send id to func
            return f'Ticket ID {id} deleted'
        except:
            logging.error(f'Delete from TICKETS table by ID {id} error')    #log in case of error
            return f'Delete from TICKETS table by ID {id} error'

@app.route('/flights', methods = ['GET', 'POST'])               #FLIGHTS GET,POST REST API
def getpostFlights():

    if request.method == 'GET':
        try:
            flightsArray = functions.get_flights()              #receive array from func
            return json.dumps(flightsArray)                     #return as json
        except:
            logging.error(f'Read from FLIGHTS table error')     #log if error
            return f'Read from FLIGHTS table error'

    if request.method == 'POST':
        try:
            dict = request.get_json()                           #receive json to dict
            functions.post_flights(dict)                        #pass to func to work
            return f'Flight Created'
        except:
            logging.error(f'Write to FLIGHTS table error')      #log if error
            return f'Write to FLIGHTS table error'

@app.route('/flights/<int:id>', methods = ['GET', 'PUT', 'DELETE']) #FLIGHTS GET,PUT,DELETE REST API
def idFlights(id):

    if request.method == 'GET':
        try:
            flightsArray = functions.get_flight_id(id)          #receive array from func
            return json.dumps(flightsArray)                     #convert to json and return
        except:
            return f'Read from FLIGHTS table by ID {id} error'  #log for error

    if request.method == 'DELETE':
        try:
            functions.delete_flight_id(id)                      #pass id to func
            return f'Flight ID {id} deleted'
        except:
            logging.error(f'Delete from FLIGHTS table by ID {id} error')    #log if error
            return f'Delete from FLIGHTS table by ID {id} error'

    if request.method == 'PUT':
        dict = request.get_json()                               #receive json to dict
        try:
            functions.put_flight_id(dict,id)                    #pass to func to work
            return f'Flight with ID {id} updated'
        except:
            logging.error(f'Updating flight with ID {id} error')    #log in case of error
            return f'Updating flight with ID {id} error'

@app.route('/countries', methods = ['GET', 'POST'])         #COUNTRIES GET,POST REST API
def getpostCountries():

    if request.method == 'GET':
        try:
            countryArray = functions.get_countries()        #receive array from func
            return  json.dumps(countryArray)                #return as json
        except:
            logging.error(f'Read from COUNTRIES table error')   #log if error
            return f'Read from COUNTRIES table error'

    if request.method == 'POST':
        try:
            dict = request.get_json()                       #receive json to dict
            functions.post_countries(dict)                  #pass to func
            return f'Country Created'
        except:
            logging.error(f'Write to COUNTRIES table error')    #log for error
            return f'Write to COUNTRIES table error'

@app.route('/countries/<int:id>', methods = ['GET', 'PUT', 'DELETE'])   #COUNTRIES GET,PUT,DELETE REST API
def idCountries(id):
    if request.method == 'GET':
        try:
            countryArray = functions.get_country_id(id)     #receive array from func
            return json.dumps(countryArray)                 #convert to json and return
        except:
            return f'Read from COUNTRIES table by ID {id} error'    #log

    if request.method == 'DELETE':
        try:
            functions.delete_country_id(id)                 #pass id to func
            return f'Country ID {id} deleted'
        except:
            logging.error(f'Delete from COUNTRIES table by ID {id} error')  #log
            return f'Delete from COUNTRIES table by ID {id} error'

    if request.method == 'PUT':
        dict = request.get_json()                           #receive imnput to dict
        try:
            functions.put_country_id(dict,id)               #pass to func
            return f'Country with ID {id} updated'
        except:
            logging.error(f'Updating country with ID {id} error')   #log
            return f'Updating country with ID {id} error'

@app.route('/')                                             #GRAPHIC USER INTERFACE - main page
def homepage():
    return render_template('main.html')

@app.route('/new_user')                                     #GRAPHIC USER INTERFACE - new user page
def new_user():
    return render_template('new_user.html')

@app.route('/login')                                        #GRAPHIC USER INTERFACE - login page
def login():
    return render_template('login.html')

@app.route('/system')                                       #GRAPHIC USER INTERFACE - system page (after login)
def system():
    return render_template('system.html', name = current_user_name)     #passing current_user_name to the html template

@app.route('/system/tickets')                               #GRAPHIC USER INTERFACE - system page - tickets managing
def tickets():
    try:
        ticketsArr = functions.tickets_gui(current_id)      #tickets reading from DB function
    except:
        logging.error(f'Read from TICKETS and FLIGHTS table error')
    return render_template('tickets.html', name = current_user_name, len = len(ticketsArr), source = ticketsArr)    #passing current user and array from DB to html template

@app.route('/system/buy')                                   #GRAPHIC USER INTERFACE - flights section (to buy tickets)
def buy():
    flightsArr = functions.buy_ticket_gui()                 #receive flights from funct
    return render_template('buy.html', name = current_user_name, len = len(flightsArr), source = flightsArr) #pass to html template

@app.route('/form_acc', methods = ['POST'])                 ##GRAPHIC USER INTERFACE - new user creation FORM
def new_usr_form():

    full_name = request.form['full_name']                   #receive data from the form
    password = request.form['password']
    real_id = request.form['real_id']

    if full_name == '' or password == '' or real_id == '':  #if empty - redirect to the same page
        return redirect('/new_user')

    try:
        functions.new_user(full_name,password,real_id)      #pass data to function for user creation
        logging.info(f'New user created in DB')
        return redirect('/')                                #and redirect to main page for login
    except:
        logging.error(f'Error creating new user')           #log if error
        return redirect('/new_user')                        #redirect to the same page (new_user)

@app.route('/login_form', methods = ['GET'])                ##GRAPHIC USER INTERFACE - login FORM
def login_usr_form():
    flag = 0                                                #flag in case data wrong
    real_id = request.args.get('real_id')                   #receive data from form
    password = request.args.get('password')

    dbConnect = sqlite3.connect('static/data.db')           #connect to DB
    try:
        check = dbConnect.execute(f"SELECT real_id, password, id_AI, full_name from users where real_id = {real_id}")   #try to search for user in DB
    except:
        return redirect('/login')                              #if fail - return to same page
    for c in check:
        if real_id == c[0] and password == c[1]:                #check if real_id and password == entry from DB
            global current_user, current_id, current_user_name
            current_user = real_id                              #if yes - global variable current_user,current_id and current_user_name
            current_id = c[2]                                   #received data from the DB to further work with the GUI (buy,delete tickets)
            current_user_name = c[3]
            logging.info(f'User {current_user_name} logged in')
            flag = 1                                            #flag = 1 in case login succesfull
            dbConnect.close()
            return  redirect('/system')                         #and redirect to system page
    if flag == 0:
        dbConnect.close()
        return redirect('/login')                               #flag = 0 if no sucessful login and try again

@app.route('/delete_ticket', methods = ['GET','DELETE'])        ##GRAPHIC USER INTERFACE - delete tickets form
def delete_ticket():
    id = request.args.get('id')                                 #receive id from form
    try:
        functions.delete_ticket_gui(id)                         #pass id to funct
        logging.info(f'User {current_user_name} deleted ticket ID {id}')
        return redirect('/system/tickets')
    except:
        logging.error(f'Error deleting ticket ID {id} for user {current_user_name}')    #log
        return redirect('/system/tickets')

@app.route('/buy_ticket', methods = ['POST'])                   ##GRAPHIC USER INTERFACE - buy ticket form
def buy_ticket():
    flight_id = request.form.get('flight_id')                   #receive flight id from form
    try:
        functions.buy_ticket_form(flight_id, current_id)        #pass flight id + current_user id to func to buy ticket
        logging.info(f'User {current_user_name} bought ticket fo flight id {flight_id}')
        return redirect('/system/buy')
    except:
        logging.error(f'Error purchasing ticket to flight ID {flight_id} for user {current_user_name}') #log
        return redirect('/system/buy')

app.run()                                   #run flask
