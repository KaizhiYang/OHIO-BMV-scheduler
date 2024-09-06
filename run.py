import threading
import keyboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
from wxauto import *

from login_info import *

lastMessage = ''
suspend = False  # Variable to control suspension

# Function to check if the slot datetime is before the cutoff date
def is_before_cutoff(date_str, cutoff):
    slot_date = datetime.strptime(date_str, '%m/%d/%Y at %I:%M %p')
    return slot_date < cutoff

def keyboard_listener():
    global suspend
    while True:
        if keyboard.is_pressed(']'):
            suspend = not suspend
            print(f"Loop {'suspended' if suspend else 'resumed'}")
            keyboard.wait(']')  # Wait for the key to be released to avoid toggling multiple times

def script(county, date, vx_receiver):
    global lastMessage  # Declare lastMessage as global to modify it within the function
    global suspend  # Declare suspend as global to modify it within the function

    # Initialize the Edge browser
    driver = webdriver.Edge()

    # Navigate to the specified URL
    driver.get('https://bmvonline.dps.ohio.gov/bmvonline/auth/login?returnURL=%2Fbmvonline%2Fdxscheduling&loginOptions=License&loginOptions=Name&loginOptions=DX&loginOptions=OHID')

    # Wait for the "Log in as a Guest" button to be clickable and click it
    guest_login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//button[.//div[contains(text(), "Log in as a Guest")]]'))
    )
    guest_login_button.click()

    # Wait for the "Personal Information" tab button to be clickable
    personal_info_tab_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'tabName'))
    )

    # Scroll to the element and click it
    personal_info_tab_button.click()

    # Wait for the form fields to be clickable
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'NameModel_LastName'))
    )

    # Fill out the form fields
    driver.find_element(By.ID, 'NameModel_LastName').send_keys(last_name)
    driver.find_element(By.ID, 'NameModel_FirstName').send_keys(first_name)
    driver.find_element(By.ID, 'NameModel_DateOfBirth').send_keys(date_of_birth)
    driver.find_element(By.ID, 'NameModel_LastFourOfSSN').send_keys(last4ssn)

    # Submit the form (if needed)
    submit_button = driver.find_element(By.XPATH, '//input[@type="submit" and @value="Log in"]')
    submit_button.click()

    # Continue after submitting the form
    continue_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'btnContinue'))
    )
    continue_button.click()

    # Schedule after Continue
    schedule_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'btnSchdeule0'))
    )
    schedule_button.click()

    # Select "Franklin" from the dropdown
    dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, 'AvailableCounties'))
    )
    select = Select(dropdown)
    select.select_by_visible_text(county)

    # 获取当前微信客户端
    wx = WeChat()

    while True:
        if suspend:
            print("Loop is suspended. Press ']' to resume.")
            while suspend:
                pass  # Wait until the loop is resumed

        # Find and click the link with the text "Select First Available for Franklin County"
        # select_first_available_link = WebDriverWait(driver, 20).until(
        #     EC.element_to_be_clickable((By.XPATH, '//a[text()="Select First Available for ' + county + ' County"]'))
        # )
        select_first_available_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'submitFirstAvailable_1'))
        )
        select_first_available_link.click()

        # Wait for the available slots to be visible
        available_slots_div = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'row'))
        )

        # Extract and organize available slots
        slots = []

        slot_elements = driver.find_elements(By.XPATH, '//input[starts-with(@id, "morningDateTime_") or starts-with(@id, "afternoonDateTime_")]')

        for slot_element in slot_elements:
            slot_id = slot_element.get_attribute("id")
            slot_value = slot_element.get_attribute("value")
            date_time = datetime.strptime(slot_value, "%m/%d/%Y %H:%M:%S").strftime("%m/%d/%Y at %I:%M %p")
            
            # Find the corresponding button text (using XPath relative to the input element)
            button_element = slot_element.find_element(By.XPATH, 'ancestor::tr//button')
            button_text = button_element.text

            slots.append({
                "id": slot_id,
                "datetime": date_time,
                "button_text": button_text
            })

        # 向某人发送消息（以`文件传输助手`为例）
        msg = '****' + county + '最新路考时间' + '****'
        checker = 0

        # Print out the slots
        for slot in slots:
            msg += f"\nID: {slot['id']}, DateTime: {slot['datetime']}"
            if is_before_cutoff(slot['datetime'], date):
                checker = 1

        msg += '\n****' + county + '最新路考时间' + '****'

        print(msg)

        if checker == 1 and lastMessage != msg:
            # 获取会话列表
            wx.GetSessionList()
            wx.SendMsg(msg, vx_receiver)
        
        # Refresh page
        # Continue after submitting the form
        back_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, 'btnStepperBack'))
        )
        back_button.click()

        lastMessage = msg

if __name__ == '__main__':
    # Start the keyboard listener in a separate thread
    keyboard_thread = threading.Thread(target=keyboard_listener, daemon=True)
    keyboard_thread.start()

    script(county, TARGATE_DATE, WX_RECEIVER)
