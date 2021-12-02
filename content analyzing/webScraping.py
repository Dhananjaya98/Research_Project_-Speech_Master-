from selenium import webdriver


def suggest_youtube_content():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get('https://youtube.com')
    search_box = driver.find_element_by_xpath('//*[@id="search"]')
    search_box.send_keys(['speeches', 'Transportation'])

    search_button = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
    search_button.click()
