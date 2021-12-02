from selenium import webdriver


def suggestContent():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get('https://wikipedia.com')
    search_box = driver.find_element_by_xpath('//*[@id="searchInput"]')
    search_box.send_keys(['cricket'])

    search_button = driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/button')
    search_button.click()

