# -*- coding: utf-8 -*-
#!/usr/bin/python3

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time
from datetime import datetime


# This script allows to check all important
# menu items in TMall AliExpress mobile android application.
# This script is just an example how you can use Appium with Python
# to test real application (example of deep test, which automatically detects
# all items which should be checked).


RESULTS = ""
start = datetime.now()


def check_products_count(path=''):
    global RESULTS

    # if returned -1 - it means it is not the list of products page:
    count = -1
    driver.implicitly_wait(1)

    try:
        driver.find_element_by_id('com.alibaba.aliexpresshd:id/search_btn_filter').click()
        counter = driver.find_element_by_id('com.alibaba.aliexpresshd:id/refine_title_count')
        count = int(counter.text.split()[0])

        driver.find_element_by_id('com.alibaba.aliexpresshd:id/btn_apply_refine').click()

        # Advanced:
        title = driver.find_element_by_id('com.alibaba.aliexpresshd:id/tv_spellcheck_result')
        if 'не найдено' in title.text:
            count = 0

    except Exception as e:
        pass

    if count == 0:
        RESULTS += '\n\n-------'
        RESULTS += '\n0 RESULTS in AliExpress Android application: \n'
        RESULTS += '\n' + path + '\n'
        RESULTS += '---\n\n'

        print('\n---\n ZERO RESULTS! ' + path[:-3] + '\n---\n')

    driver.implicitly_wait(10)

    return count


# Start application on real device:
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '8.0'
desired_caps['deviceName'] = 'Android'

desired_caps['appPackage'] = 'com.alibaba.aliexpresshd'
desired_caps['appActivity'] = 'com.aliexpress.module.home.MainActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(10)


# GoTo TMall:
menu = driver.find_element_by_id('com.alibaba.aliexpresshd:id/left_action')
menu.click()

driver.find_elements_by_id('com.alibaba.aliexpresshd:id/title')[8].click()

driver.find_element_by_id('com.alibaba.aliexpresshd:id/iv_country_selected').click()

driver.find_element_by_id('com.alibaba.aliexpresshd:id/rb_selected_item').click()

driver.find_elements_by_class_name('android.widget.ImageView')[3].click()
driver.find_elements_by_id('com.alibaba.aliexpresshd:id/iv_photo')[5].click()


### ------------


def click(element):

    y = element.location_once_scrolled_into_view['y']

    try:
        window_size = driver.get_window_size()
        if (window_size['height'] - y < 30):
            # Go down:
            driver.swipe(70, 510, 70, 100, 400)
            y = element.location_once_scrolled_into_view['y']
    except:
        pass

    TouchAction(driver).tap(None, 10, y+10, 1).perform()


def check(element, path=''):
    go_back_item = None

    count = check_products_count(path)

    if count < 0:
        menu_list = element.find_elements_by_class_name('android.widget.ListView')

        for i, _ in enumerate(menu_list):
            menu = menu_list[i]

            menu_items = menu.find_elements_by_class_name('android.view.View')

            for j, _ in enumerate(menu_items):
                menu_items = menu.find_elements_by_class_name('android.view.View')
                item = menu_items[j]

                text = item.text.strip()

                if text == 'Назад':
                    go_back_item = item

                if text > '' and text != 'Назад':
                    print('{0}{1}'.format(path, text))

                    click(item)

                    check(menu, path + text + ' > ')

            # GoUp:
            driver.swipe(0, 400, 0, 1000, 1000)

            # GoBack:
            click(go_back_item)

            menu_list = element.find_elements_by_class_name('android.widget.ListView')
    else:
        driver.find_element_by_class_name('android.widget.ImageButton').click()


check(driver)


print(RESULTS)

print('\n\n Full run took:')
print(datetime.now() - start)
