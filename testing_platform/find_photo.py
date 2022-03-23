from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import urllib
import os

# What you enter here will be searched for in
# Google Images
query = "triangle transparent"
#circle transparent
#rectangle transparent
#triangle transparent

# Creating a webdriver instance

driver = webdriver.Chrome('chromedriver.exe')

# Maximize the screen
driver.maximize_window()

# Open Google Images in the browser
driver.get('https://images.google.com/')

# Finding the search box
box = driver.find_element_by_xpath('//input[@class="gLFyf gsfi"]')

# Type the search query in the search box
box.send_keys(query)

# Pressing enter
box.send_keys(Keys.ENTER)

if not os.path.exists('../teachable machine testing/{}_train'.format(query)):
    os.makedirs('../teachable machine testing/{}_train'.format(query))

if not os.path.exists('../teachable machine testing/testing'.format(query)):
    os.makedirs('../teachable machine testing/testing'.format(query))

# Function for scrolling to the bottom of Google
# Images results
def scroll_to_bottom(scroll_time):
    last_height = driver.execute_script('\
    return document.body.scrollHeight')
    sctoll_count = 0
    while True:
        driver.execute_script('\
        window.scrollTo(0,document.body.scrollHeight)')

        # waiting for the results to load
        # Increase the sleep time if your internet is slow
        time.sleep(3)

        new_height = driver.execute_script('\
        return document.body.scrollHeight')

        # click on "Show more results" (if exists)
        try:
            driver.find_element_by_css_selector(".YstHxe input").click()

            # waiting for the results to load
            # Increase the sleep time if your internet is slow
            time.sleep(3)

        except:
            pass

        # checking if we have reached the bottom of the page
        if new_height == last_height:
            break
        if sctoll_count == scroll_time:
            break

        sctoll_count+=1
        last_height = new_height


# Calling the functionsc
# NOTE: If you only want to capture a few images,
# there is no need to use the scroll_to_bottom() function.
scroll_time= 8
scroll_to_bottom(scroll_time)

img = driver.find_elements_by_xpath('//img[@class="rg_i Q4LuWd"]')
i=0
for image in img:
    image_url= image.get_attribute('src')
    # Enter the location of folder in which
    # the images will be saved
    try:
        if (i<300):
            urllib.request.urlretrieve(str(image_url),'../teachable machine testing/{}_train/{}_{}.jpg'.format(query,query,i))
        else:
            urllib.request.urlretrieve(str(image_url), '../teachable machine testing/testing/{}_{}.jpg'.format(query, i))

        if i==400:
            break

        i += 1
    except Exception:
        print(Exception)
        pass
    # Each new screenshot will automatically
    # have its name updated

    # Just to avoid unwanted errors
    time.sleep(0.2)


# Finally, we close the driver
driver.close()
