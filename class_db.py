
#CLASSES FILE#

class User:
    def __init__(self, id_AI, full_name, password, real_id):
        self.id_AI = id_AI
        self.full_name = full_name
        self.password = password
        self.real_id = real_id
    def __str__(self):
        return f'{self.id_AI}, {self.full_name}, {self.password}, {self.real_id}'

class Ticket:
    def __init__(self, ticket_id, user_id, flight_id):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.flight_id = flight_id
    def __str__(self):
        return f'{self.ticket_id}, {self.user_id}, {self.flight_id}'

class Flight:
    def __init__(self, flight_id, timestamp, remaining_seats, origin_country_id, dest_country_id):
        self.flight_id = flight_id
        self.timestamp = timestamp
        self.remaining_seats = remaining_seats
        self.origin_country_id = origin_country_id
        self.dest_country_id = dest_country_id
    def __str__(self):
        return f'{self.flight_id}, {self.timestamp}, {self.remaining_seats}, {self.origin_country_id}, {self.dest_country_id}'

class Country:
    def __init__(self, code_AI, name):
        self.code_AI = code_AI
        self.name = name
    def __str__(self):
        return f' {self.code_AI}, {self.name}'
