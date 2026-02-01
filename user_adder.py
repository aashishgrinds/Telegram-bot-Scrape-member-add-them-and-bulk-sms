from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import time
import random
import pyfiglet
# import traceback
from colorama import init, Fore
import os

init()

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

r = Fore.RED
g = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, g, w, ye, cy]
info = g + '[' + w + 'i' + g + ']' + rs
attempt = g + '[' + w + '+' + g + ']' + rs
sleep = g + '[' + w + '*' + g + ']' + rs
error = g + '[' + r + '!' + g + ']' + rs


def banner_text():
    f = pyfiglet.Figlet(font='slant')
    banner = f.renderText('Telegram Bot')
    print(random.choice(colors) + banner + rs)
    print(f'{info}{g} Telegram Adder[USERNAME] V1.1{rs}')
    print(f'{info}{g} Author: github.com/shamimkhaled{rs}\n')

def clear_screen():
    os.system('cls')

clear_screen()
banner_text()

api_id = int(sys.argv[1])
api_hash = str(sys.argv[2])
phone = str(sys.argv[3])
file = str(sys.argv[4])
group = str(sys.argv[5])

# Create sessions directory if it doesn't exist
sessions_dir = os.path.join(BASE_DIR, 'sessions')
success, message = ensure_directory_exists(sessions_dir, 'sessions')
if not success:
    print(f'{error}{r} {message}{rs}')
    sys.exit()

# Verify the CSV file exists
if not os.path.exists(file):
    print(f'{error}{r} CSV file not found: {file}{rs}')
    sys.exit()

print(f'{info}{g} Loading members from: {file}{rs}')

class Relog:
    def __init__(self, lst, filename):
        self.lst = lst
        self.filename = filename
    def start(self):
        with open(self.filename, 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
            for user in self.lst:
                writer.writerow([user['username'], user['id'], user['access_hash'], user['group'], user['group_id']])
            f.close()

def update_list(lst, temp_lst):
    count = 0
    while count != len(temp_lst):
        del lst[0]
        count += 1
    return lst

users = []
with open(file, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=',', lineterminator='\n')
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['user_id'] = row[1]
        user['access_hash'] = row[2]
        user['group'] = row[3]
        user['group_id'] = row[4]
        users.append(user)

client = TelegramClient(os.path.join(BASE_DIR, 'sessions', phone), api_id, api_hash)
client.connect()
time.sleep(random.uniform(1, 2))
target_group = client.get_entity(group)
entity = InputPeerChannel(target_group.id, target_group.access_hash)
group_name = target_group.title
print(f'{info}{g} Adding members to {group_name}{rs}\n')

n = 0
added_users = []
for user in users:
    n += 1
    added_users.append(user)
    if n % 50 == 0:
        print(f'{sleep}{g} Sleep 2 min to prevent possible account ban{rs}')
        time.sleep(random.randint(100, 140))
    try:
        if user['username'] == "":
            continue
        user_to_add = client.get_input_entity(user['username'])
        client(InviteToChannelRequest(entity, [user_to_add]))
        usr_id = user['user_id']
        print(f'{attempt}{g} Adding {usr_id}{rs}')
        print(f'{sleep}{g} Sleep 30s{rs}')
        time.sleep(random.randint(25, 35))
    except PeerFloodError as e:
        print(f'{error}{r} Peer Flood Error: {e}{rs}')
        os.system(f'del {file}')
        sys.exit(f'\n{error}{r} Aborted due to flood limits{rs}')
    except FloodWaitError as e:
        print(f'{error}{r} Flood wait: {e.seconds} seconds{rs}')
        time.sleep(e.seconds)
        continue
    except UserPrivacyRestrictedError:
        print(f'{error}{r} User Privacy Restriction{rs}')
        continue
    except KeyboardInterrupt:
        print(f'{error}{r} Aborted. Keyboard Interrupt{rs}')
        update_list(users, added_users)
        if not len(users) == 0:
            print(f'{info}{g} Remaining users logged to {file}')
            logger = Relog(users, file)
            logger.start()
        sys.exit()
    except Exception as e:
        print(f'{error}{r} Error: {e}{rs}')
        continue

input(f'{info}{g}Adding complete...Press enter to exit...')
sys.exit()
