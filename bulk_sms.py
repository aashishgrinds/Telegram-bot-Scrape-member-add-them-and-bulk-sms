import csv
import os
import sys
import random
import time
import pickle
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError, PeerFloodError, FloodWaitError
from telethon.tl.types import InputPeerUser
from telethon.sync import events
import pyfiglet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ensure_directory_exists(dir_path, dir_name):
    """Ensure directory exists and create if it doesn't"""
    try:
        os.makedirs(dir_path, exist_ok=True)
        if not os.path.exists(dir_path):
            return False, f"Failed to create {dir_name} directory"
        return True, f"{dir_name} directory ready"
    except Exception as e:
        return False, f"Error creating {dir_name} directory: {e}"

# Constants for console colors
light_green = '\033[92m'
white = '\033[0m'
red = '\033[91m'
cyan = '\033[96m'
rs = '\033[0m'


info = light_green + '(' + white + 'i' + light_green + ')' + rs
error = light_green + '(' + red + '!' + light_green + ')' + rs
success = white + '(' + light_green + '+' + white + ')' + rs
INPUT = light_green + '(' + cyan + '~' + light_green + ')' + rs
colors = [light_green, white, red, cyan]

# Constants for sleep time between messages (in seconds)
MIN_SLEEP_TIME = 15
MAX_SLEEP_TIME = 25

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def banner_text():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram Bot')
    print(random.choice([light_green, white, red]) + banner + rs)

clear()
banner_text()

try:
    with open(os.path.join(BASE_DIR, 'account_info.txt'), 'rb') as f:
        accounts = []
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
except FileNotFoundError:
    print(f'{error}Account file not found! Please run authenticate.py first.')
    sys.exit()
except Exception as e:
    print(f'{error}Error loading accounts: {e}')
    sys.exit()
print(f'{INPUT}{light_green}({cyan}~{light_green}) Choose an account\n')
for i, acc in enumerate(accounts):
    print(f'{light_green}({white}{i}{light_green}) {acc[2]}')
ind = input(f'\n {INPUT}{light_green}({cyan}~{light_green}) Enter your choice: ')
try:
    ind = int(ind)
    if ind < 0 or ind >= len(accounts):
        print(f'{error}Invalid choice! Using first account.')
        ind = 0
except ValueError:
    print(f'{error}Invalid input! Using first account.')
    ind = 0
api_id = accounts[ind][0]
api_hash = accounts[ind][1]
phone = accounts[ind][2]

# Create sessions directory if it doesn't exist
sessions_dir = os.path.join(BASE_DIR, 'sessions')
success, message = ensure_directory_exists(sessions_dir, 'sessions')
if not success:
    print(f'{error}{message}')
    sys.exit()

c = TelegramClient(os.path.join(BASE_DIR, 'sessions', phone), api_id, api_hash)
c.connect()

if not c.is_user_authorized():
    try:
        c.send_code_request(phone)
        code = input(f'{light_green}({cyan}~{light_green}) Enter the login code for {white}{phone}{red}: ')
        c.sign_in(phone, code)
    except PhoneNumberBannedError:
        print(f'{error}{white}{phone}{red} is banned!{rs}')
        print(f'{error}{light_green} Run {white}manage.py{light_green} to filter them{rs}')
        sys.exit()

# Assuming members.csv file structure: username,user_id,access_hash,group,group_id,status
input_file = os.path.join(BASE_DIR, 'members', 'members.csv')

# Verify members directory exists
members_dir = os.path.join(BASE_DIR, 'members')
if not os.path.exists(members_dir):
    print(f'{error}Members directory not found! Please run member_scraper.py first.')
    sys.exit()

# Verify members file exists
if not os.path.exists(input_file):
    print(f'{error}Members file not found! Please run member_scraper.py first.')
    sys.exit()

print(f'{info}Loading members from: {input_file}')

users = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {
            'username': row[0],
            'user id': int(row[1]),
            'access hash': int(row[2]),
            'group': row[3],
            'group_id': row[4],
            'status': row[5]
        }
        users.append(user)

print(f'{light_green}[1] Send SMS by user ID\n[2] Send SMS by username ')
mode = int(input(f'{light_green}Input: {rs}'))

message = input(f'{light_green}[+] Enter Your Message: {rs}')

for user in users:
    try:
        if mode == 2:
            if user['username'] == "":
                continue
            receiver = c.get_input_entity(user['username'])
        elif mode == 1:
            receiver = InputPeerUser(user['user id'], user['access hash'])
        else:
            print(f'{red}[!] Invalid Mode. Exiting.')
            c.disconnect()
            sys.exit()

        print(f'{light_green}[+] Sending Message to: {user["username"]}')
        c.send_message(receiver, message.format(user['username']))
        sleep_time = random.randint(MIN_SLEEP_TIME, MAX_SLEEP_TIME)
        print(f'{light_green}[+] Waiting {sleep_time} seconds')
        time.sleep(sleep_time)
    except PeerFloodError as e:
        print(f'{red}[!] Getting Flood Error from Telegram.')
        print(f'{red}[!] Script is stopping now. Please try again after some time.')
    except FloodWaitError as e:
        print(f'{red}[!] Flood wait: {e.seconds} seconds. Please wait...')
        time.sleep(e.seconds)
    except Exception as e:
        print(f'{red}[!] Error sending message: {e}')
        c.disconnect()
        sys.exit()
    except Exception as e:
        print(f'{red}[!] Error: {e}')
        print(f'{red}[!] Trying to continue...')
        continue

c.disconnect()
print("Done. Message sent to all users.")
