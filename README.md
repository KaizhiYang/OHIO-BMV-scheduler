# BMV-scheduler

## Description

Automatically extract available slots at OHIO BMV for driver test. **To use this script, you have to have a valid learner's permit!**

## Installation

To get started with this project, you'll need to install the following Python packages:

1. **Selenium**: Package for browser automation.
2. **wxauto**: Package for wxWidgets automation.
3. **Microsoft Edge**: The defualt browser.
4. **Edge WebDriver**: Web Driver for Microsoft Edge.
5. **Microsoft Win10: This script only works on Win10.**


You can install Selenium and wxauto using `pip`.
To install the packages manually, you can use the following commands in your CMD:

```bash
pip install selenium
pip install wxauto
```

Use this link to download Edge WebDriver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/


## Usage

Before running `run.py`, you’ll need to modify some variables in `login_info.py` to fit your personal information.

Modify the following fields in `login_info.py`:

1.	Personal Information:
    ```python
    first_name = 'adam'     # your first name
    last_name = 'smith'     # your last name
    date_of_birth = '01/01/2001'  # your DOB in the format MM/DD/YYYY 
    last4ssn = '0000'       # your last four digits of SSN, enter 0000 if you don't have a SSN
    ```
2.	WeChat Notification:
    ```python
    WX_RECEIVER = 'chat_channel'  # The name of your contact in WeChat where notifications will be sent.
    ```
3.	Target Appointment Date:
    ```python
    TARGATE_DATE = datetime(2024, 9, 5)  # Set your target date, so the script will only notify if there are spots available before 9/5/2024
    ```
4. County Selection:
    ```python
    county = franklin  # Choose your county from the available options: franklin, fairfield, union, delaware.
    ```
    Available counties:
    ```python
    franklin = 'Franklin'
    fairfield = 'Fairfield'
    union = 'Union'
    delaware = 'Delaware'
    ```
    You can add more counties as you want.

Once you have modified the necessary fields in `login_info.py`, you can execute `run.py` to check available slots for the specific county.

## Disclaimer

This script is intended for personal use and study purpose only. The user assumes full responsibility for ensuring that the usage of this script complies with any applicable laws, regulations, and the terms of service of the Ohio BMV or any other relevant entity. The author is not liable for any misuse of this script, including but not limited to account suspension, legal action, or penalties arising from non-compliance with these terms. It is the user's responsibility to use the script ethically and within legal boundaries.
