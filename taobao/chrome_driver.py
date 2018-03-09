import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def chrome_driver(query_str):
    proxies_txt = requests.get("http://api.xicidaili.com/free2016.txt")

    proxies_list = proxies_txt.text.splitlines()

    print(proxies_list)

    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1200x600')
    # options.add_argument('--proxy-server=%s' % random.choice(proxies_list))

    driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)
    wait = WebDriverWait(driver, 10)
    file_lock = open("./taobao.lock", "w")
    item_list = open("./item_list.txt", "w")

    driver.get(query_str)
    list_button = driver.find_element_by_css_selector(
        "#J_relative > div.sort-row > div > div.styles > ul > li:nth-child(2) > a")
    list_button.click()

    wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, "#mainsrp-itemlist > div > div > div > div > div:nth-child(1) > div.col.col-2 > p > a"))
    )

    page_num = 1
    while True:
        try:
            driver.find_element_by_css_selector(
                "#mainsrp-pager > div > div > div > ul > li.item.next.next-disabled > span")
            break
        except NoSuchElementException:
            pass
        main_window = driver.current_window_handle
        for i in range(1, 61):
            file_lock.write(query_str + ": " + str(page_num) + ": " + str(i) + "\n")
            try:
                item = driver.find_element_by_css_selector("#mainsrp-itemlist > div > div > div > div > div:nth-child("
                                                           + str(i) + ") > div.col.col-2 > p > a")
                item.click()
                windows = driver.window_handles
                driver.switch_to_window(windows[len(windows) - 1])

                try:
                    not_found = driver.find_element_by_css_selector("#content > link")
                    if "//assets.alicdn.com/p/mall/404/404.css" in str(not_found.get_attribute("href")):
                        print(str(i) + ": " + "很抱歉，您查看的商品找不到了！" + "\n")
                        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
                        continue
                except NoSuchElementException:
                    pass

                try:
                    print(driver.title)
                    item_name = driver.find_element_by_css_selector(
                        "#J_DetailMeta > div.tm-clear > div.tb-property > div > div.tb-detail-hd > h1")
                    driver.find_element_by_css_selector(
                        "#J_DetailMeta > div.tm-clear > div.tb-property > div > div.tb-key > div > div > div.tm-countdown > div.tb-btn-wait")
                    item_list.write(driver.current_url + ": " + "OK: " + item_name.text + "\n")
                    print(driver.current_url + ": " + "OK: " + item_name.text + "\n")
                except NoSuchElementException:
                    pass
            except:
                break

            driver.close()
            driver.switch_to_window(main_window)
            file_lock.flush()
            item_list.flush()


        next_page = driver.find_element_by_css_selector(
            "#mainsrp-pager > div > div > div > ul > li.item.next > a")
        next_page.click()
        page_num += 1

    driver.quit()
