from datetime import datetime
## Name of the counties (do not change)
franklin = 'Franklin'
fairfield = 'Fairfield'
union = 'Union'
delaware = 'Delaware'


## Modify followings before start 'run.py'
first_name = 'adam'     # your fist name
last_name = 'smith'      # your last name
date_of_birth = '01/01/2001'  # your DOB in the format of MM/DD/YYYY 
last4ssn = '0000'   # your last four digits of ssn, enter 0000 if you don't have a ssn

WX_RECEIVER = 'chat_channel'    # The name of your contact in WeChat where notifications will be sent.
TARGATE_DATE = datetime(2024, 9, 5)     # Set your target date, so the script will only notify if there are spots available before 9/5/2024
county = franklin   # Choose your county from the available options: franklin, fairfield, union, delaware.

