# -*- coding: utf-8 -*-
#!/usr/bin/python3

# This script allows to check all important
# menu items in TMall AliExpress mobile Android application.
# This script is just an example how you can use Appium with Python
# to test real application (example of deep test, which automatically detects
# all items which should be checked).

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time
from datetime import datetime


RESULTS = ""
CHECKED = []
start = datetime.now()


desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '8.0'
desired_caps['deviceName'] = 'Android'

desired_caps['appPackage'] = 'com.alibaba.aliexpresshd'
desired_caps['appActivity'] = 'com.aliexpress.module.home.MainActivity'

# This command starts application (should be installed on your device):
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(10)


# Open Left menu:
driver.find_element_by_id('com.alibaba.aliexpresshd:id/left_action').click()
# Click "Configuration":
driver.find_elements_by_id('com.alibaba.aliexpresshd:id/title')[8].click()
# Click "Select Country":
driver.find_element_by_id('com.alibaba.aliexpresshd:id/iv_country_selected').click()
# Select Russia:
driver.find_element_by_id('com.alibaba.aliexpresshd:id/rb_selected_item').click()
# Click to TMall:
driver.find_elements_by_class_name('android.widget.ImageView')[3].click()
# Click to "List Of Categories":
driver.find_elements_by_id('com.alibaba.aliexpresshd:id/iv_photo')[5].click()


### ------------


def check_products_count(path=''):
    """ This function checks how many products are presented on
        the page. If this page shows menu items, this function will
        return -1. Otherwise it will return the number of found products.
    """

    global RESULTS
    global CHECKED

    # if function returned -1 it means that the current activity
    # is not the list of products page:
    count = -1
    driver.implicitly_wait(1)

    if path not in CHECKED:
        CHECKED.append(path)

        try:
            # Try to get count of products on the page:
            driver.find_element_by_id('com.alibaba.aliexpresshd:id/search_btn_filter').click()
            counter = driver.find_element_by_id('com.alibaba.aliexpresshd:id/refine_title_count')
            count = int(counter.text.split()[0])

            # Advanced check for 0 results:
            title = driver.find_element_by_id('com.alibaba.aliexpresshd:id/tv_spellcheck_result')
            if 'не найдено' in title.text:
                count = 0

        except Exception as e:
            pass  # just ignore any errors here

        # if it is a page with the list of products, we need go click GoBack button:
        if count >= 0:
            driver.back()

        # We need report a bug in case if some category has 0 products:
        if count == 0:
            RESULTS += '\n\n-------'
            RESULTS += '\nZERO RESULTS in AliExpress Android application: \n'
            RESULTS += '\n' + path[:-3] + '\n'
            RESULTS += '---\n\n'

            print('\n---\n ZERO RESULTS! ' + path[:-3] + '\n---\n')

    driver.implicitly_wait(10)

    return count


def click(element):
    """ This tricky method allows to click to any menu item
        even if Appium can't properly click this element.
    """

    driver.swipe(0, 400, 0, 700, 500)

    y = 0

    try:
        y = element.location_once_scrolled_into_view['y']
    except:
        pass  # just ignore any errors here.

    try:
        window_size = driver.get_window_size()
        if (window_size['height'] - y < 30):
            # Go down:
            driver.swipe(70, 510, 70, 100, 400)
            y = element.location_once_scrolled_into_view['y']
    except:
        pass  # just ignore any errors here.

    TouchAction(driver).tap(None, 200, y + 10, 1).perform()


def get_menu_items(menu):
    """ This function collects all visible menu items on the page
        and returns the list of items in descend order.
    """

    # Appium bug, need to search two times to get all elements:
    menu_items = menu.find_elements_by_xpath("//*[string-length( @text ) > 1 and not(starts-with(@text, ' '))]")
    menu_items = menu.find_elements_by_xpath("//*[string-length( @text ) > 1 and not(starts-with(@text, ' '))]")

    with_text = []

    for i in menu_items:
        try:
            text = i.text.strip()
        except Exception as e:
            print(e)
            print('Trying another way to detect elements...')
            # Try to find elements one more time with different method:
            menu_items = menu.find_elements_by_class_name('android.view.View')
            break

    for item in menu_items:
        text = ''

        try:
            text = item.text.strip() or ''
        except Exception as e:
            print(e)
            pass  # just ignore any error

        if text > '':
            with_text.append(item)

    return with_text[::-1]


def check(element, path=''):
    """ This is main recursive function will check every menu item. """

    count = check_products_count(path)

    if count < 0:
        menu_list = element.find_elements_by_class_name('android.widget.ListView')

        for i, _ in enumerate(menu_list):
            menu = menu_list[i]

            menu_items = get_menu_items(menu)

            changed = False
            for j, _ in enumerate(menu_items):

                if changed:
                    # After some clicks the elements in the list can be changed,
                    # We need to get the list of elements after every click:
                    menu_items = get_menu_items(menu)
                    changed = False

                item = menu_items[j]

                text = item.text.strip()

                if text > '':
                    print('{0}{1}'.format(path, text))

                    click(item)

                    if text != 'Назад':
                        res = check(menu, path + text + ' > ')

                        if res == 0:
                            changed = True

            menu_list = element.find_elements_by_class_name('android.widget.ListView')
    else:
        driver.find_element_by_class_name('android.widget.ImageButton').click()

        return -1

    return 0


# Run recursive check for all menu items:
check(driver)

# Print the list of pages with problems:
print(RESULTS)

# Report time which required to perform full verification:
print('\n\n Full run took:')
print(datetime.now() - start)
