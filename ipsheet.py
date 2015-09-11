import sys
import netifaces as ni
import json
import gspread
import threading
import yaml
import time
from oauth2client.client import SignedJwtAssertionCredentials
from sshpubkeys import SSHKey, InvalidKeyException

config = yaml.load(open("./config.yml"))

def log(message):
    print >> sys.stderr, message
    return

# connect to spreadsheet
json_key = json.load(open(config['key_file']))
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(json_key['client_email'],
                                            json_key['private_key'],
                                            scope)
gc = gspread.authorize(credentials)

wks = gc.open(config['spreadsheet']).sheet1

# get ip address
try:
    neti = ni.ifaddresses(config['network_interface'])
except ValueError as err:
    log(err)
    log(config['network_interface'] + " is not valid interface")
    log("Available interfaces are: ")
    log(ni.interfaces())
    sys.exit("quitting")

ip_address = neti[2][0]['addr']

# check if this ip address is already in the spreadsheet,
# if it's not append it to the column
try:
    wks.find(ip_address)
    # this is fine ip adress is already there
except:
    # append the address
    wks.update_cell(len(wks.col_values(1)) + 1, 1, ip_address)


# need to querry spreadsheet(for example every 10s)
# when key is pasted pick it up and stop queries
def fetch_key():
    cell = wks.find(ip_address)
    key = wks.cell(cell.row, 2).value
    if (key == ""):
        # querry again
        threading.Timer(1, fetch_key).start()
    else:
        wks.update_cell(cell.row, 3, time.ctime())
        # validate the key
        try:
            ssh = SSHKey(key)
            print(key)
            wks.update_cell(cell.row, 4,
                            "valid key fetched")
        except NotImplementedError:
            wks.update_cell(cell.row, 4,
                            "invalid ecdsa curve or unknown key type")
            threading.Timer(1, fetch_key).start()

        except InvalidKeyException as err:
            wks.update_cell(cell.row, 4, err)
            threading.Timer(1, fetch_key).start()

fetch_key()
